"""Offline measured-fact audit for the frozen M30 cylindrical-cut design."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from brep2code.brep import load_model
from brep2code.brep.probes import _bbox, _face_properties


SUPPORTED_AXIS = "+Z"
FOOTPRINT_FACTOR = 1.25


def audit(path: Path) -> dict[str, Any]:
    """Return only measured facts and a bounded blind/through disposition."""

    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE
    from OCP.TopExp import TopExp
    from OCP.TopTools import TopTools_IndexedDataMapOfShapeListOfShape
    from OCP.TopoDS import TopoDS

    model = load_model(path)
    faces = {
        entity_id: shape
        for entity_id, shape in model.entities.items()
        if model.entity_types[entity_id] == "face"
    }
    cylindrical = [
        (entity_id, shape)
        for entity_id, shape in faces.items()
        if _surface_type(shape) == "GeomAbs_Cylinder"
    ]
    result: dict[str, Any] = {
        "input": str(path),
        "scope": "M30 frozen +Z single-cylinder prismatic-hole design",
        "cylindrical_face_count": len(cylindrical),
        "classification": "unsupported",
        "reason": "requires_exactly_one_cylindrical_face",
        "cylindrical_faces": [],
    }
    if len(cylindrical) != 1:
        return result

    cylinder_id, cylinder_shape = cylindrical[0]
    surface = BRepAdaptor_Surface(TopoDS.Face_s(cylinder_shape))
    axis = surface.Cylinder().Axis().Direction()
    axis_vector = [_round(axis.X()), _round(axis.Y()), _round(axis.Z())]
    radius = _round(surface.Cylinder().Radius())
    ancestors = TopTools_IndexedDataMapOfShapeListOfShape()
    TopExp.MapShapesAndAncestors_s(model.shape, TopAbs_EDGE, TopAbs_FACE, ancestors)
    adjacent_ids = _adjacent_face_ids(cylinder_shape, cylinder_id, faces, ancestors)
    planar = [
        _planar_fact(face_id, faces[face_id], radius)
        for face_id in adjacent_ids
        if _surface_type(faces[face_id]) == "GeomAbs_Plane"
    ]
    cylinder_fact = {
        "entity_id": cylinder_id,
        "radius": radius,
        "axis": axis_vector,
        "adjacent_face_ids": adjacent_ids,
        "adjacent_planar_faces": planar,
    }
    result["cylindrical_faces"] = [cylinder_fact]
    if axis_vector not in ([0.0, 0.0, 1.0], [0.0, 0.0, -1.0]):
        result["reason"] = "axis_out_of_scope"
        return result
    if len(planar) != 2:
        result["reason"] = "requires_two_adjacent_planar_terminal_faces"
        return result

    interior = [fact for fact in planar if fact["local_footprint"]]
    exterior = [fact for fact in planar if not fact["local_footprint"]]
    if len(interior) == 1 and len(exterior) == 1:
        result.update(classification="blind", reason="one_local_floor_and_one_exterior_opening")
    elif len(interior) == 0 and len(exterior) == 2:
        result.update(classification="through", reason="two_exterior_openings")
    else:
        result["reason"] = "terminal_facts_do_not_discriminate_extent"
    return result


def _adjacent_face_ids(
    cylinder: Any,
    cylinder_id: str,
    faces: dict[str, Any],
    ancestors: Any,
) -> list[str]:
    from OCP.TopAbs import TopAbs_EDGE
    from OCP.TopExp import TopExp_Explorer

    adjacent: list[str] = []
    explorer = TopExp_Explorer(cylinder, TopAbs_EDGE)
    while explorer.More():
        for candidate in list(ancestors.FindFromKey(explorer.Current())):
            for face_id, face in faces.items():
                if face_id != cylinder_id and candidate.IsSame(face) and face_id not in adjacent:
                    adjacent.append(face_id)
        explorer.Next()
    return adjacent


def _planar_fact(face_id: str, face: Any, radius: float) -> dict[str, Any]:
    bbox = _bbox(face)
    span_x = _round(bbox["max"][0] - bbox["min"][0])
    span_y = _round(bbox["max"][1] - bbox["min"][1])
    diameter_bound = _round(2 * radius * FOOTPRINT_FACTOR)
    return {
        "entity_id": face_id,
        "bbox": bbox,
        "area": _round(_face_properties(face)["area"]),
        "xy_span": [span_x, span_y],
        "local_footprint": span_x <= diameter_bound and span_y <= diameter_bound,
        "local_footprint_bound": diameter_bound,
    }


def _surface_type(face: Any) -> str:
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.TopoDS import TopoDS

    return str(BRepAdaptor_Surface(TopoDS.Face_s(face)).GetType()).split(".")[-1]


def _round(value: float) -> float:
    return round(float(value), 6)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.input), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
