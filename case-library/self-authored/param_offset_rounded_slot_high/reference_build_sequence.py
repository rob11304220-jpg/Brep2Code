from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

plate = BRepPrimAPI_MakeBox(30.0, 20.0, 5.0).Shape()
cutter = BRepPrimAPI_MakeBox(gp_Pnt(14.0, 9.5, -1.0), 12.0, 5.0, 7.0).Shape()
for x in (14.0, 26.0):
    cutter = BRepAlgoAPI_Fuse(cutter, BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, 12.0, -1.0), gp_Dir(0, 0, 1)), 2.5, 7.0).Shape()).Shape()
shape = BRepAlgoAPI_Cut(plate, cutter).Shape()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
