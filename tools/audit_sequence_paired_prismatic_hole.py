"""Offline three-layer audit for the M20 prismatic-hole sequence-paired pilot."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

from brep2code.agent.harness import _comparison_gates
from brep2code.brep.probes import load_model, probe_summary

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "docs/corpus/sequence-paired/prismatic-hole-v1-seed.json"
EXPANSION = ROOT / "docs/corpus/sequence-paired/prismatic-hole-v1-expansion.json"
TOLERANCE = 1e-5


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_sequence(sequence: dict[str, Any]) -> list[dict[str, Any]]:
    """Validate and return the exact v1 operation sequence without mutations."""

    operations = sequence.get("operations")
    if not isinstance(operations, list) or len(operations) != 3:
        raise ValueError("sequence must contain exactly three operations")
    sketch, base, cut = operations
    if sketch != {
        "id": "sketch_1",
        "kind": "SketchRect",
        "plane": "XY",
        "length_x": sketch.get("length_x"),
        "length_y": sketch.get("length_y"),
    }:
        raise ValueError("unsupported SketchRect normalization")
    if base != {
        "id": "base_1",
        "kind": "ExtrudeBase",
        "profile": "sketch_1",
        "direction": "+Z",
        "distance": base.get("distance"),
    }:
        raise ValueError("unsupported ExtrudeBase normalization")
    if cut.get("id") != "hole_1" or cut.get("kind") != "CutCylinder":
        raise ValueError("third operation must be CutCylinder hole_1")
    if cut.get("target") != "base_1" or cut.get("axis") != "+Z":
        raise ValueError("CutCylinder must target base_1 on +Z")
    center = cut.get("center_xy")
    if not isinstance(center, list) or len(center) != 2:
        raise ValueError("CutCylinder center_xy must have two coordinates")
    if cut.get("variant") == "through":
        required = {"id", "kind", "target", "variant", "center_xy", "axis", "radius"}
    elif cut.get("variant") == "blind":
        required = {"id", "kind", "target", "variant", "center_xy", "axis", "radius", "depth"}
    elif cut.get("variant") == "counterbore":
        required = {
            "id",
            "kind",
            "target",
            "variant",
            "center_xy",
            "axis",
            "through_radius",
            "bore_radius",
            "bore_depth",
        }
    else:
        raise ValueError("unsupported CutCylinder variant")
    if set(cut) != required:
        raise ValueError("CutCylinder fields do not match its normalized variant")
    numeric = list(sketch.values())[-2:] + [base["distance"]]
    numeric.extend(value for key, value in cut.items() if key.endswith("radius") or key.endswith("depth"))
    if not all(isinstance(value, (int, float)) and value > 0 for value in numeric):
        raise ValueError("all lengths and radii must be positive")
    return copy.deepcopy(operations)


def assert_sequence_agreement(candidate: dict[str, Any], oracle: dict[str, Any]) -> None:
    """Require exact agreement after the pilot's explicit normalization."""

    if canonical_sequence(candidate) != canonical_sequence(oracle):
        raise ValueError("candidate sequence differs from declared oracle")


def build_shape(sequence: dict[str, Any]):
    operations = canonical_sequence(sequence)
    sketch, base, cut = operations
    base_shape = BRepPrimAPI_MakeBox(sketch["length_x"], sketch["length_y"], base["distance"]).Shape()
    x, y = cut["center_xy"]
    distance = base["distance"]

    def cylinder(radius: float, start_z: float, height: float):
        axis = gp_Ax2(gp_Pnt(x, y, start_z), gp_Dir(0.0, 0.0, 1.0))
        return BRepPrimAPI_MakeCylinder(axis, radius, height).Shape()

    if cut["variant"] == "through":
        return BRepAlgoAPI_Cut(base_shape, cylinder(cut["radius"], -1.0, distance + 2.0)).Shape()
    if cut["variant"] == "blind":
        tool = cylinder(cut["radius"], distance - cut["depth"], cut["depth"] + 1.0)
        return BRepAlgoAPI_Cut(base_shape, tool).Shape()
    through = cylinder(cut["through_radius"], -1.0, distance + 2.0)
    bore = cylinder(cut["bore_radius"], distance - cut["bore_depth"], cut["bore_depth"] + 1.0)
    return BRepAlgoAPI_Cut(BRepAlgoAPI_Cut(base_shape, through).Shape(), bore).Shape()


def write_step(shape: Any, path: Path) -> None:
    writer = STEPControl_Writer()
    writer.Transfer(shape, STEPControl_AsIs)
    if writer.Write(str(path)) != IFSelect_RetDone:
        raise RuntimeError(f"failed to write STEP: {path}")


def replay_summary(sequence: dict[str, Any], directory: Path) -> dict[str, Any]:
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "model.step"
    write_step(build_shape(sequence), output)
    return probe_summary(load_model(output))


