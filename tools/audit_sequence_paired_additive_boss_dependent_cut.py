"""Offline audit for the frozen ``additive-boss-dependent-cut-v1`` family."""

from __future__ import annotations

import copy
import hashlib
import math
import tempfile
from pathlib import Path
from typing import Any

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

from brep2code.agent.harness import _comparison_gates
from brep2code.brep.probes import load_model, probe_summary
try:
    from tools.audit_sequence_paired_prismatic_hole import load_json, write_step
except ModuleNotFoundError:  # pragma: no cover
    from audit_sequence_paired_prismatic_hole import load_json, write_step

ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "docs/corpus/sequence-paired/additive-boss-dependent-cut-v1-preregistration.json"
TOLERANCE = 1e-5


def _positive(value: Any) -> bool:
    return isinstance(value, (int, float)) and value > 0


def _inside_rect(center: list[float], length_x: float, length_y: float, container_center: list[float], container_x: float, container_y: float) -> bool:
    return (center[0] - length_x / 2 > container_center[0] - container_x / 2 and center[0] + length_x / 2 < container_center[0] + container_x / 2 and center[1] - length_y / 2 > container_center[1] - container_y / 2 and center[1] + length_y / 2 < container_center[1] + container_y / 2)


def canonical_sequence(entry: dict[str, Any]) -> dict[str, Any]:
    """Return the sole permitted base-to-boss-to-dependent-blind-cut sequence."""
    p = entry["parameters"]
    names = ("base_length_x", "base_length_y", "base_height", "boss_length_x", "boss_length_y", "boss_height", "cut_radius", "cut_depth")
    if not all(_positive(p.get(name)) for name in names):
        raise ValueError("additive boss dimensions must be positive")
    boss_center, cut_center = p.get("boss_center_xy"), p.get("cut_center_xy")
    if not all(isinstance(point, list) and len(point) == 2 and all(isinstance(value, (int, float)) for value in point) for point in (boss_center, cut_center)):
        raise ValueError("boss and cut centers must be numeric coordinates")
    base_center = [p["base_length_x"] / 2, p["base_length_y"] / 2]
    if not _inside_rect(boss_center, p["boss_length_x"], p["boss_length_y"], base_center, p["base_length_x"], p["base_length_y"]):
        raise ValueError("boss must be strictly contained in base")
    if not (cut_center[0] - p["cut_radius"] > boss_center[0] - p["boss_length_x"] / 2 and cut_center[0] + p["cut_radius"] < boss_center[0] + p["boss_length_x"] / 2 and cut_center[1] - p["cut_radius"] > boss_center[1] - p["boss_length_y"] / 2 and cut_center[1] + p["cut_radius"] < boss_center[1] + p["boss_length_y"] / 2):
        raise ValueError("cut circle must be strictly contained in boss")
    if p["cut_depth"] >= p["boss_height"]:
        raise ValueError("cut must be blind within boss")
    return {"operations": [
        {"id": "sketch_base", "kind": "SketchRect", "plane": "XY", "length_x": p["base_length_x"], "length_y": p["base_length_y"]},
        {"id": "base", "kind": "ExtrudeBase", "profile": "sketch_base", "direction": "+Z", "distance": p["base_height"]},
        {"id": "sketch_boss", "kind": "SketchRect", "support": "base.top_face", "center_xy": boss_center, "length_x": p["boss_length_x"], "length_y": p["boss_length_y"]},
        {"id": "boss", "kind": "ExtrudeBoss", "target": "base", "profile": "sketch_boss", "direction": "+Z", "operation": "join", "distance": p["boss_height"]},
        {"id": "sketch_cut", "kind": "SketchCircle", "support": "boss.top_face", "center_xy": cut_center, "radius": p["cut_radius"]},
        {"id": "cut", "kind": "CutCylinder", "target": "boss", "profile": "sketch_cut", "direction": "-Z", "variant": "blind", "depth": p["cut_depth"]},
    ]}


def assert_sequence_agreement(candidate: dict[str, Any], entry: dict[str, Any]) -> None:
    if candidate != canonical_sequence(entry):
        raise ValueError("candidate sequence differs from declared additive-boss oracle")


def build_shape(entry: dict[str, Any]):
    operations = canonical_sequence(entry)["operations"]
    base_sketch, base, boss_sketch, boss, cut_sketch, cut = operations
    base_shape = BRepPrimAPI_MakeBox(base_sketch["length_x"], base_sketch["length_y"], base["distance"]).Shape()
    boss_shape = BRepPrimAPI_MakeBox(gp_Pnt(boss_sketch["center_xy"][0] - boss_sketch["length_x"] / 2, boss_sketch["center_xy"][1] - boss_sketch["length_y"] / 2, base["distance"]), boss_sketch["length_x"], boss_sketch["length_y"], boss["distance"]).Shape()
    joined = BRepAlgoAPI_Fuse(base_shape, boss_shape).Shape()
    cut_axis = gp_Ax2(gp_Pnt(cut_sketch["center_xy"][0], cut_sketch["center_xy"][1], base["distance"] + boss["distance"] - cut["depth"]), gp_Dir(0, 0, 1))
    cylinder = BRepPrimAPI_MakeCylinder(cut_axis, cut_sketch["radius"], cut["depth"]).Shape()
    return BRepAlgoAPI_Cut(joined, cylinder).Shape()


