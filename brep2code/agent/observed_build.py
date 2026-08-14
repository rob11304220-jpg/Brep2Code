"""Offline Q01-observation to Q02-build loop using a deterministic fake provider."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile, TemporaryDirectory
from time import perf_counter
from typing import Callable

from brep2code.agent.harness import HarnessRunResult, ManualHarness
from brep2code.agent.guidance import GuidanceBundle, GuidanceCardBridge, TOOL_NAME
from brep2code.agent.observation import build_observation_context
from brep2code.agent.provider import FakeLLMProvider, LLMMessage, LLMProvider, ProviderRequest
from brep2code.agent.repair import (
    ProviderRequestLifecycleError,
    ProviderRequestTimeoutError,
    RepairLoopResult,
    RepairLoopRunner,
    _complete_provider,
    _write_script_update,
)
from brep2code.agent.tools import BRepToolBridge
from brep2code.agent.trace import append_llm_messages, write_provider_response_trace
from brep2code.cad import WslBubblewrapExecutor
from brep2code.storage.store import write_json


@dataclass(frozen=True)
class ObservationCall:
    call_id: str
    tool: str
    arguments: dict | None = None


@dataclass(frozen=True)
class ObservedBuildResult:
    status: str
    harness_result: HarnessRunResult | None
    provider_requests: int
    error: dict | None = None
    repair: RepairLoopResult | None = None
    telemetry: dict = field(default_factory=dict)


class ObservedBuildLoopRunner:
    """Run one offline provider generation from bounded observations only."""

    def __init__(
        self,
        *,
        harness: ManualHarness,
        provider: LLMProvider,
        bridge: BRepToolBridge | None = None,
        allow_hosted: bool = False,
    ) -> None:
        if not isinstance(provider, FakeLLMProvider):
            if not allow_hosted:
                raise ValueError("ObservedBuildLoopRunner requires explicit allow_hosted for a non-fake provider")
            if not isinstance(harness.executor, WslBubblewrapExecutor):
                raise ValueError("non-fake observed builds require WslBubblewrapExecutor")
        self.harness = harness
        self.provider = provider
        self.bridge = bridge or BRepToolBridge(store=harness.store)

    def run(
        self,
        record_id: str,
        *,
        input_path: Path,
        observation_session_id: str,
        observation_calls: list[ObservationCall],
        observation_context: str | None = None,
        timeout: int = 60,
        provider_timeout: int | None = None,
        max_output_tokens: int | None = None,
        max_repair_rounds: int = 0,
        guidance_bundle: GuidanceBundle | None = None,
        required_guidance_role: str | None = None,
        direct_guidance: dict | None = None,
        before_provider_request: Callable[[], None] | None = None,
    ) -> ObservedBuildResult:
        if max_output_tokens is not None and (
            not isinstance(max_output_tokens, int)
            or isinstance(max_output_tokens, bool)
            or max_output_tokens < 1
        ):
            raise ValueError("max_output_tokens must be a positive integer")
        overall_started = perf_counter()
        record = self.harness.store.ensure_record(record_id)
        input_prepare_started = perf_counter()
        self.harness._prepare_input(record, input_path)
        input_prepare_ms = _elapsed_ms(input_prepare_started)
        with TemporaryDirectory(prefix="brep2code-observation-") as temporary:
            query_trace = Path(temporary)
            observation_started = perf_counter()
            if observation_context is None:
                envelopes = [
                    self.bridge.observe(
                        record_id,
                        observation_session_id,
                        call.call_id,
                        call.tool,
                        call.arguments,
                        trace_dir=query_trace,
                    )
                    for call in observation_calls
                ]
                context = build_observation_context(envelopes)
            else:
                payload = json.loads(observation_context)
                envelopes = payload.get("observation_transcript") if isinstance(payload, dict) else None
                if not isinstance(envelopes, list):
                    raise ValueError("observation_context must contain an observation transcript")
                context = build_observation_context(envelopes)
            observation_ms = _elapsed_ms(observation_started)
            system_instruction = (
                "Generate one complete build_sequence.py from the bounded observation transcript. "
                "The build has no input STEP mount; write only output/model.step. "
                "Use only installed OCP modules and symbols; never cadquery, OCC.Core, or invented OCP names."
            )
            request = ProviderRequest(
                model=getattr(self.provider, "model", "fake-observation-build"),
                messages=[
                    LLMMessage(
                        role="system",
                        content=system_instruction,
                    ),
                    LLMMessage(role="user", content=context),
                ],
                max_output_tokens=max_output_tokens,
                metadata={"policy": "q01-observation-build-v1", "record_id": record_id},
            )
            telemetry = _telemetry_base(
                system_instruction=system_instruction,
                observation_context=context,
                input_prepare_ms=input_prepare_ms,
                observation_ms=observation_ms,
            )
            guidance_result = None
            guidance_request = None
            guidance_response = None
            if direct_guidance is not None:
                if guidance_bundle is None or required_guidance_role is None:
                    raise ValueError("direct_guidance requires a guidance bundle and declared role")
                bridge = GuidanceCardBridge("pending", guidance_bundle)
                direct = bridge.call(TOOL_NAME, {"role": required_guidance_role})
                if not direct.ok or direct.result != direct_guidance:
                    raise ValueError("direct_guidance does not match the frozen guidance bundle")
                request = ProviderRequest(
                    model=getattr(self.provider, "model", "fake-observation-build"),
                    messages=[
                        LLMMessage(role="system", content=system_instruction),
                        LLMMessage(role="user", content=context),
                        LLMMessage(role="tool", name=TOOL_NAME, content=json.dumps(direct_guidance, sort_keys=True)),
                    ],
                    max_output_tokens=max_output_tokens,
                    metadata={"policy": "q01-observation-build-v1", "record_id": record_id, "guidance_mode": "direct"},
                )
                telemetry["context_ledger"]["message_count"] = 3
                telemetry["context_ledger"]["sections"]["guidance_card"] = _content_counts(request.messages[-1].content)
            if guidance_bundle is not None and direct_guidance is None:
                if required_guidance_role is None:
                    raise ValueError("required_guidance_role is required with guidance_bundle")
                guidance_request = ProviderRequest(
                    model=getattr(self.provider, "model", "fake-guidance"),
                    messages=[
                        LLMMessage(role="system", content="Request exactly one bounded guidance card; do not generate code."),
                        LLMMessage(role="user", content=context),
                    ],
                    max_output_tokens=max_output_tokens,
                    metadata={"policy": "m85-reference-assisted-v1", "phase": "guidance_request", "record_id": record_id, "required_guidance_role": required_guidance_role},
                )
                if before_provider_request is not None:
                    before_provider_request()
                guidance_response = _complete_provider(self.provider, guidance_request, timeout_seconds=provider_timeout)
                call = guidance_response.tool_call
                if call is None or call.tool != TOOL_NAME or call.arguments != {"role": required_guidance_role}:
                    return ObservedBuildResult(status="provider_error", harness_result=None, provider_requests=1, error={"code": "invalid_guidance_tool_call", "message": "first response must request the fixed guidance card"}, telemetry=telemetry)
                guidance_result = GuidanceCardBridge("pending", guidance_bundle).call(call.tool, call.arguments, trace_dir=query_trace)
                if not guidance_result.ok or guidance_result.result is None:
                    return ObservedBuildResult(status="provider_error", harness_result=None, provider_requests=1, error=guidance_result.error, telemetry=telemetry)
                request = ProviderRequest(model=getattr(self.provider, "model", "fake-observation-build"), messages=[LLMMessage(role="system", content=system_instruction), LLMMessage(role="user", content=context), LLMMessage(role="tool", name=TOOL_NAME, content=json.dumps(guidance_result.result, sort_keys=True))], max_output_tokens=max_output_tokens, metadata={"policy": "m85-reference-assisted-v1", "phase": "script_generation", "record_id": record_id})
                telemetry["context_ledger"]["message_count"] = 3
                telemetry["context_ledger"]["sections"]["guidance_card"] = _content_counts(request.messages[-1].content)

            provider_started = perf_counter()
            telemetry["request_timing"]["send_offset_ms"] = _elapsed_ms(overall_started)
            try:
                if before_provider_request is not None:
                    before_provider_request()
                response = _complete_provider(self.provider, request, timeout_seconds=provider_timeout)
            except (ProviderRequestTimeoutError, ProviderRequestLifecycleError) as exc:
                telemetry["phase_elapsed_ms"]["provider_wait"] = _elapsed_ms(provider_started)
                telemetry["phase_elapsed_ms"]["end_to_end"] = _elapsed_ms(overall_started)
                setattr(exc, "telemetry", telemetry)
                raise
            telemetry["phase_elapsed_ms"]["provider_wait"] = _elapsed_ms(provider_started)
            telemetry["request_timing"]["done_offset_ms"] = _elapsed_ms(overall_started)
            first_response_byte_elapsed_ms = response.raw_summary.get("first_response_byte_elapsed_ms")
            if isinstance(first_response_byte_elapsed_ms, int) and not isinstance(first_response_byte_elapsed_ms, bool):
                telemetry["request_timing"]["first_byte_offset_ms"] = (
                    telemetry["request_timing"]["send_offset_ms"] + first_response_byte_elapsed_ms
                )
            if response.script_update is None or response.script_update.kind != "replace" or response.script_update.content is None:
                telemetry["phase_elapsed_ms"]["harness"] = None
                telemetry["phase_elapsed_ms"]["end_to_end"] = _elapsed_ms(overall_started)
                return ObservedBuildResult(
                    status="provider_error",
                    harness_result=None,
                    provider_requests=1,
                    error={"code": "missing_script_update", "message": "provider returned no replacement script"},
                    telemetry=telemetry,
                )
            with NamedTemporaryFile("w", encoding="utf-8", suffix=".py", delete=False) as generated:
                generated.write(response.script_update.content)
                script_path = Path(generated.name)
            try:
                harness_started = perf_counter()
                result = self.harness.run(
                    record_id,
                    script=script_path,
                    timeout=timeout,
                    build_without_input=True,
                    observation_envelopes=envelopes,
                )
                telemetry["phase_elapsed_ms"]["harness"] = _elapsed_ms(harness_started)
            finally:
                script_path.unlink(missing_ok=True)

            trace_dir = result.revision.traces
            query_path = query_trace / "observation_queries.jsonl"
            if query_path.exists():
                shutil.copy2(query_path, trace_dir / query_path.name)
            if guidance_result is not None:
                guidance_trace = query_trace / "guidance_calls.jsonl"
                if guidance_trace.exists():
                    payload = guidance_trace.read_text(encoding="utf-8").replace('"revision_id": "pending"', f'"revision_id": "{result.revision.revision_id}"')
                    (trace_dir / "guidance_calls.jsonl").write_text(payload, encoding="utf-8")
                result.signal_bundle["guidance"] = {
                    "enabled": True,
                    "index_sha256": guidance_bundle.index_sha256,
                    "selected_role": required_guidance_role,
                    "returned_card_ids": [guidance_result.result["id"]],
                    "calls": [{"tool": TOOL_NAME, "ok": True, "card_id": guidance_result.result["id"], "error": None}],
                }
                write_json(result.revision.signal_bundle, result.signal_bundle)
            if guidance_request is not None and guidance_response is not None:
                append_llm_messages(trace_dir, guidance_request.messages, direction="request")
                append_llm_messages(trace_dir, [LLMMessage(role="assistant", content=guidance_response.output_text)], direction="response")
            append_llm_messages(trace_dir, request.messages, direction="request")
            append_llm_messages(trace_dir, [LLMMessage(role="assistant", content=response.output_text)], direction="response")
            write_provider_response_trace(trace_dir, response)
            _write_script_update(trace_dir, response.script_update)
            repair = None
            if result.status != "pass" and max_repair_rounds:
                repair = RepairLoopRunner(harness=self.harness, provider=self.provider).run(
                    record_id,
                    result.revision.workspace / "build_sequence.py",
                    max_rounds=max_repair_rounds,
                    timeout=timeout,
                    provider_timeout=provider_timeout,
                    build_without_input=True,
                    observation_only=True,
                )
            telemetry["phase_elapsed_ms"]["end_to_end"] = _elapsed_ms(overall_started)
            return ObservedBuildResult(
                status=repair.status if repair is not None else result.status,
                harness_result=result,
                provider_requests=(2 if guidance_result is not None else 1) + (repair.provider_requests if repair is not None else 0),
                repair=repair,
                telemetry=telemetry,
            )


def _telemetry_base(*, system_instruction: str, observation_context: str, input_prepare_ms: int, observation_ms: int) -> dict:
    """Return a content-free request/context ledger; character counts are not tokens."""

    return {
        "schema_version": 1,
        "request_timing": {
            "send_offset_ms": None,
            "first_byte_offset_ms": None,
            "done_offset_ms": None,
            "token_usage": None,
        },
        "context_ledger": {
            "message_count": 2,
            "sections": {
                "system_instruction": _content_counts(system_instruction),
                "observation_transcript": _content_counts(observation_context),
            },
        },
        "phase_elapsed_ms": {
            "input_prepare": input_prepare_ms,
            "observation": observation_ms,
            "provider_wait": None,
            "harness": None,
            "end_to_end": None,
        },
    }


def _content_counts(content: str) -> dict:
    return {"chars": len(content), "utf8_bytes": len(content.encode("utf-8"))}


def _elapsed_ms(started: float) -> int:
    return int((perf_counter() - started) * 1000)
