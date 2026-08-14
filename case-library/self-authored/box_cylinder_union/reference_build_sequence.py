from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer


box = BRepPrimAPI_MakeBox(14.0, 10.0, 5.0).Shape()
cylinder_axis = gp_Ax2(gp_Pnt(7.0, 5.0, 5.0), gp_Dir(0.0, 0.0, 1.0))
cylinder = BRepPrimAPI_MakeCylinder(cylinder_axis, 3.0, 6.0).Shape()
shape = BRepAlgoAPI_Fuse(box, cylinder).Shape()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
status = writer.Write("output/model.step")
if status != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
