"""OpenCascade-backed B-Rep probe tools."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from brep2code.brep.readin import input_format
from brep2code.brep.serialize import DEFAULT_RESULT_LIMIT_BYTES, bounded_result_with_trace


class ProbeError(Exception):
    """Structured probe failure."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message

    def to_result(self) -> dict[str, Any]:
        return {"ok": False, "error": {"code": self.code, "message": self.message}}


@dataclass(frozen=True)
class ProbeModel:
    input_path: Path
    shape: Any
    entities: dict[str, Any]
    entity_types: dict[str, str]


def load_model(input_path: Path) -> ProbeModel:
    """Load a supported CAD input and build stable entity ids."""

    path = input_path.resolve()
    if not path.is_file():
        raise ProbeError("input_not_found", f"CAD input does not exist: {input_path}")
    fmt = input_format(path)
    if fmt != "step":
        raise ProbeError("unsupported_format", f"M1 currently supports STEP input only: {path.name}")

    try:
        from OCP.IFSelect import IFSelect_RetDone
        from OCP.STEPControl import STEPControl_Reader
    except ImportError as exc:
        raise ProbeError("backend_unavailable", "OCP backend is not importable.") from exc

    reader = STEPControl_Reader()
    status = reader.ReadFile(str(path))
    if status != IFSelect_RetDone:
        raise ProbeError("read_failed", f"OpenCascade failed to read STEP input: {path.name}")
    reader.TransferRoots()
    shape = reader.OneShape()
    entities, entity_types = _index_entities(shape)
    return ProbeModel(path, shape, entities, entity_types)


def probe_summary(
    model: ProbeModel,
    *,
    trace_dir: Path | None = None,
    limit_bytes: int = DEFAULT_RESULT_LIMIT_BYTES,
) -> dict[str, Any]:
    try:
        from OCP.BRepGProp import BRepGProp
        from OCP.GProp import GProp_GProps
    except ImportError as exc:
        raise ProbeError("backend_unavailable", "OCP backend is not importable.") from exc

    surface_props = GProp_GProps()
    volume_props = GProp_GProps()
    BRepGProp.SurfaceProperties_s(model.shape, surface_props)
    BRepGProp.VolumeProperties_s(model.shape, volume_props)
    payload = {
        "ok": True,
        "input": str(model.input_path),
        "file_name": model.input_path.name,
        "format": input_format(model.input_path),
        "unit": "unknown",
        "bbox": _bbox(model.shape),
        "counts": _counts(model),
        "area": surface_props.Mass(),
        "volume": volume_props.Mass(),
    }
    return bounded_result_with_trace(payload, trace_dir, "probe_summary.json", limit_bytes)


def probe_topology(
    model: ProbeModel,
    selector: str = "all",
    *,
    max_entities: int = 80,
    trace_dir: Path | None = None,
    limit_bytes: int = DEFAULT_RESULT_LIMIT_BYTES,
) -> dict[str, Any]:
    selected = [
        {"entity_id": entity_id, "entity_type": entity_type}
        for entity_id, entity_type in model.entity_types.items()
        if selector == "all" or entity_type == selector
    ]
    payload = {
        "ok": True,
        "input": str(model.input_path),
        "selector": selector,
        "counts": _counts(model),
        "entities": selected[:max_entities],
        "truncated": len(selected) > max_entities,
        "returned": min(len(selected), max_entities),
        "total_selected": len(selected),
    }
    return bounded_result_with_trace(payload, trace_dir, "probe_topology.json", limit_bytes)


def probe_entity(
    model: ProbeModel,
    entity_id: str,
    *,
    trace_dir: Path | None = None,
    limit_bytes: int = DEFAULT_RESULT_LIMIT_BYTES,
) -> dict[str, Any]:
    shape = _get_entity(model, entity_id)
    entity_type = model.entity_types[entity_id]
    payload: dict[str, Any] = {
        "ok": True,
        "input": str(model.input_path),
        "entity_id": entity_id,
        "entity_type": entity_type,
        "bbox": _bbox(shape),
    }
    if entity_type == "face":
        payload.update(_face_properties(shape))
    elif entity_type == "edge":
        payload.update(_edge_properties(shape))
    return bounded_result_with_trace(payload, trace_dir, f"probe_entity_{entity_id}.json", limit_bytes)


def sample_entity(
    model: ProbeModel,
    entity_id: str,
    n: int,
    *,
    max_samples: int = 32,
    trace_dir: Path | None = None,
    limit_bytes: int = DEFAULT_RESULT_LIMIT_BYTES,
) -> dict[str, Any]:
    if n < 1:
        raise ProbeError("invalid_sample_count", "sample count must be >= 1")
    sample_count = min(n, max_samples)
    shape = _get_entity(model, entity_id)
    entity_type = model.entity_types[entity_id]
    if entity_type == "face":
        samples = _sample_face(shape, sample_count)
    elif entity_type == "edge":
        samples = _sample_edge(shape, sample_count)
    else:
        raise ProbeError("unsupported_entity", f"sampling is supported for face and edge, not {entity_type}")
    payload = {
        "ok": True,
        "input": str(model.input_path),
        "entity_id": entity_id,
        "entity_type": entity_type,
        "requested": n,
        "returned": sample_count,
        "truncated": n > max_samples,
        "samples": samples,
    }
    return bounded_result_with_trace(payload, trace_dir, f"sample_entity_{entity_id}.json", limit_bytes)


