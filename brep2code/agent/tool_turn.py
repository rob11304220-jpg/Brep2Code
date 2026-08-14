"""Fail-closed, offline Harness-owned tool-turn orchestration.

This module deliberately stops after one script submission and its Harness
feedback.  A later repair policy may consume that feedback, but is not part of
this tool-turn contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import Any

from brep2code.agent.guidance import GuidanceBundle, GuidanceCardBridge, TOOL_NAME
from brep2code.agent.harness import HarnessRunResult, ManualHarness
from brep2code.agent.provider import (
    FakeLLMProvider,
    LLMMessage,
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
)
from brep2code.agent.repair import _write_script_update
from brep2code.agent.tools import BRepToolBridge, ToolSpec
from brep2code.agent.trace import append_llm_messages, write_provider_response_trace
from brep2code.storage.store import write_json


@dataclass(frozen=True)
class ToolTurnLimits:
    """Static limits for one prepared campaign/revision conversation."""

    max_turns: int = 8
    max_tool_calls: int = 8
    max_tool_result_bytes: int = 12_000

    def __post_init__(self) -> None:
        for name, value in vars(self).items():
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise ValueError(f"{name} must be a positive integer")


@dataclass(frozen=True)
class ToolTurnResult:
    status: str
    provider_requests: int
    tool_calls: int
    stop_reason: str
    harness_result: HarnessRunResult | None = None
    error: dict[str, str] | None = None
    trace: list[dict[str, Any]] = field(default_factory=list)


class ToolTurnLoopRunner:
    """Run declared probes/cards followed by one generated script locally.

    The provider only chooses a single tool or a final replacement script per
    turn.  Every tool request is dispatched by the Harness; no provider can
    read a workspace, input B-Rep, card directory, or shell.
    """

    def __init__(
        self,
        *,
        harness: ManualHarness,
        provider: LLMProvider,
        bridge: BRepToolBridge | None = None,
        limits: ToolTurnLimits | None = None,
    ) -> None:
        if not isinstance(provider, FakeLLMProvider):
            raise ValueError("ToolTurnLoopRunner is offline and requires FakeLLMProvider")
        self.harness = harness
        self.provider = provider
        self.bridge = bridge or BRepToolBridge(store=harness.store)
        self.limits = limits or ToolTurnLimits()

    def run(
        self,
        record_id: str,
        *,
        input_path: Path,
        campaign_identity: dict[str, str],
        observation_session_id: str,
        guidance_bundle: GuidanceBundle | None = None,
        selected_guidance_role: str | None = None,
        timeout: int = 60,
        max_output_tokens: int | None = None,
    ) -> ToolTurnResult:
        """Continue tool turns until a script is submitted or a limit stops it."""

        _validate_campaign_identity(campaign_identity)
        if (guidance_bundle is None) != (selected_guidance_role is None):
            raise ValueError("guidance bundle and selected guidance role must be supplied together")
        if max_output_tokens is not None and (
            not isinstance(max_output_tokens, int) or isinstance(max_output_tokens, bool) or max_output_tokens < 1
        ):
            raise ValueError("max_output_tokens must be a positive integer")

        record = self.harness.store.ensure_record(record_id)
        self.harness._prepare_input(record, input_path)
        tool_specs = self.bridge.specs() + GuidanceCardBridge("pending", guidance_bundle).specs()
        messages = _initial_messages(tool_specs, campaign_identity)
        trace: list[dict[str, Any]] = []
        tool_calls = 0

        with TemporaryDirectory(prefix="brep2code-tool-turn-") as temporary:
            pending_trace = Path(temporary)
            for turn in range(1, self.limits.max_turns + 1):
                request = ProviderRequest(
                    model=getattr(self.provider, "model", "fake-tool-turn"),
                    messages=list(messages),
                    max_output_tokens=max_output_tokens,
                    metadata={
                        "policy": "harness-tool-turn-v1",
                        "campaign_id": campaign_identity["campaign_id"],
                        "campaign_spec_sha256": campaign_identity["campaign_spec_sha256"],
                        "turn": turn,
                    },
                )
                response = self.provider.complete(request)
                if response.tool_call is not None and response.script_update is not None:
                    return self._error(
                        "ambiguous_provider_response",
                        "response must contain a tool call or replacement script, not both",
                        turn,
                        tool_calls,
                        trace,
                    )
                if response.tool_call is not None:
                    tool_calls += 1
                    result = self._dispatch_tool(
                        record_id,
                        observation_session_id,
                        response.tool_call.tool,
                        response.tool_call.arguments,
                        guidance_bundle=guidance_bundle,
                        selected_guidance_role=selected_guidance_role,
                        trace_dir=pending_trace,
                        tool_calls=tool_calls,
                    )
                    payload = _tool_payload(response.tool_call.tool, result)
                    trace.append(_trace_entry(turn, "tool", response.tool_call.tool, payload))
                    messages.append(LLMMessage(role="assistant", content=response.output_text))
                    messages.append(LLMMessage(role="tool", name=response.tool_call.tool, content=_canonical(payload)))
                    if tool_calls >= self.limits.max_tool_calls:
                        return self._stopped("tool_call_limit_exceeded", turn, tool_calls, trace)
                    continue

                if response.script_update is None or response.script_update.kind != "replace" or response.script_update.content is None:
                    return self._error("missing_script_update", "response must contain one tool call or replacement script", turn, tool_calls, trace)
                result = self._execute_script(record_id, response, pending_trace, timeout)
                _copy_pending_trace(pending_trace, result.revision.traces)
                append_llm_messages(result.revision.traces, messages, direction="request")
                append_llm_messages(result.revision.traces, [LLMMessage(role="assistant", content=response.output_text)], direction="response")
                write_provider_response_trace(result.revision.traces, response)
                _write_script_update(result.revision.traces, response.script_update)
                feedback = _feedback(result.signal_bundle)
                trace.append(_trace_entry(turn, "execution_feedback", None, feedback))
                _write_turn_trace(result.revision.traces, campaign_identity, trace, self.limits)
                return ToolTurnResult("pass" if result.status == "pass" else "fail", turn, tool_calls, "execution_feedback", result, trace=trace)

        return self._stopped("turn_limit_exceeded", self.limits.max_turns, tool_calls, trace)

    def _dispatch_tool(
        self,
        record_id: str,
        session_id: str,
        tool: str,
        arguments: dict[str, Any],
        *,
        guidance_bundle: GuidanceBundle | None,
        selected_guidance_role: str | None,
        trace_dir: Path,
        tool_calls: int,
    ) -> dict[str, Any]:
        if tool_calls > self.limits.max_tool_calls:
            return {"ok": False, "error": {"code": "tool_call_limit_exceeded", "message": "tool call limit exceeded"}}
        if tool == TOOL_NAME:
            if guidance_bundle is None or arguments != {"role": selected_guidance_role}:
                return {"ok": False, "error": {"code": "guidance_not_selected", "message": "requested card is not selected for this campaign"}}
            called = GuidanceCardBridge("pending", guidance_bundle).call(tool, arguments, trace_dir=trace_dir)
            result = {"ok": called.ok, "result": called.result, "error": called.error}
        else:
            envelope = self.bridge.observe(record_id, session_id, f"turn-{tool_calls}", tool, arguments, trace_dir=trace_dir)
            result = {"ok": envelope["ok"], "result": envelope["data"], "error": envelope["error"]}
        if len(_canonical(result).encode("utf-8")) > self.limits.max_tool_result_bytes:
            return {"ok": False, "error": {"code": "response_too_large", "message": "tool result exceeds tool-turn byte limit"}}
        return result

    def _execute_script(self, record_id: str, response: ProviderResponse, pending_trace: Path, timeout: int) -> HarnessRunResult:
        assert response.script_update is not None and response.script_update.content is not None
        with NamedTemporaryFile("w", encoding="utf-8", suffix=".py", delete=False) as generated:
            generated.write(response.script_update.content)
            script_path = Path(generated.name)
        try:
            return self.harness.run(record_id, script=script_path, timeout=timeout, build_without_input=True)
        finally:
            script_path.unlink(missing_ok=True)

    def _stopped(self, reason: str, provider_requests: int, tool_calls: int, trace: list[dict[str, Any]]) -> ToolTurnResult:
        return ToolTurnResult("provider_error", provider_requests, tool_calls, reason, error={"code": reason, "message": reason.replace("_", " ")}, trace=trace)

    def _error(self, code: str, message: str, provider_requests: int, tool_calls: int, trace: list[dict[str, Any]]) -> ToolTurnResult:
        return ToolTurnResult("provider_error", provider_requests, tool_calls, code, error={"code": code, "message": message}, trace=trace)


def _initial_messages(specs: list[ToolSpec], campaign_identity: dict[str, str]) -> list[LLMMessage]:
    return [
        LLMMessage(role="system", content="Use only declared Harness tools. Submit one complete replacement build_sequence.py when ready. Tool results are bounded and path-free."),
        LLMMessage(role="user", content=_canonical({"campaign": campaign_identity, "tools": [{"name": spec.name, "description": spec.description, "schema": spec.schema} for spec in specs]})),
    ]


def _validate_campaign_identity(value: dict[str, str]) -> None:
    if set(value) != {"campaign_id", "campaign_spec_sha256"} or not all(isinstance(item, str) and item for item in value.values()):
        raise ValueError("campaign_identity must contain only frozen campaign_id and campaign_spec_sha256")


def campaign_identity_from_prepared_checkpoint(payload: dict[str, Any]) -> dict[str, str]:
    """Extract the only M139 identity fields that may enter the tool loop."""

    if payload.get("request_state") != "prepared" or payload.get("requests_used") != 0:
        raise ValueError("campaign checkpoint is not a fresh prepared identity")
    identity = {
        "campaign_id": payload.get("campaign_id"),
        "campaign_spec_sha256": payload.get("campaign_spec_sha256"),
    }
    _validate_campaign_identity(identity)  # type: ignore[arg-type]
    return identity  # type: ignore[return-value]


def _tool_payload(tool: str, result: dict[str, Any]) -> dict[str, Any]:
    return {"tool": tool, **result}


def _feedback(bundle: dict[str, Any]) -> dict[str, Any]:
    return {"status": bundle["status"], "execution": {key: bundle["execution"].get(key) for key in ("exit_code", "timed_out", "sandboxed", "sandbox_termination_reason")}, "gates": bundle["gates"], "repair_hints": bundle["repair_hints"]}


def _trace_entry(turn: int, kind: str, tool: str | None, payload: dict[str, Any]) -> dict[str, Any]:
    return {"turn": turn, "kind": kind, "tool": tool, "payload_sha256": sha256(_canonical(payload).encode("utf-8")).hexdigest(), "ok": payload.get("ok")}


def _write_turn_trace(path: Path, campaign_identity: dict[str, str], trace: list[dict[str, Any]], limits: ToolTurnLimits) -> None:
    write_json(path / "tool_turn_trace.json", {"schema_version": 1, "campaign": campaign_identity, "limits": vars(limits), "turns": trace})


def _copy_pending_trace(source: Path, destination: Path) -> None:
    for item in source.iterdir():
        if item.is_file():
            shutil.copy2(item, destination / item.name)


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
