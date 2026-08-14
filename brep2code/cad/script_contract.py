"""Static, fail-closed checks for generated ``build_sequence.py`` files."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import importlib
from pathlib import Path


CONTRACT_VERSION = "build-script-api-v1"
_UNSUPPORTED_ROOTS = {"cadquery", "OCC"}


@dataclass(frozen=True)
class BuildScriptContractResult:
    """A content-free validation result suitable for local execution evidence."""

    valid: bool
    violations: tuple[dict[str, object], ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "version": CONTRACT_VERSION,
            "status": "pass" if self.valid else "fail",
            "violations": list(self.violations),
        }


def validate_build_script(path: Path) -> BuildScriptContractResult:
    """Reject statically visible imports of CAD APIs absent from the runtime.

    This deliberately does not attempt to allow-list Python or model all
    dynamic imports. It blocks the incompatible import families observed at
    the Harness boundary while leaving sandbox policy authoritative elsewhere.
    """

    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        return BuildScriptContractResult(
            valid=False,
            violations=(
                {
                    "code": "invalid_python_syntax",
                    "line": exc.lineno,
                    "message": "build_sequence.py is not valid Python source",
                },
            ),
        )

    violations: list[dict[str, object]] = []
    for node in ast.walk(tree):
        for module in _imported_modules(node):
            if module.split(".", 1)[0] not in _UNSUPPORTED_ROOTS:
                continue
            violations.append(
                {
                    "code": "unsupported_cad_import",
                    "line": node.lineno,
                    "module": module,
                    "message": f"{module} is unavailable; use installed OCP bindings instead",
                }
            )
        if isinstance(node, ast.ImportFrom) and node.module is not None and node.module.startswith("OCP"):
            violations.extend(_unsupported_ocp_symbols(node))
    return BuildScriptContractResult(valid=not violations, violations=tuple(violations))


def _unsupported_ocp_symbols(node: ast.ImportFrom) -> list[dict[str, object]]:
    """Classify unavailable statically imported OCP names before execution."""

    try:
        module = importlib.import_module(node.module or "")
    except ImportError:
        return [
            {
                "code": "unsupported_ocp_module",
                "line": node.lineno,
                "module": node.module,
                "message": f"{node.module} is unavailable in the installed OCP bindings",
            }
        ]
    return [
        {
            "code": "unsupported_ocp_symbol",
            "line": node.lineno,
            "module": node.module,
            "symbol": alias.name,
            "message": f"{alias.name} is unavailable from {node.module}; use installed OCP bindings only",
        }
        for alias in node.names
        if alias.name != "*" and not hasattr(module, alias.name)
    ]


def _imported_modules(node: ast.AST) -> tuple[str, ...]:
    if isinstance(node, ast.Import):
        return tuple(alias.name for alias in node.names)
    if isinstance(node, ast.ImportFrom):
        return (node.module,) if node.module is not None else ()
    return ()
