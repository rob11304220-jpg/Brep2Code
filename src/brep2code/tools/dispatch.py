from __future__ import annotations

from copy import deepcopy
from typing import Any

from brep2code.cases import ValidatedCase
from brep2code.geometry.observe import observe_edges, observe_step


class ToolError(ValueError):
    pass


OCP_SYMBOL_REFERENCES = {
    "OCP.module_scope_imports": {
        "symbol": "OCP.module_scope_imports",
        "summary": "Keep every OCP import at Python module scope.",
        "usage": "Move each required OCP import above all function definitions.",
        "notes": [
            "Do not import OCP inside a function or method.",
            "Import only the OCP modules and symbols required by the script.",
        ],
    },
    "TopoDS.Edge_s": {
        "symbol": "TopoDS.Edge_s",
        "summary": "Downcast a generic TopoDS_Shape to TopoDS_Edge in OCP Python.",
        "usage": "edge = TopoDS.Edge_s(shape)",
        "notes": ["Import TopoDS from OCP.TopoDS.", "Do not call TopoDS_Edge(shape)."],
    },
    "BRepAdaptor_Curve": {
        "symbol": "BRepAdaptor_Curve",
        "summary": "Inspect the bounded geometric curve carried by a TopoDS_Edge.",
        "usage": "curve = BRepAdaptor_Curve(edge)",
        "notes": [
            "Import BRepAdaptor_Curve from OCP.BRepAdaptor.",
            "Use FirstParameter, LastParameter, GetType, and typed analytic accessors.",
        ],
    },
    "BRepAdaptor_Surface": {
        "symbol": "BRepAdaptor_Surface",
        "summary": "Inspect the bounded geometric surface carried by a TopoDS_Face.",
        "usage": "surface = BRepAdaptor_Surface(face)",
        "notes": [
            "Import BRepAdaptor_Surface from OCP.BRepAdaptor.",
            "Use GetType and typed analytic accessors such as Plane or Cylinder.",
        ],
    },
    "TopExp.MapShapes_s": {
        "symbol": "TopExp.MapShapes_s",
        "summary": "Collect unique subshapes of one requested topology type.",
        "usage": "TopExp.MapShapes_s(shape, TopAbs_EDGE, edge_map)",
        "notes": [
            "Use TopTools_IndexedMapOfShape for stable one-based indexed traversal.",
            "Import TopExp from OCP.TopExp and TopAbs_EDGE from OCP.TopAbs.",
        ],
    },
    "GeomLProp_SLProps": {
        "symbol": "GeomLProp_SLProps",
        "summary": "Evaluate bounded local surface differential properties at known UV parameters.",
        "usage": "props = GeomLProp_SLProps(surface, u, v, 1, tolerance)",
        "notes": [
            "Import GeomLProp_SLProps from OCP.GeomLProp.",
            "Check IsNormalDefined before reading Normal.",
        ],
    },
}


def dispatch_tool(
    name: str, case: ValidatedCase, arguments: dict[str, Any] | None = None
) -> dict[str, Any]:
    arguments = {} if arguments is None else arguments
    if not isinstance(arguments, dict):
        raise ToolError("tool arguments must be an object")
    if name == "brep_observations":
        if arguments:
            raise ToolError("brep_observations does not accept arguments")
        metadata = case.metadata
        return {
            "case_id": case.case.case_id,
            "split": case.case.split,
            "unit": metadata["unit"],
            "brep": observe_step(case.case.input_step),
        }
    if name == "edge_candidates":
        if arguments:
            raise ToolError("edge_candidates does not accept arguments")
        return observe_edges(case.case.input_step)
    if name == "ocp_symbol":
        if set(arguments) != {"topic"} or not isinstance(arguments["topic"], str):
            raise ToolError("ocp_symbol requires one string topic")
        try:
            return deepcopy(OCP_SYMBOL_REFERENCES[arguments["topic"]])
        except KeyError as exc:
            raise ToolError("ocp_symbol topic is not allowlisted") from exc
    raise ToolError(f"unknown tool: {name}")
