from pathlib import Path

from OCP.BRepFilletAPI import BRepFilletAPI_MakeChamfer
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS


def first_edge(shape):
    explorer = TopExp_Explorer(shape, TopAbs_EDGE)
    if not explorer.More():
        raise RuntimeError("shape has no edge to chamfer")
    return TopoDS.Edge_s(explorer.Current())


def first_face(shape):
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    if not explorer.More():
        raise RuntimeError("shape has no face for chamfer reference")
    return TopoDS.Face_s(explorer.Current())


box = BRepPrimAPI_MakeBox(16.0, 12.0, 8.0).Shape()
chamfer = BRepFilletAPI_MakeChamfer(box)
chamfer.Add(1.0, 1.0, first_edge(box), first_face(box))
shape = chamfer.Shape()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
status = writer.Write("output/model.step")
if status != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
