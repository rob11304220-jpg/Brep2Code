"""Offline three-layer audit for the frozen ``rounded-slot-v1`` family."""

from __future__ import annotations

import copy
import hashlib
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
EXPANSION = ROOT / "docs/corpus/sequence-paired/rounded-slot-v1-expansion.json"
TOLERANCE = 1e-5


def canonical_sequence(entry: dict[str, Any]) -> dict[str, Any]:
    """Return the sole allowed sequence, including its profile dependency."""

    params = entry["parameters"]
    center = params["center_xy"]
    width, length = params["width"], params["straight_length"]
    if not isinstance(center, list) or len(center) != 2 or min(width, length) <= 0:
        raise ValueError("rounded-slot parameters are invalid")
    radius = width / 2.0
    base_length_x = params.get("base_length_x", 30.0)
    if center[0] - length / 2.0 - radius <= 0 or center[0] + length / 2.0 + radius >= base_length_x:
        raise ValueError("rounded slot exceeds base X extent")
    if center[1] - radius <= 0 or center[1] + radius >= 20:
        raise ValueError("rounded slot exceeds base Y extent")
    return {
        "operations": [
            {"id": "sketch_1", "kind": "SketchRect", "plane": "XY", "length_x": base_length_x, "length_y": 20.0},
            {"id": "base_1", "kind": "ExtrudeBase", "profile": "sketch_1", "direction": "+Z", "distance": 5.0},
            {"id": "slot_sketch_1", "kind": "SketchRoundedSlot", "plane": "XY", "support": "base_1", "center_xy": center, "width": width, "straight_length": length, "cap_radius": radius},
            {"id": "slot_cut_1", "kind": "CutThrough", "target": "base_1", "profile": "slot_sketch_1", "direction": "+Z"},
        ]
    }


def assert_sequence_agreement(candidate: dict[str, Any], entry: dict[str, Any]) -> None:
    if candidate != canonical_sequence(entry):
        raise ValueError("candidate sequence differs from declared rounded-slot oracle")


def build_shape(entry: dict[str, Any]):
    params = entry["parameters"]
    x, y = params["center_xy"]
    width, length = params["width"], params["straight_length"]
    base = BRepPrimAPI_MakeBox(params.get("base_length_x", 30.0), 20.0, 5.0).Shape()
    cutter = BRepPrimAPI_MakeBox(gp_Pnt(x - length / 2.0, y - width / 2.0, -1.0), length, width, 7.0).Shape()
    for cap_x in (x - length / 2.0, x + length / 2.0):
        cap = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(cap_x, y, -1.0), gp_Dir(0, 0, 1)), width / 2.0, 7.0).Shape()
        cutter = BRepAlgoAPI_Fuse(cutter, cap).Shape()
    return BRepAlgoAPI_Cut(base, cutter).Shape()


def replay_summary(entry: dict[str, Any], directory: Path) -> dict[str, Any]:
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "model.step"
    write_step(build_shape(entry), output)
    return probe_summary(load_model(output))


def apply_mutation(entry: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(entry)
    if mutation["kind"] == "base_length_x":
        candidate["parameters"]["base_length_x"] = candidate["parameters"].get("base_length_x", 30.0) + mutation["delta"]
        canonical_sequence(candidate)
        return candidate
    key = {"slot_width": "width", "straight_length": "straight_length"}.get(mutation["kind"])
    if key is None:
        raise ValueError("mutation is incompatible with rounded-slot grammar")
    candidate["parameters"][key] += mutation["delta"]
    canonical_sequence(candidate)
    return candidate


def _record_path(entry: dict[str, Any]) -> Path:
    if "case_record" in entry:
        return ROOT / entry["case_record"]
    return ROOT / entry["candidate_directory"] / "case.json"


def audit(record_path: Path = EXPANSION) -> list[dict[str, Any]]:
    record = load_json(record_path)
    cases = record.get("cases")
    if record.get("selection_status") != "preregistered_before_candidate_production" or not isinstance(cases, list) or len(cases) != 6:
        raise ValueError("rounded-slot record must retain exactly six preregistered rows")
    family_splits = {entry["family_id"]: entry["data_split"] for entry in cases}
    if len(family_splits) != 2 or set(family_splits.values()) != {"development", "held_out"}:
        raise ValueError("family split leak detected")
    if sum(entry["data_split"] == "development" for entry in cases) != 3:
        raise ValueError("rounded-slot development count changed")
    rows = []
    for entry in cases:
        path = _record_path(entry)
        case = load_json(path)
        input_path = path.parent / case["input_step"]
        if hashlib.sha256(input_path.read_bytes()).hexdigest() != case["sha256"]:
            raise ValueError(f"input SHA-256 mismatch: {entry['case_id']}")
        candidate_path = path.parent / "candidate_sequence.json"
        if candidate_path.is_file():
            assert_sequence_agreement(load_json(candidate_path)["sequence"], entry)
        with tempfile.TemporaryDirectory(prefix="brep2code-m21-") as temp_dir:
            workdir = Path(temp_dir)
            baseline = replay_summary(entry, workdir)
            gates = _comparison_gates(probe_summary(load_model(input_path)), baseline)
            if not all(gate["status"] == "pass" for gate in gates):
                raise ValueError(f"geometry replay mismatch: {entry['case_id']}")
            for index, mutation in enumerate(entry["mutations"]):
                mutated = replay_summary(apply_mutation(entry, mutation), workdir / str(index))
                if mutation["kind"] == "base_length_x":
                    if abs(mutated["bbox"]["max"][0] - baseline["bbox"]["max"][0] - mutation["delta"]) > TOLERANCE or mutated["volume"] <= baseline["volume"]:
                        raise ValueError("base mutation did not change extent and volume as declared")
                else:
                    if max(abs(a - b) for first, second in zip((baseline["bbox"]["min"], baseline["bbox"]["max"]), (mutated["bbox"]["min"], mutated["bbox"]["max"]), strict=True) for a, b in zip(first, second, strict=True)) > TOLERANCE:
                        raise ValueError("slot mutation changed the outer bbox")
                    if mutated["volume"] >= baseline["volume"]:
                        raise ValueError("slot mutation did not increase removed volume")
        rows.append({"case_id": entry["case_id"], "gates": gates, "mutations": len(entry["mutations"])})
    return rows


if __name__ == "__main__":
    rows = audit()
    print(f"rounded-slot sequence-pair audit passed: {len(rows)} records")
