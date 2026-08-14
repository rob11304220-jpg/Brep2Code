from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.gp import gp_Pnt
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer


base = BRepPrimAPI_MakeBox(30.0, 20.0, 6.0).Shape()
step = BRepPrimAPI_MakeBox(gp_Pnt(7.5, 5.0, 6.0), 15.0, 10.0, 6.0).Shape()
shape = BRepAlgoAPI_Fuse(base, step).Shape()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
