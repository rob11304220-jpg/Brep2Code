import json
from dataclasses import asdict
from pathlib import Path

import pytest

from brep2code.cases import validate_case
from brep2code.harness import (
    ActiveBudgets,
    ActiveHostedAuthorization,
    ActiveResultValidationError,
    preflight_active_hosted,
)
from brep2code.providers import ProviderLimits


def _case():
    return validate_case(Path("cases/smoke/box"), Path("cases"))


def _budgets() -> ActiveBudgets:
    return ActiveBudgets(4, 1, 1, 2, 2, 1, 100, 1.0)


def _limits(**overrides) -> ProviderLimits:
    values = {
        "max_requests": 4,
        "timeout_seconds": 30,
        "max_retries": 0,
        "max_output_tokens": 50,
        "max_total_tokens": 200,
        "max_cost_usd": 2.0,
        "input_cost_per_million": 1.0,
        "output_cost_per_million": 2.0,
    }
    values.update(overrides)
    return ProviderLimits(**values)


def _authorization(**overrides) -> ActiveHostedAuthorization:
    values = {
        "hosted": True,
        "observations": True,
        "tool_results": True,
        "revision_source": True,
        "feedback": True,
    }
    values.update(overrides)
    return ActiveHostedAuthorization(**values)


def _accounting(**overrides):
    value = {
        "http_attempts": 1,
        "in_flight_requests": 0,
        "tokens": {"prompt": 6, "completion": 4, "total": 10},
        "cost_usd": 0.000014,
        "pricing": {
            "input_cost_per_million": 1.0,
            "output_cost_per_million": 2.0,
        },
        "ceilings": {
            "max_requests": 4,
            "timeout_seconds": 30,
            "max_retries": 0,
            "max_output_tokens": 50,
            "max_total_tokens": 200,
            "max_cost_usd": 2.0,
        },
    }
    value.update(overrides)
    return value


def test_active_hosted_preflight_declares_projection_and_double_budgets(
    tmp_path: Path,
) -> None:
    plan = preflight_active_hosted(
        _case(),
        tmp_path / "fresh",
        provider="deepseek",
        model="deepseek-v4-pro",
        thinking_mode="disabled",
        budgets=_budgets(),
        build_timeout_seconds=5,
        provider_limits=_limits(),
        authorization=_authorization(),
    )

    assert plan["remaining_model_requests"] == 4
    assert plan["controller_budget"]["tokens"] == 100
    assert plan["provider_budget"]["max_total_tokens"] == 200
    assert plan["outbound_projection"]["initial"] == [
        "case_id",
        "unit",
        "initial_observations",
        "allowed_actions",
        "available_tools",
        "session_phase",
        "retrieval_policy",
        "backend_profile",
        "current_revision",
    ]
    assert "budgets" not in plan["outbound_projection"]["initial"]
    assert plan["outbound_projection"]["iterative"] == [
        "bounded_tool_results",
        "typed_feedback",
        "current_revision",
    ]
    assert "repository_files" in plan["outbound_projection"]["excluded"]


def test_active_hosted_preflight_requires_itemized_fresh_authorization(
    tmp_path: Path,
) -> None:
    with pytest.raises(ActiveResultValidationError, match="tool-results"):
        preflight_active_hosted(
            _case(),
            tmp_path / "fresh",
            provider="deepseek",
            model="deepseek-v4-pro",
            thinking_mode="disabled",
            budgets=_budgets(),
            build_timeout_seconds=5,
            provider_limits=_limits(),
            authorization=_authorization(tool_results=False),
        )


def test_active_hosted_preflight_rejects_controller_budget_above_provider(
    tmp_path: Path,
) -> None:
    with pytest.raises(ActiveResultValidationError, match="token budget"):
        preflight_active_hosted(
            _case(),
            tmp_path / "fresh",
            provider="deepseek",
            model="deepseek-v4-pro",
            thinking_mode="disabled",
            budgets=_budgets(),
            build_timeout_seconds=5,
            provider_limits=_limits(max_total_tokens=50),
            authorization=_authorization(),
        )


