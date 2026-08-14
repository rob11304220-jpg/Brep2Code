# Deterministic local oracle only. Not provider, runtime, or training input.
from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

SEQUENCE = {'operations': [{'id': 'sketch_base', 'kind': 'SketchRect', 'plane': 'XY', 'length_x': 30.0, 'length_y': 20.0}, {'id': 'base', 'kind': 'ExtrudeBase', 'profile': 'sketch_base', 'direction': '+Z', 'distance': 10.0}, {'id': 'hole_tool', 'kind': 'MakeCylinder', 'axis': '+Z', 'center_xy': [21.0, 10.0], 'start_z': -1.0, 'radius': 4.0, 'height': 12.0}, {'id': 'through_cut', 'kind': 'CutThroughAll', 'target': 'base', 'tool': 'hole_tool', 'direction': '+Z'}]}
base = BRepPrimAPI_MakeBox(30.0, 20.0, 10.0).Shape()
radius, x = 4.0, 21.0
cutter = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, 10.0, -1.0), gp_Dir(0.0, 0.0, 1.0)), radius, 12.0).Shape()
shape = BRepAlgoAPI_Cut(base, cutter).Shape()
Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
