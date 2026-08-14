"""Offline audit for the frozen ``multi-inner-loop-pocket-v1`` family."""

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
EXPANSION = ROOT / "docs/corpus/sequence-paired/multi-inner-loop-pocket-v1-preregistration.json"
TOLERANCE = 1e-5


def _inside(center: list[float], size_x: float, size_y: float, outer_center: list[float], outer_x: float, outer_y: float) -> bool:
    return center[0] - size_x / 2 > outer_center[0] - outer_x / 2 and center[0] + size_x / 2 < outer_center[0] + outer_x / 2 and center[1] - size_y / 2 > outer_center[1] - outer_y / 2 and center[1] + size_y / 2 < outer_center[1] + outer_y / 2


def _disjoint(first: list[float], second: list[float], size_x: float, size_y: float) -> bool:
    return abs(first[0] - second[0]) > size_x or abs(first[1] - second[1]) > size_y


def canonical_sequence(entry: dict[str, Any]) -> dict[str, Any]:
    params = entry["parameters"]
    scalars = ("base_length_x", "base_length_y", "base_height", "outer_length_x", "outer_length_y", "inner_length_x", "inner_length_y", "pocket_depth")
    if not all(isinstance(params.get(name), (int, float)) and params[name] > 0 for name in scalars):
        raise ValueError("multi-inner-loop pocket dimensions must be positive")
    centers = (params.get("outer_center_xy"), params.get("inner_left_center_xy"), params.get("inner_right_center_xy"))
    if not all(isinstance(center, list) and len(center) == 2 and all(isinstance(value, (int, float)) for value in center) for center in centers):
        raise ValueError("multi-inner-loop pocket centers must be two numeric coordinates")
    base_center = [params["base_length_x"] / 2, params["base_length_y"] / 2]
    outer, left, right = centers
    if not _inside(outer, params["outer_length_x"], params["outer_length_y"], base_center, params["base_length_x"], params["base_length_y"]):
        raise ValueError("outer loop must be strictly contained in base")
    if not all(_inside(center, params["inner_length_x"], params["inner_length_y"], outer, params["outer_length_x"], params["outer_length_y"]) for center in (left, right)):
        raise ValueError("inner loops must be strictly contained in outer loop")
    if not _disjoint(left, right, params["inner_length_x"], params["inner_length_y"]):
        raise ValueError("inner loops must not overlap")
    if params["pocket_depth"] >= params["base_height"]:
        raise ValueError("pocket must be blind")
    return {"operations": [
        {"id": "sketch_base", "kind": "SketchRect", "plane": "XY", "length_x": params["base_length_x"], "length_y": params["base_length_y"]},
        {"id": "base", "kind": "ExtrudeBase", "profile": "sketch_base", "direction": "+Z", "distance": params["base_height"]},
        {"id": "sketch_pocket", "kind": "SketchPocketLoops", "support": "base.top_face", "outer_center_xy": outer, "outer_length_x": params["outer_length_x"], "outer_length_y": params["outer_length_y"], "inner_left_center_xy": left, "inner_right_center_xy": right, "inner_length_x": params["inner_length_x"], "inner_length_y": params["inner_length_y"]},
        {"id": "pocket", "kind": "CutPocket", "target": "base", "profile": "sketch_pocket", "direction": "-Z", "variant": "blind", "depth": params["pocket_depth"]},
    ]}


def assert_sequence_agreement(candidate: dict[str, Any], entry: dict[str, Any]) -> None:
    if candidate != canonical_sequence(entry):
        raise ValueError("candidate sequence differs from declared multi-inner-loop pocket oracle")


