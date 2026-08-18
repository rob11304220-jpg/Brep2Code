from __future__ import annotations

import ast
from typing import Any


_UNSUPPORTED_IMPORT_ROOTS = frozenset({"OCC", "Part", "FreeCAD", "cadquery"})
_COMPATIBILITY_MESSAGE = (
    "Use imports from the installed OCP package only; do not use OCC.Core, Part, FreeCAD, "
    "or cadquery."
)
_TOPEXP_STATIC_METHODS = frozenset(
    {"FirstVertex", "LastVertex", "MapShapes", "MapShapesAndAncestors"}
)
_MAX_COMPATIBILITY_ISSUES = 4


def validate_script_compatibility(script: str) -> dict[str, Any] | None:
    """Return bounded generation feedback for runtime compatibility errors."""
    try:
        tree = ast.parse(script)
    except SyntaxError:
        return {
            "stage": "generation",
            "reason": "syntax_error",
            "message": "Generated script is not valid Python.",
        }

    issues: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        for module in _imported_modules(node):
            root = module.split(".", 1)[0]
            if root not in _UNSUPPORTED_IMPORT_ROOTS:
                continue
            _append_issue(
                issues,
                {
                    "stage": "generation",
                    "reason": "unsupported_import",
                    "module": root,
                    "message": _COMPATIBILITY_MESSAGE,
                },
            )
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _has_local_ocp_import(
            node
        ):
            _append_issue(
                issues,
                {
                    "stage": "generation",
                    "reason": "function_local_ocp_import",
                    "scope": "module",
                    "reference_topic": "OCP.module_scope_imports",
                    "message": (
                        "Place every OCP import at module scope; do not import OCP "
                        "inside functions."
                    ),
                },
            )
        if _unsupported_topexp_static_call(node):
            method = node.func.attr
            feedback = {
                "stage": "generation",
                "reason": "ocp_static_method_suffix",
                "method": f"TopExp.{method}",
                "replacement": f"TopExp.{method}_s",
                "message": "Use the OCP Python static-method binding with its _s suffix.",
            }
            if method == "MapShapes":
                feedback["reference_topic"] = "TopExp.MapShapes_s"
            _append_issue(issues, feedback)
        invalid_downcast = _invalid_topods_edge_downcast(node)
        if invalid_downcast is not None:
            _append_issue(
                issues,
                {
                    "stage": "generation",
                    "reason": "invalid_ocp_downcast",
                    "symbol": invalid_downcast,
                    "replacement": "TopoDS.Edge_s",
                    "reference_topic": "TopoDS.Edge_s",
                    "message": "Use the OCP Python downcast binding with its _s suffix.",
                },
            )
        pnt_argument_count = _invalid_brep_tool_pnt_call(node)
        if pnt_argument_count is not None:
            _append_issue(
                issues,
                {
                    "stage": "generation",
                    "reason": "invalid_ocp_call_signature",
                    "symbol": "BRep_Tool.Pnt_s",
                    "expected_arguments": 1,
                    "actual_arguments": pnt_argument_count,
                    "reference_topic": "BRepAdaptor_Curve",
                    "message": (
                        "BRep_Tool.Pnt_s reads one vertex; retrieve the approved curve "
                        "adaptor reference for parameterized edge evaluation."
                    ),
                },
            )
    if _has_legacy_topods_import(tree) and not any(
        issue.get("symbol") == "topods.Edge" for issue in issues
    ):
        _append_issue(
            issues,
            {
                "stage": "generation",
                "reason": "invalid_ocp_downcast",
                "symbol": "topods",
                "replacement": "TopoDS",
                "reference_topic": "TopoDS.Edge_s",
                "message": "Import and use the supported OCP TopoDS binding.",
            },
        )
    invalid_instance_call = _invalid_topexp_instance_static_call(tree)
    if invalid_instance_call is not None:
        instance, method = invalid_instance_call
        feedback = {
            "stage": "generation",
            "reason": "ocp_static_method_suffix",
            "method": f"{instance}.{method}",
            "replacement": f"TopExp.{method}_s",
            "message": "Use the OCP Python static-method binding with its _s suffix.",
        }
        if method == "MapShapes":
            feedback["reference_topic"] = "TopExp.MapShapes_s"
        _append_issue(issues, feedback)
    return _bounded_compatibility_feedback(issues)


def _append_issue(issues: list[dict[str, Any]], issue: dict[str, Any]) -> None:
    if issue not in issues:
        issues.append(issue)


def _bounded_compatibility_feedback(
    issues: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if not issues:
        return None
    if len(issues) == 1:
        return issues[0]
    return {
        "stage": "generation",
        "reason": "compatibility_errors",
        "issues": issues[:_MAX_COMPATIBILITY_ISSUES],
        "issues_truncated": len(issues) > _MAX_COMPATIBILITY_ISSUES,
        "message": "Generated script has multiple bounded compatibility errors.",
    }


def _imported_modules(node: ast.AST) -> tuple[str, ...]:
    if isinstance(node, ast.Import):
        return tuple(alias.name for alias in node.names)
    if isinstance(node, ast.ImportFrom) and node.module is not None:
        return (node.module,)
    return ()


def _has_local_ocp_import(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(
        module.split(".", 1)[0] == "OCP"
        for child in ast.walk(node)
        for module in _imported_modules(child)
    )


def _unsupported_topexp_static_call(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "TopExp"
        and node.func.attr in _TOPEXP_STATIC_METHODS
    )


def _invalid_topexp_instance_static_call(tree: ast.AST) -> tuple[str, str] | None:
    scopes = [tree, *(node for node in ast.walk(tree) if _is_nested_scope(node))]
    for scope in scopes:
        nodes = tuple(_walk_scope(scope))
        instances = {
            target.id
            for node in nodes
            if isinstance(node, ast.Assign)
            and _constructs_topexp(node.value)
            for target in node.targets
            if isinstance(target, ast.Name)
        }
        for node in nodes:
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id in instances
                and node.func.attr in _TOPEXP_STATIC_METHODS
            ):
                return node.func.value.id, node.func.attr
    return None


def _walk_scope(scope: ast.AST):
    yield scope
    for child in ast.iter_child_nodes(scope):
        if _is_nested_scope(child):
            continue
        yield from _walk_scope(child)


def _is_nested_scope(node: ast.AST) -> bool:
    return isinstance(
        node,
        ast.FunctionDef | ast.AsyncFunctionDef | ast.Lambda | ast.ClassDef,
    )


def _constructs_topexp(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "TopExp"
    )


def _invalid_topods_edge_downcast(node: ast.AST) -> str | None:
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in {"TopoDS", "topods"}
        and node.func.attr == "Edge"
    ):
        return f"{node.func.value.id}.Edge"
    return None


def _invalid_brep_tool_pnt_call(node: ast.AST) -> int | None:
    if not (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "BRep_Tool"
        and node.func.attr == "Pnt_s"
    ):
        return None
    if any(isinstance(argument, ast.Starred) for argument in node.args) or any(
        keyword.arg is None for keyword in node.keywords
    ):
        return None
    argument_count = len(node.args) + len(node.keywords)
    return argument_count if argument_count != 1 else None


def _has_legacy_topods_import(tree: ast.AST) -> bool:
    return any(
        isinstance(node, ast.ImportFrom)
        and node.module == "OCP.TopoDS"
        and any(alias.name == "topods" for alias in node.names)
        for node in ast.walk(tree)
    )
