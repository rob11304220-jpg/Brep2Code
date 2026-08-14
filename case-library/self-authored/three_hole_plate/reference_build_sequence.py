from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer


shape = BRepPrimAPI_MakeBox(30.0, 10.0, 4.0).Shape()
for x_position in (7.5, 15.0, 22.5):
    axis = gp_Ax2(gp_Pnt(x_position, 5.0, -1.0), gp_Dir(0.0, 0.0, 1.0))
    tool = BRepPrimAPI_MakeCylinder(axis, 1.5, 6.0).Shape()
    shape = BRepAlgoAPI_Cut(shape, tool).Shape()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
status = writer.Write("output/model.step")
if status != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
