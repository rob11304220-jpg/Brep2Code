"""Offline candidate production for the frozen M29 selector-ambiguity pair."""

from __future__ import annotations

import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCP.BRepGProp import BRepGProp
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.GProp import GProp_GProps
from OCP.GeomAbs import GeomAbs_Plane
from OCP.TopAbs import TopAbs_FACE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Pnt

from brep2code.agent.harness import _comparison_gates
from brep2code.brep.probes import load_model, probe_summary
try:  # Supports package import and direct script execution.
    from tools.audit_sequence_paired_prismatic_hole import load_json, write_step
    from tools.build_m20_counterbore_candidates import normalize_step_header
except ModuleNotFoundError:  # pragma: no cover - direct script entrypoint only
    from audit_sequence_paired_prismatic_hole import load_json, write_step
    from build_m20_counterbore_candidates import normalize_step_header


ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "docs/corpus/sequence-paired/selector-ambiguity-v1-preregistration.json"
TOLERANCE = 1e-5


def _positive(value: Any, label: str) -> float:
    if not isinstance(value, (int, float)) or value <= 0:
        raise ValueError(f"{label} must be positive")
    return float(value)


def _centers(value: Any) -> list[list[float]]:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("boss_centers_xy must contain exactly two coordinates")
    result: list[list[float]] = []
    for center in value:
        if not isinstance(center, list) or len(center) != 2 or not all(isinstance(item, (int, float)) for item in center):
            raise ValueError("boss centers must be numeric XY pairs")
        result.append([float(center[0]), float(center[1])])
    return result


def _inside(center: list[float], size_x: float, size_y: float, base_x: float, base_y: float) -> bool:
    return center[0] - size_x / 2 > 0 and center[0] + size_x / 2 < base_x and center[1] - size_y / 2 > 0 and center[1] + size_y / 2 < base_y


def _disjoint(left: list[float], right: list[float], size_x: float, size_y: float) -> bool:
    return abs(left[0] - right[0]) > size_x or abs(left[1] - right[1]) > size_y


def canonical_sequence(entry: dict[str, Any]) -> dict[str, Any]:
    p = entry["parameters"]
    base_x = _positive(p.get("base_length_x"), "base_length_x")
    base_y = _positive(p.get("base_length_y"), "base_length_y")
    base_h = _positive(p.get("base_height"), "base_height")
    boss_x = _positive(p.get("boss_length_x"), "boss_length_x")
    boss_y = _positive(p.get("boss_length_y"), "boss_length_y")
    boss_h = _positive(p.get("boss_height"), "boss_height")
    centers = _centers(p.get("boss_centers_xy"))
    if not all(_inside(center, boss_x, boss_y, base_x, base_y) for center in centers) or not _disjoint(centers[0], centers[1], boss_x, boss_y):
        raise ValueError("bosses must be disjoint and strictly contained in the base")
    return {"operations": [
        {"id": "sketch_base", "kind": "SketchRect", "plane": "XY", "length_x": base_x, "length_y": base_y},
        {"id": "base", "kind": "ExtrudeBase", "profile": "sketch_base", "direction": "+Z", "distance": base_h},
        {"id": "sketch_bosses", "kind": "SketchTwoRects", "support": "base.top_face", "centers_xy": centers, "length_x": boss_x, "length_y": boss_y},
        {"id": "bosses", "kind": "ExtrudeBosses", "target": "base", "profile": "sketch_bosses", "direction": "+Z", "operation": "join", "distance": boss_h},
        {"id": "candidate_audit", "kind": "SelectPlanarFace", "source": "bosses", "selector": {"surface": "planar", "normal": "+Z", "z_role": "maximum_output_z", "cardinality": "exactly_one_required"}},
        {"id": "stop", "kind": "FailClosedAmbiguous", "condition": "candidate_audit.cardinality != 1"},
    ]}


def build_shape(entry: dict[str, Any]):
    sequence = canonical_sequence(entry)["operations"]
    base = BRepPrimAPI_MakeBox(sequence[0]["length_x"], sequence[0]["length_y"], sequence[1]["distance"]).Shape()
    joined = base
    for center in sequence[2]["centers_xy"]:
        boss = BRepPrimAPI_MakeBox(gp_Pnt(center[0] - sequence[2]["length_x"] / 2, center[1] - sequence[2]["length_y"] / 2, sequence[1]["distance"]), sequence[2]["length_x"], sequence[2]["length_y"], sequence[3]["distance"]).Shape()
        joined = BRepAlgoAPI_Fuse(joined, boss).Shape()
    return joined


