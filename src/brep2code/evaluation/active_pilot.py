from __future__ import annotations

from typing import Any


ACTIVE_COHORT_LABELS = (
    "nominal",
    "parameter_variation",
    "failure_sensitive",
    "controls",
    "held_out",
)


def build_active_pilot_report(
    results: dict[str, dict[str, Any]], fixed_pilot: dict[str, Any] | None = None
) -> dict[str, Any]:
    if tuple(results) != ACTIVE_COHORT_LABELS:
        raise ValueError("active pilot cohort labels are invalid")
    if fixed_pilot is not None and fixed_pilot.get("artifact") != "l0_l2_fake_pilot":
        raise ValueError("active pilot fixed baseline is invalid")
    rows = [_active_row(label, results[label]) for label in ACTIVE_COHORT_LABELS]
    expectations = {
        "nominal": "pass",
        "parameter_variation": "pass",
        "failure_sensitive": "fail",
        "controls": "pass",
        "held_out": "pass",
    }
    for row in rows:
        row["expected_terminal"] = expectations[row["cohort"]]
        row["matches_expectation"] = (
            "pass" if row["terminal_classification"] == "pass" else "fail"
        ) == row["expected_terminal"]

    active_requests = sum(int(row["usage"]["model_requests"]) for row in rows)
    fixed_requests = int(fixed_pilot.get("provider_requests", 0)) if fixed_pilot else None
    checks = {
        "all_active_results_terminal": all(row["terminal"] for row in rows),
        "all_cohort_expectations_match": all(row["matches_expectation"] for row in rows),
        "held_out_passed": rows[-1]["terminal_classification"] == "pass",
        "fake_only": all(result.get("provider") == "fake" for result in results.values()),
        "probe_path_exercised": any(row["usage"]["probes"] > 0 for row in rows),
        "retrieval_policy_consistent": len(
            {result.get("retrieval_policy", "bounded_seed") for result in results.values()}
        )
        == 1,
        "submission_path_exercised": any(
            row["usage"]["script_submissions"] > 0 for row in rows
        ),
    }
    comparison_checks = {
        "provided": fixed_pilot is not None,
        "fixed_fake_pilot_succeeded": (
            fixed_pilot.get("status") == "succeeded" if fixed_pilot else None
        ),
    }
    active_succeeded = all(checks.values())
    return {
        "schema_version": 1,
        "artifact": "l2_fake_active_pilot",
        "provider": "fake",
        "harness_protocol": "active-v1",
        "baseline_role": "primary",
        "status": "succeeded" if active_succeeded else "failed",
        "stop_reason": "decision_gate_passed" if active_succeeded else "decision_gate_failed",
        "cohort_order": list(ACTIVE_COHORT_LABELS),
        "cohorts": rows,
        "comparison": {
            "fixed_loop": {
                "role": "optional_control",
                "status": fixed_pilot.get("status") if fixed_pilot else None,
                "provider_requests": fixed_requests,
                "runtime_case_count": len(fixed_pilot.get("runtime_case_ids", [])) if fixed_pilot else 0,
                "held_out_case_count": len(fixed_pilot.get("held_out_case_ids", [])) if fixed_pilot else 0,
                "control_count": int(fixed_pilot.get("control_count", 0)) if fixed_pilot else 0,
            },
            "active_loop": {
                "role": "primary",
                "status": "succeeded" if active_succeeded else "failed",
                "model_requests": active_requests,
                "probes": sum(int(row["usage"]["probes"]) for row in rows),
                "retrievals": sum(int(row["usage"]["retrievals"]) for row in rows),
                "script_submissions": sum(
                    int(row["usage"]["script_submissions"]) for row in rows
                ),
                "repairs": sum(int(row["usage"]["repairs"]) for row in rows),
            },
            "model_request_delta": (
                active_requests - fixed_requests if fixed_requests is not None else None
            ),
            "checks": comparison_checks,
        },
        "hosted_pilot_decision_gate": {
            "checks": checks,
            "eligible_to_request_single_pilot_authorization": active_succeeded,
            "authorization_required": True,
            "authorization_granted": False,
            "network_requests": 0,
        },
    }


def _active_row(label: str, payload: dict[str, Any]) -> dict[str, Any]:
    budgets = payload["budgets"]
    usage = payload["usage"]
    return {
        "cohort": label,
        "case_id": payload["case_id"],
        "terminal": payload["terminal"],
        "state": payload["state"],
        "stop_reason": payload["stop_reason"],
        "terminal_classification": _terminal_classification(payload),
        "action_sequence": [item["action"] for item in payload["trace"]],
        "usage": dict(usage),
        "budgets": {
            name: {
                "used": usage[name],
                "limit": limit,
                "remaining": limit - usage[name],
            }
            for name, limit in budgets.items()
        },
        "result_path": f"{label}/result.json",
    }


def _terminal_classification(payload: dict[str, Any]) -> str:
    if payload["state"] == "succeeded":
        return "pass"
    stop_reason = payload["stop_reason"]
    if payload["state"] == "exhausted":
        return "budget"
    if stop_reason == "provider_error":
        return "provider"
    if stop_reason in {"sandbox_unavailable", "execution_error"}:
        return "execution"
    if stop_reason in {"tool_error", "finish_without_verifier"}:
        return "harness"
    return "failed"
