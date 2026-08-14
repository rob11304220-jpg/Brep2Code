from __future__ import annotations

import math

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax1, gp_Ax2, gp_Dir, gp_Pnt, gp_Trsf

from tools.audit_axis_relative_nested_cylindrical_shoulder import audit
from tools.audit_nested_cylindrical_shoulder import audit as z_axis_audit
from tools.audit_sequence_paired_prismatic_hole import write_step


def test_axis_relative_reporter_matches_temporary_plus_y_relation(tmp_path) -> None:
    path = tmp_path / "plus-y.step"
    write_step(_rotate_to_y(_nested_z_shape()), path)
    result = audit(path)
    assert result["classification"] == "axis_relative_nested_cylindrical_shoulder"
    assert result["shared_planar_shoulders"][0]["transverse_xz_span"] == [10.0, 10.0]


def test_z_axis_global_reporter_does_not_promote_plus_y_relation(tmp_path) -> None:
    path = tmp_path / "plus-y.step"
    write_step(_rotate_to_y(_nested_z_shape()), path)
    assert z_axis_audit(path)["classification"] == "unsupported"


def test_non_y_axis_is_out_of_scope(tmp_path) -> None:
    path = tmp_path / "plus-x.step"
    write_step(_rotate(_nested_z_shape(), gp_Dir(0, 1, 0), math.pi / 2), path)
    assert audit(path)["reason"] == "axis_out_of_scope"


def test_noncoaxial_and_missing_shoulder_controls_fail_closed(tmp_path) -> None:
    noncoaxial = tmp_path / "noncoaxial.step"
    missing = tmp_path / "missing.step"
    write_step(_rotate_to_y(_noncoaxial_z_shape()), noncoaxial)
    write_step(_rotate_to_y(_missing_shoulder_z_shape()), missing)
    assert audit(noncoaxial)["reason"] == "cylinders_not_coaxial"
    assert audit(missing)["reason"] == "requires_one_shared_planar_shoulder"


def _cylinder(x: float, y: float, z: float, radius: float, height: float):
    return BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, y, z), gp_Dir(0, 0, 1)), radius, height).Shape()


def _nested_z_shape():
    base = BRepPrimAPI_MakeBox(30, 20, 10).Shape()
    inner = _cylinder(15, 10, -1, 3, 12)
    outer = _cylinder(15, 10, 7, 5, 4)
    return BRepAlgoAPI_Cut(BRepAlgoAPI_Cut(base, inner).Shape(), outer).Shape()


def _noncoaxial_z_shape():
    base = BRepPrimAPI_MakeBox(30, 20, 10).Shape()
    inner = _cylinder(15, 10, -1, 3, 12)
    outer = _cylinder(16, 10, 7, 5, 4)
    return BRepAlgoAPI_Cut(BRepAlgoAPI_Cut(base, inner).Shape(), outer).Shape()


def _missing_shoulder_z_shape():
    base = BRepPrimAPI_MakeBox(30, 20, 10).Shape()
    top = _cylinder(15, 10, 7, 5, 4)
    bottom = _cylinder(15, 10, -1, 3, 4)
    return BRepAlgoAPI_Cut(BRepAlgoAPI_Cut(base, top).Shape(), bottom).Shape()


def _rotate_to_y(shape):
    return _rotate(shape, gp_Dir(1, 0, 0), -math.pi / 2)


def _rotate(shape, direction: gp_Dir, angle: float):
    transform = gp_Trsf()
    transform.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), direction), angle)
    return BRepBuilderAPI_Transform(shape, transform, True).Shape()
