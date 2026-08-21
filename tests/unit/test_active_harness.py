from pathlib import Path

import pytest

from brep2code.cases import validate_case
from brep2code.harness import (
    ActionContractError,
    ActiveBudgets,
    ActiveHarnessController,
    ActiveState,
    HarnessAction,
    RetrievalPolicy,
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


def test_active_harness_can_retrieve_a_general_recipe_projection() -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))
    provider = FakeActionProvider(
        [
            {
                "action": "retrieve",
                "retrieve": {
                    "query": "deterministic STEP export",
                    "scope": ["recipe"],
                    "limit": 1,
                },
            },
            {"action": "submit", "submit": {"script": "candidate"}},
        ]
    )

    result = ActiveHarnessController(provider).run(
        case,
        _budgets(model_requests=2, retrievals=1, script_submissions=1, executions=1, repairs=0),
        lambda _, **__: SubmissionResult(True, executed=True),
    )

    assert result.state is ActiveState.SUCCEEDED
    retrieved = provider.requests[1].session["tool_results"][0]
    assert retrieved["result"]["matches"][0]["id"] == "recipe.step_export"


def test_active_harness_projects_only_currently_available_actions() -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))
    provider = FakeActionProvider(
        [{"action": "probe", "probe": {"tool": "edge_candidates", "arguments": {}}}]
    )

    result = ActiveHarnessController(provider).run(
        case, _budgets(probes=0), lambda _, **__: SubmissionResult(True, executed=True)
    )

    assert result.state is ActiveState.FAILED
    assert result.stop_reason == "harness_policy"
    assert result.usage["model_requests"] == 1
    assert result.usage["probes"] == 0
    assert result.trace == (
        {
            "action": "provider",
            "requested_action": "probe",
            "error": "action_not_available",
        },
    )


def test_disabled_retrieval_policy_removes_tools_and_fails_closed() -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))
    provider = FakeActionProvider(
        [{"action": "retrieve", "retrieve": {"topic": "TopoDS.Edge_s"}}]
    )

    result = ActiveHarnessController(provider).run(
        case,
        _budgets(model_requests=1, retrievals=0),
        lambda _, **__: SubmissionResult(True, executed=True),
        retrieval_policy=RetrievalPolicy.DISABLED,
    )

    assert result.state is ActiveState.FAILED
    assert result.stop_reason == "harness_policy"
    assert result.usage["retrievals"] == 0
    assert provider.requests[0].session["available_tools"] == ["edge_candidates"]
    assert provider.requests[0].session["allowed_actions"] == ["probe", "submit", "finish"]
    assert "budgets" not in provider.requests[0].session
    assert provider.requests[0].session["retrieval_policy"] == "disabled"


def test_active_harness_hides_internal_limits_and_contract_identity() -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))
    provider = FakeActionProvider(
        [{"action": "submit", "submit": {"script": "candidate"}}]
    )

    result = ActiveHarnessController(provider).run(
        case,
        _budgets(model_requests=1, probes=0, retrievals=0),
        lambda _, **__: SubmissionResult(True, executed=True),
        retrieval_policy=RetrievalPolicy.DISABLED,
    )

    assert result.state is ActiveState.SUCCEEDED
    session = provider.requests[0].session
    assert session["allowed_actions"] == ["submit", "finish"]
    assert session["available_tools"] == []
    assert session["session_phase"] == "initial_attempt"
    assert "budgets" not in session


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
