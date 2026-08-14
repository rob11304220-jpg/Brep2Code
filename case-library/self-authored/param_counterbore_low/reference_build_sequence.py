from pathlib import Path

from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

SEQUENCE = {'operations': [{'id': 'sketch_1', 'kind': 'SketchRect', 'plane': 'XY', 'length_x': 30.0, 'length_y': 20.0}, {'id': 'base_1', 'kind': 'ExtrudeBase', 'profile': 'sketch_1', 'direction': '+Z', 'distance': 10.0}, {'id': 'hole_1', 'kind': 'CutCylinder', 'target': 'base_1', 'variant': 'counterbore', 'center_xy': [9.0, 10.0], 'axis': '+Z', 'through_radius': 2.0, 'bore_radius': 3.5, 'bore_depth': 2.0}], 'mutations': [{'kind': 'base_length_x', 'delta': 2.0}, {'kind': 'bore_depth', 'delta': 0.5}]}

base = BRepPrimAPI_MakeBox(30.0, 20.0, 10.0).Shape()
x, y = [9.0, 10.0]
through = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, y, -1.0), gp_Dir(0.0, 0.0, 1.0)), 2.0, 12.0).Shape()
bore = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, y, 8.0), gp_Dir(0.0, 0.0, 1.0)), 3.5, 3.0).Shape()
shape = BRepAlgoAPI_Cut(BRepAlgoAPI_Cut(base, through).Shape(), bore).Shape()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(shape, STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("failed to write STEP")
