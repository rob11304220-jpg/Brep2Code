"""Offline audit for the frozen ``oriented-rounded-slot-v1`` family."""

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
try:  # Supports both package import and direct script execution.
    from tools.audit_sequence_paired_prismatic_hole import load_json, write_step
except ModuleNotFoundError:  # pragma: no cover - direct script entrypoint only
    from audit_sequence_paired_prismatic_hole import load_json, write_step


ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "docs/corpus/sequence-paired/oriented-rounded-slot-v1-preregistration.json"
TOLERANCE = 1e-5
_FRAMES = {0: "+X", 90: "+Y"}


def canonical_sequence(entry: dict[str, Any]) -> dict[str, Any]:
    params = entry["parameters"]
    scalars = ("base_length_x", "base_length_y", "base_height", "width", "straight_length")
    if not all(isinstance(params.get(name), (int, float)) and params[name] > 0 for name in scalars):
        raise ValueError("oriented rounded-slot dimensions must be positive")
    center = params.get("center_xy")
    if not isinstance(center, list) or len(center) != 2 or not all(isinstance(value, (int, float)) for value in center):
        raise ValueError("oriented rounded-slot centre must be two numeric coordinates")
    angle = params.get("orientation_degrees")
    if angle not in _FRAMES or params.get("local_axis") != _FRAMES[angle]:
        raise ValueError("oriented rounded-slot local axis and orientation must agree")
    radius = params["width"] / 2.0
    half_x, half_y = ((params["straight_length"] / 2.0 + radius), radius) if angle == 0 else (radius, (params["straight_length"] / 2.0 + radius))
    if not (half_x < center[0] < params["base_length_x"] - half_x and half_y < center[1] < params["base_length_y"] - half_y):
        raise ValueError("oriented rounded slot exceeds base extent")
    return {"operations": [
        {"id": "sketch_base", "kind": "SketchRect", "plane": "XY", "length_x": params["base_length_x"], "length_y": params["base_length_y"]},
        {"id": "base", "kind": "ExtrudeBase", "profile": "sketch_base", "direction": "+Z", "distance": params["base_height"]},
        {"id": "sketch_slot", "kind": "SketchRoundedSlot", "plane": "XY", "support": "base.top_face", "center_xy": center, "width": params["width"], "straight_length": params["straight_length"], "orientation_degrees": angle, "local_axis": params["local_axis"], "cap_radius": radius},
        {"id": "slot_cut", "kind": "CutThrough", "target": "base", "profile": "sketch_slot", "direction": "+Z"},
    ]}


def assert_sequence_agreement(candidate: dict[str, Any], entry: dict[str, Any]) -> None:
    if candidate != canonical_sequence(entry):
        raise ValueError("candidate sequence differs from declared oriented rounded-slot oracle")


def build_shape(entry: dict[str, Any]):
    operations = canonical_sequence(entry)["operations"]
    sketch, base, slot, _ = operations
    base_shape = BRepPrimAPI_MakeBox(sketch["length_x"], sketch["length_y"], base["distance"]).Shape()
    x, y = slot["center_xy"]
    width, length, height = slot["width"], slot["straight_length"], base["distance"] + 2.0
    if slot["orientation_degrees"] == 0:
        cutter = BRepPrimAPI_MakeBox(gp_Pnt(x - length / 2.0, y - width / 2.0, -1.0), length, width, height).Shape()
        caps = ((x - length / 2.0, y), (x + length / 2.0, y))
    else:
        cutter = BRepPrimAPI_MakeBox(gp_Pnt(x - width / 2.0, y - length / 2.0, -1.0), width, length, height).Shape()
        caps = ((x, y - length / 2.0), (x, y + length / 2.0))
    for cap_x, cap_y in caps:
        cutter = BRepAlgoAPI_Fuse(cutter, BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(cap_x, cap_y, -1.0), gp_Dir(0, 0, 1)), width / 2.0, height).Shape()).Shape()
    return BRepAlgoAPI_Cut(base_shape, cutter).Shape()


