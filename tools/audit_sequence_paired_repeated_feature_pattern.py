"""Offline audit for the frozen ``repeated-feature-pattern-v1`` family."""

from __future__ import annotations

import copy
import hashlib
import math
import tempfile
from pathlib import Path
from typing import Any

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

from brep2code.agent.harness import _comparison_gates
from brep2code.brep.probes import load_model, probe_summary
try:
    from tools.audit_sequence_paired_prismatic_hole import load_json, write_step
except ModuleNotFoundError:  # pragma: no cover - direct script entrypoint only
    from audit_sequence_paired_prismatic_hole import load_json, write_step


ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "docs/corpus/sequence-paired/repeated-feature-pattern-v1-preregistration.json"
TOLERANCE = 1e-5


def _parameters(entry: dict[str, Any]) -> tuple[float, float, float, float, float, float, float, float]:
    params = entry["parameters"]
    fields = ("base_length_x", "base_length_y", "base_height", "x_spacing", "y_spacing", "hole_radius")
    if not all(isinstance(params.get(field), (int, float)) and params[field] > 0 for field in fields):
        raise ValueError("repeated-feature pattern dimensions must be positive")
    center = params.get("grid_center_xy")
    if not isinstance(center, list) or len(center) != 2 or not all(isinstance(value, (int, float)) for value in center):
        raise ValueError("grid centre must be two numeric coordinates")
    return (*[float(params[field]) for field in fields], float(center[0]), float(center[1]))


def _centres(entry: dict[str, Any]) -> list[tuple[float, float]]:
    length_x, length_y, _, spacing_x, spacing_y, radius, center_x, center_y = _parameters(entry)
    if not radius < min(spacing_x, spacing_y) / 2.0:
        raise ValueError("hole radius must be less than half the smaller spacing")
    centres = [(center_x + dx * spacing_x / 2.0, center_y + dy * spacing_y / 2.0) for dx in (-1.0, 1.0) for dy in (-1.0, 1.0)]
    if len(set(centres)) != 4:
        raise ValueError("pattern must have exactly four distinct positions")
    if not all(radius < x < length_x - radius and radius < y < length_y - radius for x, y in centres):
        raise ValueError("pattern holes exceed base extent")
    return centres


def canonical_sequence(entry: dict[str, Any]) -> dict[str, Any]:
    length_x, length_y, height, spacing_x, spacing_y, radius, center_x, center_y = _parameters(entry)
    centres = _centres(entry)
    return {"operations": [
        {"id": "sketch_base", "kind": "SketchRect", "plane": "XY", "length_x": length_x, "length_y": length_y},
        {"id": "base", "kind": "ExtrudeBase", "profile": "sketch_base", "direction": "+Z", "distance": height},
        {"id": "sketch_pattern", "kind": "SketchCircularGrid", "support": "base.top_face", "layout": "rectangular_2x2", "instances": 4, "center_xy": [center_x, center_y], "x_spacing": spacing_x, "y_spacing": spacing_y, "radius": radius, "positions_xy": [[x, y] for x, y in centres]},
        {"id": "pattern_cut", "kind": "CutThroughAll", "target": "base", "profile": "sketch_pattern", "direction": "-Z", "instances": 4},
    ]}


def build_shape(entry: dict[str, Any]):
    sequence = canonical_sequence(entry)["operations"]
    sketch, base, pattern, _ = sequence
    result = BRepPrimAPI_MakeBox(sketch["length_x"], sketch["length_y"], base["distance"]).Shape()
    cutter_height = base["distance"] + 2.0
    for x, y in pattern["positions_xy"]:
        cutter = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, y, -1.0), gp_Dir(0, 0, 1)), pattern["radius"], cutter_height).Shape()
        result = BRepAlgoAPI_Cut(result, cutter).Shape()
    return result


def replay_summary(entry: dict[str, Any], directory: Path) -> dict[str, Any]:
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "model.step"
    write_step(build_shape(entry), output)
    return probe_summary(load_model(output))


