from pathlib import Path

import pytest

from brep2code.cases import validate_case
from brep2code.execution import run_build
from brep2code.geometry.compare import compare_geometry
from brep2code.geometry.inspect import inspect_step


pytestmark = pytest.mark.secure


BOX_BUILD = '''\
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer

shape = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
'''


def test_box_build_executes_and_passes_geometry_gates(tmp_path: Path) -> None:
    workspace = tmp_path / "revision-000"
    workspace.mkdir()
    (workspace / "build.py").write_text(BOX_BUILD, encoding="utf-8")

    execution = run_build(workspace)
    assert execution.exit_code == 0, execution.stderr
    assert execution.output_step is not None

    case = validate_case(Path("cases/smoke/box"), Path("cases"))
    signals = compare_geometry(inspect_step(execution.output_step), case.metadata["expected"])
    assert signals.passed
