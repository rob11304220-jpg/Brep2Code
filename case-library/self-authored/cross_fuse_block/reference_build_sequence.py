from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.gp import gp_Pnt
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer


long_x = BRepPrimAPI_MakeBox(30.0, 12.0, 6.0).Shape()
long_y = BRepPrimAPI_MakeBox(gp_Pnt(9.0, -9.0, 0.0), 12.0, 30.0, 6.0).Shape()
shape = BRepAlgoAPI_Fuse(long_x, long_y).Shape()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
