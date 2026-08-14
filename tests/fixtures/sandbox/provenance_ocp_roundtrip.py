from pathlib import Path

from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Reader, STEPControl_Writer

reader = STEPControl_Reader()
if reader.ReadFile("/input/model.step") != IFSelect_RetDone:
    raise RuntimeError("input STEP unreadable")
reader.TransferRoots()

Path("output").mkdir(exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(reader.Shape(), STEPControl_AsIs)
writer.Write("output/model.step")
