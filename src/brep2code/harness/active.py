from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

from brep2code.cases import ValidatedCase
from brep2code.providers.action_protocol import ActionProvider, ActionRequest
from brep2code.tools import ToolError, dispatch_tool


class ActionContractError(ValueError):
    pass


class SubmissionAborted(RuntimeError):
    def __init__(self, stop_reason: str, message: str, *, executed: bool = False) -> None:
        super().__init__(message)
        self.stop_reason = stop_reason
        self.executed = executed


class ActiveState(StrEnum):
    OBSERVING = "observing"
    PROBING = "probing"
    RETRIEVING = "retrieving"
    SYNTHESIZING = "synthesizing"
    EXECUTING = "executing"
    VERIFYING = "verifying"
    REPAIRING = "repairing"
    SUCCEEDED = "succeeded"
    EXHAUSTED = "exhausted"
    FAILED = "failed"


class RetrievalPolicy(StrEnum):
    DISABLED = "disabled"
    BOUNDED_SEED = "bounded_seed"


@dataclass(frozen=True)
class ActiveBudgets:
    model_requests: int
    probes: int
    retrievals: int
    script_submissions: int
    executions: int
    repairs: int
    tokens: int
    cost_usd: float

    def __post_init__(self) -> None:
        integer_values = (
            self.model_requests,
            self.probes,
            self.retrievals,
            self.script_submissions,
            self.executions,
            self.repairs,
            self.tokens,
        )
        if any(not isinstance(value, int) or isinstance(value, bool) for value in integer_values):
            raise ValueError("active Harness budgets must be integers")
        if any(value < 0 for value in integer_values) or self.model_requests < 1:
            raise ValueError("active Harness budgets must be non-negative")
        if not isinstance(self.cost_usd, (int, float)) or isinstance(self.cost_usd, bool):
            raise ValueError("active Harness cost budget must be numeric")
        if self.cost_usd < 0:
            raise ValueError("active Harness cost budget must be non-negative")


@dataclass(frozen=True)
class SubmissionResult:
    passed: bool
    feedback: dict[str, Any] | None = None
    executed: bool = False

    def __post_init__(self) -> None:
        if self.passed and self.feedback is not None:
            raise ValueError("a passed submission cannot include repair feedback")
        if self.passed and not self.executed:
            raise ValueError("a passed submission must have been executed and verified")
        if not self.passed and not isinstance(self.feedback, dict):
            raise ValueError("a failed submission requires typed feedback")


@dataclass(frozen=True)
class ActiveHarnessResult:
    state: ActiveState
    stop_reason: str
    usage: dict[str, int | float]
    trace: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class ActiveCheckpoint:
    state: ActiveState
    stop_reason: str | None
    usage: dict[str, int | float]
    trace: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class ActiveResumeState:
    state: ActiveState
    usage: dict[str, int | float]
    trace: tuple[dict[str, Any], ...]
    current_revision: str | None
    feedback: dict[str, Any] | None


@dataclass(frozen=True)
class HarnessAction:
    name: str
    payload: dict[str, Any]

    @classmethod
    def parse(cls, value: dict[str, Any]) -> HarnessAction:
        if not isinstance(value, dict):
            raise ActionContractError("action response must be an object")
        name = value.get("action")
        if name not in {"probe", "retrieve", "submit", "finish"}:
            raise ActionContractError("action must be probe, retrieve, submit, or finish")
        if set(value) != {"action", name}:
            raise ActionContractError(f"{name} action fields are invalid")
        payload = value[name]
        if not isinstance(payload, dict):
            raise ActionContractError(f"{name} payload must be an object")
        validators = {
            "probe": _validate_probe,
            "retrieve": _validate_retrieve,
            "submit": _validate_submit,
            "finish": _validate_finish,
        }
        validators[name](payload)
        return cls(name=name, payload=payload)


