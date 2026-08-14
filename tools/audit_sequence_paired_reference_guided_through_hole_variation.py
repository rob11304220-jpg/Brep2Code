"""Offline audit for M94's frozen reference-guided through-hole candidates."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import tempfile
from pathlib import Path
from typing import Any

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

from brep2code.agent.harness import _comparison_gates
from brep2code.brep.probes import load_model, probe_summary
try:  # Supports both ``python tools/...`` and package import from tests.
    from tools.audit_sequence_paired_prismatic_hole import load_json, write_step
except ModuleNotFoundError:  # pragma: no cover - direct script entrypoint only
    from audit_sequence_paired_prismatic_hole import load_json, write_step


ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "docs/corpus/sequence-paired/reference-guided-through-hole-variation-v1-preregistration.json"
TOLERANCE = 1e-5
BASE_LENGTH_X = 30.0
BASE_LENGTH_Y = 20.0
BASE_HEIGHT = 10.0
FORBIDDEN_METADATA_KEYS = {"provider_payload", "runtime_resource", "training_input", "manifest_entry", "registry_entry"}


def _parameters(entry: dict[str, Any]) -> tuple[float, float]:
    params = entry.get("parameters")
    if not isinstance(params, dict):
        raise ValueError("parameters must be an object")
    radius, x = params.get("radius"), params.get("x")
    if not isinstance(radius, (int, float)) or not isinstance(x, (int, float)):
        raise ValueError("radius and x must be numeric")
    radius, x = float(radius), float(x)
    if not 0.0 < radius < 10.0 or not radius < x < BASE_LENGTH_X - radius:
        raise ValueError("through-hole containment failed")
    return radius, x


def canonical_sequence(entry: dict[str, Any]) -> dict[str, Any]:
    """Return the one permitted four-operation oracle sequence."""

    radius, x = _parameters(entry)
    return {"operations": [
        {"id": "sketch_base", "kind": "SketchRect", "plane": "XY", "length_x": BASE_LENGTH_X, "length_y": BASE_LENGTH_Y},
        {"id": "base", "kind": "ExtrudeBase", "profile": "sketch_base", "direction": "+Z", "distance": BASE_HEIGHT},
        {"id": "hole_tool", "kind": "MakeCylinder", "axis": "+Z", "center_xy": [x, 10.0], "start_z": -1.0, "radius": radius, "height": BASE_HEIGHT + 2.0},
        {"id": "through_cut", "kind": "CutThroughAll", "target": "base", "tool": "hole_tool", "direction": "+Z"},
    ]}


def build_shape(entry: dict[str, Any]):
    sequence = canonical_sequence(entry)["operations"]
    sketch, base, hole, _ = sequence
    block = BRepPrimAPI_MakeBox(sketch["length_x"], sketch["length_y"], base["distance"]).Shape()
    x, y = hole["center_xy"]
    cutter = BRepPrimAPI_MakeCylinder(
        gp_Ax2(gp_Pnt(x, y, hole["start_z"]), gp_Dir(0.0, 0.0, 1.0)),
        hole["radius"],
        hole["height"],
    ).Shape()
    return BRepAlgoAPI_Cut(block, cutter).Shape()


def replay_summary(entry: dict[str, Any], directory: Path) -> dict[str, Any]:
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "model.step"
    write_step(build_shape(entry), output)
    return probe_summary(load_model(output))


def apply_mutation(entry: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(entry)
    parameters = candidate["parameters"]
    kind = mutation["kind"]
    if kind == "base_length_x":
        # This mutation tests sequence editability, not the fixed 30-mm
        # candidate contract; build it directly in the audit below.
        candidate["_mutated_base_length_x"] = BASE_LENGTH_X + mutation["delta"]
    elif kind == "hole_radius":
        parameters["radius"] += mutation["delta"]
    elif kind == "hole_x":
        parameters["x"] += mutation["delta"]
    else:
        raise ValueError("mutation is incompatible with through-hole grammar")
    _parameters(candidate)
    return candidate


def _build_mutated_shape(entry: dict[str, Any]):
    length_x = float(entry.get("_mutated_base_length_x", BASE_LENGTH_X))
    radius, x = _parameters(entry)
    if not radius < x < length_x - radius:
        raise ValueError("mutated base containment failed")
    block = BRepPrimAPI_MakeBox(length_x, BASE_LENGTH_Y, BASE_HEIGHT).Shape()
    cutter = BRepPrimAPI_MakeCylinder(
        gp_Ax2(gp_Pnt(x, 10.0, -1.0), gp_Dir(0.0, 0.0, 1.0)), radius, BASE_HEIGHT + 2.0
    ).Shape()
    return BRepAlgoAPI_Cut(block, cutter).Shape()


def _mutated_summary(entry: dict[str, Any], directory: Path) -> dict[str, Any]:
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "model.step"
    write_step(_build_mutated_shape(entry), output)
    return probe_summary(load_model(output))


def _bbox_delta(first: dict[str, Any], second: dict[str, Any]) -> float:
    return max(
        abs(left - right)
        for first_group, second_group in zip((first["bbox"]["min"], first["bbox"]["max"]), (second["bbox"]["min"], second["bbox"]["max"]), strict=True)
        for left, right in zip(first_group, second_group, strict=True)
    )


def assert_semantic_invariants(entry: dict[str, Any], summary: dict[str, Any]) -> None:
    radius, _ = _parameters(entry)
    expected_volume = BASE_LENGTH_X * BASE_LENGTH_Y * BASE_HEIGHT - math.pi * radius**2 * BASE_HEIGHT
    if summary["counts"]["solid"] != 1 or abs(summary["volume"] - expected_volume) > TOLERANCE:
        raise ValueError("through-hole semantic invariant failed")
    if summary["bbox"]["min"] != [0.0, 0.0, 0.0] or summary["bbox"]["max"] != [BASE_LENGTH_X, BASE_LENGTH_Y, BASE_HEIGHT]:
        raise ValueError("base extents changed")


def _assert_candidate_only(case: dict[str, Any], entry: dict[str, Any]) -> None:
    if case.get("status") != "experimental" or case.get("data_split") != entry["data_split"] or case.get("family_id") != entry["family_id"]:
        raise ValueError("candidate metadata drift")
    if set(case).intersection(FORBIDDEN_METADATA_KEYS):
        raise ValueError("source leak through candidate metadata")
    boundary = case.get("admission_boundary")
    if not isinstance(boundary, str) or "provider" not in boundary or "runtime" not in boundary:
        raise ValueError("candidate-only admission boundary missing")


def audit(record_path: Path = EXPANSION) -> list[dict[str, Any]]:
    record = load_json(record_path)
    cases = record.get("cases")
    if record.get("selection_status") != "preregistered_before_candidate_production" or not isinstance(cases, list) or len(cases) != 6:
        raise ValueError("M95 requires exactly six preregistered rows")
    development = [entry for entry in cases if entry.get("data_split") == "development"]
    held_out = [entry for entry in cases if entry.get("data_split") == "held_out"]
    if len(development) != 3 or len(held_out) != 3:
        raise ValueError("M95 requires a 3/3 split")
    if {entry.get("family_id") for entry in development} & {entry.get("family_id") for entry in held_out}:
        raise ValueError("family split leak detected")

    rows = []
    for entry in cases:
        directory = ROOT / entry["candidate_directory"]
        case = load_json(directory / "case.json")
        _assert_candidate_only(case, entry)
        input_path = directory / case["input_step"]
        if hashlib.sha256(input_path.read_bytes()).hexdigest() != case.get("sha256"):
            raise ValueError(f"input SHA-256 mismatch: {entry['case_id']}")
        candidate = load_json(directory / "candidate_sequence.json")
        if candidate.get("grammar_version") != record["grammar_version"] or candidate.get("sequence") != canonical_sequence(entry):
            raise ValueError("candidate sequence differs from declared oracle")
        with tempfile.TemporaryDirectory(prefix="brep2code-m95-") as temp:
            baseline = replay_summary(entry, Path(temp))
            gates = _comparison_gates(probe_summary(load_model(input_path)), baseline)
            if not all(gate["status"] == "pass" for gate in gates):
                raise ValueError(f"geometry replay mismatch: {entry['case_id']}")
            assert_semantic_invariants(entry, baseline)
            for index, mutation in enumerate(entry["mutations"]):
                mutated_entry = apply_mutation(entry, mutation)
                mutated = _mutated_summary(mutated_entry, Path(temp) / f"mutation-{index}")
                if mutation["kind"] == "base_length_x":
                    if abs(mutated["bbox"]["max"][0] - baseline["bbox"]["max"][0] - mutation["delta"]) > TOLERANCE or mutated["volume"] <= baseline["volume"]:
                        raise ValueError("base mutation did not change declared observables")
                elif mutation["kind"] == "hole_radius":
                    if _bbox_delta(baseline, mutated) > TOLERANCE or mutated["volume"] >= baseline["volume"]:
                        raise ValueError("radius mutation did not preserve bbox and increase removed volume")
                elif mutation["kind"] == "hole_x":
                    if _bbox_delta(baseline, mutated) > TOLERANCE or abs(mutated["volume"] - baseline["volume"]) > TOLERANCE:
                        raise ValueError("x mutation changed non-positional observables")
                else:  # pragma: no cover - frozen preregistration guards this
                    raise ValueError("unsupported mutation")
        rows.append({"case_id": entry["case_id"], "gates": gates, "mutations": len(entry["mutations"])})
    return rows


if __name__ == "__main__":
    print(json.dumps({"cases": audit(), "status": "pass"}, indent=2))
