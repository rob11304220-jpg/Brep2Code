from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

from brep2code.cases import ValidatedCase
from brep2code.domain import RunStatus
from brep2code.execution import SandboxUnavailable, run_untrusted_build
from brep2code.geometry.gates import GateDispatchError, dispatch_gates
from brep2code.geometry.inspect import inspect_step
from brep2code.geometry.observe import observe_step
from brep2code.harness.compatibility import validate_script_compatibility
from brep2code.harness.verification import gate_oracles, geometry_feedback, required_gates
from brep2code.providers import ProviderBudgetError
from brep2code.providers.protocol import Provider, ProviderRequest
from brep2code.tools import dispatch_tool


@dataclass(frozen=True)
class HarnessResult:
    status: str
    stop_reason: str
    provider_requests: int
    result_path: Path


class RepairLoopRunner:
    def __init__(self, provider: Provider) -> None:
        self.provider = provider

    def run(
        self,
        case: ValidatedCase,
        run_root: Path,
        *,
        max_rounds: int,
        timeout_seconds: int = 30,
        initial_script: str | None = None,
        campaign: dict[str, Any] | None = None,
    ) -> HarnessResult:
        if max_rounds < 1:
            raise ValueError("max_rounds must be at least 1")
        model_context = dispatch_tool("brep_observations", case)
        run_root.mkdir(parents=True, exist_ok=False)
        result_path = run_root / "result.json"
        payload: dict[str, Any] = {
            "schema_version": 1,
            "case_id": case.case.case_id,
            "mechanism": case.metadata["mechanism"],
            "capability_level": case.metadata["capability_level"],
            "provider": self.provider.name,
            "model": self.provider.model,
            "max_rounds": max_rounds,
            "has_initial_script": initial_script is not None,
            "provider_requests": 0,
            "status": RunStatus.CREATED,
            "stop_reason": None,
            "revisions": [],
        }
        if campaign is not None:
            payload["campaign"] = campaign
        limits = getattr(self.provider, "limits", None)
        if limits is not None:
            payload["provider_limits"] = asdict(limits)
            payload["accounting_scope"] = getattr(limits, "scope", "provider")
            payload["provider_accounting"] = _provider_accounting(self.provider)
        _write_checkpoint(result_path, payload)
        feedback = None
        previous_script = None

        for index in range(max_rounds):
            revision_id = f"revision-{index:03d}"
            workspace = run_root / revision_id
            workspace.mkdir()
            revision: dict[str, Any] = {
                "index": index,
                "revision_id": revision_id,
                "source": (
                    "initial_script"
                    if index == 0 and initial_script is not None
                    else "provider"
                ),
                "status": RunStatus.CREATED,
                "workspace": revision_id,
            }
            payload["revisions"].append(revision)
            if index == 0 and initial_script is not None:
                script = initial_script
            else:
                revision["status"] = RunStatus.MODEL_CALL
                payload["status"] = RunStatus.MODEL_CALL
                _write_checkpoint(result_path, payload)
                request = ProviderRequest(
                    case_id=case.case.case_id,
                    round_index=index,
                    context=model_context,
                    feedback=feedback,
                    previous_script=previous_script,
                )
                payload["provider_requests"] += 1
                try:
                    response = self.provider.generate(request)
                except ProviderBudgetError as exc:
                    if "provider_accounting" in payload:
                        payload["provider_accounting"] = _provider_accounting(self.provider)
                    revision["status"] = RunStatus.BUDGET_EXHAUSTED
                    revision["error"] = {
                        "stage": "budget",
                        "scope": exc.scope,
                        "message": str(exc),
                    }
                    payload["status"] = RunStatus.BUDGET_EXHAUSTED
                    payload["stop_reason"] = "provider_budget"
                    _write_checkpoint(result_path, payload)
                    return _result(payload, result_path)
                except RuntimeError as exc:
                    if "provider_accounting" in payload:
                        payload["provider_accounting"] = _provider_accounting(self.provider)
                    revision["status"] = RunStatus.FAILED
                    revision["error"] = {"stage": "provider", "message": str(exc)}
                    payload["status"] = RunStatus.FAILED
                    payload["stop_reason"] = "provider_error"
                    _write_checkpoint(result_path, payload)
                    return _result(payload, result_path)
                if "provider_accounting" in payload:
                    payload["provider_accounting"] = _provider_accounting(self.provider)
                (workspace / "request.json").write_text(
                    json.dumps(asdict(request), indent=2), encoding="utf-8"
                )
                (workspace / "response.json").write_text(
                    json.dumps(
                        {
                            "provider": response.provider,
                            "model": response.model,
                            "usage": response.usage,
                        },
                        indent=2,
                    ),
                    encoding="utf-8",
                )
                script = response.script
            (workspace / "build.py").write_text(script, encoding="utf-8")
            previous_script = script

            compatibility_feedback = validate_script_compatibility(script)
            if compatibility_feedback is not None:
                feedback = compatibility_feedback
                revision["status"] = RunStatus.FAILED
                revision["feedback"] = compatibility_feedback
                payload["status"] = RunStatus.FAILED
                _write_checkpoint(result_path, payload)
                continue

            revision["status"] = RunStatus.EXECUTION
            payload["status"] = RunStatus.EXECUTION
            _write_checkpoint(result_path, payload)
            try:
                execution = run_untrusted_build(workspace, timeout_seconds=timeout_seconds)
            except SandboxUnavailable as exc:
                revision["status"] = RunStatus.FAILED
                revision["error"] = {"stage": "sandbox", "message": str(exc)}
                payload["status"] = RunStatus.FAILED
                payload["stop_reason"] = "sandbox_unavailable"
                _write_checkpoint(result_path, payload)
                return _result(payload, result_path)
            revision["execution"] = {
                "exit_code": execution.exit_code,
                "stdout": execution.stdout,
                "stderr": execution.stderr,
                "duration_seconds": execution.duration_seconds,
                "timed_out": execution.timed_out,
                "sandboxed": execution.sandboxed,
                "sandbox_backend": execution.sandbox_backend,
                "termination_reason": execution.termination_reason,
                "output_step": "output.step" if execution.output_step else None,
            }
            if execution.output_step is None:
                feedback = {
                    "stage": "execution",
                    "exit_code": execution.exit_code,
                    "timed_out": execution.timed_out,
                    "termination_reason": execution.termination_reason,
                    "stderr": execution.stderr[-2000:],
                }
                revision["status"] = RunStatus.FAILED
                revision["feedback"] = feedback
                payload["status"] = RunStatus.FAILED
                _write_checkpoint(result_path, payload)
                continue

            revision["status"] = RunStatus.VALIDATION
            payload["status"] = RunStatus.VALIDATION
            _write_checkpoint(result_path, payload)
            try:
                metrics = inspect_step(execution.output_step)
                gate_report = dispatch_gates(
                    metrics,
                    case.metadata["expected"],
                    required_gates(case),
                    observations=observe_step(execution.output_step),
                    gate_oracles=gate_oracles(case),
                )
                signals = gate_report.as_signal_bundle()
            except (FileNotFoundError, GateDispatchError, ValueError) as exc:
                feedback = {"stage": "validation", "error": str(exc)}
                revision["status"] = RunStatus.FAILED
                revision["feedback"] = feedback
                payload["status"] = RunStatus.FAILED
                _write_checkpoint(result_path, payload)
                continue
            revision["signals"] = asdict(signals)
            revision["gates"] = gate_report.as_dict()
            if signals.passed:
                revision["status"] = RunStatus.SUCCEEDED
                payload["status"] = RunStatus.SUCCEEDED
                payload["stop_reason"] = "passed"
                _write_checkpoint(result_path, payload)
                return _result(payload, result_path)
            feedback = geometry_feedback(metrics, model_context["brep"], signals)
            revision["status"] = RunStatus.FAILED
            revision["feedback"] = feedback
            payload["status"] = RunStatus.FAILED
            _write_checkpoint(result_path, payload)

        payload["status"] = RunStatus.BUDGET_EXHAUSTED
        payload["stop_reason"] = "max_rounds"
        _write_checkpoint(result_path, payload)
        return _result(payload, result_path)


def _result(payload: dict[str, Any], path: Path) -> HarnessResult:
    return HarnessResult(
        status=str(payload["status"]),
        stop_reason=str(payload["stop_reason"]),
        provider_requests=int(payload["provider_requests"]),
        result_path=path,
    )


def _write_checkpoint(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    temporary.replace(path)


def _provider_accounting(provider: Provider) -> dict[str, int | float]:
    requests_issued = getattr(provider, "requests_issued", None)
    if requests_issued is None:
        requests_issued = len(getattr(provider, "requests", ()))
    return {
        "http_attempts": int(requests_issued),
        "total_tokens": int(getattr(provider, "total_tokens", 0)),
        "cost_usd": float(getattr(provider, "cost_usd", 0.0)),
    }
