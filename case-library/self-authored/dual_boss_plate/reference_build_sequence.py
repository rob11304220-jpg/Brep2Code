from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer


shape = BRepPrimAPI_MakeBox(30.0, 20.0, 4.0).Shape()
for x_position in (8.0, 22.0):
    axis = gp_Ax2(gp_Pnt(x_position, 10.0, 4.0), gp_Dir(0.0, 0.0, 1.0))
    shape = BRepAlgoAPI_Fuse(shape, BRepPrimAPI_MakeCylinder(axis, 3.0, 6.0).Shape()).Shape()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
