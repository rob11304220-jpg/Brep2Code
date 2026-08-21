import cadquery as cq


result = cq.Workplane("XY").box(10.0, 20.0, 30.0, centered=(False, False, False))
cq.exporters.export(result, "output.step")
