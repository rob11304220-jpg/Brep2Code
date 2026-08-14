from pathlib import Path

from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer

FAMILY_ID = 'fillet'
PARAMETERS = {'radius': 1.5}

def first_edge(shape):
    explorer = TopExp_Explorer(shape, TopAbs_EDGE)
    if not explorer.More():
        raise RuntimeError("shape has no edge")
    return TopoDS.Edge_s(explorer.Current())

base = BRepPrimAPI_MakeBox(24.0, 18.0, 10.0).Shape()
operation = BRepFilletAPI_MakeFillet(base)
operation.Add(1.5, first_edge(base))
shape = operation.Shape()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
