from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer


block = BRepPrimAPI_MakeBox(20.0, 20.0, 8.0).Shape()
hole_axis = gp_Ax2(gp_Pnt(10.0, 10.0, -1.0), gp_Dir(0.0, 0.0, 1.0))
tool = BRepPrimAPI_MakeCylinder(hole_axis, 4.0, 10.0).Shape()
shape = BRepAlgoAPI_Cut(block, tool).Shape()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
status = writer.Write("output/model.step")
if status != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
