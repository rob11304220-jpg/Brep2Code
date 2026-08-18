from OCP.BRep import BRep_Tool
from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS


box = BRepPrimAPI_MakeBox(20.0, 16.0, 12.0).Shape()
explorer = TopExp_Explorer(box, TopAbs_EDGE)
while explorer.More():
    edge = TopoDS.Edge_s(explorer.Current())
    curve = BRep_Tool.Curve_s(edge, 0.0, 1.0)
    first = curve.Value(curve.FirstParameter())
    last = curve.Value(curve.LastParameter())
    if abs(first.Y()) < 1e-7 and abs(first.Z()) < 1e-7 and abs(last.Y()) < 1e-7 and abs(last.Z()) < 1e-7 and abs(last.X() - first.X()) > 10.0:
        fillet = BRepFilletAPI_MakeFillet(box)
        fillet.Add(2.0, edge)
        fillet.Build()
        shape = fillet.Shape()
        break
    explorer.Next()
else:
    raise RuntimeError("target fillet edge was not found")
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