def test_active_hosted_continuation_requires_same_scope_and_reauthorization(
    tmp_path: Path,
) -> None:
    root = tmp_path / "active"
    root.mkdir()
    payload = {
        "schema_version": 4,
        "mode": "active",
        "case_id": "box",
        "provider": "deepseek",
        "model": "deepseek-v4-pro",
        "budgets": {
            "model_requests": 4,
            "probes": 1,
            "retrievals": 1,
            "script_submissions": 2,
            "executions": 2,
            "repairs": 1,
            "tokens": 100,
            "cost_usd": 1.0,
        },
        "timeout_seconds": 5,
        "checkpoint_index": 1,
        "terminal": False,
        "continuation_policy": {
            "eligible": True,
            "implemented": True,
            "requirements": [
                "same_case",
                "same_budgets",
                "remaining_model_requests",
                "existing_revision_root",
            ],
        },
        "state": "synthesizing",
        "stop_reason": None,
        "usage": {
            "model_requests": 1,
            "probes": 0,
            "retrievals": 0,
            "script_submissions": 0,
            "executions": 0,
            "repairs": 0,
            "tokens": 10,
            "cost_usd": 0.000014,
        },
        "trace": [],
        "provider_accounting": _accounting(),
    }
    result_path = root / "result.json"
    result_path.write_text(json.dumps(payload), encoding="utf-8")

    plan = preflight_active_hosted(
        _case(),
        root,
        provider="deepseek",
        model="deepseek-v4-pro",
        thinking_mode="disabled",
        budgets=_budgets(),
        build_timeout_seconds=5,
        provider_limits=_limits(),
        authorization=_authorization(),
        continuation_payload=payload,
        continuation_result=result_path,
    )

    assert plan["continuation"] is True
    assert plan["continuation_requires_fresh_authorization"] is True
    assert plan["remaining_model_requests"] == 3

    with pytest.raises(ActiveResultValidationError, match="fresh authorization"):
        preflight_active_hosted(
            _case(),
            root,
            provider="deepseek",
            model="deepseek-v4-pro",
            thinking_mode="disabled",
            budgets=_budgets(),
            build_timeout_seconds=5,
            provider_limits=_limits(),
            authorization=_authorization(hosted=False),
            continuation_payload=payload,
            continuation_result=result_path,
        )


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda payload: (
                payload["provider_accounting"]["pricing"].update(input_cost_per_million=1.5),
                payload["provider_accounting"].update(cost_usd=0.000017),
                payload["usage"].update(cost_usd=0.000017),
            ),
            "pricing drift",
        ),
        (
            lambda payload: payload["provider_accounting"]["ceilings"].update(max_requests=3),
            "ceiling drift",
        ),
        (
            lambda payload: payload["provider_accounting"]["tokens"].update(total=11),
            "token accounting drift",
        ),
    ],
)
def test_active_hosted_continuation_rejects_provider_accounting_drift(
    tmp_path: Path, mutation, message: str
) -> None:
    root = tmp_path / "active"
    root.mkdir()
    payload = {
        "schema_version": 4,
        "mode": "active",
        "case_id": "box",
        "provider": "deepseek",
        "model": "deepseek-v4-pro",
        "budgets": asdict(_budgets()),
        "timeout_seconds": 5,
        "checkpoint_index": 1,
        "terminal": False,
        "continuation_policy": {
            "eligible": True,
            "implemented": True,
            "requirements": [
                "same_case",
                "same_budgets",
                "remaining_model_requests",
                "existing_revision_root",
            ],
        },
        "state": "synthesizing",
        "stop_reason": None,
        "usage": {
            "model_requests": 1,
            "probes": 0,
            "retrievals": 0,
            "script_submissions": 0,
            "executions": 0,
            "repairs": 0,
            "tokens": 10,
            "cost_usd": 0.000014,
        },
        "trace": [],
        "provider_accounting": _accounting(),
    }
    mutation(payload)

    with pytest.raises(ActiveResultValidationError, match=message):
        preflight_active_hosted(
            _case(),
            root,
            provider="deepseek",
            model="deepseek-v4-pro",
            thinking_mode="disabled",
            budgets=_budgets(),
            build_timeout_seconds=5,
            provider_limits=_limits(),
            authorization=_authorization(),
            continuation_payload=payload,
            continuation_result=root / "result.json",
        )