def _summary(entry: dict[str, Any], directory: Path) -> dict[str, Any]:
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "model.step"
    write_step(build_shape(entry), output)
    return probe_summary(load_model(output))


def apply_mutation(entry: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(entry)
    key = mutation["kind"]
    if key not in {"base_length_x", "boss_length_x", "cut_radius", "cut_depth"}:
        raise ValueError("mutation is incompatible with additive-boss grammar")
    candidate["parameters"][key] += mutation["delta"]
    canonical_sequence(candidate)
    return candidate


def assert_editability(baseline: dict[str, Any], mutated: dict[str, Any], mutation: dict[str, Any]) -> None:
    if mutation["kind"] == "base_length_x":
        if abs(mutated["bbox"]["max"][0] - baseline["bbox"]["max"][0] - mutation["delta"]) > TOLERANCE or mutated["volume"] <= baseline["volume"]:
            raise ValueError("base mutation did not change the declared observable")
    elif mutation["kind"] == "boss_length_x":
        if abs(mutated["bbox"]["max"][2] - baseline["bbox"]["max"][2]) > TOLERANCE or mutated["volume"] <= baseline["volume"]:
            raise ValueError("boss mutation did not preserve height and enlarge volume")
    elif mutation["kind"] == "cut_radius":
        if mutated["volume"] >= baseline["volume"]:
            raise ValueError("cut radius mutation did not remove more material")
    elif mutation["kind"] == "cut_depth" and mutated["volume"] >= baseline["volume"]:
        raise ValueError("cut depth mutation did not remove more material")


def assert_semantic_invariants(entry: dict[str, Any], summary: dict[str, Any]) -> None:
    p = entry["parameters"]
    expected = p["base_length_x"] * p["base_length_y"] * p["base_height"] + p["boss_length_x"] * p["boss_length_y"] * p["boss_height"] - math.pi * p["cut_radius"] ** 2 * p["cut_depth"]
    if summary["counts"]["solid"] != 1:
        raise ValueError("boss and base must remain one connected solid")
    if abs(summary["volume"] - expected) > TOLERANCE:
        raise ValueError("boss/cut volume invariant failed")
    if summary["bbox"]["min"] != [0.0, 0.0, 0.0] or any(abs(value - expected_value) > TOLERANCE for value, expected_value in zip(summary["bbox"]["max"], [p["base_length_x"], p["base_length_y"], p["base_height"] + p["boss_height"]], strict=True)):
        raise ValueError("base extents or boss height invariant failed")


def audit(record_path: Path = EXPANSION) -> list[dict[str, Any]]:
    record = load_json(record_path)
    cases = record.get("cases")
    if record.get("selection_status") != "preregistered_before_candidate_production" or not isinstance(cases, list) or len(cases) != 6:
        raise ValueError("M23 record must retain exactly six preregistered rows")
    development = [entry for entry in cases if entry.get("data_split") == "development"]
    held_out = [entry for entry in cases if entry.get("data_split") == "held_out"]
    if len(development) != 3 or len(held_out) != 3 or {entry.get("family_id") for entry in development} != {"additive_boss_dependent_cut_centered"} or {entry.get("family_id") for entry in held_out} != {"additive_boss_dependent_cut_offset"}:
        raise ValueError("family split leak detected")
    rows = []
    for entry in cases:
        canonical_sequence(entry)
        directory = ROOT / entry["candidate_directory"]
        case = load_json(directory / "case.json")
        input_path = directory / case["input_step"]
        if case.get("status") != "active" or case.get("data_split") != entry["data_split"] or case.get("family_id") != entry["family_id"] or hashlib.sha256(input_path.read_bytes()).hexdigest() != case["sha256"]:
            raise ValueError(f"candidate metadata drift: {entry['case_id']}")
        if case.get("reference_script_status") != "available" or not (directory / case.get("reference_script", "")).is_file():
            raise ValueError(f"reference script drift: {entry['case_id']}")
        candidate = load_json(directory / "candidate_sequence.json")
        if candidate.get("grammar_version") != record["grammar_version"]:
            raise ValueError("candidate sequence grammar drift")
        assert_sequence_agreement(candidate.get("sequence", {}), entry)
        with tempfile.TemporaryDirectory(prefix="brep2code-m23-") as temp:
            baseline = _summary(entry, Path(temp))
            gates = _comparison_gates(probe_summary(load_model(input_path)), baseline)
            if not all(gate["status"] == "pass" for gate in gates):
                raise ValueError(f"geometry replay mismatch: {entry['case_id']}")
            assert_semantic_invariants(entry, baseline)
            for index, mutation in enumerate(entry["mutations"]):
                assert_editability(baseline, _summary(apply_mutation(entry, mutation), Path(temp) / f"mutation-{index}"), mutation)
        rows.append({"case_id": entry["case_id"], "gates": gates, "mutations": len(entry["mutations"])})
    return rows


if __name__ == "__main__":
    print(f"additive-boss dependent-cut sequence-pair audit passed: {len(audit())} records")