class ActiveHarnessController:
    def __init__(self, provider: ActionProvider) -> None:
        self.provider = provider

    def run(
        self,
        case: ValidatedCase,
        budgets: ActiveBudgets,
        submit: Callable[..., SubmissionResult],
        checkpoint: Callable[[ActiveCheckpoint], None] | None = None,
        resume: ActiveResumeState | None = None,
        retrieval_policy: RetrievalPolicy = RetrievalPolicy.BOUNDED_SEED,
    ) -> ActiveHarnessResult:
        if retrieval_policy is RetrievalPolicy.DISABLED and budgets.retrievals != 0:
            raise ValueError("disabled retrieval policy requires zero retrieval budget")
        initial = dispatch_tool("brep_observations", case)
        usage: dict[str, int | float] = (
            dict(resume.usage)
            if resume is not None
            else {name: 0.0 if name == "cost_usd" else 0 for name in asdict(budgets)}
        )
        trace: list[dict[str, Any]] = list(resume.trace) if resume is not None else []
        current_revision = resume.current_revision if resume is not None else None
        feedback = resume.feedback if resume is not None else None

        def notify(state: ActiveState, stop_reason: str | None = None) -> None:
            if checkpoint is not None:
                checkpoint(ActiveCheckpoint(state, stop_reason, dict(usage), tuple(trace)))

        def finish(state: ActiveState, stop_reason: str) -> ActiveHarnessResult:
            result = _active_result(state, stop_reason, usage, trace)
            notify(state, stop_reason)
            return result

        notify(resume.state if resume is not None else ActiveState.OBSERVING)

        while usage["model_requests"] < budgets.model_requests:
            request = ActionRequest(
                case_id=case.case.case_id,
                turn_index=usage["model_requests"],
                session={
                    "case_id": case.case.case_id,
                    "unit": case.metadata["unit"],
                    "initial_observations": initial["brep"],
                    "available_tools": (
                        ["edge_candidates"]
                        if retrieval_policy is RetrievalPolicy.DISABLED
                        else ["edge_candidates", "knowledge_search", "ocp_symbol"]
                    ),
                    "retrieval_policy": retrieval_policy,
                    "budgets": _budget_snapshot(budgets, usage),
                    "current_revision": current_revision,
                    "feedback": feedback,
                    "tool_results": [
                        item for item in trace if item["action"] in {"probe", "retrieve"}
                    ],
                },
            )
            usage["model_requests"] += 1
            notify(ActiveState.SYNTHESIZING)
            try:
                response = self.provider.choose_action(request)
            except RuntimeError as exc:
                trace.append({"action": "provider", "error": str(exc)})
                return finish(ActiveState.FAILED, "provider_error")
            try:
                accounting_error = _account_usage(response.usage, budgets, usage)
            except ActionContractError as exc:
                trace.append({"action": "provider", "error": str(exc)})
                return finish(ActiveState.FAILED, "provider_error")
            if accounting_error is not None:
                return finish(ActiveState.EXHAUSTED, accounting_error)
            notify(ActiveState.SYNTHESIZING)
            try:
                action = HarnessAction.parse(response.action)
            except ActionContractError as exc:
                trace.append({"action": "provider", "error": str(exc)})
                return finish(ActiveState.FAILED, "provider_error")

            if action.name == "probe":
                if not _consume("probes", budgets, usage):
                    return finish(ActiveState.EXHAUSTED, "probe_budget")
                notify(ActiveState.PROBING)
                try:
                    result = dispatch_tool(
                        action.payload["tool"], case, action.payload["arguments"]
                    )
                except ToolError as exc:
                    trace.append({"action": "probe", "error": str(exc)})
                    return finish(ActiveState.FAILED, "tool_error")
                trace.append(
                    {
                        "action": "probe",
                        "state": ActiveState.PROBING,
                        "request": action.payload,
                        "result": result,
                    }
                )
                notify(ActiveState.PROBING)
                continue

            if action.name == "retrieve":
                if retrieval_policy is RetrievalPolicy.DISABLED:
                    trace.append(
                        {
                            "action": "provider",
                            "error": "retrieve action is disabled by harness policy",
                        }
                    )
                    return finish(ActiveState.FAILED, "harness_policy")
                if not _consume("retrievals", budgets, usage):
                    return finish(ActiveState.EXHAUSTED, "retrieval_budget")
                notify(ActiveState.RETRIEVING)
                try:
                    tool_name = "ocp_symbol" if "topic" in action.payload else "knowledge_search"
                    tool_arguments = (
                        {"topic": action.payload["topic"]}
                        if tool_name == "ocp_symbol"
                        else {
                            key: action.payload[key]
                            for key in ("query", "scope", "limit")
                            if key in action.payload
                        }
                    )
                    result = dispatch_tool(tool_name, case, tool_arguments)
                except ToolError as exc:
                    trace.append({"action": "retrieve", "error": str(exc)})
                    return finish(ActiveState.FAILED, "tool_error")
                trace.append(
                    {
                        "action": "retrieve",
                        "state": ActiveState.RETRIEVING,
                        "request": action.payload,
                        "result": result,
                    }
                )
                notify(ActiveState.RETRIEVING)
                continue

            if action.name == "finish":
                trace.append({"action": "finish", "request": action.payload})
                return finish(ActiveState.FAILED, "finish_without_verifier")

            if not _consume("script_submissions", budgets, usage):
                return finish(ActiveState.EXHAUSTED, "submission_budget")
            current_revision = action.payload["script"]
            notify(ActiveState.EXECUTING)
            try:
                submission = submit(
                    current_revision,
                    execution_allowed=usage["executions"] < budgets.executions,
                )
            except SubmissionAborted as exc:
                if exc.executed:
                    usage["executions"] += 1
                trace.append(
                    {
                        "action": "submit",
                        "state": ActiveState.FAILED,
                        "error": str(exc),
                    }
                )
                state = (
                    ActiveState.EXHAUSTED
                    if exc.stop_reason == "execution_budget"
                    else ActiveState.FAILED
                )
                return finish(state, exc.stop_reason)
            if submission.executed:
                usage["executions"] += 1
            trace.append(
                {
                    "action": "submit",
                    "state": (
                        ActiveState.SUCCEEDED if submission.passed else ActiveState.REPAIRING
                    ),
                    "passed": submission.passed,
                    "feedback": submission.feedback,
                }
            )
            if submission.passed:
                return finish(ActiveState.SUCCEEDED, "passed")
            if not _consume("repairs", budgets, usage):
                return finish(ActiveState.EXHAUSTED, "repair_budget")
            feedback = submission.feedback
            notify(ActiveState.REPAIRING)

        return finish(ActiveState.EXHAUSTED, "model_request_budget")