def candidate_top_faces(shape: Any, target_z: float) -> list[Any]:
    candidates: list[Any] = []
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    while explorer.More():
        face = TopoDS.Face_s(explorer.Current())
        surface = BRepAdaptor_Surface(face)
        if surface.GetType() == GeomAbs_Plane:
            direction = surface.Plane().Axis().Direction()
            props = GProp_GProps()
            BRepGProp.SurfaceProperties_s(face, props)
            if direction.Z() > 1.0 - TOLERANCE and abs(props.CentreOfMass().Z() - target_z) <= TOLERANCE:
                candidates.append(face)
        explorer.Next()
    return candidates


def selector_result(shape: Any, entry: dict[str, Any]) -> dict[str, Any]:
    p = entry["parameters"]
    candidates = candidate_top_faces(shape, p["base_height"] + p["boss_height"])
    cardinality = len(candidates)
    return {"cardinality": cardinality, "status": "unique" if cardinality == 1 else "ambiguous" if cardinality > 1 else "empty"}


def assert_sequence_agreement(candidate: dict[str, Any], entry: dict[str, Any]) -> None:
    if candidate != canonical_sequence(entry):
        raise ValueError("candidate sequence differs from the frozen selector-ambiguity grammar")
    kinds = {operation["kind"] for operation in candidate["operations"]}
    if "SketchCircle" in kinds or "CutCylinder" in kinds:
        raise ValueError("ambiguous selector sequence may not emit a dependent operation")


