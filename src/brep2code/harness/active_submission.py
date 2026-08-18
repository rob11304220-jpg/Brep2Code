from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from brep2code.cases import ValidatedCase
from brep2code.execution import ExecutionResult, SandboxUnavailable, run_untrusted_build
from brep2code.geometry.gates import GateDispatchError, GateReport, dispatch_gates
from brep2code.geometry.inspect import GeometryMetrics, inspect_step
from brep2code.geometry.observe import observe_step
from brep2code.harness.active import (
    ActiveBudgets,
    ActiveCheckpoint,
    ActiveHarnessController,
    ActiveHarnessResult,
    ActiveResumeState,
    ActiveState,
    SubmissionAborted,
    SubmissionResult,
)
from brep2code.harness.compatibility import validate_script_compatibility
from brep2code.harness.active_results import ActiveResultValidationError, validate_active_result
from brep2code.harness.verification import gate_oracles, geometry_feedback, required_gates
from brep2code.providers.action_protocol import ActionProvider


Executor = Callable[..., ExecutionResult]
Inspector = Callable[[Path], GeometryMetrics]
Observer = Callable[[Path], dict[str, Any]]
GateDispatcher = Callable[..., GateReport]
SubmissionFactory = Callable[[ValidatedCase, Path, int], Callable[..., SubmissionResult]]


class ActiveSubmissionVerifier:
    """Persist, securely execute, and verify each active Harness submission."""

    def __init__(
        self,
        case: ValidatedCase,
        run_root: Path,
        timeout_seconds: int,
        *,
        executor: Executor = run_untrusted_build,
        inspector: Inspector = inspect_step,
        observer: Observer = observe_step,
        gate_dispatcher: GateDispatcher = dispatch_gates,
        starting_submission: int = 0,
    ) -> None:
        if timeout_seconds < 1:
            raise ValueError("timeout_seconds must be positive")
        if not run_root.is_dir():
            raise ValueError("active run root must already exist")
        self.case = case
        self.run_root = run_root
        self.timeout_seconds = timeout_seconds
        self.executor = executor
        self.inspector = inspector
        self.observer = observer
        self.gate_dispatcher = gate_dispatcher
        self.target_observations = observe_step(case.case.input_step)
        if starting_submission < 0:
            raise ValueError("starting_submission must be non-negative")
        self.submissions = starting_submission

    def __call__(self, script: str, *, execution_allowed: bool = True) -> SubmissionResult:
        revision_id = f"revision-{self.submissions:03d}"
        self.submissions += 1
        workspace = self.run_root / revision_id
        workspace.mkdir()
        (workspace / "build.py").write_text(script, encoding="utf-8")
        artifact: dict[str, Any] = {
            "revision_id": revision_id,
            "status": "created",
            "workspace": revision_id,
        }

        if self.submissions > 1:
            previous_script = (
                self.run_root / f"revision-{self.submissions - 2:03d}" / "build.py"
            ).read_text(encoding="utf-8")
            if script == previous_script:
                feedback = {
                    "stage": "generation",
                    "reason": "unchanged_revision",
                    "message": (
                        "The repair submission is identical to the failed revision; "
                        "change the complete script to address typed feedback or retrieve "
                        "an allowlisted OCP reference before resubmitting."
                    ),
                }
                artifact.update(status="failed", feedback=feedback)
                _write_json(workspace / "result.json", artifact)
                return SubmissionResult(False, feedback)

        feedback = validate_script_compatibility(script)
        if feedback is not None:
            artifact.update(status="failed", feedback=feedback)
            _write_json(workspace / "result.json", artifact)
            return SubmissionResult(False, feedback)

        if not execution_allowed:
            artifact.update(
                status="budget_exhausted",
                error={"stage": "budget", "scope": "execution"},
            )
            _write_json(workspace / "result.json", artifact)
            raise SubmissionAborted("execution_budget", "execution budget exhausted")
        artifact["status"] = "execution"
        _write_json(workspace / "result.json", artifact)
        try:
            execution = self.executor(workspace, timeout_seconds=self.timeout_seconds)
        except SandboxUnavailable as exc:
            artifact.update(
                status="failed",
                error={"stage": "sandbox", "message": str(exc)},
            )
            _write_json(workspace / "result.json", artifact)
            raise SubmissionAborted("sandbox_unavailable", str(exc), executed=True) from exc
        artifact["execution"] = _execution_artifact(execution)
        if execution.output_step is None:
            feedback = {
                "stage": "execution",
                "exit_code": execution.exit_code,
                "timed_out": execution.timed_out,
                "termination_reason": execution.termination_reason,
                "stderr": execution.stderr[-2000:],
            }
            artifact.update(status="failed", feedback=feedback)
            _write_json(workspace / "result.json", artifact)
            return SubmissionResult(False, feedback, executed=True)

        artifact["status"] = "validation"
        _write_json(workspace / "result.json", artifact)
        try:
            metrics = self.inspector(execution.output_step)
            report = self.gate_dispatcher(
                metrics,
                self.case.metadata["expected"],
                required_gates(self.case),
                observations=self.observer(execution.output_step),
                gate_oracles=gate_oracles(self.case),
            )
            signals = report.as_signal_bundle()
        except (FileNotFoundError, GateDispatchError, ValueError) as exc:
            feedback = {"stage": "validation", "error": str(exc)}
            artifact.update(status="failed", feedback=feedback)
            _write_json(workspace / "result.json", artifact)
            return SubmissionResult(False, feedback, executed=True)
        artifact["signals"] = asdict(signals)
        artifact["gates"] = report.as_dict()
        if signals.passed:
            artifact["status"] = "succeeded"
            _write_json(workspace / "result.json", artifact)
            return SubmissionResult(True, executed=True)
        feedback = geometry_feedback(metrics, self.target_observations, signals)
        artifact.update(status="failed", feedback=feedback)
        _write_json(workspace / "result.json", artifact)
        return SubmissionResult(False, feedback, executed=True)


