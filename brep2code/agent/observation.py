"""Bounded Q01 observation context for a future tool-facing runtime."""

from __future__ import annotations

import json
from typing import Any


MAX_OBSERVATION_CONTEXT_BYTES = 12_000
_FORBIDDEN_KEYS = {
    "input",
    "trace_path",
    "normal_trace_path",
    "path",
    "reference_script",
    "source_hash",
    "sha256",
    "provider_payload",
}


def build_observation_context(envelopes: list[dict[str, Any]]) -> str:
    """Serialize a small, path-free observation transcript for runtime use."""
    _reject_forbidden_fields(envelopes)
    encoded = json.dumps(
        {"schema_version": 1, "observation_transcript": envelopes},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    if len(encoded.encode("utf-8")) > MAX_OBSERVATION_CONTEXT_BYTES:
        raise ValueError("observation_context_too_large")
    return encoded


def _reject_forbidden_fields(value: Any) -> None:
    if isinstance(value, dict):
        if _FORBIDDEN_KEYS.intersection(value):
            raise ValueError("observation_context_contains_forbidden_field")
        for nested in value.values():
            _reject_forbidden_fields(nested)
    elif isinstance(value, list):
        for nested in value:
            _reject_forbidden_fields(nested)
