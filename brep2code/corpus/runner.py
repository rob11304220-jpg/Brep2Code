"""Corpus runner built on the existing Harness-first loop."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from time import perf_counter

from brep2code.agent.harness import HarnessRunResult, ManualHarness
from brep2code.agent.provider import (
    DeepSeekProviderError,
    FakeLLMProvider,
    LLMMessage,
    LLMProvider,
    ProviderRequest,
    ProviderResponse,
    fake_replacement_response,
)
from brep2code.agent.repair import (
    ProviderRequestTimeoutError,
    RepairLoopResult,
    RepairLoopRunner,
    _complete_provider,
    _write_script_update,
    repair_result_to_dict,
)
from brep2code.agent.trace import append_llm_messages, write_provider_response_trace
from brep2code.brep.safe_probe import INPUT_PROBE_TIMEOUT_SECONDS, safe_probe_summary
from brep2code.cad import WslBubblewrapExecutor
from brep2code.corpus.manifest import CaseManifest
from brep2code.corpus.report import write_corpus_report


@dataclass(frozen=True)
class CorpusCaseResult:
    case_id: str
    tier: str
    record_id: str
    revision_id: str
    status: str
    gate_statuses: dict[str, str]
    failure_type: str | None
    signal_bundle_path: str
    probes: dict
    provenance: dict | None = None
    observation: dict | None = None
    repair: dict | None = None
    repair_failure_type: str | None = None
    primary_generation: dict | None = None
    fake_provider_replay: dict | None = None


@dataclass(frozen=True)
class CorpusRunResult:
    run_id: str
    manifest_path: str
    report_path: str | None
    cases: tuple[CorpusCaseResult, ...]
    summary: dict
    evaluation: dict | None = None
    run_status: str = "completed"
    interruption: dict | None = None
    generation_policy: dict | None = None


class CorpusRunner:
    """Execute manifest cases through ManualHarness and write a compact report."""

    def __init__(self, harness: ManualHarness | None = None) -> None:
        self.harness = harness or ManualHarness()

    def run(
        self,
        manifest: CaseManifest,
        *,
        record_prefix: str = "corpus",
        timeout: int = 60,
        repair: bool = False,
        report_path: Path | str | None = None,
        provider: LLMProvider | None = None,
        hosted_options: dict | None = None,
        first_pass: bool = False,
    ) -> CorpusRunResult:
        if provider is None and hosted_options is not None:
            raise ValueError("hosted_options requires an explicit provider")
        if provider is not None and hosted_options is None and not first_pass:
            raise ValueError("hosted provider requires explicit hosted_options")
        if hosted_options is not None and not isinstance(self.harness.executor, WslBubblewrapExecutor):
            raise ValueError("hosted provider evaluation requires WslBubblewrapExecutor")
        if hosted_options is not None and repair:
            raise ValueError("hosted provider evaluation cannot use local fake-provider --repair mode")
        if first_pass and provider is None:
            raise ValueError("first_pass requires an explicit provider")
        run_id = _run_id()
        results: list[CorpusCaseResult] = []
        selected_cases = manifest.cases if hosted_options is None else manifest.cases[: hosted_options["max_cases"]]
        requests_remaining = hosted_options["request_budget"] if hosted_options else 0
        current_case_id: str | None = None

        def checkpoint(*, run_status: str, interruption: dict | None = None) -> dict:
            payload = _report_payload(
                run_id,
                manifest,
                tuple(results),
                evaluation=_evaluation(provider, hosted_options, requests_remaining),
                run_status=run_status,
                interruption=interruption,
                first_pass=first_pass,
            )
            if report_path is not None:
                write_corpus_report(report_path, payload)
            return payload

        checkpoint(run_status="running")
        try:
            for case in selected_cases:
                current_case_id = case.case_id
                record_id = f"{record_prefix}-{case.case_id}"
                primary_generation = None
                if first_pass:
                    if hosted_options is not None and requests_remaining == 0:
                        generation = _generation_not_run(case.input_step)
                    else:
                        generation = self._generate_first_pass(
                            case_id=case.case_id,
                            record_id=record_id,
                            input_path=case.input_step,
                            provider=provider,
                            provider_timeout=hosted_options["provider_timeout"] if hosted_options else None,
                            first_pass_script=case.first_pass_script,
                        )
                    if generation["error"] is not None:
                        requests_remaining -= generation["provider_requests"]
                        results.append(_generation_error_case_result(case.case_id, case.tier, record_id, generation))
                        checkpoint(run_status="running")
                        continue
                    generated_path = generation["script_path"]
                    try:
                        harness_result = self.harness.run(
                            record_id=record_id,
                            script=generated_path,
                            input_path=case.input_step,
                            timeout=timeout,
                        )
                    finally:
                        generated_path.unlink(missing_ok=True)
                    _write_first_pass_trace(harness_result, generation)
                    requests_remaining -= generation["provider_requests"]
                    primary_generation = _primary_generation_payload(harness_result, generation)
                else:
                    harness_result = self.harness.run(
                        record_id=record_id,
                        input_path=case.input_step,
                        timeout=timeout,
                    )
                repair_payload = None
                fake_replay_payload = None
                if repair and case.reference_script is not None and harness_result.status != "pass":
                    repair_result = self._run_fake_repair(
                        record_id=record_id,
                        initial_result=harness_result,
                        reference_script=case.reference_script,
                        timeout=timeout,
                    )
                    if first_pass:
                        fake_replay_payload = repair_result_to_dict(repair_result)
                    else:
                        repair_payload = repair_result_to_dict(repair_result)
                elif hosted_options is not None and provider is not None and harness_result.status != "pass":
                    if _sandbox_unavailable(harness_result):
                        repair_payload = {
                            "status": "not_run",
                            "stop_reason": "sandbox_unavailable",
                            "error": {
                                "code": "sandbox_unavailable",
                                "message": "secure executor was unavailable before a hosted provider request",
                            },
                        }
                    elif requests_remaining == 0:
                        repair_payload = {
                            "status": "not_run",
                            "stop_reason": "request_budget_exhausted",
                            "error": {"code": "request_budget_exhausted", "message": "hosted request budget exhausted"},
                        }
                    else:
                        repair_result = self._run_provider_repair(
                            record_id=record_id,
                            initial_result=harness_result,
                            provider=provider,
                            max_rounds=min(hosted_options["max_rounds"], requests_remaining),
                            timeout=timeout,
                            provider_timeout=hosted_options["provider_timeout"],
                        )
                        repair_payload = repair_result_to_dict(repair_result)
                        requests_remaining -= repair_result.provider_requests
                results.append(
                    _case_result(
                        case.case_id,
                        case.tier,
                        record_id,
                        harness_result,
                        repair_payload,
                        primary_generation=primary_generation,
                        fake_provider_replay=fake_replay_payload,
                    )
                )
                checkpoint(run_status="running")
        except KeyboardInterrupt:
            payload = checkpoint(
                run_status="interrupted",
                interruption={"code": "keyboard_interrupt", "case_id": current_case_id},
            )
            raise
        except Exception as exc:
            payload = checkpoint(
                run_status="interrupted",
                interruption={"code": "runner_exception", "case_id": current_case_id, "exception_type": type(exc).__name__},
            )
            raise
        else:
            payload = checkpoint(run_status="completed")
        written_report = str(report_path) if report_path is not None else None
        return CorpusRunResult(
            run_id=run_id,
            manifest_path=str(manifest.path),
            report_path=written_report,
            cases=tuple(results),
            summary=payload["summary"],
            evaluation=payload.get("evaluation"),
            run_status=payload["run_status"],
            interruption=payload.get("interruption"),
            generation_policy=payload.get("generation_policy"),
        )

    def _generate_first_pass(
        self,
        *,
        case_id: str,
        record_id: str,
        input_path: Path,
        provider: LLMProvider | None,
        provider_timeout: int | None,
        first_pass_script: Path | None,
    ) -> dict:
        assert provider is not None
        started = perf_counter()
        summary = safe_probe_summary(input_path, timeout_seconds=INPUT_PROBE_TIMEOUT_SECONDS)
        if not summary.get("ok"):
            return _generation_preflight_error(summary, perf_counter() - started)
        provider_summary = _provider_probe_summary(summary)
        request = ProviderRequest(
            model=getattr(provider, "model", "fake-first-pass"),
            messages=[
                LLMMessage(
                    role="system",
                    content=(
                        "Generate build_sequence.py from the bounded B-Rep summary. "
                        "Runtime contract: the input STEP is available only at /input/model.step; "
                        "write the output STEP only to output/model.step; use installed OCP imports, "
                        "not OCC.Core; return one complete replacement build_sequence.py as the JSON "
                        "script_update, with no Markdown fence."
                    ),
                ),
                LLMMessage(
                    role="user",
                    content=json.dumps(
                        {"policy": "first-pass-summary-v1", "case_id": case_id, "probe_summary": provider_summary}
                    ),
                ),
            ],
            metadata={"record_id": record_id, "case_id": case_id, "policy": "first-pass-summary-v1"},
        )
        if isinstance(provider, FakeLLMProvider):
            assert first_pass_script is not None
            provider = FakeLLMProvider([fake_replacement_response(first_pass_script.read_text(encoding="utf-8"), model="fake-first-pass")])
        started = perf_counter()
        try:
            response = _complete_provider(provider, request, timeout_seconds=provider_timeout)
        except ProviderRequestTimeoutError as exc:
            return _generation_error(request, summary, "provider_request_timeout", str(exc), perf_counter() - started)
        except DeepSeekProviderError as exc:
            return _generation_error(request, summary, "provider_request_failed", str(exc), perf_counter() - started)
        if response.script_update is None or response.script_update.kind != "replace" or response.script_update.content is None:
            return _generation_error(
                request, summary, "missing_script_update", "provider returned no replacement build_sequence.py", perf_counter() - started
            )
        with NamedTemporaryFile("w", encoding="utf-8", suffix=".py", delete=False) as file:
            file.write(response.script_update.content)
            script_path = Path(file.name)
        return {
            "request": request,
            "response": response,
            "probe_summary": summary,
            "duration_seconds": perf_counter() - started,
            "provider_requests": 1,
            "script_path": script_path,
            "error": None,
        }

    def _run_fake_repair(
        self,
        *,
        record_id: str,
        initial_result: HarnessRunResult,
        reference_script: Path,
        timeout: int,
    ) -> RepairLoopResult:
        replacement = reference_script.read_text(encoding="utf-8")
        provider = FakeLLMProvider([fake_replacement_response(replacement)])
        runner = RepairLoopRunner(harness=self.harness, provider=provider)
        initial_script = initial_result.revision.workspace / "build_sequence.py"
        return runner.run(record_id, initial_script, max_rounds=1, timeout=timeout)

    def _run_provider_repair(
        self,
        *,
        record_id: str,
        initial_result: HarnessRunResult,
        provider: LLMProvider,
        max_rounds: int,
        timeout: int,
        provider_timeout: int,
    ) -> RepairLoopResult:
        runner = RepairLoopRunner(harness=self.harness, provider=provider)
        initial_script = initial_result.revision.workspace / "build_sequence.py"
        return runner.run(
            record_id,
            initial_script,
            max_rounds=max_rounds,
            timeout=timeout,
            provider_timeout=provider_timeout,
        )


def corpus_run_to_dict(result: CorpusRunResult) -> dict:
    first_pass = result.generation_policy is not None
    return {
        "schema_version": 3 if first_pass else (2 if result.evaluation is not None else 1),
        "run_id": result.run_id,
        "manifest": result.manifest_path,
        "report_path": result.report_path,
        "summary": result.summary,
        "run_status": result.run_status,
        "cases": [_case_dataclass_to_dict(case, first_pass=first_pass) for case in result.cases],
        **({"evaluation": result.evaluation} if result.evaluation is not None else {}),
        **({"generation_policy": result.generation_policy} if result.generation_policy is not None else {}),
        **({"interruption": result.interruption} if result.interruption is not None else {}),
    }


def _case_result(
    case_id: str,
    tier: str,
    record_id: str,
    result: HarnessRunResult,
    repair: dict | None,
    *,
    primary_generation: dict | None = None,
    fake_provider_replay: dict | None = None,
) -> CorpusCaseResult:
    gates = result.signal_bundle.get("gates", [])
    gate_statuses = {gate["name"]: gate["status"] for gate in gates}
    return CorpusCaseResult(
        case_id=case_id,
        tier=tier,
        record_id=record_id,
        revision_id=result.revision.revision_id,
        status=result.status,
        gate_statuses=gate_statuses,
        failure_type=_failure_type(result),
        signal_bundle_path=str(result.revision.signal_bundle),
        probes=result.signal_bundle.get("probes", {}),
        provenance=result.signal_bundle.get("provenance"),
        observation=result.signal_bundle.get("observation"),
        repair=repair,
        repair_failure_type=_repair_failure_type(repair),
        primary_generation=primary_generation,
        fake_provider_replay=fake_provider_replay,
    )


def _failure_type(result: HarnessRunResult) -> str | None:
    if result.status == "pass":
        return None
    gates = {gate["name"]: gate for gate in result.signal_bundle.get("gates", [])}
    if gates.get("script_exit_code", {}).get("status") == "fail":
        return "script_failure"
    if gates.get("output_model_step_exists", {}).get("status") == "fail":
        return "missing_output"
    if gates.get("output_model_step_readable", {}).get("status") == "fail":
        return "output_probe_failure"
    if result.signal_bundle.get("probes", {}).get("input_summary", {}).get("ok") is False:
        return "input_probe_failure"
    failed = [name for name, gate in gates.items() if gate.get("status") == "fail"]
    if failed:
        return "gate_failure"
    return "unknown_failure"


def _report_payload(
    run_id: str,
    manifest: CaseManifest,
    cases: tuple[CorpusCaseResult, ...],
    *,
    evaluation: dict | None,
    run_status: str,
    interruption: dict | None,
    first_pass: bool,
) -> dict:
    return {
        "schema_version": 3 if first_pass else (2 if evaluation is not None else 1),
        "run_id": run_id,
        "manifest": str(manifest.path),
        "run_status": run_status,
        "summary": _summary(cases),
        "cases": [_case_dataclass_to_dict(case, first_pass=first_pass) for case in cases],
        **({"evaluation": evaluation} if evaluation is not None else {}),
        **({"generation_policy": _generation_policy()} if first_pass else {}),
        **({"interruption": interruption} if interruption is not None else {}),
    }


def _summary(cases: tuple[CorpusCaseResult, ...]) -> dict:
    by_status: dict[str, int] = {}
    by_tier: dict[str, dict[str, int]] = {}
    by_failure_type: dict[str, int] = {}
    repair_statuses: dict[str, int] = {}
    repair_failure_types: dict[str, int] = {}
    for case in cases:
        by_status[case.status] = by_status.get(case.status, 0) + 1
        by_tier.setdefault(case.tier, {})
        by_tier[case.tier][case.status] = by_tier[case.tier].get(case.status, 0) + 1
        if case.failure_type is not None:
            by_failure_type[case.failure_type] = by_failure_type.get(case.failure_type, 0) + 1
        if case.repair is not None:
            repair_status = case.repair["status"]
            repair_statuses[repair_status] = repair_statuses.get(repair_status, 0) + 1
        if case.repair_failure_type is not None:
            repair_failure_types[case.repair_failure_type] = repair_failure_types.get(case.repair_failure_type, 0) + 1
    return {
        "total_cases": len(cases),
        "by_status": by_status,
        "by_tier": by_tier,
        "by_failure_type": by_failure_type,
        "repair": repair_statuses,
        "by_repair_failure_type": repair_failure_types,
    }


def _case_dataclass_to_dict(case: CorpusCaseResult, *, first_pass: bool = False) -> dict:
    payload = {
        "case_id": case.case_id,
        "tier": case.tier,
        "record_id": case.record_id,
        "revision_id": case.revision_id,
        "status": case.status,
        "gate_statuses": case.gate_statuses,
        "failure_type": case.failure_type,
        "signal_bundle_path": case.signal_bundle_path,
        "probes": case.probes,
        "provenance": case.provenance,
        "reconstruction_eligible": _reconstruction_eligible(case.provenance),
        "repair": case.repair,
        "repair_failure_type": case.repair_failure_type,
    }
    if first_pass:
        payload["observation"] = case.observation
        payload["primary_generation"] = case.primary_generation
        payload["fake_provider_replay"] = case.fake_provider_replay
    return payload


def _reconstruction_eligible(provenance: dict | None) -> bool:
    return bool(provenance and provenance.get("classification") == "independent_reconstruction")


def _repair_failure_type(repair: dict | None) -> str | None:
    if repair is None or repair.get("status") == "pass":
        return None
    error = repair.get("error") or {}
    code = error.get("code")
    if code == "request_budget_exhausted":
        return "repair_exhausted"
    if code == "sandbox_unavailable":
        return "sandbox"
    if code in {"provider_request_failed", "provider_request_timeout"}:
        return "provider_request"
    if code in {"missing_script_update", "unsupported_script_update"}:
        return "provider_response"
    if repair.get("stop_reason") == "max_rounds":
        return "repair_exhausted"
    return "unknown"


def _sandbox_unavailable(result: HarnessRunResult) -> bool:
    execution = result.signal_bundle.get("execution", {})
    event = execution.get("sandbox_event") or {}
    return execution.get("sandboxed") is not True or event.get("code") == "sandbox_unavailable"


def _evaluation(provider: LLMProvider | None, hosted_options: dict | None, requests_remaining: int) -> dict | None:
    if hosted_options is None:
        return None
    assert provider is not None
    return {
        "mode": "hosted",
        "provider": provider.name,
        "model": getattr(provider, "model", None),
        "repair_policy": "repair-loop-v1",
        "executor": "wsl-bwrap",
        "authorization": hosted_options["authorization"],
        "max_cases": hosted_options["max_cases"],
        "max_rounds": hosted_options["max_rounds"],
        "request_budget": hosted_options["request_budget"],
        "provider_timeout_seconds": hosted_options["provider_timeout"],
        "requests_used": hosted_options["request_budget"] - requests_remaining,
    }


def _run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def _generation_error(request: ProviderRequest, summary: dict, code: str, message: str, duration_seconds: float) -> dict:
    return {
        "request": request,
        "response": None,
        "probe_summary": summary,
        "duration_seconds": duration_seconds,
        "provider_requests": 1,
        "script_path": None,
        "error": {"code": code, "message": message},
    }


def _generation_not_run(input_path: Path) -> dict:
    started = perf_counter()
    summary = safe_probe_summary(input_path, timeout_seconds=INPUT_PROBE_TIMEOUT_SECONDS)
    if not summary.get("ok"):
        return _generation_preflight_error(summary, perf_counter() - started)
    return {
        "request": None,
        "response": None,
        "probe_summary": summary,
        "duration_seconds": 0.0,
        "provider_requests": 0,
        "script_path": None,
        "error": {"code": "request_budget_exhausted", "message": "hosted request budget exhausted before first pass"},
    }


def _generation_preflight_error(summary: dict, duration_seconds: float) -> dict:
    error = summary.get("error", {})
    return {
        "request": None,
        "response": None,
        "probe_summary": summary,
        "duration_seconds": duration_seconds,
        "provider_requests": 0,
        "script_path": None,
        "error": {
            "code": "input_probe_failure",
            "message": error.get("message", "B-Rep input summary was unavailable before generation."),
        },
    }


def _write_first_pass_trace(result: HarnessRunResult, generation: dict) -> None:
    trace_dir = result.revision.traces
    append_llm_messages(trace_dir, generation["request"].messages, direction="request")
    response = generation["response"]
    assert isinstance(response, ProviderResponse)
    append_llm_messages(trace_dir, [LLMMessage(role="assistant", content=response.output_text)], direction="response")
    write_provider_response_trace(trace_dir, response)
    assert response.script_update is not None
    _write_script_update(trace_dir, response.script_update)


def _primary_generation_payload(result: HarnessRunResult, generation: dict) -> dict:
    return {
        "status": result.status,
        "revision_id": result.revision.revision_id,
        "signal_bundle_path": str(result.revision.signal_bundle),
        "gate_statuses": {gate["name"]: gate["status"] for gate in result.signal_bundle.get("gates", [])},
        "failure_type": _failure_type(result),
        "provider_requests": generation["provider_requests"],
        "duration_seconds": generation["duration_seconds"],
        "probe_summary": generation["probe_summary"],
    }


def _generation_error_case_result(case_id: str, tier: str, record_id: str, generation: dict) -> CorpusCaseResult:
    error = generation["error"]
    assert error is not None
    error_code = error["code"]
    status = "not_run" if error_code in {"request_budget_exhausted", "input_probe_failure"} else "provider_error"
    failure_type = "generation_exhausted" if error_code == "request_budget_exhausted" else (
        "input_probe_failure" if error_code == "input_probe_failure" else "provider_request"
    )
    primary_generation = {
        "status": status,
        "revision_id": None,
        "signal_bundle_path": None,
        "gate_statuses": {},
        "failure_type": failure_type,
        "provider_requests": generation["provider_requests"],
        "duration_seconds": generation["duration_seconds"],
        "probe_summary": generation["probe_summary"],
        "error": error,
    }
    return CorpusCaseResult(
        case_id=case_id,
        tier=tier,
        record_id=record_id,
        revision_id="",
        status=primary_generation["status"],
        gate_statuses={},
        failure_type=primary_generation["failure_type"],
        signal_bundle_path="",
        probes={"input_summary": generation["probe_summary"]},
        primary_generation=primary_generation,
    )


def _generation_policy() -> dict:
    return {"id": "first-pass-summary-v1", "probe_context": "probe_summary", "provider_response": "replace-script-only"}


def _provider_probe_summary(summary: dict) -> dict:
    """Return the geometry summary allowed to leave the local workspace."""
    allowed = ("ok", "file_name", "format", "unit", "bbox", "counts", "area", "volume")
    return {key: summary[key] for key in allowed if key in summary}
