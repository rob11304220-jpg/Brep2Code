from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt


length, width, height = (24.0, 18.0, 10.0)
radius, depth = (3.0, 6.0)
center = gp_Pnt(length / 2.0, width / 2.0, height - depth)
box = BRepPrimAPI_MakeBox(length, width, height).Shape()
tool = BRepPrimAPI_MakeCylinder(
    gp_Ax2(center, gp_Dir(0.0, 0.0, 1.0)), radius, depth
).Shape()
shape = BRepAlgoAPI_Cut(box, tool).Shape()
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
