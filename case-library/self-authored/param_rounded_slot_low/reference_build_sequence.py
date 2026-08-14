from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer

FAMILY_ID = 'rounded_slot'
PARAMETERS = {'width': 3.0, 'straight_length': 8.0}

plate = BRepPrimAPI_MakeBox(30.0, 20.0, 5.0).Shape()
cutter = BRepPrimAPI_MakeBox(gp_Pnt(11.0, 8.5, -1), 8.0, 3.0, 7).Shape()
for x in (11.0, 19.0):
    cutter = BRepAlgoAPI_Fuse(cutter, BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, 10, -1), gp_Dir(0, 0, 1)), 1.5, 7).Shape()).Shape()
shape = BRepAlgoAPI_Cut(plate, cutter).Shape()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
