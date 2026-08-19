from __future__ import annotations

from pathlib import Path

import pytest

from brep2code.cases import validate_case
from brep2code.knowledge import search_knowledge
from brep2code.tools import ToolError, dispatch_tool


def test_knowledge_search_returns_bounded_general_projection() -> None:
    result = search_knowledge("topology edge selection", scopes=["recipe"], limit=2)

    assert result["matches"]
    assert len(result["matches"]) <= 2
    assert result["matches"][0]["kind"] == "recipe"
    serialized = repr(result)
    assert "repository" not in serialized.lower()
    assert "target solution" not in serialized.lower()


def test_knowledge_search_rejects_unbounded_queries() -> None:
    with pytest.raises(ValueError, match="too long"):
        search_knowledge("x" * 257)
    with pytest.raises(ValueError, match="between 1 and 5"):
        search_knowledge("edge", limit=6)


def test_knowledge_search_is_available_as_a_harness_tool() -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))

    result = dispatch_tool(
        "knowledge_search", case, {"query": "deterministic STEP export", "scope": ["recipe"]}
    )

    assert result["matches"][0]["id"] == "recipe.step_export"
    with pytest.raises(ToolError, match="unknown arguments"):
        dispatch_tool("knowledge_search", case, {"query": "edge", "repository": True})
