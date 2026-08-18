from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GeometryMetrics:
    bbox_min: tuple[float, float, float]
    bbox_max: tuple[float, float, float]
    volume: float
    counts: dict[str, int]


def inspect_step(path: Path) -> GeometryMetrics:
    if path.suffix.lower() not in {".step", ".stp"}:
        raise ValueError(f"only STEP input is supported: {path.name}")
    if not path.is_file():
        raise FileNotFoundError(path)

    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps
    from OCP.IFSelect import IFSelect_RetDone
    from OCP.STEPControl import STEPControl_Reader
    from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SHELL, TopAbs_SOLID
    reader = STEPControl_Reader()
    if reader.ReadFile(str(path.resolve())) != IFSelect_RetDone:
        raise ValueError(f"OpenCascade could not read STEP input: {path.name}")
    reader.TransferRoots()
    shape = reader.OneShape()

    box = Bnd_Box()
    BRepBndLib.Add_s(shape, box)
    xmin, ymin, zmin, xmax, ymax, zmax = box.Get()
    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape, props)
    targets = {
        "solid": TopAbs_SOLID,
        "shell": TopAbs_SHELL,
        "face": TopAbs_FACE,
        "edge": TopAbs_EDGE,
    }
    counts = {name: _count(shape, shape_type) for name, shape_type in targets.items()}
    return GeometryMetrics(
        bbox_min=_vector(xmin, ymin, zmin),
        bbox_max=_vector(xmax, ymax, zmax),
        volume=float(props.Mass()),
        counts=counts,
    )


def _count(shape, shape_type) -> int:
    from OCP.TopExp import TopExp_Explorer

    explorer = TopExp_Explorer(shape, shape_type)
    count = 0
    while explorer.More():
        count += 1
        explorer.Next()
    return count


def _vector(x: float, y: float, z: float) -> tuple[float, float, float]:
    return tuple(_rounded(value) for value in (x, y, z))


def _rounded(value: float) -> float:
    rounded = round(float(value), 6)
    return 0.0 if abs(rounded) < 1e-6 else rounded
