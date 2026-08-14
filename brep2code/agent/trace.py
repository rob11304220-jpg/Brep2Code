"""Trace writers for LLM repair messages and provider responses."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Literal

from brep2code.agent.provider import LLMMessage, ProviderResponse


TraceDirection = Literal["request", "response"]
SECRET_KEY_PARTS = ("api_key", "apikey", "authorization", "bearer", "env", "password", "secret", "token")
DEFAULT_LIMIT_CHARS = 12_000


def append_llm_messages(
    trace_dir: Path,
    messages: list[LLMMessage],
    *,
    direction: TraceDirection,
    limit_chars: int = DEFAULT_LIMIT_CHARS,
) -> Path:
    """Append sanitized messages to traces/llm_messages.jsonl."""

    path = trace_dir / "llm_messages.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        for message in messages:
            payload = {
                "schema_version": 1,
                "created_at": _utc_now(),
                "direction": direction,
                "message": _sanitize(asdict(message), limit_chars=limit_chars),
            }
            file.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    return path


def write_provider_response_trace(
    trace_dir: Path,
    response: ProviderResponse,
    *,
    limit_chars: int = DEFAULT_LIMIT_CHARS,
) -> Path:
    """Write a sanitized provider response summary to traces/provider_response.json."""

    path = trace_dir / "provider_response.json"
    payload = {
        "schema_version": 1,
        "created_at": _utc_now(),
        "response": _sanitize(_to_plain(response), limit_chars=limit_chars),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _to_plain(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    return value


def _sanitize(value: Any, *, limit_chars: int) -> Any:
    if isinstance(value, dict):
        sanitized = {}
        for key, item in value.items():
            if _is_secret_key(str(key)):
                sanitized[key] = "[redacted]"
            else:
                sanitized[key] = _sanitize(item, limit_chars=limit_chars)
        return sanitized
    if isinstance(value, list):
        return [_sanitize(item, limit_chars=limit_chars) for item in value]
    if isinstance(value, str):
        return _truncate(value, limit_chars)
    return value


def _is_secret_key(key: str) -> bool:
    lowered = key.lower()
    return any(part in lowered for part in SECRET_KEY_PARTS)


def _truncate(value: str, limit_chars: int) -> str:
    if limit_chars < 0 or len(value) <= limit_chars:
        return value
    return value[:limit_chars] + "\n...[truncated]"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
