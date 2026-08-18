from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt


box = BRepPrimAPI_MakeBox(18.0, 22.0, 13.0).Shape()
tool = BRepPrimAPI_MakeCylinder(
    gp_Ax2(gp_Pnt(9.0, 11.0, 8.0), gp_Dir(0.0, 0.0, 1.0)), 4.0, 5.0
).Shape()
shape = BRepAlgoAPI_Cut(box, tool).Shape()
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
