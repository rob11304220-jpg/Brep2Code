"""Revision-scoped, bounded access to explicitly selected guidance cards."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from brep2code.agent.tools import ToolCallResult, ToolSpec


MAX_RESPONSE_BYTES = 3_000
TOOL_NAME = "get_guidance_card"
DEFAULT_ROLES = (
    "final primitive",
    "single boolean-cut tool",
    "repeated boolean-cut tool",
)


@dataclass(frozen=True)
class GuidanceBundle:
    index_path: Path
    card_path: Path
    index_sha256: str
    card_sha256: str
    roles: tuple[str, ...] = DEFAULT_ROLES

    @classmethod
    def from_paths(
        cls,
        index_path: Path,
        card_path: Path,
        *,
        roles: tuple[str, ...] = DEFAULT_ROLES,
    ) -> "GuidanceBundle":
        if not roles or len(set(roles)) != len(roles) or any(not role for role in roles):
            raise ValueError("guidance bundle roles must be non-empty and unique")
        return cls(index_path, card_path, _sha256(index_path), _sha256(card_path), roles)


class GuidanceCardBridge:
    """Returns one explicit card for one revision; no directory search is performed."""

    def __init__(self, revision_id: str, bundle: GuidanceBundle | None = None) -> None:
        self.revision_id = revision_id
        self.bundle = bundle

    def specs(self) -> list[ToolSpec]:
        if self.bundle is None:
            return []
        return [ToolSpec(TOOL_NAME, "Return one bounded, revision-scoped guidance card.", {"type": "object", "properties": {"role": {"type": "string", "enum": sorted(self.bundle.roles)}}, "required": ["role"], "additionalProperties": False})]

    def call(self, tool_name: str, arguments: dict[str, Any] | None = None, *, trace_dir: Path | None = None) -> ToolCallResult:
        result = self._dispatch(tool_name, arguments or {})
        if trace_dir is not None:
            trace_dir.mkdir(parents=True, exist_ok=True)
            payload = {"schema_version": 1, "revision_id": self.revision_id, "tool": tool_name, "selected_role": arguments.get("role") if isinstance(arguments, dict) and isinstance(arguments.get("role"), str) else None, "ok": result.ok, "error": result.error, "guidance_index_sha256": self.bundle.index_sha256 if self.bundle else None, "returned_card_ids": [result.result["id"]] if result.ok and result.result else []}
            with (trace_dir / "guidance_calls.jsonl").open("a", encoding="utf-8") as file:
                file.write(json.dumps(payload, sort_keys=True) + "\n")
        return result

    def _dispatch(self, tool_name: str, arguments: dict[str, Any]) -> ToolCallResult:
        if self.bundle is None:
            return _error(tool_name, "guidance_not_enabled", "no guidance bundle selected for this revision")
        if tool_name != TOOL_NAME:
            return _error(tool_name, "unknown_tool", f"unknown tool: {tool_name}")
        if set(arguments) != {"role"} or arguments["role"] not in self.bundle.roles:
            return _error(tool_name, "invalid_arguments", "role must be declared by the selected guidance bundle")
        try:
            valid = _sha256(self.bundle.index_path) == self.bundle.index_sha256 and _sha256(self.bundle.card_path) == self.bundle.card_sha256
            index = _load_json(self.bundle.index_path)
            card = _load_json(self.bundle.card_path)
        except OSError:
            return _error(tool_name, "guidance_unavailable", "guidance bundle is unavailable")
        except json.JSONDecodeError:
            return _error(tool_name, "guidance_index_invalid", "guidance bundle is invalid JSON")
        if not valid:
            return _error(tool_name, "guidance_index_invalid", "guidance bundle hash no longer matches")
        relative = f"cards/{self.bundle.card_path.name}"
        if relative not in index.get("cards", []) or card.get("id") != self.bundle.card_path.stem:
            return _error(tool_name, "guidance_index_invalid", "selected card is not declared by the index")
        response = {key: card[key] for key in ("id", "scope", "claim", "runtime_action", "validation", "sources")}
        if len(json.dumps(response, sort_keys=True).encode()) > MAX_RESPONSE_BYTES:
            return _error(tool_name, "response_too_large", "bounded guidance response exceeds byte limit")
        return ToolCallResult(ok=True, tool=tool_name, result=response)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _error(tool: str, code: str, message: str) -> ToolCallResult:
    return ToolCallResult(ok=False, tool=tool, error={"code": code, "message": message})
