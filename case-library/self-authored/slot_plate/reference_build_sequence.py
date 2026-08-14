from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer


plate = BRepPrimAPI_MakeBox(30.0, 20.0, 5.0).Shape()
slot = BRepPrimAPI_MakeBox(gp_Pnt(9.0, 8.0, -1.0), 12.0, 4.0, 7.0).Shape()
for x_position in (9.0, 21.0):
    axis = gp_Ax2(gp_Pnt(x_position, 10.0, -1.0), gp_Dir(0.0, 0.0, 1.0))
    slot = BRepAlgoAPI_Fuse(slot, BRepPrimAPI_MakeCylinder(axis, 2.0, 7.0).Shape()).Shape()
shape = BRepAlgoAPI_Cut(plate, slot).Shape()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
