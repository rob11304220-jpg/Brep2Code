from __future__ import annotations

from typing import Any


MAX_QUERY_CHARS = 256
MAX_RESULTS = 5
MAX_CONTENT_CHARS = 1600

_RECIPE_RECORDS: tuple[dict[str, Any], ...] = (
    {
        "id": "recipe.boolean_feature",
        "kind": "recipe",
        "title": "Ordered boolean feature construction",
        "summary": "Build independent solids first, then apply the boolean operation to the intended base result.",
        "content": (
            "Keep base and tool construction explicit. Apply the boolean operation to the "
            "actual preceding result, and export only the final solid. Check placement, "
            "intersections, and the expected topology after execution."
        ),
        "tags": ["boolean", "feature", "sequence", "topology"],
    },
    {
        "id": "recipe.topology_selection",
        "kind": "recipe",
        "title": "Topology-aware feature selection",
        "summary": "Select edges or faces from bounded geometric and adjacency properties instead of unstable indices.",
        "content": (
            "Map unique subshapes, inspect analytic type, geometry parameters, orientation, "
            "and adjacent faces, then select only candidates satisfying the intended role. "
            "Treat ambiguous selectors as a reason to probe or repair rather than guessing."
        ),
        "tags": ["topology", "edge", "face", "selection", "fillet"],
    },
    {
        "id": "recipe.step_export",
        "kind": "recipe",
        "title": "Deterministic STEP export",
        "summary": "Write one deterministic output.step from a self-contained OCP program.",
        "content": (
            "Keep imports at module scope, avoid repository or input-file access, use the "
            "installed OCP binding, write exactly output.step, and fail if STEPControl_Writer "
            "does not return IFSelect_RetDone."
        ),
        "tags": ["step", "export", "ocp", "sandbox"],
    },
)


def search_knowledge(
    query: str, *, scopes: list[str] | None = None, limit: int = 3
) -> dict[str, Any]:
    """Return a bounded projection of approved SDK and recipe knowledge.

    The catalog is intentionally answer-free: it contains general modeling guidance,
    not target-specific scripts, expected values, or repository paths.
    """

    if not isinstance(query, str) or not query.strip():
        raise ValueError("knowledge query must be a non-empty string")
    if len(query) > MAX_QUERY_CHARS:
        raise ValueError("knowledge query is too long")
    if scopes is not None and (
        not isinstance(scopes, list)
        or any(not isinstance(scope, str) or not scope for scope in scopes)
        or len(scopes) != len(set(scopes))
    ):
        raise ValueError("knowledge scopes must be a unique string array")
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= MAX_RESULTS:
        raise ValueError(f"knowledge limit must be between 1 and {MAX_RESULTS}")

    tokens = {token for token in _tokens(query) if len(token) > 1}
    records = _all_records()
    if scopes:
        records = tuple(record for record in records if record["kind"] in scopes)
    ranked = sorted(
        (
            (_score(record, tokens), record)
            for record in records
            if _score(record, tokens) > 0
        ),
        key=lambda item: (-item[0], item[1]["id"]),
    )
    matches = [
        {
            "id": record["id"],
            "kind": record["kind"],
            "title": record["title"],
            "summary": record["summary"],
            "content": record["content"][:MAX_CONTENT_CHARS],
        }
        for _, record in ranked[:limit]
    ]
    return {
        "query": query,
        "matches": matches,
        "truncated": len(ranked) > limit,
    }


def _all_records() -> tuple[dict[str, Any], ...]:
    from brep2code.tools.dispatch import OCP_SYMBOL_REFERENCES

    symbols = tuple(
        {
            "id": f"sdk.{topic}",
            "kind": "sdk",
            "title": topic,
            "summary": value["summary"],
            "content": " ".join(
                [value["summary"], value["usage"], *value.get("notes", [])]
            ),
            "tags": ["ocp", "sdk", topic.lower()],
        }
        for topic, value in OCP_SYMBOL_REFERENCES.items()
    )
    return symbols + _RECIPE_RECORDS


def _score(record: dict[str, Any], tokens: set[str]) -> int:
    haystack = " ".join(
        [record["title"], record["summary"], record["content"], *record.get("tags", [])]
    ).lower()
    return sum(token in haystack for token in tokens)


def _tokens(value: str) -> tuple[str, ...]:
    normalized = "".join(character.lower() if character.isalnum() else " " for character in value)
    return tuple(normalized.split())