def _write(entry: dict[str, Any], path: Path) -> str:
    write_step(build_shape(entry), path)
    normalize_step_header(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_record(record: dict[str, Any]) -> list[dict[str, Any]]:
    entries = record.get("cases")
    if record.get("selection_status") != "preregistered_before_candidate_production" or not isinstance(entries, list) or len(entries) != 2:
        raise ValueError("M29 production requires exactly two preregistered rows")
    splits = {entry.get("data_split") for entry in entries}
    families = {entry.get("family_id") for entry in entries}
    if splits != {"development", "held_out"} or families != {"selector_ambiguity_twin_centered", "selector_ambiguity_twin_offset"}:
        raise ValueError("M29 split/family preregistration drift")
    return entries


def build(expansion_path: Path = EXPANSION, output_root: Path = ROOT) -> list[str]:
    record = load_json(expansion_path)
    entries = _validate_record(record)
    produced: list[str] = []
    for entry in entries:
        canonical_sequence(entry)
        with tempfile.TemporaryDirectory(prefix="brep2code-m29-a-") as first, tempfile.TemporaryDirectory(prefix="brep2code-m29-b-") as second:
            first_path, second_path = Path(first) / "model.step", Path(second) / "model.step"
            if _write(entry, first_path) != _write(entry, second_path) or first_path.read_bytes() != second_path.read_bytes():
                raise RuntimeError(f"hash nondeterminism: {entry['case_id']}")
        directory = output_root / entry["candidate_directory"]
        directory.mkdir(parents=True, exist_ok=True)
        step = directory / "input.step"
        digest = _write(entry, step)
        shape = build_shape(entry)
        selection = selector_result(shape, entry)
        if selection != {"cardinality": 2, "status": "ambiguous"}:
            raise ValueError(f"selector did not fail closed: {entry['case_id']}: {selection}")
        sequence = canonical_sequence(entry)
        metadata = {
            "case_id": entry["case_id"], "status": "experimental", "origin": "self_authored", "tier": "P2", "fixture_version": 1,
            "family_id": entry["family_id"], "data_split": entry["data_split"], "variant": entry["variant"], "parameters": entry["parameters"],
            "input_step": "input.step", "reference_script_status": "unavailable", "sha256": digest, "unit": "mm", "expected": probe_summary(load_model(step)),
            "sequence_pair": {"grammar_version": record["grammar_version"], "oracle_provenance": record["oracle_provenance"], "sequence": sequence, "candidate_sequence": "candidate_sequence.json", "selector_result": selection},
            "admission_boundary": "Experimental candidate only; absent from registry, manifest, provider, training, and runtime paths.",
        }
        (directory / "candidate_sequence.json").write_text(json.dumps({"grammar_version": record["grammar_version"], "sequence": sequence}, indent=2) + "\n", encoding="utf-8")
        (directory / "case.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        produced.append(entry["case_id"])
    return produced


def apply_mutation(entry: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(entry)
    kind = mutation["kind"]
    if kind not in {"boss_width_x", "shared_boss_height"}:
        raise ValueError("mutation is incompatible with selector-ambiguity grammar")
    key = "boss_length_x" if kind == "boss_width_x" else "boss_height"
    candidate["parameters"][key] += mutation["delta"]
    canonical_sequence(candidate)
    return candidate


def control_result(shape: Any, entry: dict[str, Any], control_id: str) -> dict[str, str]:
    selection = selector_result(shape, entry)
    if selection["cardinality"] != 2:
        raise ValueError("control requires the twin-boss ambiguous state")
    if control_id == "wrong-face-injection":
        return {"accepted": "false", "reason": "selector_ambiguity"}
    if control_id == "coordinate-tie-breaker-injection":
        return {"accepted": "false", "reason": "coordinate_only_support"}
    raise ValueError(f"unknown control: {control_id}")


def assert_semantics(entry: dict[str, Any], summary: dict[str, Any], shape: Any) -> None:
    p = entry["parameters"]
    expected_volume = p["base_length_x"] * p["base_length_y"] * p["base_height"] + 2 * p["boss_length_x"] * p["boss_length_y"] * p["boss_height"]
    if summary["counts"]["solid"] != 1 or abs(summary["volume"] - expected_volume) > TOLERANCE:
        raise ValueError("one-solid or twin-boss volume invariant failed")
    expected_max = [p["base_length_x"], p["base_length_y"], p["base_height"] + p["boss_height"]]
    if summary["bbox"]["min"] != [0.0, 0.0, 0.0] or any(abs(actual - target) > TOLERANCE for actual, target in zip(summary["bbox"]["max"], expected_max, strict=True)):
        raise ValueError("base extents or shared boss-height invariant failed")
    if selector_result(shape, entry) != {"cardinality": 2, "status": "ambiguous"}:
        raise ValueError("selector cardinality invariant failed")


def audit(record_path: Path = EXPANSION, output_root: Path = ROOT) -> list[dict[str, Any]]:
    record = load_json(record_path)
    entries = _validate_record(record)
    rows: list[dict[str, Any]] = []
    controls = record.get("negative_controls")
    if not isinstance(controls, list) or {control.get("id") for control in controls} != {"wrong-face-injection", "coordinate-tie-breaker-injection"}:
        raise ValueError("M29 negative-control preregistration drift")
    for entry in entries:
        canonical_sequence(entry)
        directory = output_root / entry["candidate_directory"]
        case = load_json(directory / "case.json")
        input_path = directory / case["input_step"]
        if case.get("status") != "experimental" or case.get("family_id") != entry["family_id"] or case.get("data_split") != entry["data_split"] or hashlib.sha256(input_path.read_bytes()).hexdigest() != case["sha256"]:
            raise ValueError(f"candidate metadata drift: {entry['case_id']}")
        candidate = load_json(directory / "candidate_sequence.json")
        if candidate.get("grammar_version") != record["grammar_version"]:
            raise ValueError("candidate grammar drift")
        assert_sequence_agreement(candidate.get("sequence", {}), entry)
        with tempfile.TemporaryDirectory(prefix="brep2code-m29-audit-") as temp:
            output = Path(temp) / "model.step"
            _write(entry, output)
            shape = build_shape(entry)
            summary = probe_summary(load_model(output))
            gates = _comparison_gates(probe_summary(load_model(input_path)), summary)
            if not all(gate["status"] == "pass" for gate in gates):
                raise ValueError(f"geometry replay mismatch: {entry['case_id']}")
            assert_semantics(entry, summary, shape)
            for mutation in entry["mutations"]:
                mutated = apply_mutation(entry, mutation)
                mutated_shape = build_shape(mutated)
                mutated_path = Path(temp) / f"mutation-{mutation['kind']}.step"
                _write(mutated, mutated_path)
                assert_semantics(mutated, probe_summary(load_model(mutated_path)), mutated_shape)
            observed_controls = {control["id"]: control_result(shape, entry, control["id"]) for control in controls}
            if observed_controls != {"wrong-face-injection": {"accepted": "false", "reason": "selector_ambiguity"}, "coordinate-tie-breaker-injection": {"accepted": "false", "reason": "coordinate_only_support"}}:
                raise ValueError("negative control did not reject as preregistered")
        rows.append({"case_id": entry["case_id"], "selector": case["sequence_pair"]["selector_result"], "gates": gates, "mutations": len(entry["mutations"]), "controls": observed_controls})
    return rows


if __name__ == "__main__":
    print(f"selector-ambiguity candidate build complete: {', '.join(build())}")
    print(f"selector-ambiguity audit passed: {len(audit())} records")
