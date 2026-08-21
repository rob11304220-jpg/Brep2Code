from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class BackendProfileId(StrEnum):
    OCP_V1 = "ocp_v1"
    CADQUERY_V1 = "cadquery_v1"


@dataclass(frozen=True)
class BackendProfile:
    profile_id: BackendProfileId
    package: str
    version_spec: str
    import_roots: tuple[str, ...]
    api_summary: str
    export_contract: str


_PROFILES = {
    BackendProfileId.OCP_V1: BackendProfile(
        profile_id=BackendProfileId.OCP_V1,
        package="cadquery-ocp",
        version_spec="==7.9.3.1.1",
        import_roots=("OCP",),
        api_summary=(
            "Use only the installed OCP Python bindings. Approved module families are gp, "
            "BRepPrimAPI, BRepAlgoAPI, BRepFilletAPI, BRepBuilderAPI, TopAbs, TopExp, "
            "TopoDS, STEPControl, IFSelect, and BRepTools."
        ),
        export_contract=(
            "Use OCP.STEPControl to write the final TopoDS shape to exactly output.step."
        ),
    ),
    BackendProfileId.CADQUERY_V1: BackendProfile(
        profile_id=BackendProfileId.CADQUERY_V1,
        package="cadquery",
        version_spec="==2.8.0",
        import_roots=("cadquery",),
        api_summary=(
            "Use only import cadquery as cq and the CadQuery Workplane modeling API, including "
            "primitive, sketch, extrude, boolean, selector, and fillet operations."
        ),
        export_contract=(
            "Use the CadQuery STEP exporter to write the final shape to exactly output.step."
        ),
    ),
}


def backend_profile(value: BackendProfileId | str) -> BackendProfile:
    try:
        profile_id = BackendProfileId(value)
    except ValueError as exc:
        raise ValueError(f"unknown backend profile: {value}") from exc
    return _PROFILES[profile_id]


def backend_profile_ids() -> tuple[str, ...]:
    return tuple(item.value for item in BackendProfileId)
