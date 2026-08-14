from __future__ import annotations

from pathlib import Path

import pytest
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

from tools.audit_nested_cylindrical_shoulder import audit
from tools.audit_sequence_paired_prismatic_hole import write_step


CASES = Path("case-library/self-authored")


@pytest.mark.parametrize("case_id", ["param_counterbore_low", "param_counterbore_nominal", "param_counterbore_high"])
def test_frozen_counterbore_rows_match_nested_relation_from_measured_facts(case_id: str) -> None:
    result = audit(CASES / case_id / "input.step")
    assert result["classification"] == "nested_cylindrical_shoulder"
    assert result["reason"] == "coaxial_ordered_cylinders_share_planar_shoulder"
    assert len(result["shared_planar_faces"]) == 1


def test_noncoaxial_control_is_unsupported(tmp_path) -> None:
    path = tmp_path / "noncoaxial.step"
    write_step(_noncoaxial_shape(), path)
    assert audit(path)["reason"] == "cylinders_not_coaxial"


def test_missing_shoulder_control_is_unsupported(tmp_path) -> None:
    path = tmp_path / "missing-shoulder.step"
    write_step(_missing_shoulder_shape(), path)
    assert audit(path)["reason"] == "requires_one_shared_planar_shoulder"


def _cylinder(x: float, y: float, z: float, radius: float, height: float):
    return BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, y, z), gp_Dir(0, 0, 1)), radius, height).Shape()


def _noncoaxial_shape():
    base = BRepPrimAPI_MakeBox(30, 20, 10).Shape()
    through = _cylinder(15, 10, -1, 3, 12)
    offset_bore = _cylinder(16, 10, 7, 5, 4)
    return BRepAlgoAPI_Cut(BRepAlgoAPI_Cut(base, through).Shape(), offset_bore).Shape()


def _missing_shoulder_shape():
    base = BRepPrimAPI_MakeBox(30, 20, 10).Shape()
    top_bore = _cylinder(15, 10, 7, 5, 4)
    bottom_bore = _cylinder(15, 10, -1, 3, 4)
    return BRepAlgoAPI_Cut(BRepAlgoAPI_Cut(base, top_bore).Shape(), bottom_bore).Shape()
