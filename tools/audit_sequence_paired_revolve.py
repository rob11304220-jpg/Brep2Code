"""Offline audit for the frozen ``revolve-v1`` experimental family."""

from __future__ import annotations

import copy
import hashlib
import math
import tempfile
from pathlib import Path
from typing import Any

from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakePolygon
from OCP.BRepPrimAPI import BRepPrimAPI_MakeRevol
from OCP.gp import gp_Ax1, gp_Dir, gp_Pnt

from brep2code.agent.harness import _comparison_gates
from brep2code.brep.probes import load_model, probe_summary

try:
    from tools.audit_sequence_paired_prismatic_hole import load_json, write_step
except ModuleNotFoundError:  # pragma: no cover
    from audit_sequence_paired_prismatic_hole import load_json, write_step

ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "docs/corpus/sequence-paired/revolve-v1-preregistration.json"
TOLERANCE = 1e-5


def _p(entry: dict[str, Any]) -> dict[str, float]:
    values = entry["parameters"]
    required = (
        "axis_x",
        "z_min",
        "inner_radius",
        "lower_outer_radius",
        "upper_outer_radius",
        "lower_height",
        "upper_height",
        "angle_deg",
    )
    if not all(isinstance(values.get(k), (int, float)) for k in required):
        raise ValueError("missing_q01_fact")
    p = {k: float(values[k]) for k in required}
    if not (
        0 < p["inner_radius"] < p["upper_outer_radius"] < p["lower_outer_radius"]
        and p["z_min"] < p["lower_height"] < p["upper_height"]
    ):
        raise ValueError("radius_or_height_order_failure")
    if p["angle_deg"] != 360.0:
        raise ValueError("partial_angle")
    return p


def canonical_sequence(entry: dict[str, Any]) -> dict[str, Any]:
    p = _p(entry)
    return {
        "operations": [
            {
                "id": "sketch_profile",
                "kind": "SketchSteppedRadialProfile",
                "plane": "XZ",
                "radial_side": "positive_x_from_declared_axis",
                "axis_x": p["axis_x"],
            },
            {
                "id": "revolve",
                "kind": "RevolveFace",
                "profile": "sketch_profile",
                "axis": {"origin_role": "declared_axis_origin", "direction": "+Z"},
                "angle_deg": p["angle_deg"],
            },
        ]
    }


def build_shape(entry: dict[str, Any]):
    p = _p(entry)
    x = p["axis_x"]
    z = p["z_min"]
    points = [
        (x + p["inner_radius"], z),
        (x + p["lower_outer_radius"], z),
        (x + p["lower_outer_radius"], p["lower_height"]),
        (x + p["upper_outer_radius"], p["lower_height"]),
        (x + p["upper_outer_radius"], p["upper_height"]),
        (x + p["inner_radius"], p["upper_height"]),
    ]
    wire = BRepBuilderAPI_MakePolygon()
    for px, pz in points:
        wire.Add(gp_Pnt(px, 0.0, pz))
    wire.Close()
    return BRepPrimAPI_MakeRevol(
        BRepBuilderAPI_MakeFace(wire.Wire()).Face(),
        gp_Ax1(gp_Pnt(x, 0.0, z), gp_Dir(0, 0, 1)),
        2.0 * math.pi,
    ).Shape()


def replay_summary(entry: dict[str, Any], directory: Path) -> dict[str, Any]:
    directory.mkdir(parents=True, exist_ok=True)
    out = directory / "model.step"
    write_step(build_shape(entry), out)
    return probe_summary(load_model(out))


def apply_mutation(entry: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    changed = copy.deepcopy(entry)
    changed["parameters"][mutation["kind"]] += mutation["delta"]
    _p(changed)
    return changed


def assert_semantic_invariants(entry: dict[str, Any], summary: dict[str, Any]) -> None:
    p = _p(entry)
    expected = math.pi * (
        (p["lower_outer_radius"] ** 2 - p["inner_radius"] ** 2) * (p["lower_height"] - p["z_min"])
        + (p["upper_outer_radius"] ** 2 - p["inner_radius"] ** 2)
        * (p["upper_height"] - p["lower_height"])
    )
    if summary["counts"]["solid"] != 1 or abs(summary["volume"] - expected) > TOLERANCE:
        raise ValueError("semantic degeneration")


def audit(record_path: Path = EXPANSION) -> list[dict[str, Any]]:
    record = load_json(record_path)
    cases = record.get("cases")
    if not isinstance(cases, list) or len(cases) != 6:
        raise ValueError("revolve requires six frozen rows")
    dev = [e for e in cases if e.get("data_split") == "development"]
    held = [e for e in cases if e.get("data_split") == "held_out"]
    if (
        len(dev) != 3
        or len(held) != 3
        or {e.get("family_id") for e in dev} != {"revolve_centered"}
        or {e.get("family_id") for e in held} != {"revolve_offset"}
    ):
        raise ValueError("split_leak")
    result = []
    for entry in cases:
        directory = ROOT / entry["candidate_directory"]
        case = load_json(directory / "case.json")
        input_path = directory / case["input_step"]
        if (
            case.get("status") not in {"experimental", "active"}
            or case.get("parameters") != entry["parameters"]
            or hashlib.sha256(input_path.read_bytes()).hexdigest() != case.get("sha256")
        ):
            raise ValueError("candidate metadata drift")
        if load_json(directory / "candidate_sequence.json").get("sequence") != canonical_sequence(
            entry
        ):
            raise ValueError("sequence_mismatch")
        with tempfile.TemporaryDirectory(prefix="brep2code-m106-") as temp:
            baseline = replay_summary(entry, Path(temp))
            gates = _comparison_gates(probe_summary(load_model(input_path)), baseline)
            if not all(g["status"] == "pass" for g in gates):
                raise ValueError("geometry replay mismatch")
            assert_semantic_invariants(entry, baseline)
            for i, mutation in enumerate(entry["mutations"]):
                mutated = replay_summary(apply_mutation(entry, mutation), Path(temp) / str(i))
                assert_semantic_invariants(apply_mutation(entry, mutation), mutated)
        result.append(
            {"case_id": entry["case_id"], "gates": gates, "mutations": len(entry["mutations"])}
        )
    return result


if __name__ == "__main__":
    print(f"revolve sequence-pair audit passed: {len(audit())} records")