def build_shape(entry: dict[str, Any]):
    operations = canonical_sequence(entry)["operations"]
    sketch, base, loops, pocket = operations
    base_shape = BRepPrimAPI_MakeBox(sketch["length_x"], sketch["length_y"], base["distance"]).Shape()
    start_z = base["distance"] - pocket["depth"]
    outer_x, outer_y = loops["outer_center_xy"]
    outer = BRepPrimAPI_MakeBox(gp_Pnt(outer_x - loops["outer_length_x"] / 2, outer_y - loops["outer_length_y"] / 2, start_z), loops["outer_length_x"], loops["outer_length_y"], pocket["depth"] + 1).Shape()
    result = BRepAlgoAPI_Cut(base_shape, outer).Shape()
    for center in (loops["inner_left_center_xy"], loops["inner_right_center_xy"]):
        island = BRepPrimAPI_MakeBox(gp_Pnt(center[0] - loops["inner_length_x"] / 2, center[1] - loops["inner_length_y"] / 2, start_z), loops["inner_length_x"], loops["inner_length_y"], pocket["depth"]).Shape()
        result = BRepAlgoAPI_Fuse(result, island).Shape()
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
    if kind in {"base_length_x", "outer_length_x", "inner_left_length_x", "inner_right_length_y", "pocket_depth"}:
        key = {"inner_left_length_x": "inner_length_x", "inner_right_length_y": "inner_length_y"}.get(kind, kind)
        params[key] += mutation["delta"]
    elif kind == "inner_separation_x":
        params["inner_left_center_xy"][0] -= mutation["delta"] / 2
        params["inner_right_center_xy"][0] += mutation["delta"] / 2
    else:
        raise ValueError("mutation is incompatible with multi-inner-loop pocket grammar")
    canonical_sequence(candidate)
    return candidate


def _bbox_delta(first: dict[str, Any], second: dict[str, Any]) -> float:
    return max(abs(left - right) for first_values, second_values in zip((first["bbox"]["min"], first["bbox"]["max"]), (second["bbox"]["min"], second["bbox"]["max"]), strict=True) for left, right in zip(first_values, second_values, strict=True))


def assert_semantic_invariants(entry: dict[str, Any], summary: dict[str, Any]) -> None:
    params = entry["parameters"]
    expected = params["base_length_x"] * params["base_length_y"] * params["base_height"] - (params["outer_length_x"] * params["outer_length_y"] - 2 * params["inner_length_x"] * params["inner_length_y"]) * params["pocket_depth"]
    extent = {"bbox": {"min": [0.0, 0.0, 0.0], "max": [params["base_length_x"], params["base_length_y"], params["base_height"]]}}
    if summary["counts"]["solid"] != 1 or _bbox_delta(summary, extent) > TOLERANCE or abs(summary["volume"] - expected) > TOLERANCE:
        raise ValueError("multi-inner-loop pocket semantic invariant failed")


def audit(record_path: Path = EXPANSION) -> list[dict[str, Any]]:
    record = load_json(record_path)
    cases = record.get("cases")
    if record.get("selection_status") != "preregistered_before_candidate_production" or not isinstance(cases, list) or len(cases) != 6:
        raise ValueError("multi-inner-loop record must retain exactly six preregistered rows")
    development = [entry for entry in cases if entry.get("data_split") == "development"]
    held_out = [entry for entry in cases if entry.get("data_split") == "held_out"]
    if len(development) != 3 or len(held_out) != 3 or {entry.get("family_id") for entry in development} != {"multi_inner_loop_pocket_centered"} or {entry.get("family_id") for entry in held_out} != {"multi_inner_loop_pocket_offset"}:
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
        with tempfile.TemporaryDirectory(prefix="brep2code-m26-") as temp:
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
                elif mutation["kind"] == "inner_separation_x":
                    if _bbox_delta(baseline, mutated) > TOLERANCE or abs(baseline["volume"] - mutated["volume"]) > TOLERANCE:
                        raise ValueError("separation mutation changed non-positional observables")
                elif mutation["kind"] in {"inner_left_length_x", "inner_right_length_y"}:
                    if _bbox_delta(baseline, mutated) > TOLERANCE or mutated["volume"] <= baseline["volume"]:
                        raise ValueError("inner-island mutation did not enlarge retained volume")
                elif _bbox_delta(baseline, mutated) > TOLERANCE or mutated["volume"] >= baseline["volume"]:
                    raise ValueError("pocket mutation did not increase removed volume")
        rows.append({"case_id": entry["case_id"], "gates": gates, "mutations": len(entry["mutations"])})
    return rows


if __name__ == "__main__":
    print(f"multi-inner-loop pocket sequence-pair audit passed: {len(audit())} records")
