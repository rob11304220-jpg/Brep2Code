"""Offline-only static API classifier for the M115 prismatic policy.

This module is deliberately not imported by the Harness or a provider path.
It validates only the pre-sandbox API boundary frozen in the M115 policy.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass


M115_STATIC_API_CLASSIFIER_VERSION = "m115-prismatic-through-cut-static-api-v1"

_REQUIRED_IMPORTS = {
    "pathlib": {"Path"},
    "OCP.BRepAlgoAPI": {"BRepAlgoAPI_Cut"},
    "OCP.BRepPrimAPI": {"BRepPrimAPI_MakeBox", "BRepPrimAPI_MakeCylinder"},
    "OCP.IFSelect": {"IFSelect_RetDone"},
    "OCP.STEPControl": {"STEPControl_AsIs", "STEPControl_Writer"},
    "OCP.gp": {"gp_Ax2", "gp_Dir", "gp_Pnt"},
}

_CONSTRUCTOR_ARITIES = {
    "BRepPrimAPI_MakeBox": 3,
    "BRepPrimAPI_MakeCylinder": 3,
    "BRepAlgoAPI_Cut": 2,
    "STEPControl_Writer": 0,
}


@dataclass(frozen=True)
class StaticApiClassification:
    """One mutually exclusive pre-sandbox classification result."""

    category: str
    reason: str | None
    classifier_version: str = M115_STATIC_API_CLASSIFIER_VERSION


def classify_static_api(script: str) -> StaticApiClassification:
    """Classify a declared through-cut script without executing it.

    The classifier intentionally recognizes only the fixed OCP import and
    constructor surface in the M115 policy.  It is not a general CAD checker.
    """

    try:
        tree = ast.parse(script)
    except SyntaxError:
        return _inadmissible("syntax_error")

    imports: dict[str, set[str]] = {}
    calls: list[ast.Call] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            return _inadmissible("forbidden_import")
        if isinstance(node, ast.ImportFrom):
            if node.level != 0 or node.module not in _REQUIRED_IMPORTS:
                return _inadmissible("forbidden_import")
            names = {alias.name for alias in node.names}
            if any(alias.asname is not None or alias.name == "*" for alias in node.names):
                return _inadmissible("unsupported_symbol")
            imports.setdefault(node.module, set()).update(names)
        elif isinstance(node, ast.Call):
            calls.append(node)

    if imports != _REQUIRED_IMPORTS:
        return _inadmissible("missing_or_unsupported_import_symbol")

    for constructor, arity in _CONSTRUCTOR_ARITIES.items():
        matching = [call for call in calls if _call_name(call) == constructor]
        if len(matching) != 1:
            return _inadmissible("missing_through_cut_recipe")
        call = matching[0]
        if len(call.args) != arity or call.keywords:
            return _inadmissible("constructor_arity_mismatch")

    cylinder = next(call for call in calls if _call_name(call) == "BRepPrimAPI_MakeCylinder")
    if not isinstance(cylinder.args[0], ast.Call) or _call_name(cylinder.args[0]) != "gp_Ax2":
        return _inadmissible("missing_through_cut_recipe")
    if not any(_call_name(call) == "gp_Dir" for call in calls):
        return _inadmissible("missing_through_cut_recipe")
    return StaticApiClassification(category="api_admissible", reason=None)


def _call_name(call: ast.Call) -> str | None:
    return call.func.id if isinstance(call.func, ast.Name) else None


def _inadmissible(reason: str) -> StaticApiClassification:
    return StaticApiClassification(category="api_inadmissible", reason=reason)
