"""Offline three-layer audit for the frozen ``multi-contour-pocket-v1`` family."""

from __future__ import annotations

import copy
import hashlib
import tempfile
from pathlib import Path
from typing import Any

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.gp import gp_Pnt

from brep2code.agent.harness import _comparison_gates
from brep2code.brep.probes import load_model, probe_summary
try:  # Supports both package import and direct script execution.
    from tools.audit_sequence_paired_prismatic_hole import load_json, write_step
except ModuleNotFoundError:  # pragma: no cover - direct script entrypoint only
    from audit_sequence_paired_prismatic_hole import load_json, write_step

ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "docs/corpus/sequence-paired/multi-contour-pocket-v1-preregistration.json"
TOLERANCE = 1e-5


def _positive_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and value > 0


def _inside(center: list[float], length_x: float, length_y: float, container_center: list[float], container_x: float, container_y: float) -> bool:
    return (
        center[0] - length_x / 2.0 > container_center[0] - container_x / 2.0
        and center[0] + length_x / 2.0 < container_center[0] + container_x / 2.0
        and center[1] - length_y / 2.0 > container_center[1] - container_y / 2.0
        and center[1] + length_y / 2.0 < container_center[1] + container_y / 2.0
    )


def canonical_sequence(entry: dict[str, Any]) -> dict[str, Any]:
    """Return the sole permitted, fully parameterized pocket sequence."""

    params = entry["parameters"]
    scalar_names = (
        "base_length_x",
        "base_length_y",
        "base_height",
        "outer_length_x",
        "outer_length_y",
        "inner_length_x",
        "inner_length_y",
        "pocket_depth",
    )
    if not all(_positive_number(params.get(name)) for name in scalar_names):
        raise ValueError("multi-contour pocket dimensions must be positive")
    outer_center = params.get("outer_center_xy")
    inner_center = params.get("inner_center_xy")
    if not all(isinstance(point, list) and len(point) == 2 and all(isinstance(value, (int, float)) for value in point) for point in (outer_center, inner_center)):
        raise ValueError("multi-contour pocket centers must be two numeric coordinates")
    base_center = [params["base_length_x"] / 2.0, params["base_length_y"] / 2.0]
    if not _inside(outer_center, params["outer_length_x"], params["outer_length_y"], base_center, params["base_length_x"], params["base_length_y"]):
        raise ValueError("outer loop must be strictly contained in base")
    if not _inside(inner_center, params["inner_length_x"], params["inner_length_y"], outer_center, params["outer_length_x"], params["outer_length_y"]):
        raise ValueError("inner loop must be strictly contained in outer loop")
    if params["pocket_depth"] >= params["base_height"]:
        raise ValueError("pocket must be blind")
    return {
        "operations": [
            {"id": "sketch_base", "kind": "SketchRect", "plane": "XY", "length_x": params["base_length_x"], "length_y": params["base_length_y"]},
            {"id": "base", "kind": "ExtrudeBase", "profile": "sketch_base", "direction": "+Z", "distance": params["base_height"]},
            {
                "id": "sketch_pocket",
                "kind": "SketchPocketLoops",
                "support": "base.top_face",
                "outer_center_xy": outer_center,
                "outer_length_x": params["outer_length_x"],
                "outer_length_y": params["outer_length_y"],
                "inner_center_xy": inner_center,
                "inner_length_x": params["inner_length_x"],
                "inner_length_y": params["inner_length_y"],
            },
            {"id": "pocket", "kind": "CutPocket", "target": "base", "profile": "sketch_pocket", "direction": "-Z", "variant": "blind", "depth": params["pocket_depth"]},
        ]
    }


def assert_sequence_agreement(candidate: dict[str, Any], entry: dict[str, Any]) -> None:
    if candidate != canonical_sequence(entry):
        raise ValueError("candidate sequence differs from declared multi-contour pocket oracle")


def build_shape(entry: dict[str, Any]):
    """Build a blind annular pocket by removing an outer prism and restoring its inner island."""

    sequence = canonical_sequence(entry)["operations"]
    sketch, base, loops, pocket = sequence
    base_shape = BRepPrimAPI_MakeBox(sketch["length_x"], sketch["length_y"], base["distance"]).Shape()
    start_z = base["distance"] - pocket["depth"]
    outer_x, outer_y = loops["outer_center_xy"]
    inner_x, inner_y = loops["inner_center_xy"]
    outer = BRepPrimAPI_MakeBox(gp_Pnt(outer_x - loops["outer_length_x"] / 2.0, outer_y - loops["outer_length_y"] / 2.0, start_z), loops["outer_length_x"], loops["outer_length_y"], pocket["depth"] + 1.0).Shape()
    inner = BRepPrimAPI_MakeBox(gp_Pnt(inner_x - loops["inner_length_x"] / 2.0, inner_y - loops["inner_length_y"] / 2.0, start_z), loops["inner_length_x"], loops["inner_length_y"], pocket["depth"]).Shape()
    return BRepAlgoAPI_Fuse(BRepAlgoAPI_Cut(base_shape, outer).Shape(), inner).Shape()


def replay_summary(entry: dict[str, Any], directory: Path) -> dict[str, Any]:
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "model.step"
    write_step(build_shape(entry), output)
    return probe_summary(load_model(output))


