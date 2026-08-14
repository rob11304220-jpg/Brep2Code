"""Bounded bridge from agent tool calls to B-Rep probe tools."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from brep2code.brep import (
    ProbeError,
    discover_input_file,
    load_model,
    probe_entity,
    probe_summary,
    probe_topology,
    sample_entity,
)
from brep2code.brep.serialize import DEFAULT_RESULT_LIMIT_BYTES
from brep2code.storage import RecordStore


ALLOWED_SELECTORS = ("all", "solid", "shell", "face", "edge")


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    schema: dict[str, Any]


@dataclass(frozen=True)
class ToolCallResult:
    ok: bool
    tool: str
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    trace_path: str | None = None

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


class BRepToolBridge:
    """Validates and dispatches bounded B-Rep probe tool calls."""

    def __init__(
        self,
        store: RecordStore | None = None,
        *,
        max_calls: int = 8,
        max_entities: int = 80,
        max_samples: int = 32,
        result_limit_bytes: int = DEFAULT_RESULT_LIMIT_BYTES,
    ) -> None:
        self.store = store or RecordStore()
        self.max_calls = max_calls
        self.max_entities = max_entities
        self.max_samples = max_samples
        self.result_limit_bytes = result_limit_bytes
        self.call_count = 0
        self._observation_call_counts: dict[str, int] = {}

    def specs(self) -> list[ToolSpec]:
        return [
            ToolSpec(
                name="probe_summary",
                description="Return input file, bbox, topology counts, area, and volume summary.",
                schema={"type": "object", "properties": {}, "additionalProperties": False},
            ),
            ToolSpec(
                name="probe_topology",
                description="Return bounded topology entity ids by selector.",
                schema={
                    "type": "object",
                    "properties": {
                        "selector": {"type": "string", "enum": list(ALLOWED_SELECTORS)},
                        "max_entities": {"type": "integer", "minimum": 1, "maximum": self.max_entities},
                    },
                    "additionalProperties": False,
                },
            ),
            ToolSpec(
                name="probe_entity",
                description="Return details for one stable entity id.",
                schema={
                    "type": "object",
                    "properties": {"entity_id": {"type": "string"}},
                    "required": ["entity_id"],
                    "additionalProperties": False,
                },
            ),
            ToolSpec(
                name="sample_entity",
                description="Return bounded samples for one face or edge entity id.",
                schema={
                    "type": "object",
                    "properties": {
                        "entity_id": {"type": "string"},
                        "samples": {"type": "integer", "minimum": 1, "maximum": self.max_samples},
                    },
                    "required": ["entity_id", "samples"],
                    "additionalProperties": False,
                },
            ),
        ]

    def call(
        self,
        record_id: str,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
        *,
        trace_dir: Path | None = None,
    ) -> ToolCallResult:
        arguments = arguments or {}
        if self.call_count >= self.max_calls:
            result = _error(tool_name, "tool_call_limit_exceeded", "tool call limit exceeded")
            _append_tool_trace(trace_dir, tool_name, arguments, result)
            return result

        self.call_count += 1
        result = self._dispatch(record_id, tool_name, arguments, trace_dir=trace_dir)
        _append_tool_trace(trace_dir, tool_name, arguments, result)
        return result

    def observe(
        self,
        record_id: str,
        observation_session_id: str,
        call_id: str,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
        *,
        trace_dir: Path,
    ) -> dict[str, Any]:
        """Return an LLM-visible, path-free Q01 observation envelope."""
        calls = self._observation_call_counts.get(observation_session_id, 0)
        if calls >= self.max_calls:
            result = _error(tool_name, "tool_call_limit_exceeded", "tool call limit exceeded")
        else:
            self._observation_call_counts[observation_session_id] = calls + 1
            result = self._dispatch(record_id, tool_name, arguments or {}, trace_dir=None)
        data = _sanitize_observation_data(result.result) if result.ok and result.result is not None else None
        envelope = {
            "schema_version": 1,
            "observation_session_id": observation_session_id,
            "call_id": call_id,
            "ok": result.ok,
            "data": data,
            "error": result.error,
            "truncated": bool(data and data.get("truncated")),
        }
        encoded = _canonical_json(envelope)
        if len(encoded.encode("utf-8")) > self.result_limit_bytes:
            envelope.update(
                ok=False,
                data=None,
                error={"code": "response_too_large", "message": "bounded observation response exceeds byte limit"},
                truncated=True,
            )
            encoded = _canonical_json(envelope)
        envelope["response_sha256"] = sha256(encoded.encode("utf-8")).hexdigest()
        _append_observation_trace(trace_dir, tool_name, arguments or {}, envelope)
        return envelope

    def _dispatch(
        self,
        record_id: str,
        tool_name: str,
        arguments: dict[str, Any],
        *,
        trace_dir: Path | None,
    ) -> ToolCallResult:
        if tool_name not in {spec.name for spec in self.specs()}:
            return _error(tool_name, "unknown_tool", f"unknown tool: {tool_name}")

        validation_error = self._validate(tool_name, arguments)
        if validation_error is not None:
            return validation_error

        try:
            record = self.store.ensure_record(record_id)
            input_path = discover_input_file(record.input_dir)
            model = load_model(input_path)
            if tool_name == "probe_summary":
                payload = probe_summary(model, trace_dir=trace_dir, limit_bytes=self.result_limit_bytes)
            elif tool_name == "probe_topology":
                payload = probe_topology(
                    model,
                    selector=arguments.get("selector", "all"),
                    max_entities=arguments.get("max_entities", self.max_entities),
                    trace_dir=trace_dir,
                    limit_bytes=self.result_limit_bytes,
                )
            elif tool_name == "probe_entity":
                payload = probe_entity(
                    model,
                    arguments["entity_id"],
                    trace_dir=trace_dir,
                    limit_bytes=self.result_limit_bytes,
                )
            else:
                payload = sample_entity(
                    model,
                    arguments["entity_id"],
                    arguments["samples"],
                    max_samples=self.max_samples,
                    trace_dir=trace_dir,
                    limit_bytes=self.result_limit_bytes,
                )
        except ProbeError as exc:
            return _error(tool_name, exc.code, exc.message)
        except (FileNotFoundError, ValueError) as exc:
            return _error(tool_name, exc.__class__.__name__, str(exc))

        return ToolCallResult(
            ok=bool(payload.get("ok")),
            tool=tool_name,
            result=payload,
            trace_path=payload.get("trace_path"),
        )

    def _validate(self, tool_name: str, arguments: dict[str, Any]) -> ToolCallResult | None:
        if not isinstance(arguments, dict):
            return _error(tool_name, "invalid_arguments", "arguments must be an object")

        allowed = {
            "probe_summary": set(),
            "probe_topology": {"selector", "max_entities"},
            "probe_entity": {"entity_id"},
            "sample_entity": {"entity_id", "samples"},
        }[tool_name]
        unknown = sorted(set(arguments) - allowed)
        if unknown:
            return _error(tool_name, "invalid_arguments", f"unknown argument(s): {', '.join(unknown)}")

        if tool_name == "probe_topology":
            selector = arguments.get("selector", "all")
            if selector not in ALLOWED_SELECTORS:
                return _error(tool_name, "invalid_selector", f"unsupported selector: {selector}")
            max_entities = arguments.get("max_entities", self.max_entities)
            if not isinstance(max_entities, int) or not 1 <= max_entities <= self.max_entities:
                return _error(
                    tool_name,
                    "invalid_max_entities",
                    f"max_entities must be an integer from 1 to {self.max_entities}",
                )

        if tool_name in {"probe_entity", "sample_entity"}:
            entity_id = arguments.get("entity_id")
            if not isinstance(entity_id, str) or not entity_id:
                return _error(tool_name, "invalid_entity_id", "entity_id must be a non-empty string")

        if tool_name == "sample_entity":
            samples = arguments.get("samples")
            if not isinstance(samples, int) or not 1 <= samples <= self.max_samples:
                return _error(
                    tool_name,
                    "invalid_sample_count",
                    f"samples must be an integer from 1 to {self.max_samples}",
                )

        return None


def _error(tool_name: str, code: str, message: str) -> ToolCallResult:
    return ToolCallResult(ok=False, tool=tool_name, error={"code": code, "message": message})


def _append_tool_trace(
    trace_dir: Path | None,
    tool_name: str,
    arguments: dict[str, Any],
    result: ToolCallResult,
) -> None:
    if trace_dir is None:
        return
    trace_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "created_at": _utc_now(),
        "tool": tool_name,
        "arguments": arguments,
        "ok": result.ok,
        "result": result.result,
        "error": result.error,
        "trace_path": result.trace_path,
    }
    path = trace_dir / "tool_calls.jsonl"
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def _sanitize_observation_data(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if key not in {"input", "file_name", "trace_path"}}


def _canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _append_observation_trace(trace_dir: Path, tool_name: str, arguments: dict[str, Any], envelope: dict[str, Any]) -> None:
    trace_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "created_at": _utc_now(),
        "observation_session_id": envelope["observation_session_id"],
        "call_id": envelope["call_id"],
        "tool": tool_name,
        "arguments": arguments,
        "ok": envelope["ok"],
        "error": envelope["error"],
        "truncated": envelope["truncated"],
        "response_sha256": envelope["response_sha256"],
        "response_bytes": len(_canonical_json(envelope).encode("utf-8")),
    }
    with (trace_dir / "observation_queries.jsonl").open("a", encoding="utf-8") as file:
        file.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
