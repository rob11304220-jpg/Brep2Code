from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt


block_x, block_y, block_z = (20.0, 20.0, 8.0)
center_x, center_y = (block_x / 2.0, block_y / 2.0)
hole_radius, tool_margin = (4.0, 1.0)
box = BRepPrimAPI_MakeBox(block_x, block_y, block_z).Shape()
tool = BRepPrimAPI_MakeCylinder(
    gp_Ax2(gp_Pnt(center_x, center_y, -tool_margin), gp_Dir(0.0, 0.0, 1.0)),
    hole_radius,
    block_z + 2.0 * tool_margin,
).Shape()
shape = BRepAlgoAPI_Cut(box, tool).Shape()
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
