from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.gp import gp_Pnt


origin = gp_Pnt(0.0, 0.0, 0.0)
length, width, height = (10.0, 20.0, 30.0)
shape = BRepPrimAPI_MakeBox(origin, length, width, height).Shape()
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
