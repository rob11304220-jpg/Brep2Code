from __future__ import annotations

from collections import Counter
from math import sqrt
from pathlib import Path
from typing import Any

from brep2code.geometry.inspect import inspect_step


MAX_OBSERVED_FACES = 128
MAX_OBSERVED_EDGES = 256


def observe_step(path: Path) -> dict[str, Any]:
    """Return bounded, path-free geometric observations for a STEP model."""
    metrics = inspect_step(path)
    shape = _read_shape(path)
    faces = _observe_faces(shape)
    surface_counts = Counter(face["surface"] for face in faces)
    return {
        "bbox": {"min": list(metrics.bbox_min), "max": list(metrics.bbox_max)},
        "volume": metrics.volume,
        "topology": metrics.counts,
        "surface_counts": dict(sorted(surface_counts.items())),
        "faces": faces,
        "faces_truncated": metrics.counts["face"] > len(faces),
    }


def observe_edges(path: Path) -> dict[str, Any]:
    """Return bounded, session-local edge candidates without exposing the STEP path."""
    shape = _read_shape(path)
    faces = _collect_subshapes(shape, "face", MAX_OBSERVED_FACES)
    edges = _collect_subshapes(shape, "edge", MAX_OBSERVED_EDGES)
    observations = [
        _observe_edge(edge, index, faces, shape) for index, edge in enumerate(edges)
    ]
    incidence = [
        {
            "face_id": f"face-{face_index:03d}",
            "edge_ids": [
                item["edge_id"]
                for item in observations
                if f"face-{face_index:03d}" in item["adjacent_faces"]
            ],
        }
        for face_index in range(len(faces))
    ]
    return {
        "edges": observations,
        "face_edge_incidence": incidence,
        "parallel_edge_groups": _parallel_groups(observations),
        "collinear_edge_groups": _collinear_groups(observations),
        "edges_truncated": _count_subshapes(shape, "edge") > len(edges),
        "faces_truncated": _count_subshapes(shape, "face") > len(faces),
    }


def _read_shape(path: Path):
    from OCP.IFSelect import IFSelect_RetDone
    from OCP.STEPControl import STEPControl_Reader

    reader = STEPControl_Reader()
    if reader.ReadFile(str(path.resolve())) != IFSelect_RetDone:
        raise ValueError(f"OpenCascade could not read STEP input: {path.name}")
    reader.TransferRoots()
    return reader.OneShape()


def _observe_faces(shape) -> list[dict[str, Any]]:
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane
    from OCP.TopAbs import TopAbs_FACE
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopoDS import TopoDS

    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    observations = []
    while explorer.More() and len(observations) < MAX_OBSERVED_FACES:
        face = TopoDS.Face_s(explorer.Current())
        adaptor = BRepAdaptor_Surface(face)
        surface_type = adaptor.GetType()
        item: dict[str, Any] = {
            "surface": _surface_name(surface_type),
            "bbox": _face_bbox(face),
        }
        if surface_type == GeomAbs_Plane:
            axis = adaptor.Plane().Axis()
            item["origin"] = _point(axis.Location())
            item["normal"] = _direction(axis.Direction())
        elif surface_type == GeomAbs_Cylinder:
            cylinder = adaptor.Cylinder()
            axis = cylinder.Axis()
            item["axis_origin"] = _point(axis.Location())
            item["axis_direction"] = _direction(axis.Direction())
            item["radius"] = _rounded(cylinder.Radius())
        observations.append(item)
        explorer.Next()
    return observations


def _collect_subshapes(shape, kind: str, limit: int) -> list[Any]:
    from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE
    from OCP.TopExp import TopExp
    from OCP.TopoDS import TopoDS
    from OCP.TopTools import TopTools_IndexedMapOfShape

    shape_type, caster = {
        "edge": (TopAbs_EDGE, TopoDS.Edge_s),
        "face": (TopAbs_FACE, TopoDS.Face_s),
    }[kind]
    mapped = TopTools_IndexedMapOfShape()
    TopExp.MapShapes_s(shape, shape_type, mapped)
    return [caster(mapped.FindKey(index)) for index in range(1, min(mapped.Size(), limit) + 1)]


def _count_subshapes(shape, kind: str) -> int:
    from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE
    from OCP.TopExp import TopExp
    from OCP.TopTools import TopTools_IndexedMapOfShape

    shape_type = {"edge": TopAbs_EDGE, "face": TopAbs_FACE}[kind]
    mapped = TopTools_IndexedMapOfShape()
    TopExp.MapShapes_s(shape, shape_type, mapped)
    return mapped.Size()


