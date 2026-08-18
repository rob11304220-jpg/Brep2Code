from pathlib import Path

import pytest

from brep2code.cases import validate_case
from brep2code.harness import (
    ActionContractError,
    ActiveBudgets,
    ActiveHarnessController,
    ActiveState,
    HarnessAction,
    SubmissionResult,
)
from brep2code.providers import ActionResponse, FakeActionProvider


def _budgets(**overrides: int) -> ActiveBudgets:
    values = {
        "model_requests": 5,
        "probes": 1,
        "retrievals": 1,
        "script_submissions": 2,
        "executions": 2,
        "repairs": 1,
        "tokens": 100,
        "cost_usd": 1.0,
    }
    values.update(overrides)
    return ActiveBudgets(**values)


def test_action_contract_rejects_extra_or_mismatched_fields() -> None:
    with pytest.raises(ActionContractError, match="fields are invalid"):
        HarnessAction.parse(
            {"action": "submit", "submit": {"script": "pass"}, "reason": "extra"}
        )
    with pytest.raises(ActionContractError, match="probe tool"):
        HarnessAction.parse(
            {"action": "probe", "probe": {"tool": "read_repository", "arguments": {}}}
        )


def test_active_harness_runs_deterministic_probe_retrieve_repair_sequence() -> None:
    case = validate_case(Path("cases/train/filleted_box"), Path("cases"))
    provider = FakeActionProvider(
        [
            {"action": "probe", "probe": {"tool": "edge_candidates", "arguments": {}}},
            {"action": "retrieve", "retrieve": {"topic": "TopoDS.Edge_s"}},
            {"action": "submit", "submit": {"script": "candidate"}},
            {"action": "submit", "submit": {"script": "repair"}},
        ]
    )
    submissions = iter(
        [
            SubmissionResult(
                False, {"stage": "geometry", "code": "volume_mismatch"}, executed=True
            ),
            SubmissionResult(True, executed=True),
        ]
    )

    result = ActiveHarnessController(provider).run(
        case, _budgets(), lambda _, **__: next(submissions)
    )

    assert result.state is ActiveState.SUCCEEDED
    assert result.stop_reason == "passed"
    assert result.usage == {
        "model_requests": 4,
        "probes": 1,
        "retrievals": 1,
        "script_submissions": 2,
        "executions": 2,
        "repairs": 1,
        "tokens": 0,
        "cost_usd": 0.0,
    }
    assert [item["action"] for item in result.trace] == [
        "probe",
        "retrieve",
        "submit",
        "submit",
    ]
    final_request = provider.requests[-1]
    assert final_request.session["current_revision"] == "candidate"
    assert final_request.session["feedback"] == {
        "stage": "geometry",
        "code": "volume_mismatch",
    }
    assert [item["action"] for item in final_request.session["tool_results"]] == [
        "probe",
        "retrieve",
    ]
    serialized = repr(final_request.session)
    assert "input.step" not in serialized
    assert str(case.case.root) not in serialized


def test_active_harness_stops_at_each_independent_budget() -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))
    provider = FakeActionProvider(
        [{"action": "probe", "probe": {"tool": "edge_candidates", "arguments": {}}}]
    )

    result = ActiveHarnessController(provider).run(
        case, _budgets(probes=0), lambda _, **__: SubmissionResult(True, executed=True)
    )

    assert result.state is ActiveState.EXHAUSTED
    assert result.stop_reason == "probe_budget"
    assert result.usage["model_requests"] == 1
    assert result.usage["probes"] == 0


def test_finish_cannot_bypass_verifier() -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))
    provider = FakeActionProvider(
        [{"action": "finish", "finish": {"reason": "looks correct"}}]
    )

    result = ActiveHarnessController(provider).run(
        case, _budgets(), lambda _, **__: SubmissionResult(True, executed=True)
    )

    assert result.state is ActiveState.FAILED
    assert result.stop_reason == "finish_without_verifier"


def test_malformed_action_usage_is_still_accounted() -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))

    class MalformedProvider:
        name = "fake"
        model = "malformed"

        def choose_action(self, request):
            return ActionResponse(
                provider=self.name,
                model=self.model,
                action={"action": "invalid"},
                usage={"total_tokens": 7, "cost_usd": 0.25},
            )

    result = ActiveHarnessController(MalformedProvider()).run(
        case, _budgets(), lambda _, **__: SubmissionResult(True, executed=True)
    )

    assert result.state is ActiveState.FAILED
    assert result.stop_reason == "provider_error"
    assert result.usage["tokens"] == 7
    assert result.usage["cost_usd"] == 0.25
