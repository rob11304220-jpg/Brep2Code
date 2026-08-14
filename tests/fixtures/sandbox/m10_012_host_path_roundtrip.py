"""M10-012 baseline: a host-only input path is unavailable in wsl-bwrap."""

import os

from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Reader, STEPControl_Writer


input_path = r"D:\m10-012-host-only\model.step"
reader = STEPControl_Reader()
if reader.ReadFile(input_path) != IFSelect_RetDone:
    raise RuntimeError(f"host-path STEP read failed: {input_path}")
reader.TransferRoot()

os.makedirs("output", exist_ok=True)
writer = STEPControl_Writer()
writer.Transfer(reader.OneShape(), STEPControl_AsIs)
if writer.Write("output/model.step") != IFSelect_RetDone:
    raise RuntimeError("STEP write failed")
