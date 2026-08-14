"""Offline M33 +Y axis-relative nested-cylinder shoulder audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from brep2code.brep import load_model
from brep2code.brep.probes import _bbox, _face_properties


AXIS_TOLERANCE = 1e-6
SUPPORTED_AXIS = [0.0, 1.0, 0.0]


def audit(path: Path) -> dict[str, Any]:
    """Measure the preregistered +Y relation in an axis-relative frame."""

    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE
    from OCP.TopExp import TopExp
    from OCP.TopTools import TopTools_IndexedDataMapOfShapeListOfShape
    from OCP.TopoDS import TopoDS

    model = load_model(path)
    faces = {entity_id: shape for entity_id, shape in model.entities.items() if model.entity_types[entity_id] == "face"}
    ancestors = TopTools_IndexedDataMapOfShapeListOfShape()
    TopExp.MapShapesAndAncestors_s(model.shape, TopAbs_EDGE, TopAbs_FACE, ancestors)
    cylinders = []
    for face_id, shape in faces.items():
        if _surface_type(shape) != "GeomAbs_Cylinder":
            continue
        surface = BRepAdaptor_Surface(TopoDS.Face_s(shape))
        axis = surface.Cylinder().Axis()
        location, direction = axis.Location(), axis.Direction()
        bbox = _bbox(shape)
        cylinders.append(
            {
                "entity_id": face_id,
                "radius": _round(surface.Cylinder().Radius()),
                "axis_location": [_round(location.X()), _round(location.Y()), _round(location.Z())],
                "axis_direction": [_round(direction.X()), _round(direction.Y()), _round(direction.Z())],
                "axial_span": [bbox["min"][1], bbox["max"][1]],
                "adjacent_face_ids": _adjacent_face_ids(shape, face_id, faces, ancestors),
            }
        )
    result: dict[str, Any] = {
        "input": str(path),
        "scope": "M33 frozen +Y axis-relative nested-cylinder shoulder design",
        "cylindrical_face_count": len(cylinders),
        "cylindrical_faces": cylinders,
        "classification": "unsupported",
        "reason": "requires_exactly_two_cylindrical_faces",
    }
    if len(cylinders) != 2:
        return result
    first, second = cylinders
    if not all(face["axis_direction"] == SUPPORTED_AXIS for face in cylinders):
        result["reason"] = "axis_out_of_scope"
        return result
    if any(abs(first["axis_location"][index] - second["axis_location"][index]) > AXIS_TOLERANCE for index in (0, 2)):
        result["reason"] = "cylinders_not_coaxial"
        return result
    if first["radius"] == second["radius"]:
        result["reason"] = "requires_strict_radius_order"
        return result
    shared = sorted(set(first["adjacent_face_ids"]) & set(second["adjacent_face_ids"]))
    shoulders = [_shoulder_fact(face_id, faces[face_id]) for face_id in shared if _surface_type(faces[face_id]) == "GeomAbs_Plane"]
    result["shared_planar_shoulders"] = shoulders
    if len(shoulders) != 1:
        result["reason"] = "requires_one_shared_planar_shoulder"
        return result
    result.update(classification="axis_relative_nested_cylindrical_shoulder", reason="plus_y_coaxial_ordered_cylinders_share_planar_shoulder")
    return result


def _adjacent_face_ids(cylinder: Any, cylinder_id: str, faces: dict[str, Any], ancestors: Any) -> list[str]:
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


def _shoulder_fact(face_id: str, face: Any) -> dict[str, Any]:
    bbox = _bbox(face)
    return {
        "entity_id": face_id,
        "axis_coordinate_y": bbox["min"][1],
        "transverse_xz_span": [
            _round(bbox["max"][0] - bbox["min"][0]),
            _round(bbox["max"][2] - bbox["min"][2]),
        ],
        "area": _round(_face_properties(face)["area"]),
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