def _validate_probe(payload: dict[str, Any]) -> None:
    if set(payload) != {"tool", "arguments"}:
        raise ActionContractError("probe requires tool and arguments")
    if payload["tool"] != "edge_candidates" or not isinstance(payload["arguments"], dict):
        raise ActionContractError("probe tool must be edge_candidates with object arguments")


def _validate_retrieve(payload: dict[str, Any]) -> None:
    if set(payload) == {"topic"} and isinstance(payload["topic"], str) and payload["topic"]:
        return
    allowed = {"query", "scope", "limit"}
    if "query" not in payload or set(payload) - allowed:
        raise ActionContractError("retrieve requires a topic or query projection")
    if not isinstance(payload["query"], str) or not payload["query"]:
        raise ActionContractError("retrieve query must be a non-empty string")
    if "scope" in payload and (
        not isinstance(payload["scope"], list)
        or any(not isinstance(scope, str) or not scope for scope in payload["scope"])
    ):
        raise ActionContractError("retrieve scope must be a string array")
    if "limit" in payload and (
        not isinstance(payload["limit"], int) or isinstance(payload["limit"], bool)
        or not 1 <= payload["limit"] <= 5
    ):
        raise ActionContractError("retrieve limit must be between 1 and 5")


def _validate_submit(payload: dict[str, Any]) -> None:
    if set(payload) != {"script"} or not isinstance(payload["script"], str) or not payload["script"]:
        raise ActionContractError("submit requires one non-empty script")


def _validate_finish(payload: dict[str, Any]) -> None:
    if set(payload) != {"reason"} or not isinstance(payload["reason"], str):
        raise ActionContractError("finish requires one string reason")


def _consume(name: str, budgets: ActiveBudgets, usage: dict[str, int | float]) -> bool:
    if usage[name] >= getattr(budgets, name):
        return False
    usage[name] += 1
    return True


def _budget_snapshot(
    budgets: ActiveBudgets, usage: dict[str, int | float]
) -> dict[str, dict[str, int | float]]:
    return {
        name: {"used": usage[name], "limit": limit, "remaining": limit - usage[name]}
        for name, limit in asdict(budgets).items()
    }


def _active_result(
    state: ActiveState,
    stop_reason: str,
    usage: dict[str, int | float],
    trace: list[dict[str, Any]],
) -> ActiveHarnessResult:
    return ActiveHarnessResult(state, stop_reason, dict(usage), tuple(trace))


def _account_usage(
    reported: dict[str, int | float] | None,
    budgets: ActiveBudgets,
    usage: dict[str, int | float],
) -> str | None:
    if reported is None:
        return None
    total_tokens = reported.get("total_tokens", 0)
    cost_usd = reported.get("cost_usd", 0.0)
    if not isinstance(total_tokens, int) or isinstance(total_tokens, bool) or total_tokens < 0:
        raise ActionContractError("provider total_tokens usage must be a non-negative integer")
    if not isinstance(cost_usd, (int, float)) or isinstance(cost_usd, bool) or cost_usd < 0:
        raise ActionContractError("provider cost_usd usage must be non-negative")
    usage["tokens"] += total_tokens
    usage["cost_usd"] += float(cost_usd)
    if usage["tokens"] > budgets.tokens:
        return "token_budget"
    if usage["cost_usd"] > budgets.cost_usd:
        return "cost_budget"
    return None
