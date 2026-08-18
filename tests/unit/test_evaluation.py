import pytest

from brep2code.evaluation import (
    build_held_out_report,
    build_hosted_pilot_report,
    build_mechanism_report,
    build_pilot_report,
    classify_result,
)


def test_failure_classification_covers_terminal_categories() -> None:
    base = {"case_id": "case", "provider_requests": 1}
    assert classify_result({**base, "status": "failed", "stop_reason": "provider_error"}) == "provider"
    assert classify_result({**base, "status": "budget_exhausted"}) == "budget"
    assert classify_result(
        {**base, "status": "failed", "revisions": [{"feedback": {"stage": "generation"}}]}
    ) == "generation"
    assert classify_result(
        {**base, "status": "failed", "revisions": [{"feedback": {"stage": "execution", "stderr": "SyntaxError"}}]}
    ) == "generation"
    assert classify_result(
        {**base, "status": "failed", "revisions": [{"feedback": {"stage": "execution", "stderr": "boom"}}]}
    ) == "execution"
    assert classify_result(
        {**base, "status": "failed", "revisions": [{"feedback": {"stage": "geometry"}}]}
    ) == "geometry"


def test_geometry_gate_failure_stays_geometry_when_round_budget_ends() -> None:
    assert classify_result(
        {"status": "budget_exhausted", "revisions": [{"gates": {"passed": False}}]}
    ) == "geometry"


def test_mechanism_report_groups_only_by_capability_level() -> None:
    results = [
        {
            "case_id": "box",
            "mechanism": "primitive",
            "capability_level": "L0",
            "status": "succeeded",
            "classification": "pass",
        },
        {
            "case_id": "cylinder",
            "mechanism": "analytic_surface",
            "capability_level": "L0",
            "status": "failed",
            "classification": "geometry",
        },
        {
            "case_id": "block_with_hole",
            "mechanism": "boolean_cut",
            "capability_level": "L1",
            "status": "succeeded",
            "classification": "pass",
        },
    ]

    report = build_mechanism_report(results)

    assert [(row["mechanism"], row["capability_level"]) for row in report] == [
        ("analytic_surface", "L0"),
        ("boolean_cut", "L1"),
        ("primitive", "L0"),
    ]
    assert report[0]["classification_counts"] == {"geometry": 1}
    assert all("capability_tier" not in row for row in report)


def test_held_out_report_preserves_failure_class_and_expectation_counts() -> None:
    report = build_held_out_report(
        [
            {
                "case_id": "box_held_out",
                "mechanism": "primitive",
                "capability_level": "L0",
                "actual_failure_class": "pass",
                "matches_expectation": True,
            },
            {
                "case_id": "cylinder_held_out",
                "mechanism": "analytic_surface",
                "capability_level": "L0",
                "actual_failure_class": "geometry",
                "matches_expectation": False,
            },
        ]
    )

    assert report == [
        {
            "mechanism": "analytic_surface",
            "capability_level": "L0",
            "case_ids": ["cylinder_held_out"],
            "case_count": 1,
            "actual_failure_class_counts": {"geometry": 1},
            "expectation_matches": 0,
        },
        {
            "mechanism": "primitive",
            "capability_level": "L0",
            "case_ids": ["box_held_out"],
            "case_count": 1,
            "actual_failure_class_counts": {"pass": 1},
            "expectation_matches": 1,
        },
    ]


