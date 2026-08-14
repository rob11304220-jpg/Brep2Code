"""Serialization helpers for bounded probe tool results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_RESULT_LIMIT_BYTES = 12_000


def bounded_result(payload: dict[str, Any], limit_bytes: int = DEFAULT_RESULT_LIMIT_BYTES) -> dict[str, Any]:
    """Return payload if it fits the limit, otherwise return a structured overflow summary."""

    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    if len(encoded.encode("utf-8")) <= limit_bytes:
        return payload
    return {
        "ok": False,
        "error": {
            "code": "result_too_large",
            "message": "Probe result exceeds the configured response size limit.",
            "size_bytes": len(encoded.encode("utf-8")),
            "limit_bytes": limit_bytes,
        },
        "summary": _summary(payload),
    }


def bounded_result_with_trace(
    payload: dict[str, Any],
    trace_dir: Path | None,
    trace_name: str,
    limit_bytes: int = DEFAULT_RESULT_LIMIT_BYTES,
) -> dict[str, Any]:
    """Bound a payload and write the full result to trace_dir when it overflows."""

    encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    if len(encoded.encode("utf-8")) <= limit_bytes:
        return payload
    if trace_dir is None:
        return bounded_result(payload, limit_bytes=limit_bytes)
    trace_dir.mkdir(parents=True, exist_ok=True)
    trace_path = trace_dir / trace_name
    trace_path.write_text(encoded + "\n", encoding="utf-8")
    return {
        "ok": True,
        "truncated": True,
        "trace_path": str(trace_path),
        "size_bytes": len(encoded.encode("utf-8")),
        "limit_bytes": limit_bytes,
        "summary": _summary(payload),
    }


def _summary(payload: dict[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for key in ("ok", "input", "format", "entity_id", "entity_type", "counts", "bbox"):
        if key in payload:
            summary[key] = payload[key]
    return summary