def apply_mutation(entry: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(entry)
    params = candidate["parameters"]
    kind = mutation["kind"]
    if kind == "grid_offset_x":
        params["grid_center_xy"][0] += mutation["delta"]
    elif kind in {"base_length_x", "hole_radius", "x_spacing", "y_spacing"}:
        params[kind] += mutation["delta"]
    else:
        raise ValueError("mutation is incompatible with repeated-feature pattern grammar")
    canonical_sequence(candidate)
    return candidate


def _bbox_delta(first: dict[str, Any], second: dict[str, Any]) -> float:
    return max(abs(left - right) for group_a, group_b in zip((first["bbox"]["min"], first["bbox"]["max"]), (second["bbox"]["min"], second["bbox"]["max"]), strict=True) for left, right in zip(group_a, group_b, strict=True))


def assert_semantic_invariants(entry: dict[str, Any], summary: dict[str, Any]) -> None:
    length_x, length_y, height, _, _, radius, _, _ = _parameters(entry)
    expected = length_x * length_y * height - 4.0 * math.pi * radius**2 * height
    if summary["counts"]["solid"] != 1 or abs(summary["volume"] - expected) > TOLERANCE:
        raise ValueError("repeated-feature pattern semantic invariant failed")


def audit(record_path: Path = EXPANSION) -> list[dict[str, Any]]:
    record = load_json(record_path)
    cases = record.get("cases")
    if record.get("selection_status") != "preregistered_before_candidate_production" or not isinstance(cases, list) or len(cases) != 6:
        raise ValueError("repeated-feature pattern record must retain exactly six rows")
    development = [entry for entry in cases if entry.get("data_split") == "development"]
    held_out = [entry for entry in cases if entry.get("data_split") == "held_out"]
    if len(development) != 3 or len(held_out) != 3 or {entry.get("family_id") for entry in development} != {"repeated_feature_pattern_centered"} or {entry.get("family_id") for entry in held_out} != {"repeated_feature_pattern_offset"}:
        raise ValueError("family split leak detected")
    rows = []
    for entry in cases:
        oracle = canonical_sequence(entry)
        directory = ROOT / entry["candidate_directory"]
        case = load_json(directory / "case.json")
        input_path = directory / case["input_step"]
        if case.get("status") not in {"experimental", "active"} or case.get("data_split") != entry["data_split"] or case.get("family_id") != entry["family_id"] or hashlib.sha256(input_path.read_bytes()).hexdigest() != case.get("sha256"):
            raise ValueError(f"candidate metadata drift: {entry['case_id']}")
        candidate = load_json(directory / "candidate_sequence.json")
        if candidate.get("grammar_version") != record["grammar_version"] or candidate.get("sequence") != oracle:
            raise ValueError("candidate sequence differs from declared oracle")
        with tempfile.TemporaryDirectory(prefix="brep2code-m90-") as temp:
            baseline = replay_summary(entry, Path(temp))
            gates = _comparison_gates(probe_summary(load_model(input_path)), baseline)
            if not all(gate["status"] == "pass" for gate in gates):
                raise ValueError(f"geometry replay mismatch: {entry['case_id']}")
            assert_semantic_invariants(entry, baseline)
            for index, mutation in enumerate(entry["mutations"]):
                mutated = replay_summary(apply_mutation(entry, mutation), Path(temp) / f"mutation-{index}")
                if mutation["kind"] == "base_length_x":
                    if mutated["bbox"]["max"][0] <= baseline["bbox"]["max"][0] or mutated["volume"] <= baseline["volume"]:
                        raise ValueError("base mutation did not change declared observables")
                elif mutation["kind"] in {"grid_offset_x", "x_spacing", "y_spacing"}:
                    if _bbox_delta(baseline, mutated) > TOLERANCE or abs(baseline["volume"] - mutated["volume"]) > TOLERANCE:
                        raise ValueError("placement mutation changed non-positional observables")
                    original = canonical_sequence(entry)["operations"][2]["positions_xy"]
                    changed = canonical_sequence(apply_mutation(entry, mutation))["operations"][2]["positions_xy"]
                    if original == changed:
                        raise ValueError("placement mutation did not change pattern positions")
                elif _bbox_delta(baseline, mutated) > TOLERANCE or mutated["volume"] >= baseline["volume"]:
                    raise ValueError("pattern mutation did not increase removed volume")
        rows.append({"case_id": entry["case_id"], "gates": gates, "mutations": len(entry["mutations"])})
    return rows


if __name__ == "__main__":
    print(f"repeated-feature pattern sequence-pair audit passed: {len(audit())} records")
