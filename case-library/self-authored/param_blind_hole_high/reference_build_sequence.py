from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer

FAMILY_ID = 'blind_hole'
PARAMETERS = {'radius': 4.0, 'depth': 7.0}

base = BRepPrimAPI_MakeBox(30.0, 20.0, 10.0).Shape()
cutter = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(15, 10, 3.0), gp_Dir(0, 0, 1)), 4.0, 7.0).Shape()
shape = BRepAlgoAPI_Cut(base, cutter).Shape()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
