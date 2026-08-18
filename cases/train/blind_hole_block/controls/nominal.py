from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt


box = BRepPrimAPI_MakeBox(24.0, 18.0, 10.0).Shape()
tool = BRepPrimAPI_MakeCylinder(
    gp_Ax2(gp_Pnt(12.0, 9.0, 4.0), gp_Dir(0.0, 0.0, 1.0)), 3.0, 6.0
).Shape()
shape = BRepAlgoAPI_Cut(box, tool).Shape()
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