def apply_mutation(entry: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(entry)
    key = mutation["kind"]
    mapping = {
        "base_length_x": "base_length_x",
        "outer_length_x": "outer_length_x",
        "inner_length_y": "inner_length_y",
        "pocket_depth": "pocket_depth",
    }
    if key not in mapping:
        raise ValueError("mutation is incompatible with multi-contour pocket grammar")
    candidate["parameters"][mapping[key]] += mutation["delta"]
    canonical_sequence(candidate)
    return candidate


def _flat_bbox_delta(first: dict[str, Any], second: dict[str, Any]) -> float:
    return max(
        abs(a - b)
        for first_values, second_values in zip((first["bbox"]["min"], first["bbox"]["max"]), (second["bbox"]["min"], second["bbox"]["max"]), strict=True)
        for a, b in zip(first_values, second_values, strict=True)
    )


def assert_editability(baseline: dict[str, Any], mutated: dict[str, Any], mutation: dict[str, Any]) -> None:
    if mutation["kind"] == "base_length_x":
        if abs(mutated["bbox"]["max"][0] - baseline["bbox"]["max"][0] - mutation["delta"]) > TOLERANCE:
            raise ValueError("base mutation did not change X extent as declared")
        if mutated["volume"] <= baseline["volume"]:
            raise ValueError("base mutation did not increase volume")
        return
    if _flat_bbox_delta(baseline, mutated) > TOLERANCE:
        raise ValueError("pocket mutation changed outer bbox")
    if mutation["kind"] == "inner_length_y":
        if mutated["volume"] <= baseline["volume"]:
            raise ValueError("inner-loop mutation did not enlarge the retained island")
    elif mutated["volume"] >= baseline["volume"]:
        raise ValueError("pocket mutation did not increase removed volume")


def assert_semantic_invariants(entry: dict[str, Any], summary: dict[str, Any]) -> None:
    params = entry["parameters"]
    expected_volume = params["base_length_x"] * params["base_length_y"] * params["base_height"] - (params["outer_length_x"] * params["outer_length_y"] - params["inner_length_x"] * params["inner_length_y"]) * params["pocket_depth"]
    if summary["counts"]["solid"] != 1:
        raise ValueError("pocket must retain one connected solid")
    if _flat_bbox_delta(summary, {"bbox": {"min": [0.0, 0.0, 0.0], "max": [params["base_length_x"], params["base_length_y"], params["base_height"]]}}) > TOLERANCE:
        raise ValueError("pocket must preserve outer base extents")
    if abs(summary["volume"] - expected_volume) > TOLERANCE:
        raise ValueError("pocket volume does not preserve the annular blind-cut invariant")


def _record_path(entry: dict[str, Any]) -> Path:
    return ROOT / entry["candidate_directory"] / "case.json"


def audit(record_path: Path = EXPANSION) -> list[dict[str, Any]]:
    record = load_json(record_path)
    cases = record.get("cases")
    if record.get("selection_status") != "preregistered_before_candidate_production" or not isinstance(cases, list) or len(cases) != 6:
        raise ValueError("multi-contour record must retain exactly six preregistered rows")
    development = [entry for entry in cases if entry.get("data_split") == "development"]
    held_out = [entry for entry in cases if entry.get("data_split") == "held_out"]
    if len(development) != 3 or len(held_out) != 3:
        raise ValueError("multi-contour split counts changed")
    if {entry.get("family_id") for entry in development} != {"multi_contour_pocket_centered"} or {entry.get("family_id") for entry in held_out} != {"multi_contour_pocket_offset"}:
        raise ValueError("family split leak detected")
    rows = []
    for entry in cases:
        canonical_sequence(entry)
        path = _record_path(entry)
        case = load_json(path)
        input_path = path.parent / case["input_step"]
        if case.get("status") != "active" or case.get("data_split") != entry["data_split"] or case.get("family_id") != entry["family_id"]:
            raise ValueError(f"governed metadata drift: {entry['case_id']}")
        if case.get("reference_script_status") != "available" or not (path.parent / case.get("reference_script", "")).is_file():
            raise ValueError(f"reference script drift: {entry['case_id']}")
        if hashlib.sha256(input_path.read_bytes()).hexdigest() != case["sha256"]:
            raise ValueError(f"input SHA-256 mismatch: {entry['case_id']}")
        candidate = load_json(path.parent / "candidate_sequence.json")
        if candidate.get("grammar_version") != record["grammar_version"]:
            raise ValueError("candidate sequence grammar drift")
        assert_sequence_agreement(candidate.get("sequence", {}), entry)
        with tempfile.TemporaryDirectory(prefix="brep2code-m22-") as temp_dir:
            workdir = Path(temp_dir)
            baseline = replay_summary(entry, workdir)
            gates = _comparison_gates(probe_summary(load_model(input_path)), baseline)
            if not all(gate["status"] == "pass" for gate in gates):
                raise ValueError(f"geometry replay mismatch: {entry['case_id']}")
            assert_semantic_invariants(entry, baseline)
            for index, mutation in enumerate(entry["mutations"]):
                mutated = replay_summary(apply_mutation(entry, mutation), workdir / f"mutation-{index}")
                assert_editability(baseline, mutated, mutation)
        rows.append({"case_id": entry["case_id"], "gates": gates, "mutations": len(entry["mutations"])})
    return rows


if __name__ == "__main__":
    rows = audit()
    print(f"multi-contour pocket sequence-pair audit passed: {len(rows)} records")
