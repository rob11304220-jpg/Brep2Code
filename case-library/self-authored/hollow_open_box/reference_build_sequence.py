from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.gp import gp_Pnt
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer


outer = BRepPrimAPI_MakeBox(30.0, 20.0, 12.0).Shape()
inner = BRepPrimAPI_MakeBox(gp_Pnt(4.0, 4.0, 4.0), 22.0, 12.0, 10.0).Shape()
shape = BRepAlgoAPI_Cut(outer, inner).Shape()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