def _observe_edge(edge, index: int, faces: list[Any], shape) -> dict[str, Any]:
    from OCP.BRep import BRep_Tool
    from OCP.BRepAdaptor import BRepAdaptor_Curve
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps
    from OCP.TopAbs import TopAbs_EDGE
    from OCP.TopExp import TopExp, TopExp_Explorer

    adaptor = BRepAdaptor_Curve(edge)
    properties = GProp_GProps()
    BRepGProp.LinearProperties_s(edge, properties)
    first = TopExp.FirstVertex_s(edge)
    last = TopExp.LastVertex_s(edge)
    adjacent_faces = []
    for face_index, face in enumerate(faces):
        explorer = TopExp_Explorer(face, TopAbs_EDGE)
        while explorer.More():
            if explorer.Current().IsSame(edge):
                adjacent_faces.append(f"face-{face_index:03d}")
                break
            explorer.Next()
    start = _point(BRep_Tool.Pnt_s(first))
    end = _point(BRep_Tool.Pnt_s(last))
    parameters = _curve_parameters(adaptor)
    tangent = _curve_tangent(adaptor)
    edge_id = f"edge-{index:03d}"
    observation = {
        "edge_id": edge_id,
        "identity": {
            "scope": "session",
            "geometry_key": _edge_geometry_key(
                _curve_name(adaptor.GetType()), start, end, parameters
            ),
        },
        "curve": _curve_name(adaptor.GetType()),
        "length": _rounded(properties.Mass()),
        "parameter_range": [
            _rounded(adaptor.FirstParameter()),
            _rounded(adaptor.LastParameter()),
        ],
        "curve_parameters": parameters,
        "start": start,
        "end": end,
        "local_orientation": tangent,
        "adjacent_faces": adjacent_faces,
    }
    observation["dihedral"] = _classify_dihedral(edge, faces, adjacent_faces, shape)
    return observation


def _curve_parameters(adaptor) -> dict[str, Any]:
    curve = _curve_name(adaptor.GetType())
    if curve == "line":
        line = adaptor.Line()
        return {
            "origin": _point(line.Location()),
            "direction": _direction(line.Direction()),
        }
    if curve == "circle":
        circle = adaptor.Circle()
        return {
            "center": _point(circle.Location()),
            "axis_direction": _direction(circle.Axis().Direction()),
            "radius": _rounded(circle.Radius()),
        }
    if curve == "ellipse":
        ellipse = adaptor.Ellipse()
        return {
            "center": _point(ellipse.Location()),
            "axis_direction": _direction(ellipse.Axis().Direction()),
            "major_radius": _rounded(ellipse.MajorRadius()),
            "minor_radius": _rounded(ellipse.MinorRadius()),
        }
    return {}


def _curve_tangent(adaptor) -> list[float] | None:
    from OCP.gp import gp_Pnt, gp_Vec

    parameter = (adaptor.FirstParameter() + adaptor.LastParameter()) / 2.0
    point = gp_Pnt()
    tangent = gp_Vec()
    try:
        adaptor.D1(parameter, point, tangent)
    except RuntimeError:
        return None
    magnitude = tangent.Magnitude()
    if magnitude <= 1e-12:
        return None
    tangent.Multiply(1.0 / magnitude)
    return _direction(tangent)


def _edge_geometry_key(
    curve: str,
    start: list[float],
    end: list[float],
    parameters: dict[str, Any],
) -> str:
    endpoints = sorted((tuple(start), tuple(end)))
    parameter_parts = [f"{name}={parameters[name]}" for name in sorted(parameters)]
    return "|".join([curve, repr(endpoints[0]), repr(endpoints[1]), *parameter_parts])


def _parallel_groups(edges: list[dict[str, Any]]) -> list[list[str]]:
    candidates = [
        edge
        for edge in edges
        if edge["curve"] == "line" and edge["local_orientation"] is not None
    ]
    return _direction_groups(candidates, require_collinear=False)


def _collinear_groups(edges: list[dict[str, Any]]) -> list[list[str]]:
    candidates = [
        edge
        for edge in edges
        if edge["curve"] == "line" and edge["local_orientation"] is not None
    ]
    return _direction_groups(candidates, require_collinear=True)


def _direction_groups(
    edges: list[dict[str, Any]], *, require_collinear: bool
) -> list[list[str]]:
    remaining = list(edges)
    groups = []
    while remaining:
        seed = remaining.pop(0)
        group = [seed]
        unmatched = []
        for candidate in remaining:
            if _directions_parallel(
                seed["local_orientation"], candidate["local_orientation"]
            ) and (
                not require_collinear
                or _lines_collinear(
                    seed["start"], seed["local_orientation"], candidate["start"]
                )
            ):
                group.append(candidate)
            else:
                unmatched.append(candidate)
        remaining = unmatched
        if len(group) > 1:
            groups.append([edge["edge_id"] for edge in group])
    return groups


