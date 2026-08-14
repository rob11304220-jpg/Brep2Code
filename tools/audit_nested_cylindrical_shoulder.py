"""Offline M32 measured-fact audit for a nested-cylinder shoulder relation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from brep2code.brep import load_model
from brep2code.brep.probes import _bbox, _face_properties


AXIS_TOLERANCE = 1e-6


def audit(path: Path) -> dict[str, Any]:
    """Measure the frozen relation without consuming a feature label."""

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
        cylinders.append(
            {
                "entity_id": face_id,
                "radius": _round(surface.Cylinder().Radius()),
                "axis_location": [_round(location.X()), _round(location.Y()), _round(location.Z())],
                "axis_direction": [_round(direction.X()), _round(direction.Y()), _round(direction.Z())],
                "bbox": _bbox(shape),
                "adjacent_face_ids": _adjacent_face_ids(shape, face_id, faces, ancestors),
            }
        )
    result: dict[str, Any] = {
        "input": str(path),
        "scope": "M32 frozen +Z nested-cylinder shoulder design",
        "cylindrical_face_count": len(cylinders),
        "cylindrical_faces": cylinders,
        "classification": "unsupported",
        "reason": "requires_exactly_two_cylindrical_faces",
    }
    if len(cylinders) != 2:
        return result
    first, second = cylinders
    if not _coaxial(first, second):
        result["reason"] = "cylinders_not_coaxial"
        return result
    if first["radius"] == second["radius"]:
        result["reason"] = "requires_strict_radius_order"
        return result
    shared = sorted(set(first["adjacent_face_ids"]) & set(second["adjacent_face_ids"]))
    planar = [face_id for face_id in shared if _surface_type(faces[face_id]) == "GeomAbs_Plane"]
    result["shared_planar_faces"] = [_planar_fact(face_id, faces[face_id]) for face_id in planar]
    if len(planar) != 1:
        result["reason"] = "requires_one_shared_planar_shoulder"
        return result
    result.update(classification="nested_cylindrical_shoulder", reason="coaxial_ordered_cylinders_share_planar_shoulder")
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


def _coaxial(first: dict[str, Any], second: dict[str, Any]) -> bool:
    directions = (first["axis_direction"], second["axis_direction"])
    locations = (first["axis_location"], second["axis_location"])
    return all(direction in ([0.0, 0.0, 1.0], [0.0, 0.0, -1.0]) for direction in directions) and all(
        abs(locations[0][index] - locations[1][index]) <= AXIS_TOLERANCE for index in (0, 1)
    )


def _planar_fact(face_id: str, face: Any) -> dict[str, Any]:
    return {"entity_id": face_id, "bbox": _bbox(face), "area": _round(_face_properties(face)["area"])}


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
