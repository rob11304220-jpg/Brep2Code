from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer


plate = BRepPrimAPI_MakeBox(30.0, 20.0, 6.0).Shape()
axis = gp_Ax2(gp_Pnt(15.0, 10.0, -1.0), gp_Dir(0.0, 0.0, 1.0))
shape = BRepAlgoAPI_Cut(plate, BRepPrimAPI_MakeCylinder(axis, 4.0, 8.0).Shape()).Shape()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