def _directions_parallel(first: list[float], second: list[float]) -> bool:
    return abs(sum(a * b for a, b in zip(first, second, strict=True))) >= 1.0 - 1e-6


def _lines_collinear(
    origin: list[float], direction: list[float], point: list[float]
) -> bool:
    offset = [point[index] - origin[index] for index in range(3)]
    cross = [
        offset[1] * direction[2] - offset[2] * direction[1],
        offset[2] * direction[0] - offset[0] * direction[2],
        offset[0] * direction[1] - offset[1] * direction[0],
    ]
    scale = max(1.0, sqrt(sum(value * value for value in offset)))
    return sqrt(sum(value * value for value in cross)) <= 1e-6 * scale


def _classify_dihedral(
    edge, faces: list[Any], adjacent_faces: list[str], shape
) -> str:
    if len(adjacent_faces) != 2:
        return "boundary"
    first_index = int(adjacent_faces[0].split("-")[1])
    second_index = int(adjacent_faces[1].split("-")[1])
    midpoint = _edge_midpoint(edge)
    first_normal = _outward_normal(faces[first_index], midpoint)
    second_normal = _outward_normal(faces[second_index], midpoint)
    if first_normal is None or second_normal is None:
        return "unknown"
    if _directions_parallel(first_normal, second_normal):
        return "smooth"
    epsilon = max(1e-5, _edge_length(edge) * 1e-4)
    inside = sum(
        _point_inside(
            shape,
            [
                midpoint[index]
                + epsilon * (first_sign * first_normal[index] + second_sign * second_normal[index])
                for index in range(3)
            ],
        )
        for first_sign in (-1.0, 1.0)
        for second_sign in (-1.0, 1.0)
    )
    return {1: "convex", 3: "concave"}.get(inside, "unknown")


def _outward_normal(face, point: list[float]) -> list[float] | None:
    from OCP.BRep import BRep_Tool
    from OCP.GeomLProp import GeomLProp_SLProps
    from OCP.ShapeAnalysis import ShapeAnalysis_Surface
    from OCP.TopAbs import TopAbs_REVERSED
    from OCP.gp import gp_Pnt

    surface = BRep_Tool.Surface_s(face)
    try:
        parameters = ShapeAnalysis_Surface(surface).ValueOfUV(gp_Pnt(*point), 1e-7)
        properties = GeomLProp_SLProps(
            surface, parameters.X(), parameters.Y(), 1, 1e-7
        )
    except RuntimeError:
        return None
    if not properties.IsNormalDefined():
        return None
    normal = _direction(properties.Normal())
    if face.Orientation() == TopAbs_REVERSED:
        normal = [-value for value in normal]
    return normal


def _edge_midpoint(edge) -> list[float]:
    from OCP.BRepAdaptor import BRepAdaptor_Curve

    adaptor = BRepAdaptor_Curve(edge)
    parameter = (adaptor.FirstParameter() + adaptor.LastParameter()) / 2.0
    return _point(adaptor.Value(parameter))


def _edge_length(edge) -> float:
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps

    properties = GProp_GProps()
    BRepGProp.LinearProperties_s(edge, properties)
    return float(properties.Mass())


def _point_inside(shape, coordinates: list[float]) -> bool:
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.TopAbs import TopAbs_IN
    from OCP.gp import gp_Pnt

    classifier = BRepClass3d_SolidClassifier(shape)
    classifier.Perform(gp_Pnt(*coordinates), 1e-7)
    return classifier.State() == TopAbs_IN


def _curve_name(curve_type) -> str:
    name = str(curve_type).rsplit(".", 1)[-1]
    return name.removeprefix("GeomAbs_").lower()


def _surface_name(surface_type) -> str:
    name = str(surface_type).rsplit(".", 1)[-1]
    return name.removeprefix("GeomAbs_").lower()


def _face_bbox(face) -> dict[str, list[float]]:
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib

    box = Bnd_Box()
    BRepBndLib.Add_s(face, box)
    xmin, ymin, zmin, xmax, ymax, zmax = box.Get()
    return {
        "min": [_rounded(value) for value in (xmin, ymin, zmin)],
        "max": [_rounded(value) for value in (xmax, ymax, zmax)],
    }


def _point(point) -> list[float]:
    return [_rounded(point.X()), _rounded(point.Y()), _rounded(point.Z())]


def _direction(direction) -> list[float]:
    return [_rounded(direction.X()), _rounded(direction.Y()), _rounded(direction.Z())]


def _rounded(value: float) -> float:
    rounded = round(float(value), 6)
    return 0.0 if abs(rounded) < 1e-6 else rounded