class ActiveHarnessRunner:
    def __init__(
        self,
        provider: ActionProvider,
        *,
        submission_factory: SubmissionFactory | None = None,
    ) -> None:
        self.provider = provider
        self.submission_factory = submission_factory or _submission_factory

    def run(
        self,
        case: ValidatedCase,
        run_root: Path,
        *,
        budgets: ActiveBudgets,
        timeout_seconds: int = 30,
    ) -> ActiveHarnessResult:
        run_root.mkdir(parents=True, exist_ok=False)
        submit = self.submission_factory(case, run_root, timeout_seconds)
        return self._run_controller(
            case,
            run_root,
            budgets,
            timeout_seconds,
            submit,
            checkpoint_index=0,
        )

    def continue_run(
        self,
        case: ValidatedCase,
        run_root: Path,
        *,
        budgets: ActiveBudgets,
        timeout_seconds: int,
    ) -> ActiveHarnessResult:
        result_path = run_root / "result.json"
        payload = _read_json(result_path)
        validate_active_result(payload, case, run_root)
        if payload["terminal"] or not payload["continuation_policy"]["eligible"]:
            raise ActiveResultValidationError("active result is not eligible for continuation")
        if payload["provider"] != self.provider.name or payload["model"] != self.provider.model:
            raise ActiveResultValidationError("active continuation provider/model drift")
        if payload["budgets"] != asdict(budgets):
            raise ActiveResultValidationError("active continuation budget drift")
        if payload["timeout_seconds"] != timeout_seconds:
            raise ActiveResultValidationError("active continuation timeout drift")
        restore_accounting = getattr(self.provider, "restore_accounting", None)
        if payload["schema_version"] == 4:
            if not callable(restore_accounting):
                raise ActiveResultValidationError(
                    "active continuation provider cannot restore accounting"
                )
            restore_accounting(payload["provider_accounting"])
        resume = _resume_state(payload, run_root, budgets)
        starting_submission = int(resume.usage["script_submissions"])
        submit = self.submission_factory(case, run_root, timeout_seconds)
        if isinstance(submit, ActiveSubmissionVerifier):
            submit.submissions = starting_submission
        elif starting_submission:
            raise ActiveResultValidationError(
                "active continuation submission factory cannot restore revision index"
            )
        return self._run_controller(
            case,
            run_root,
            budgets,
            timeout_seconds,
            submit,
            checkpoint_index=payload["checkpoint_index"] + 1,
            resume=resume,
        )

    def _run_controller(
        self,
        case: ValidatedCase,
        run_root: Path,
        budgets: ActiveBudgets,
        timeout_seconds: int,
        submit: Callable[..., SubmissionResult],
        *,
        checkpoint_index: int,
        resume: ActiveResumeState | None = None,
    ) -> ActiveHarnessResult:
        accounting_snapshot = getattr(self.provider, "accounting_snapshot", None)
        set_accounting_checkpoint = getattr(
            self.provider, "set_accounting_checkpoint", None
        )
        hosted_accounting = callable(accounting_snapshot)
        latest_snapshot: ActiveCheckpoint | None = None

        def write_checkpoint(
            snapshot: ActiveCheckpoint, provider_accounting: dict[str, Any] | None = None
        ) -> None:
            nonlocal checkpoint_index
            terminal = snapshot.stop_reason is not None
            if hosted_accounting and provider_accounting is None:
                provider_accounting = accounting_snapshot()
            checkpoint_usage = dict(snapshot.usage)
            if provider_accounting is not None:
                checkpoint_usage["tokens"] = provider_accounting["tokens"]["total"]
                checkpoint_usage["cost_usd"] = provider_accounting["cost_usd"]
            payload = {
                "schema_version": 4 if hosted_accounting else 3,
                "mode": "active",
                "case_id": case.case.case_id,
                "provider": self.provider.name,
                "model": self.provider.model,
                "budgets": asdict(budgets),
                "timeout_seconds": timeout_seconds,
                "checkpoint_index": checkpoint_index,
                "terminal": terminal,
                "continuation_policy": {
                    "eligible": not terminal,
                    "implemented": True,
                    "requirements": [
                        "same_case",
                        "same_budgets",
                        "remaining_model_requests",
                        "existing_revision_root",
                    ],
                },
                "state": snapshot.state,
                "stop_reason": snapshot.stop_reason,
                "usage": checkpoint_usage,
                "trace": snapshot.trace,
            }
            if hosted_accounting:
                payload["provider_accounting"] = provider_accounting
            _write_json(
                run_root / "result.json",
                payload,
            )
            checkpoint_index += 1

        def checkpoint(snapshot: ActiveCheckpoint) -> None:
            nonlocal latest_snapshot
            latest_snapshot = snapshot
            write_checkpoint(snapshot)

        def provider_checkpoint(provider_accounting: dict[str, Any]) -> None:
            if latest_snapshot is not None:
                write_checkpoint(latest_snapshot, provider_accounting)

        if hosted_accounting:
            if not callable(set_accounting_checkpoint):
                raise ActiveResultValidationError(
                    "hosted active provider cannot checkpoint accounting"
                )
            set_accounting_checkpoint(provider_checkpoint)
        try:
            return ActiveHarnessController(self.provider).run(
                case, budgets, submit, checkpoint=checkpoint, resume=resume
            )
        finally:
            if hosted_accounting:
                set_accounting_checkpoint(None)


