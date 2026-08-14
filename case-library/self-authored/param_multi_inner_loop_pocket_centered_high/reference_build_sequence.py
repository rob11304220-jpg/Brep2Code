# Deterministic reference only; sandbox self-contained.
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.gp import gp_Pnt
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
p = {"ox":32.0,"oy":22.0,"ix":7.0,"iy":6.0,"d":5.0,"left":16.0,"right":32.0}
shape = BRepAlgoAPI_Cut(BRepPrimAPI_MakeBox(48,36,12).Shape(), BRepPrimAPI_MakeBox(gp_Pnt(24-p["ox"]/2,18-p["oy"]/2,12-p["d"]),p["ox"],p["oy"],p["d"]+1).Shape()).Shape()
for x in (p["left"], p["right"]):
    island = BRepPrimAPI_MakeBox(gp_Pnt(x - p["ix"] / 2, 18 - p["iy"] / 2, 12 - p["d"]), p["ix"], p["iy"], p["d"]).Shape()
    shape = BRepAlgoAPI_Fuse(shape, island).Shape()
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
writer.Write("output/model.step")