def test_pilot_report_keeps_runtime_and_held_out_scopes_and_sums_accounting() -> None:
    common = {"campaign_id": "g1", "contract_sha256": "abc", "provider": "fake"}
    runtime = {
        **common,
        "artifact": "campaign",
        "status": "succeeded",
        "stop_reason": "completed",
        "provider_requests": 2,
        "provider_accounting": {"http_attempts": 2, "total_tokens": 10, "cost_usd": 0.1},
        "cases": [
            {
                "case_id": "box",
                "mechanism": "primitive",
                "capability_level": "L0",
                "status": "succeeded",
            }
        ],
    }
    control_matrix = {
        **common,
        "artifact": "control_matrix",
        "status": "succeeded",
        "stop_reason": "control_matrix_passed",
        "provider_requests": 1,
        "provider_accounting": {"http_attempts": 1, "total_tokens": 5, "cost_usd": 0.05},
        "cases": [
            {
                "case_id": "box",
                "mechanism": "primitive",
                "capability_level": "L0",
                "matches_expectation": True,
            }
        ],
    }
    held_out = {
        **common,
        "artifact": "held_out_generalization",
        "status": "succeeded",
        "stop_reason": "held_out_passed",
        "provider_requests": 1,
        "provider_accounting": {"http_attempts": 1, "total_tokens": 3, "cost_usd": 0.02},
        "cases": [
            {
                "case_id": "box_held_out",
                "mechanism": "primitive",
                "capability_level": "L0",
                "matches_expectation": True,
            }
        ],
    }

    report = build_pilot_report(runtime, control_matrix, held_out)

    assert report["status"] == "succeeded"
    assert report["provider_requests"] == 4
    assert report["provider_accounting"] == {
        "http_attempts": 4,
        "total_tokens": 18,
        "cost_usd": 0.17,
    }
    assert report["runtime_case_ids"] == ["box"]
    assert report["held_out_case_ids"] == ["box_held_out"]
    assert report["capability_report"][0] == {
        "mechanism": "primitive",
        "capability_level": "L0",
        "runtime_case_ids": ["box"],
        "runtime_case_count": 1,
        "runtime_status_counts": {"succeeded": 1},
        "control_count": 1,
        "control_expectation_matches": 1,
        "held_out_case_ids": ["box_held_out"],
        "held_out_case_count": 1,
        "held_out_expectation_matches": 1,
    }


def test_pilot_report_rejects_runtime_held_out_overlap() -> None:
    common = {"campaign_id": "g1", "contract_sha256": "abc", "provider": "fake"}
    base = {
        "status": "succeeded",
        "stop_reason": "completed",
        "provider_requests": 0,
        "provider_accounting": {},
        "cases": [{"case_id": "box", "mechanism": "primitive", "capability_level": "L0"}],
    }
    with pytest.raises(ValueError, match="scopes overlap"):
        build_pilot_report(
            {**common, "artifact": "campaign", **base},
            {**common, "artifact": "control_matrix", **base},
            {**common, "artifact": "held_out_generalization", **base},
        )


def test_hosted_pilot_report_records_mixed_provider_routing() -> None:
    common = {"campaign_id": "g1", "contract_sha256": "abc"}
    base = {
        "status": "succeeded",
        "stop_reason": "completed",
        "provider_requests": 1,
        "provider_accounting": {"http_attempts": 1, "total_tokens": 2, "cost_usd": 0.01},
    }
    runtime = {
        **common,
        **base,
        "artifact": "campaign",
        "provider": "deepseek",
        "model": "deepseek-v4-pro",
        "cases": [
            {
                "case_id": "box",
                "mechanism": "primitive",
                "capability_level": "L0",
                "status": "succeeded",
            }
        ],
    }
    controls = {
        **common,
        **base,
        "artifact": "control_matrix",
        "provider": "fake",
        "model": "fake-script-queue-v1",
        "cases": [
            {
                "case_id": "box",
                "mechanism": "primitive",
                "capability_level": "L0",
                "matches_expectation": True,
            }
        ],
    }
    held_out = {
        **common,
        **base,
        "artifact": "held_out_generalization",
        "provider": "fake",
        "model": "fake-script-queue-v1",
        "cases": [
            {
                "case_id": "box_held_out",
                "mechanism": "primitive",
                "capability_level": "L0",
                "matches_expectation": True,
            }
        ],
    }

    report = build_hosted_pilot_report(runtime, controls, held_out)

    assert report["artifact"] == "l0_l2_hosted_pilot"
    assert report["provider"] == "mixed"
    assert report["provider_routing"] == {
        "runtime": {"provider": "deepseek", "model": "deepseek-v4-pro"},
        "control_matrix": {"provider": "fake", "model": "fake-script-queue-v1"},
        "held_out": {"provider": "fake", "model": "fake-script-queue-v1"},
    }
    assert report["provider_requests"] == 3
    assert report["provider_accounting"] == {
        "http_attempts": 3,
        "total_tokens": 6,
        "cost_usd": 0.03,
    }