def _submission_factory(
    case: ValidatedCase, run_root: Path, timeout_seconds: int
) -> ActiveSubmissionVerifier:
    return ActiveSubmissionVerifier(case, run_root, timeout_seconds)


def _execution_artifact(execution: ExecutionResult) -> dict[str, Any]:
    return {
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


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    temporary.replace(path)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ActiveResultValidationError("active continuation result is unreadable") from exc
    if not isinstance(payload, dict):
        raise ActiveResultValidationError("active continuation result must be an object")
    return payload


def _resume_state(
    payload: dict[str, Any], run_root: Path, budgets: ActiveBudgets
) -> ActiveResumeState:
    usage = dict(payload["usage"])
    trace = list(payload["trace"])
    state = ActiveState(payload["state"])
    revision_count = int(usage["script_submissions"])
    current_revision = None
    if revision_count:
        latest = run_root / f"revision-{revision_count - 1:03d}"
        current_revision = (latest / "build.py").read_text(encoding="utf-8")
        revision = _read_json(latest / "result.json")
        if state is ActiveState.EXECUTING and revision.get("status") == "execution":
            usage["executions"] += 1
    if usage["executions"] > budgets.executions:
        raise ActiveResultValidationError("active continuation execution budget exhausted")
    if usage["model_requests"] >= budgets.model_requests:
        raise ActiveResultValidationError("active continuation has no remaining model requests")
    if state is ActiveState.SYNTHESIZING:
        trace.append({"action": "provider", "state": "interrupted"})
    elif state is ActiveState.PROBING:
        trace.append({"action": "probe", "state": "interrupted"})
    elif state is ActiveState.RETRIEVING:
        trace.append({"action": "retrieve", "state": "interrupted"})
    elif state is ActiveState.EXECUTING:
        trace.append(
            {
                "action": "submit",
                "state": "interrupted",
                "passed": None,
                "feedback": None,
            }
        )
    feedback = next(
        (
            item.get("feedback")
            for item in reversed(trace)
            if item.get("action") == "submit"
            and item.get("passed") is False
            and isinstance(item.get("feedback"), dict)
        ),
        None,
    )
    if state is ActiveState.EXECUTING:
        feedback = {
            "stage": "interruption",
            "state": "executing",
            "message": "The previous submission outcome is unknown; resubmit if needed.",
        }
    return ActiveResumeState(state, usage, tuple(trace), current_revision, feedback)
