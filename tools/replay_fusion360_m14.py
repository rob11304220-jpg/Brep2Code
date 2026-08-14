"""Offline Fusion r1.0.1 replay with a restricted fail-closed Line3D default."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeWire
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.gp import gp_Ax2, gp_Circ, gp_Dir, gp_Pnt, gp_Vec

from brep2code.agent.harness import _comparison_gates
from brep2code.brep.probes import load_model, probe_summary
try:
    from tools.fusion360_line3d_selector import select_signed_axis
except ModuleNotFoundError:  # Direct ``python tools/replay_fusion360_m14.py`` execution.
    from fusion360_line3d_selector import select_signed_axis

ROOT = Path("data/datasets/fusion360_gallery/r1.0.1/extracted/r1.0.1")
ASSETS = ROOT / "reconstruction"
OUTPUT = Path("data/fusion360-gallery-m14-replay")
CASES = {
    "development": ("100243_9fb796fe_0005", "100877_ac1e5a17_0001"),
    "held_out": ("110043_b73b8beb_0000",),
}
SCALE = 10.0


def _reject(message: str) -> ValueError:
    return ValueError(f"m14_unsupported: {message}")


def _point(value: dict, transform: dict) -> gp_Pnt:
    origin = transform["origin"]
    axes = (transform["x_axis"], transform["y_axis"], transform["z_axis"])
    coords = (value.get("x", 0.0), value.get("y", 0.0), value.get("z", 0.0))
    return gp_Pnt(*[SCALE * (origin.get(key, 0.0) + sum(coords[i] * axes[i].get(key, 0.0) for i in range(3))) for key in ("x", "y", "z")])


def _direction(transform: dict) -> gp_Dir:
    axis = transform["z_axis"]
    return gp_Dir(axis["x"], axis["y"], axis["z"])


def _ordered_line_points(curves: list[dict], transform: dict) -> list[gp_Pnt]:
    segments = [(_point(curve["start_point"], transform), _point(curve["end_point"], transform)) for curve in curves]
    first, current = segments.pop(0)
    points = [first]
    while segments:
        matches = []
        for index, (start, end) in enumerate(segments):
            if current.Distance(start) <= 1e-6:
                matches.append((index, end))
            if current.Distance(end) <= 1e-6:
                matches.append((index, start))
        if len(matches) != 1:
            raise _reject("ambiguous_or_disconnected_line_loop")
        points.append(current)
        index, current = matches[0]
        segments.pop(index)
    if current.Distance(first) > 1e-6:
        raise _reject("non_closing_line_loop")
    return points


def _axis_vector(axis: dict) -> tuple[float, float, float]:
    return (float(axis["x"]), float(axis["y"]), float(axis["z"]))


def _dot(left: tuple[float, float, float], right: tuple[float, float, float]) -> float:
    return sum(component_left * component_right for component_left, component_right in zip(left, right, strict=True))


def _projection(points: list[tuple[float, float, float]], axis: tuple[float, float, float]) -> dict[str, float]:
    values = [_dot(point, axis) for point in points]
    return {"min": min(values), "max": max(values), "span": max(values) - min(values)}


def _bbox_corners(bbox: dict[str, list[float]]) -> list[tuple[float, float, float]]:
    return [
        (x, y, z)
        for x in (bbox["min"][0], bbox["max"][0])
        for y in (bbox["min"][1], bbox["max"][1])
        for z in (bbox["min"][2], bbox["max"][2])
    ]


def replay_line3d_selector(payload: dict, input_bbox: dict[str, list[float]]):
    """Candidate-only M17 path; callers must keep it within the fixed matrix."""
    entities = payload.get("entities", {})
    timeline = payload.get("timeline", [])
    ordered = [entities.get(item.get("entity")) for item in timeline]
    if len(ordered) != 2 or any(not entry for entry in ordered):
        raise _reject("timeline must resolve exactly two entities")
    sketch, extrude = ordered
    if sketch.get("type") != "Sketch" or extrude.get("type") != "ExtrudeFeature":
        raise _reject("timeline must be Sketch then ExtrudeFeature")
    if extrude.get("operation") != "NewBodyFeatureOperation" or extrude.get("extent_type") != "OneSideFeatureExtentType":
        raise _reject("only one-sided NewBody extrude is supported")
    if extrude.get("start_extent", {}).get("type") != "ProfilePlaneStartDefinition":
        raise _reject("only profile-plane starts are supported")
    extent = extrude.get("extent_one", {})
    if extent.get("type") != "DistanceExtentDefinition" or extent.get("taper_angle", {}).get("value") != 0.0:
        raise _reject("only zero-taper distance extents are supported")
    transform = sketch.get("transform")
    profiles = sketch.get("profiles", {})
    if not transform or len(profiles) != 1:
        raise _reject("exactly one transformed profile is required")
    loops = next(iter(profiles.values())).get("loops", [])
    if len(loops) != 1 or not loops[0].get("is_outer", False):
        raise _reject("exactly one outer loop is required")
    curves = loops[0].get("profile_curves", [])
    if not curves or {curve.get("type") for curve in curves} != {"Line3D"}:
        raise _reject("candidate selector requires a Line3D outer loop")

    points = _ordered_line_points(curves, transform)
    world_points = [(point.X(), point.Y(), point.Z()) for point in points]
    edge_one, edge_two = world_points[1], world_points[2]
    normal = (
        (edge_one[1] - world_points[0][1]) * (edge_two[2] - world_points[0][2]) - (edge_one[2] - world_points[0][2]) * (edge_two[1] - world_points[0][1]),
        (edge_one[2] - world_points[0][2]) * (edge_two[0] - world_points[0][0]) - (edge_one[0] - world_points[0][0]) * (edge_two[2] - world_points[0][2]),
        (edge_one[0] - world_points[0][0]) * (edge_two[1] - world_points[0][1]) - (edge_one[1] - world_points[0][1]) * (edge_two[0] - world_points[0][0]),
    )
    axes = {name: _axis_vector(transform[f"{name}_axis"]) for name in ("x", "y", "z")}
    profile_projections = {name: _projection(world_points, axis) for name, axis in axes.items()}
    step_projections = {name: _projection(_bbox_corners(input_bbox), axis) for name, axis in axes.items()}
    selected = select_signed_axis(
        ordered_profile_normal=normal,
        sketch_axes=axes,
        profile_projections=profile_projections,
        step_projections=step_projections,
        extent_magnitude_mm=SCALE * float(extent["distance"]["value"]),
    )
    axis_name, sign = selected[1:], 1.0 if selected.startswith("+") else -1.0
    axis = transform[axis_name]
    polygon = BRepBuilderAPI_MakePolygon()
    for point in points:
        polygon.Add(point)
    polygon.Close()
    face = BRepBuilderAPI_MakeFace(polygon.Wire()).Face()
    direction = gp_Dir(sign * axis["x"], sign * axis["y"], sign * axis["z"])
    distance = SCALE * extent["distance"]["value"]
    return BRepPrimAPI_MakePrism(face, gp_Vec(direction.XYZ()) * distance).Shape()


def replay(payload: dict, input_bbox: dict[str, list[float]] | None = None):
    """Replay the supported subset, using the fail-closed selector for Line3D."""
    entities = payload.get("entities", {})
    timeline = payload.get("timeline", [])
    ordered = [entities.get(item.get("entity")) for item in timeline]
    if len(ordered) == 2 and all(ordered):
        sketch = ordered[0]
        profiles = sketch.get("profiles", {})
        if len(profiles) == 1:
            loops = next(iter(profiles.values())).get("loops", [])
            if len(loops) == 1 and loops[0].get("is_outer", False):
                kinds = {curve.get("type") for curve in loops[0].get("profile_curves", [])}
                if kinds == {"Line3D"}:
                    if input_bbox is None:
                        raise _reject("Line3D selector requires input bbox")
                    return replay_line3d_selector(payload, input_bbox)
    return replay_strict(payload)


def replay_strict(payload: dict):
    """Historical listed-order / z-axis implementation retained for comparisons."""
    entities = payload.get("entities", {})
    timeline = payload.get("timeline", [])
    ordered = [entities.get(item.get("entity")) for item in timeline]
    if len(ordered) != 2 or any(not entry for entry in ordered):
        raise _reject("timeline must resolve exactly two entities")
    sketch, extrude = ordered
    if sketch.get("type") != "Sketch" or extrude.get("type") != "ExtrudeFeature":
        raise _reject("timeline must be Sketch then ExtrudeFeature")
    if extrude.get("operation") != "NewBodyFeatureOperation" or extrude.get("extent_type") != "OneSideFeatureExtentType":
        raise _reject("only one-sided NewBody extrude is supported")
    if extrude.get("start_extent", {}).get("type") != "ProfilePlaneStartDefinition":
        raise _reject("only profile-plane starts are supported")
    extent = extrude.get("extent_one", {})
    if extent.get("type") != "DistanceExtentDefinition" or extent.get("taper_angle", {}).get("value") != 0.0:
        raise _reject("only zero-taper distance extents are supported")
    transform = sketch.get("transform")
    profiles = sketch.get("profiles", {})
    if not transform or len(profiles) != 1:
        raise _reject("exactly one transformed profile is required")
    loops = next(iter(profiles.values())).get("loops", [])
    if len(loops) != 1 or not loops[0].get("is_outer", False):
        raise _reject("exactly one outer loop is required")
    curves = loops[0].get("profile_curves", [])
    kinds = {curve.get("type") for curve in curves}
    if kinds == {"Line3D"}:
        polygon = BRepBuilderAPI_MakePolygon()
        for curve in curves:
            polygon.Add(_point(curve["start_point"], transform))
        polygon.Close()
        face = BRepBuilderAPI_MakeFace(polygon.Wire()).Face()
    elif len(curves) == 1 and kinds == {"Circle3D"}:
        curve = curves[0]
        center = _point(curve["center_point"], transform)
        edge = BRepBuilderAPI_MakeEdge(gp_Circ(gp_Ax2(center, _direction(transform)), SCALE * curve["radius"])).Edge()
        face = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(edge).Wire()).Face()
    else:
        raise _reject("only Line3D polygons or a single Circle3D are supported")
    distance = SCALE * extent["distance"]["value"]
    return BRepPrimAPI_MakePrism(face, gp_Vec(_direction(transform).XYZ()) * distance).Shape()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_case(case_id: str, split: str) -> dict:
    input_path, json_path = ASSETS / f"{case_id}.step", ASSETS / f"{case_id}.json"
    output_path = OUTPUT / f"{case_id}.step"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    record = {"case_id": case_id, "split": split, "input_step": input_path.as_posix(), "input_sha256": sha256(input_path)}
    try:
        source = probe_summary(load_model(input_path))
        shape = replay(json.loads(json_path.read_text(encoding="utf-8")), source["bbox"])
        writer = STEPControl_Writer()
        writer.Transfer(shape, STEPControl_AsIs)
        if writer.Write(str(output_path)) != 1:
            raise RuntimeError("STEP writer failed")
        output = probe_summary(load_model(output_path))
        gates = _comparison_gates(source, output)
        record.update({"status": "completed", "output_step": output_path.as_posix(), "input_probe": source, "output_probe": output, "gates": gates, "passed": all(gate["status"] == "pass" for gate in gates)})
    except Exception as error:
        record.update({"status": "rejected", "error": str(error), "passed": False})
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=OUTPUT / "report.json")
    args = parser.parse_args()
    results = [run_case(case, split) for split, cases in CASES.items() for case in cases]
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps({"schema_version": 1, "unit_scale_cm_to_mm": SCALE, "cases": results}, indent=2) + "\n")
    print(args.report)
    return 0 if all(row["passed"] for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
