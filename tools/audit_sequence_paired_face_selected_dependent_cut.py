"""Offline production and audit for the frozen M25 face-selected cut family."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import tempfile
from pathlib import Path
from typing import Any

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

from brep2code.agent.harness import _comparison_gates
from brep2code.brep.probes import load_model, probe_summary
try:  # Supports package import and direct script execution.
    from tools.audit_sequence_paired_prismatic_hole import load_json, write_step
    from tools.build_m20_counterbore_candidates import normalize_step_header
except ModuleNotFoundError:  # pragma: no cover - direct script entrypoint only
    from audit_sequence_paired_prismatic_hole import load_json, write_step
    from build_m20_counterbore_candidates import normalize_step_header

ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "docs/corpus/sequence-paired/face-selected-dependent-cut-v1-preregistration.json"
TOLERANCE = 1e-5


def _inside(center: list[float], size_x: float, size_y: float, container: list[float], container_x: float, container_y: float) -> bool:
    return (center[0] - size_x / 2 > container[0] - container_x / 2 and center[0] + size_x / 2 < container[0] + container_x / 2 and center[1] - size_y / 2 > container[1] - container_y / 2 and center[1] + size_y / 2 < container[1] + container_y / 2)


def canonical_sequence(entry: dict[str, Any]) -> dict[str, Any]:
    p = entry["parameters"]
    names = ("base_length_x", "base_length_y", "base_height", "boss_length_x", "boss_length_y", "boss_height", "cut_radius", "cut_depth")
    if not all(isinstance(p.get(name), (int, float)) and p[name] > 0 for name in names):
        raise ValueError("face-selected cut dimensions must be positive")
    boss_center, cut_center = p.get("boss_center_xy"), p.get("cut_center_xy")
    if not all(isinstance(point, list) and len(point) == 2 and all(isinstance(value, (int, float)) for value in point) for point in (boss_center, cut_center)):
        raise ValueError("boss and cut centers must be numeric coordinates")
    base_center = [p["base_length_x"] / 2, p["base_length_y"] / 2]
    if not _inside(boss_center, p["boss_length_x"], p["boss_length_y"], base_center, p["base_length_x"], p["base_length_y"]):
        raise ValueError("boss must be strictly contained in base")
    if not _inside(cut_center, 2 * p["cut_radius"], 2 * p["cut_radius"], boss_center, p["boss_length_x"], p["boss_length_y"]):
        raise ValueError("cut circle must be strictly contained in selected boss top face")
    if p["cut_depth"] >= p["boss_height"]:
        raise ValueError("cut must remain blind within boss")
    return {"operations": [
        {"id": "sketch_base", "kind": "SketchRect", "plane": "XY", "length_x": p["base_length_x"], "length_y": p["base_length_y"]},
        {"id": "base", "kind": "ExtrudeBase", "profile": "sketch_base", "direction": "+Z", "distance": p["base_height"]},
        {"id": "sketch_boss", "kind": "SketchRect", "support": "base.top_face", "center_xy": boss_center, "length_x": p["boss_length_x"], "length_y": p["boss_length_y"]},
        {"id": "boss", "kind": "ExtrudeBoss", "target": "base", "profile": "sketch_boss", "direction": "+Z", "operation": "join", "distance": p["boss_height"]},
        {"id": "boss_top", "kind": "SelectPlanarFace", "source": "boss", "selector": {"normal": "+Z", "z_role": "maximum_output_z", "cardinality": "exactly_one"}},
        {"id": "sketch_cut", "kind": "SketchCircle", "support": "boss_top", "center_xy": cut_center, "radius": p["cut_radius"]},
        {"id": "cut", "kind": "CutCylinder", "target": "boss", "profile": "sketch_cut", "direction": "-Z", "variant": "blind", "depth": p["cut_depth"]},
    ]}


def assert_sequence_agreement(candidate: dict[str, Any], entry: dict[str, Any]) -> None:
    if candidate != canonical_sequence(entry):
        raise ValueError("candidate sequence differs from the frozen face-selected oracle")


def build_shape(entry: dict[str, Any]):
    base_sketch, base, boss_sketch, boss, _, cut_sketch, cut = canonical_sequence(entry)["operations"]
    base_shape = BRepPrimAPI_MakeBox(base_sketch["length_x"], base_sketch["length_y"], base["distance"]).Shape()
    boss_shape = BRepPrimAPI_MakeBox(gp_Pnt(boss_sketch["center_xy"][0] - boss_sketch["length_x"] / 2, boss_sketch["center_xy"][1] - boss_sketch["length_y"] / 2, base["distance"]), boss_sketch["length_x"], boss_sketch["length_y"], boss["distance"]).Shape()
    joined = BRepAlgoAPI_Fuse(base_shape, boss_shape).Shape()
    axis = gp_Ax2(gp_Pnt(cut_sketch["center_xy"][0], cut_sketch["center_xy"][1], base["distance"] + boss["distance"] - cut["depth"]), gp_Dir(0, 0, 1))
    return BRepAlgoAPI_Cut(joined, BRepPrimAPI_MakeCylinder(axis, cut_sketch["radius"], cut["depth"]).Shape()).Shape()


def _write(entry: dict[str, Any], path: Path) -> str:
    write_step(build_shape(entry), path)
    normalize_step_header(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(expansion_path: Path = EXPANSION, output_root: Path = ROOT) -> list[str]:
    record = load_json(expansion_path)
    entries = record.get("cases")
    if record.get("selection_status") != "preregistered_before_candidate_production" or not isinstance(entries, list) or len(entries) != 6:
        raise ValueError("M25 production requires exactly six preregistered rows")
    produced = []
    for entry in entries:
        canonical_sequence(entry)
        with tempfile.TemporaryDirectory(prefix="brep2code-m25-a-") as first, tempfile.TemporaryDirectory(prefix="brep2code-m25-b-") as second:
            first_path, second_path = Path(first) / "model.step", Path(second) / "model.step"
            if _write(entry, first_path) != _write(entry, second_path) or first_path.read_bytes() != second_path.read_bytes():
                raise RuntimeError(f"hash nondeterminism: {entry['case_id']}")
        directory = output_root / entry["candidate_directory"]
        directory.mkdir(parents=True, exist_ok=True)
        step = directory / "input.step"
        digest = _write(entry, step)
        metadata = {"case_id": entry["case_id"], "status": "experimental", "origin": "self_authored", "tier": "P2", "fixture_version": 1, "family_id": entry["family_id"], "data_split": entry["data_split"], "variant": entry["variant"], "parameters": entry["parameters"], "input_step": "input.step", "reference_script_status": "unavailable", "sha256": digest, "unit": "mm", "expected": probe_summary(load_model(step)), "sequence_pair": {"grammar_version": record["grammar_version"], "oracle_provenance": record["oracle_provenance"], "sequence": canonical_sequence(entry), "candidate_sequence": "candidate_sequence.json"}, "admission_boundary": "Experimental candidate only; absent from registry, manifest, provider, training, and runtime paths."}
        (directory / "candidate_sequence.json").write_text(json.dumps({"grammar_version": record["grammar_version"], "sequence": canonical_sequence(entry)}, indent=2) + "\n", encoding="utf-8")
        (directory / "case.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        produced.append(entry["case_id"])
    return produced


def _summary(entry: dict[str, Any], directory: Path) -> dict[str, Any]:
    output = directory / "model.step"
    directory.mkdir(parents=True, exist_ok=True)
    _write(entry, output)
    return probe_summary(load_model(output))


def apply_mutation(entry: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(entry)
    key = mutation["kind"]
    if key not in {"base_length_x", "boss_length_x", "boss_height", "cut_radius", "cut_depth"}:
        raise ValueError("mutation is incompatible with face-selected grammar")
    candidate["parameters"][key] += mutation["delta"]
    canonical_sequence(candidate)
    return candidate


def assert_semantics(entry: dict[str, Any], summary: dict[str, Any]) -> None:
    p = entry["parameters"]
    expected = p["base_length_x"] * p["base_length_y"] * p["base_height"] + p["boss_length_x"] * p["boss_length_y"] * p["boss_height"] - math.pi * p["cut_radius"] ** 2 * p["cut_depth"]
    if summary["counts"]["solid"] != 1 or abs(summary["volume"] - expected) > TOLERANCE:
        raise ValueError("one-solid or blind-cut semantic invariant failed")
    expected_max = [p["base_length_x"], p["base_length_y"], p["base_height"] + p["boss_height"]]
    if summary["bbox"]["min"] != [0.0, 0.0, 0.0] or any(abs(value - target) > TOLERANCE for value, target in zip(summary["bbox"]["max"], expected_max, strict=True)):
        raise ValueError("base extents or selected boss-top height invariant failed")


def audit(record_path: Path = EXPANSION) -> list[dict[str, Any]]:
    record = load_json(record_path)
    entries = record.get("cases")
    if not isinstance(entries, list) or len(entries) != 6:
        raise ValueError("M25 record must retain exactly six preregistered rows")
    dev = [entry for entry in entries if entry.get("data_split") == "development"]
    held = [entry for entry in entries if entry.get("data_split") == "held_out"]
    if len(dev) != 3 or len(held) != 3 or {entry.get("family_id") for entry in dev} != {"face_selected_cut_centered"} or {entry.get("family_id") for entry in held} != {"face_selected_cut_offset"}:
        raise ValueError("family split leak detected")
    rows = []
    for entry in entries:
        canonical_sequence(entry)
        directory = ROOT / entry["candidate_directory"]
        case = load_json(directory / "case.json")
        input_path = directory / case["input_step"]
        if case.get("status") not in {"experimental", "active"} or case.get("family_id") != entry["family_id"] or case.get("data_split") != entry["data_split"] or hashlib.sha256(input_path.read_bytes()).hexdigest() != case["sha256"]:
            raise ValueError(f"candidate metadata drift: {entry['case_id']}")
        candidate = load_json(directory / "candidate_sequence.json")
        if candidate.get("grammar_version") != record["grammar_version"]:
            raise ValueError("candidate grammar drift")
        assert_sequence_agreement(candidate.get("sequence", {}), entry)
        with tempfile.TemporaryDirectory(prefix="brep2code-m25-") as temp:
            baseline = _summary(entry, Path(temp))
            gates = _comparison_gates(probe_summary(load_model(input_path)), baseline)
            if not all(gate["status"] == "pass" for gate in gates):
                raise ValueError(f"geometry replay mismatch: {entry['case_id']}")
            assert_semantics(entry, baseline)
            for index, mutation in enumerate(entry["mutations"]):
                mutated = _summary(apply_mutation(entry, mutation), Path(temp) / f"mutation-{index}")
                assert_semantics(apply_mutation(entry, mutation), mutated)
        rows.append({"case_id": entry["case_id"], "gates": gates, "mutations": len(entry["mutations"])})
    return rows


if __name__ == "__main__":
    print(f"face-selected dependent-cut audit passed: {len(audit())} records")
