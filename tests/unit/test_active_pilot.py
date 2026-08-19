from brep2code.evaluation import ACTIVE_COHORT_LABELS, build_active_pilot_report


def _result(label: str, *, passed: bool = True) -> dict:
    usage = {
        "model_requests": 3,
        "probes": 1,
        "retrievals": 1,
        "script_submissions": 1,
        "executions": 1,
        "repairs": 0,
        "tokens": 0,
        "cost_usd": 0.0,
    }
    return {
        "case_id": label,
        "provider": "fake",
        "terminal": True,
        "state": "succeeded" if passed else "failed",
        "stop_reason": "passed" if passed else "finish_without_verifier",
        "budgets": {**usage, "model_requests": 4, "repairs": 1},
        "usage": usage,
        "trace": [
            {"action": "probe"},
            {"action": "retrieve"},
            {"action": "submit" if passed else "finish"},
        ],
    }


def test_active_pilot_report_compares_loops_and_opens_only_authorization_request_gate() -> None:
    results = {
        label: _result(label, passed=label != "failure_sensitive")
        for label in ACTIVE_COHORT_LABELS
    }
    fixed = {
        "artifact": "l0_l2_fake_pilot",
        "status": "succeeded",
        "provider_requests": 12,
        "runtime_case_ids": ["a", "b"],
        "held_out_case_ids": ["c"],
        "control_count": 3,
    }

    report = build_active_pilot_report(results, fixed)

    assert report["status"] == "succeeded"
    assert report["comparison"]["active_loop"]["model_requests"] == 15
    assert report["comparison"]["model_request_delta"] == 3
    assert report["cohorts"][0]["action_sequence"] == ["probe", "retrieve", "submit"]
    assert report["cohorts"][0]["budgets"]["model_requests"] == {
        "used": 3,
        "limit": 4,
        "remaining": 1,
    }
    gate = report["hosted_pilot_decision_gate"]
    assert gate["eligible_to_request_single_pilot_authorization"] is True
    assert gate["authorization_required"] is True
    assert gate["authorization_granted"] is False
    assert gate["network_requests"] == 0


def test_active_pilot_report_closes_gate_on_held_out_failure() -> None:
    results = {
        label: _result(
            label, passed=label not in {"failure_sensitive", "held_out"}
        )
        for label in ACTIVE_COHORT_LABELS
    }
    fixed = {"artifact": "l0_l2_fake_pilot", "status": "succeeded"}

    report = build_active_pilot_report(results, fixed)

    assert report["status"] == "failed"
    assert report["hosted_pilot_decision_gate"][
        "eligible_to_request_single_pilot_authorization"
    ] is False


def test_active_pilot_report_does_not_require_fixed_control() -> None:
    results = {
        label: _result(label, passed=label != "failure_sensitive")
        for label in ACTIVE_COHORT_LABELS
    }

    report = build_active_pilot_report(results)

    assert report["status"] == "succeeded"
    assert report["harness_protocol"] == "active-v1"
    assert report["baseline_role"] == "primary"
    assert report["comparison"]["fixed_loop"]["role"] == "optional_control"
    assert report["comparison"]["model_request_delta"] is None
