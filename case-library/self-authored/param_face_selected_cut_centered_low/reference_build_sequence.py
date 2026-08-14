# Deterministic reference only; sandbox self-contained.
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
p = {"bx":48.0,"by":36.0,"bh":8.0,"lx":16.0,"ly":12.0,"hh":8.0,"r":2.0,"d":3.0}
base = BRepPrimAPI_MakeBox(p["bx"], p["by"], p["bh"]).Shape()
boss = BRepPrimAPI_MakeBox(gp_Pnt(24-p["lx"]/2, 18-p["ly"]/2, p["bh"]), p["lx"], p["ly"], p["hh"]).Shape()
shape = BRepAlgoAPI_Fuse(base, boss).Shape()
cutter = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(24,18,p["bh"]+p["hh"]-p["d"]), gp_Dir(0,0,1)), p["r"], p["d"]).Shape()
writer = STEPControl_Writer()
writer.Transfer(BRepAlgoAPI_Cut(shape, cutter).Shape(), STEPControl_AsIs)
writer.Write("output/model.step")