def _index_entities(shape: Any) -> tuple[dict[str, Any], dict[str, str]]:
    from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SHELL, TopAbs_SOLID
    from OCP.TopExp import TopExp_Explorer

    targets = (
        ("solid", TopAbs_SOLID),
        ("shell", TopAbs_SHELL),
        ("face", TopAbs_FACE),
        ("edge", TopAbs_EDGE),
    )
    entities: dict[str, Any] = {}
    entity_types: dict[str, str] = {}
    for entity_type, top_abs in targets:
        explorer = TopExp_Explorer(shape, top_abs)
        index = 1
        while explorer.More():
            entity_id = f"{entity_type}:{index:06d}"
            entities[entity_id] = explorer.Current()
            entity_types[entity_id] = entity_type
            explorer.Next()
            index += 1
    return entities, entity_types


def _counts(model: ProbeModel) -> dict[str, int]:
    counts = {"solid": 0, "shell": 0, "face": 0, "edge": 0}
    for entity_type in model.entity_types.values():
        counts[entity_type] += 1
    return counts


def _get_entity(model: ProbeModel, entity_id: str) -> Any:
    try:
        return model.entities[entity_id]
    except KeyError as exc:
        raise ProbeError("entity_not_found", f"unknown entity id: {entity_id}") from exc


def _bbox(shape: Any) -> dict[str, list[float]]:
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib

    box = Bnd_Box()
    BRepBndLib.Add_s(shape, box)
    xmin, ymin, zmin, xmax, ymax, zmax = box.Get()
    return {
        "min": [_round(xmin), _round(ymin), _round(zmin)],
        "max": [_round(xmax), _round(ymax), _round(zmax)],
    }


def _face_properties(shape: Any) -> dict[str, Any]:
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.BRepGProp import BRepGProp
    from OCP.BRepTools import BRepTools
    from OCP.GProp import GProp_GProps
    from OCP.TopoDS import TopoDS

    face = TopoDS.Face_s(shape)
    props = GProp_GProps()
    BRepGProp.SurfaceProperties_s(face, props)
    umin, umax, vmin, vmax = BRepTools.UVBounds_s(face)
    surface = BRepAdaptor_Surface(face)
    return {
        "surface_type": str(surface.GetType()).split(".")[-1],
        "area": props.Mass(),
        "parameter_range": {
            "u": [_round(umin), _round(umax)],
            "v": [_round(vmin), _round(vmax)],
        },
    }


def _edge_properties(shape: Any) -> dict[str, Any]:
    from OCP.BRepAdaptor import BRepAdaptor_Curve
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps
    from OCP.TopoDS import TopoDS

    edge = TopoDS.Edge_s(shape)
    props = GProp_GProps()
    BRepGProp.LinearProperties_s(edge, props)
    curve = BRepAdaptor_Curve(edge)
    return {
        "curve_type": str(curve.GetType()).split(".")[-1],
        "length": props.Mass(),
        "parameter_range": [_round(curve.FirstParameter()), _round(curve.LastParameter())],
    }


def _sample_face(shape: Any, n: int) -> list[dict[str, list[float]]]:
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.BRepLProp import BRepLProp_SLProps
    from OCP.BRepTools import BRepTools
    from OCP.TopoDS import TopoDS

    face = TopoDS.Face_s(shape)
    umin, umax, vmin, vmax = BRepTools.UVBounds_s(face)
    surface = BRepAdaptor_Surface(face)
    props = BRepLProp_SLProps(surface, 1, 1e-7)
    samples = []
    for index in range(n):
        t = 0.5 if n == 1 else index / (n - 1)
        u = umin + (umax - umin) * t
        v = vmin + (vmax - vmin) * t
        point = surface.Value(u, v)
        props.SetParameters(u, v)
        normal = props.Normal() if props.IsNormalDefined() else None
        samples.append(
            {
                "point": _point(point),
                "normal": _direction(normal) if normal is not None else [],
            }
        )
    return samples


def _sample_edge(shape: Any, n: int) -> list[dict[str, list[float]]]:
    from OCP.BRepAdaptor import BRepAdaptor_Curve
    from OCP.BRepLProp import BRepLProp_CLProps
    from OCP.TopoDS import TopoDS

    edge = TopoDS.Edge_s(shape)
    curve = BRepAdaptor_Curve(edge)
    first = curve.FirstParameter()
    last = curve.LastParameter()
    props = BRepLProp_CLProps(curve, 1, 1e-7)
    samples = []
    for index in range(n):
        t = 0.5 if n == 1 else index / (n - 1)
        parameter = first + (last - first) * t
        point = curve.Value(parameter)
        props.SetParameter(parameter)
        tangent = props.D1() if props.IsTangentDefined() else None
        samples.append(
            {
                "point": _point(point),
                "tangent": _direction(tangent) if tangent is not None else [],
            }
        )
    return samples


def _point(point: Any) -> list[float]:
    return [_round(point.X()), _round(point.Y()), _round(point.Z())]


def _direction(direction: Any) -> list[float]:
    return [_round(direction.X()), _round(direction.Y()), _round(direction.Z())]


def _round(value: float) -> float:
    rounded = round(float(value), 6)
    return 0.0 if abs(rounded) < 1e-6 else rounded