def apply_mutation(sequence: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(sequence)
    operations = candidate["operations"]
    sketch, _, cut = operations
    delta = mutation["delta"]
    if mutation["kind"] == "base_length_x":
        sketch["length_x"] += delta
    elif mutation["kind"] == "hole_radius" and cut["variant"] in {"through", "blind"}:
        cut["radius"] += delta
    elif mutation["kind"] == "hole_depth" and cut["variant"] == "blind":
        cut["depth"] += delta
    elif mutation["kind"] == "bore_depth" and cut["variant"] == "counterbore":
        cut["bore_depth"] += delta
    else:
        raise ValueError("mutation is incompatible with the declared sequence")
    return candidate


def assert_editability(
    baseline: dict[str, Any], mutated: dict[str, Any], mutation: dict[str, Any]
) -> None:
    baseline_bbox = baseline["bbox"]
    mutated_bbox = mutated["bbox"]
    if mutation["kind"] == "base_length_x":
        actual = mutated_bbox["max"][0] - baseline_bbox["max"][0]
        if abs(actual - mutation["delta"]) > TOLERANCE:
            raise ValueError("base_length_x mutation did not change the X extent as declared")
        if mutated["volume"] <= baseline["volume"]:
            raise ValueError("base_length_x mutation did not increase volume")
        return
    flat_delta = [
        abs(mutated_value - baseline_value)
        for baseline_values, mutated_values in zip(
            (baseline_bbox["min"], baseline_bbox["max"]),
            (mutated_bbox["min"], mutated_bbox["max"]),
            strict=True,
        )
        for baseline_value, mutated_value in zip(baseline_values, mutated_values, strict=True)
    ]
    if max(flat_delta) > TOLERANCE:
        raise ValueError("hole mutation changed the outer bbox")
    if mutated["volume"] >= baseline["volume"]:
        raise ValueError("hole mutation did not decrease volume")


def audit_case(entry: dict[str, Any]) -> dict[str, Any]:
    record_path = ROOT / entry["case_record"]
    record = load_json(record_path)
    if record["case_id"] != entry["case_id"]:
        raise ValueError("case record id does not match seed entry")
    input_path = record_path.parent / record["input_step"]
    if hashlib.sha256(input_path.read_bytes()).hexdigest() != record["sha256"]:
        raise ValueError(f"input SHA-256 mismatch: {entry['case_id']}")
    sequence = entry["sequence"]
    canonical_sequence(sequence)
    candidate_path = entry.get("candidate_sequence")
    if candidate_path is not None:
        candidate = load_json(ROOT / candidate_path)
        if candidate.get("grammar_version") != "prismatic-hole-v1":
            raise ValueError("candidate sequence has an unsupported grammar version")
        assert_sequence_agreement(candidate.get("sequence", {}), sequence)
    with tempfile.TemporaryDirectory(prefix="brep2code-m20-") as temp_dir:
        workdir = Path(temp_dir)
        input_summary = probe_summary(load_model(input_path))
        output_summary = replay_summary(sequence, workdir)
        gates = _comparison_gates(input_summary, output_summary)
        if not all(gate["status"] == "pass" for gate in gates):
            raise ValueError(f"geometry gates failed: {entry['case_id']}")
        for index, mutation in enumerate(sequence["mutations"]):
            mutated = replay_summary(apply_mutation(sequence, mutation), workdir / f"mutation-{index}")
            assert_editability(output_summary, mutated, mutation)
    return {"case_id": entry["case_id"], "gates": gates, "mutations": len(sequence["mutations"])}


def audit(record_path: Path = EXPANSION) -> list[dict[str, Any]]:
    record = load_json(record_path)
    if record.get("grammar_version") != "prismatic-hole-v1":
        raise ValueError("unsupported pilot grammar version")
    if record.get("selection_status") != "preregistered":
        raise ValueError("record must be preregistered before audit")
    cases = record.get("cases")
    if not isinstance(cases, list):
        raise ValueError("record must contain a case list")
    family_splits: dict[str, set[str]] = {}
    for entry in cases:
        family_splits.setdefault(entry["family_id"], set()).add(entry["data_split"])
    if any(len(splits) != 1 for splits in family_splits.values()):
        raise ValueError("family split leak detected")
    families = {family: next(iter(splits)) for family, splits in family_splits.items()}
    if len(families) != 3 or set(families.values()) != {"development", "held_out"}:
        raise ValueError("record must keep three isolated families across both splits")
    if record.get("expansion_id") == "prismatic-hole-v1-m20-002":
        if len(cases) != 9:
            raise ValueError("M20-002 must retain exactly nine preregistered cases")
        split_counts = {split: sum(entry["data_split"] == split for entry in cases) for split in families.values()}
        if split_counts != {"development": 6, "held_out": 3}:
            raise ValueError("M20-002 must retain its 6 development / 3 held-out split")
        if {entry["family_id"] for entry in cases if entry["data_split"] == "development"} != {"through_hole", "counterbore"}:
            raise ValueError("M20-002 development families do not match preregistration")
        if {entry["family_id"] for entry in cases if entry["data_split"] == "held_out"} != {"blind_hole"}:
            raise ValueError("M20-002 held-out family does not match preregistration")
    elif len(cases) != 3:
        raise ValueError("pilot seed must retain exactly three preregistered seed cases")
    return [audit_case(entry) for entry in cases]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, default=EXPANSION)
    args = parser.parse_args()
    rows = audit(args.record)
    print(json.dumps({"cases": rows, "status": "pass"}, indent=2))


if __name__ == "__main__":
    main()
