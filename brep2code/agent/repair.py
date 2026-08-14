"""Bounded fake-provider repair loop runner."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import multiprocessing as mp
from pathlib import Path
from queue import Empty
import time

from brep2code.agent.harness import HarnessRunResult, ManualHarness
from brep2code.agent.provider import (
    DeepSeekProvider,
    DeepSeekProviderError,
    LLMMessage,
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
    ScriptUpdate,
)
from brep2code.agent.trace import append_llm_messages, write_provider_response_trace
from brep2code.storage.store import write_json


_HTTP_TIMEOUT_GRACE_SECONDS = 5


@dataclass(frozen=True)
class RepairAttempt:
    revision_id: str
    status: str
    signal_bundle_path: str


@dataclass(frozen=True)
class RepairLoopResult:
    status: str
    attempts: list[RepairAttempt]
    stop_reason: str
    error: dict | None = None
    provider_requests: int = 0


class RepairLoopRunner:
    """Runs a finite provider-driven repair loop without mutating old revisions."""

    def __init__(self, harness: ManualHarness | None = None, provider: LLMProvider | None = None) -> None:
        self.harness = harness or ManualHarness()
        if provider is None:
            raise ValueError("RepairLoopRunner requires an explicit provider")
        self.provider = provider

    def run(
        self,
        record_id: str,
        initial_script: Path,
        *,
        input_path: Path | None = None,
        max_rounds: int = 1,
        timeout: int = 60,
        provider_timeout: int | None = None,
        build_without_input: bool = False,
        observation_only: bool = False,
    ) -> RepairLoopResult:
        if max_rounds < 0:
            raise ValueError("max_rounds must be >= 0")
        if provider_timeout is not None and provider_timeout < 1:
            raise ValueError("provider_timeout must be >= 1")

        attempts: list[RepairAttempt] = []
        provider_requests = 0
        current_script = initial_script
        current_input = input_path
        last_result: HarnessRunResult | None = None

        for round_index in range(max_rounds + 1):
            run_result = self.harness.run(
                record_id,
                script=current_script,
                timeout=timeout,
                input_path=current_input,
                build_without_input=build_without_input,
            )
            current_input = None
            last_result = run_result
            attempts.append(_attempt(run_result))
            if run_result.status == "pass":
                return RepairLoopResult(
                    status="pass",
                    attempts=attempts,
                    stop_reason="pass",
                    provider_requests=provider_requests,
                )
            if round_index == max_rounds:
                break

            request = ProviderRequest(
                model=getattr(self.provider, "model", "fake-repair"),
                messages=[
                    LLMMessage(role="system", content="Repair build_sequence.py using the harness feedback."),
                    LLMMessage(role="user", content=_repair_context(run_result, observation_only=observation_only)),
                ],
                metadata={"record_id": record_id, "revision_id": run_result.revision.revision_id},
            )
            append_llm_messages(run_result.revision.traces, request.messages, direction="request")
            try:
                provider_requests += 1
                response = _complete_provider(self.provider, request, timeout_seconds=provider_timeout)
            except ProviderRequestTimeoutError as exc:
                return RepairLoopResult(
                    status="provider_error",
                    attempts=attempts,
                    stop_reason="provider_request_timeout",
                    error={"code": "provider_request_timeout", "message": str(exc), "diagnostics": exc.diagnostics},
                    provider_requests=provider_requests,
                )
            except DeepSeekProviderError as exc:
                diagnostics = getattr(exc, "diagnostics", None)
                return RepairLoopResult(
                    status="provider_error",
                    attempts=attempts,
                    stop_reason="provider_request_failed",
                    error={
                        "code": "provider_request_failed",
                        "message": str(exc),
                        **({"diagnostics": diagnostics} if diagnostics is not None else {}),
                    },
                    provider_requests=provider_requests,
                )
            append_llm_messages(
                run_result.revision.traces,
                [LLMMessage(role="assistant", content=response.output_text)],
                direction="response",
            )
            write_provider_response_trace(run_result.revision.traces, response)

            script_update = response.script_update
            if script_update is None:
                return RepairLoopResult(
                    status="provider_error",
                    attempts=attempts,
                    stop_reason="missing_script_update",
                    error={"code": "missing_script_update", "message": "provider returned no script update"},
                    provider_requests=provider_requests,
                )
            applied = _write_script_update(run_result.revision.traces, script_update)
            if applied is None:
                return RepairLoopResult(
                    status="provider_error",
                    attempts=attempts,
                    stop_reason="unsupported_script_update",
                    error={
                        "code": "unsupported_script_update",
                        "message": f"unsupported script update kind: {script_update.kind}",
                    },
                    provider_requests=provider_requests,
                )
            current_script = applied

        assert last_result is not None
        return RepairLoopResult(
            status="fail",
            attempts=attempts,
            stop_reason="max_rounds",
            provider_requests=provider_requests,
        )


def repair_result_to_dict(result: RepairLoopResult) -> dict:
    return asdict(result)


def _attempt(result: HarnessRunResult) -> RepairAttempt:
    return RepairAttempt(
        revision_id=result.revision.revision_id,
        status=result.status,
        signal_bundle_path=str(result.revision.signal_bundle),
    )


def _repair_context(result: HarnessRunResult, *, observation_only: bool = False) -> str:
    revision = result.revision
    bundle = result.signal_bundle
    context = {
        "record_id": result.record.record_id,
        "revision_id": revision.revision_id,
        "build_sequence": _read_text(revision.workspace / "build_sequence.py"),
        "execution": bundle.get("execution", {}),
        "input_summary": bundle.get("probes", {}).get("input_summary"),
        "gates": bundle.get("gates", []),
        "repair_hints": bundle.get("repair_hints", []),
        "stdout_preview": _read_text(revision.traces / "stdout.txt", limit=2000),
        "stderr_preview": _read_text(revision.traces / "stderr.txt", limit=2000),
    }
    if observation_only:
        context.pop("record_id", None)
        context.pop("input_summary", None)
        context = _without_paths(context)
    return json.dumps(context, indent=2, ensure_ascii=False)


def _without_paths(value):
    """Remove local-path-bearing fields before an observation-only repair request."""
    forbidden = {
        "command",
        "content_path",
        "context_path",
        "cwd",
        "file_name",
        "input",
        "path",
        "provenance_trace_path",
        "stderr_path",
        "stdout_path",
        "trace_path",
    }
    if isinstance(value, dict):
        return {key: _without_paths(item) for key, item in value.items() if key not in forbidden}
    if isinstance(value, list):
        return [_without_paths(item) for item in value]
    return value


def _read_text(path: Path, *, limit: int = 12_000) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    return text if len(text) <= limit else text[:limit] + "\n...[truncated]"


def _write_script_update(trace_dir: Path, script_update: ScriptUpdate) -> Path | None:
    if script_update.kind != "replace" or script_update.content is None:
        return None
    path = trace_dir / "provider_build_sequence.py"
    path.write_text(script_update.content, encoding="utf-8")
    write_json(
        trace_dir / "script_update.json",
        {
            "kind": script_update.kind,
            "path": script_update.path,
            "content_path": str(path),
        },
    )
    return path


def _complete_provider(
    provider: LLMProvider,
    request: ProviderRequest,
    *,
    timeout_seconds: int | None,
) -> ProviderResponse:
    """Bound a hosted HTTP request without changing deterministic fake-provider semantics."""

    if not isinstance(provider, DeepSeekProvider):
        return provider.complete(request)
    timeout = timeout_seconds or provider.timeout_seconds
    # Keep a return path for a sanitized worker error even for the minimum
    # accepted provider timeout; the normal 120-second setting retains 5s.
    grace_seconds = min(_HTTP_TIMEOUT_GRACE_SECONDS, timeout / 2)
    http_timeout = timeout - grace_seconds
    worker_provider = DeepSeekProvider(
        api_key=provider.api_key,
        model=provider.model,
        base_url=provider.base_url,
        timeout_seconds=http_timeout,
    )
    context = mp.get_context("spawn")
    result_queue = context.Queue()
    process = context.Process(target=_deepseek_complete_worker, args=(worker_provider, request, result_queue))
    try:
        process.start()
    except Exception as exc:
        raise ProviderRequestLifecycleError(
            "DeepSeek request worker could not start",
            diagnostics=_lifecycle_diagnostics([], error_class=type(exc).__name__),
        ) from exc
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        process.join()
        raise ProviderRequestTimeoutError(
            f"DeepSeek request exceeded the {timeout}-second provider timeout",
            diagnostics=_timeout_diagnostics(result_queue),
        )
    try:
        status, payload, events = _worker_outcome(result_queue)
    except Empty as exc:
        raise ProviderRequestLifecycleError(
            "DeepSeek request worker returned no response",
            diagnostics=_lifecycle_diagnostics([], error_class="WorkerNoResponse"),
        ) from exc
    if status == "error":
        raise ProviderRequestLifecycleError(
            str(payload["message"]),
            diagnostics=_lifecycle_diagnostics(
                events,
                error_class=str(payload["error_class"]),
            ),
        )
    return payload


def _deepseek_complete_worker(provider: DeepSeekProvider, request: ProviderRequest, result_queue) -> None:
    started = time.monotonic()
    result_queue.put(("phase", {"phase": "worker_started", "elapsed_ms": 0}))
    try:
        result_queue.put(("phase", {"phase": "http_started", "elapsed_ms": _elapsed_ms(started)}))
        response = provider.complete(
            request,
            on_first_response_byte=lambda elapsed_ms: result_queue.put(
                ("phase", {"phase": "http_first_response_byte", "elapsed_ms": elapsed_ms})
            ),
        )
        result_queue.put(("phase", {"phase": "http_response_completed", "elapsed_ms": _elapsed_ms(started)}))
        result_queue.put(("response", response))
    except DeepSeekProviderError as exc:
        result_queue.put(("phase", {"phase": "http_failed", "elapsed_ms": _elapsed_ms(started)}))
        result_queue.put(("error", {"error_class": type(exc).__name__, "message": str(exc)}))
    except Exception as exc:  # pragma: no cover - defensive process boundary
        result_queue.put(("phase", {"phase": "worker_failed", "elapsed_ms": _elapsed_ms(started)}))
        result_queue.put(("error", {"error_class": type(exc).__name__, "message": "provider worker failed"}))


def _elapsed_ms(started: float) -> int:
    return int((time.monotonic() - started) * 1000)


def _timeout_diagnostics(result_queue) -> dict:
    return _lifecycle_diagnostics(_drain_phase_events(result_queue), error_class="ProviderRequestTimeoutError")


def _drain_phase_events(result_queue) -> list[dict]:
    events: list[dict] = []
    get_nowait = getattr(result_queue, "get_nowait", None)
    if get_nowait is not None:
        while True:
            try:
                status, payload = get_nowait()
            except Empty:
                break
            if status == "phase":
                events.append(payload)
    return events


def _lifecycle_diagnostics(events: list[dict], *, error_class: str) -> dict:
    last = events[-1]["phase"] if events else "worker_phase_unobserved"
    return {"last_phase": last, "events": events, "error_class": error_class}


def _worker_outcome(result_queue):
    events: list[dict] = []
    while True:
        status, payload = result_queue.get(timeout=1)
        if status == "phase":
            events.append(payload)
            continue
        return status, payload, events


class ProviderRequestTimeoutError(DeepSeekProviderError):
    """Raised when the parent terminates a hosted provider worker after its deadline."""

    def __init__(self, message: str, *, diagnostics: dict | None = None) -> None:
        super().__init__(message)
        self.diagnostics = diagnostics or {}


class ProviderRequestLifecycleError(DeepSeekProviderError):
    """Raised when a worker returns a sanitized lifecycle failure."""

    def __init__(self, message: str, *, diagnostics: dict) -> None:
        super().__init__(message)
        self.diagnostics = diagnostics