def replay_summary(entry: dict[str, Any], directory: Path) -> dict[str, Any]:
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "model.step"
    write_step(build_shape(entry), output)
    return probe_summary(load_model(output))


def apply_mutation(entry: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(entry)
    params = candidate["parameters"]
    kind = mutation["kind"]
    if kind == "base_length_x":
        params["base_length_x"] += mutation["delta"]
    elif kind == "slot_width":
        params["width"] += mutation["delta"]
    elif kind == "straight_length":
        params["straight_length"] += mutation["delta"]
    elif kind == "center_perpendicular":
        params["center_xy"][1 if params["orientation_degrees"] == 0 else 0] += mutation["delta"]
    else:
        raise ValueError("mutation is incompatible with oriented rounded-slot grammar")
    canonical_sequence(candidate)
    return candidate


def _bbox_delta(first: dict[str, Any], second: dict[str, Any]) -> float:
    return max(abs(left - right) for values_a, values_b in zip((first["bbox"]["min"], first["bbox"]["max"]), (second["bbox"]["min"], second["bbox"]["max"]), strict=True) for left, right in zip(values_a, values_b, strict=True))


def assert_semantic_invariants(entry: dict[str, Any], summary: dict[str, Any]) -> None:
    params = entry["parameters"]
    expected = params["base_length_x"] * params["base_length_y"] * params["base_height"] - (params["width"] * params["straight_length"] + math.pi * (params["width"] / 2.0) ** 2) * params["base_height"]
    if summary["counts"]["solid"] != 1 or abs(summary["volume"] - expected) > TOLERANCE:
        raise ValueError("oriented rounded-slot semantic invariant failed")


def audit(record_path: Path = EXPANSION) -> list[dict[str, Any]]:
    record = load_json(record_path)
    cases = record.get("cases")
    if record.get("selection_status") != "preregistered_before_candidate_production" or not isinstance(cases, list) or len(cases) != 6:
        raise ValueError("oriented rounded-slot record must retain exactly six preregistered rows")
    development = [entry for entry in cases if entry.get("data_split") == "development"]
    held_out = [entry for entry in cases if entry.get("data_split") == "held_out"]
    if len(development) != 3 or len(held_out) != 3 or {entry.get("family_id") for entry in development} != {"oriented_rounded_slot_x"} or {entry.get("family_id") for entry in held_out} != {"oriented_rounded_slot_y"}:
        raise ValueError("family split leak detected")
    rows = []
    for entry in cases:
        canonical_sequence(entry)
        directory = ROOT / entry["candidate_directory"]
        case = load_json(directory / "case.json")
        input_path = directory / case["input_step"]
        if case.get("status") != "active" or case.get("data_split") != entry["data_split"] or case.get("family_id") != entry["family_id"] or hashlib.sha256(input_path.read_bytes()).hexdigest() != case.get("sha256"):
            raise ValueError(f"candidate metadata drift: {entry['case_id']}")
        candidate = load_json(directory / "candidate_sequence.json")
        if candidate.get("grammar_version") != record["grammar_version"]:
            raise ValueError("candidate sequence grammar drift")
        assert_sequence_agreement(candidate.get("sequence", {}), entry)
        with tempfile.TemporaryDirectory(prefix="brep2code-m27-") as temp:
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
                elif mutation["kind"] == "center_perpendicular":
                    if _bbox_delta(baseline, mutated) > TOLERANCE or abs(baseline["volume"] - mutated["volume"]) > TOLERANCE:
                        raise ValueError("perpendicular-centre mutation changed non-positional observables")
                elif _bbox_delta(baseline, mutated) > TOLERANCE or mutated["volume"] >= baseline["volume"]:
                    raise ValueError("slot mutation did not increase removed volume")
        rows.append({"case_id": entry["case_id"], "gates": gates, "mutations": len(entry["mutations"])})
    return rows


if __name__ == "__main__":
    print(f"oriented rounded-slot sequence-pair audit passed: {len(audit())} records")
