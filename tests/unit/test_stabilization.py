from __future__ import annotations

import json
from pathlib import Path

import pytest

from brep2code.cases import validate_catalog
from brep2code.stabilization import (
    StabilizationValidationError,
    classify_stabilization_result,
    load_stabilization_contract,
    validate_outbound_projection,
)


CONTRACT = Path("cases/campaigns/stage1-active-v4-stabilization.json")


def test_stabilization_contract_freezes_separate_twelve_run_protocol_cohort() -> None:
    contract = load_stabilization_contract(CONTRACT, validate_catalog(Path("cases")))

    phase = contract["phases"][0]
    expected_runs = (
        len(phase["cases"])
        * len(phase["backend_profiles"])
        * len(phase["cohorts"])
        * phase["replicates"]
    )
    assert contract["experiment_id"] == "stage1-active-v4-stabilization-v1"
    assert contract["result_schema_version"] == 7
    assert contract["task_contract_version"] == 2
    assert expected_runs == 12


def test_outbound_projection_accepts_capabilities_and_hides_internal_limits(
    tmp_path: Path,
) -> None:
    run_root = tmp_path / "run"
    exchange = run_root / "provider-exchanges/attempt-001"
    exchange.mkdir(parents=True)
    task = {
        "case_id": "box",
        "unit": "mm",
        "initial_observations": {"shape": "solid"},
        "allowed_actions": ["submit", "finish"],
        "available_tools": [],
        "session_phase": "initial_attempt",
        "retrieval_policy": "disabled",
        "backend_profile": "ocp_v1",
        "current_revision": None,
        "feedback": None,
        "tool_results": [],
        "turn_index": 0,
    }
    request = {
        "endpoint": "/chat/completions",
        "timeout_seconds": 120,
        "body": {
            "model": "deepseek-v4-pro",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        '- {"action":"submit","submit":{"script":"complete build.py"}}\n'
                        '- {"action":"finish","finish":{"reason":"done"}}'
                    ),
                },
                {"role": "user", "content": json.dumps(task)},
            ],
        },
    }
    (exchange / "request.json").write_text(json.dumps(request), encoding="utf-8")
    (run_root / "result.json").write_text(
        json.dumps(
            {
                "schema_version": 7,
                "provider_accounting": {
                    "http_attempts": 1,
                    "protocol_retries": 0,
                },
            }
        ),
        encoding="utf-8",
    )

    report = validate_outbound_projection(run_root)

    assert report == {
        "status": "valid",
        "schema_version": 7,
        "http_attempts": 1,
        "protocol_retries": 0,
        "model_visible_internal_fields": [],
    }


def test_outbound_projection_rejects_nested_budget_disclosure(tmp_path: Path) -> None:
    run_root = tmp_path / "run"
    exchange = run_root / "provider-exchanges/attempt-001"
    exchange.mkdir(parents=True)
    request = {
        "body": {
            "messages": [
                {"role": "system", "content": '- {"action":"finish"'},
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "allowed_actions": ["finish"],
                            "available_tools": [],
                            "feedback": {"usage": {"model_requests": 1}},
                        }
                    ),
                },
            ]
        }
    }
    (exchange / "request.json").write_text(json.dumps(request), encoding="utf-8")
    (run_root / "result.json").write_text(
        json.dumps(
            {
                "schema_version": 7,
                "provider_accounting": {"http_attempts": 1, "protocol_retries": 0},
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(StabilizationValidationError, match="internal fields"):
        validate_outbound_projection(run_root)


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        ({"state": "succeeded"}, "pass"),
        (
            {
                "state": "failed",
                "stop_reason": "provider_error",
                "trace": [{"error": "provider response violated the JSON contract"}],
            },
            "provider_protocol",
        ),
        (
            {"state": "failed", "stop_reason": "provider_error", "trace": []},
            "provider_transport",
        ),
        (
            {"state": "failed", "stop_reason": "finish_without_verifier", "trace": []},
            "model_policy",
        ),
        (
            {"state": "failed", "stop_reason": "sandbox_unavailable", "trace": []},
            "harness_infrastructure",
        ),
    ],
)
def test_stabilization_classification_is_separate_from_frozen_stage1(
    payload: dict, expected: str
) -> None:
    assert classify_stabilization_result(payload) == expected
