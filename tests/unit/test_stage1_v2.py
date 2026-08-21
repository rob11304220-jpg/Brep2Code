from __future__ import annotations

import json
from pathlib import Path

import pytest

from brep2code.cases import validate_catalog
from brep2code.stage1_v2 import (
    Stage1V2ValidationError,
    Stage1V2RunOutcome,
    expected_stage1_v2_baselines,
    build_stage1_v2_preflight,
    build_stage1_v2_report,
    expected_stage1_v2_identities,
    load_stage1_v2_contract,
    load_stage1_v3_contract,
    run_stage1_v2_cohort,
)


CONTRACT = Path("cases/campaigns/stage1-no-knowledge-v2.json")
V3_CONTRACT = Path("cases/campaigns/stage1-no-knowledge-v3.json")


def _contract() -> dict:
    return load_stage1_v2_contract(CONTRACT, validate_catalog(Path("cases")))


def _write_stabilization_report(path: Path, *, stable: bool = True) -> None:
    path.write_text(
        json.dumps(
            {
                "experiment_id": "stage1-active-v4-stabilization-v1",
                "expected_runs": 12,
                "observed_runs": 12,
                "missing_runs": [],
                "artifact_validation_failures": [],
                "projection_validation_failures": [],
                "judgment": {
                    "protocol_stable": stable,
                    "stage1_exit_changed": False,
                    "stage2_authorized": False,
                },
            }
        ),
        encoding="utf-8",
    )


def test_stage1_v2_contract_freezes_complete_eighty_run_identity_set() -> None:
    contract = _contract()

    identities = expected_stage1_v2_identities(contract)

    assert len(identities) == 80
    assert sum(item[4] == "cadquery_baseline" for item in identities) == 50
    assert sum(item[4] == "ocp_contrast" for item in identities) == 30
    assert contract["result_schema_version"] == 7
    assert contract["retrieval_policy"] == "disabled"


def test_stage1_v3_replaces_aborted_v2_without_changing_research_condition() -> None:
    v2 = _contract()
    v3 = load_stage1_v3_contract(V3_CONTRACT, validate_catalog(Path("cases")))

    assert v3["experiment_id"] == "stage1-no-knowledge-v3"
    assert v3["execution_protocol_version"] == 3
    assert v3["supersedes_experiment_id"] == v2["experiment_id"]
    for key in (
        "cases",
        "backend_profiles",
        "cohorts",
        "hosted_limits",
        "phases",
        "valid_attempt_threshold",
        "infrastructure_failure_rate_threshold",
    ):
        assert v3[key] == v2[key]


def test_stage1_v2_freezes_twenty_unique_fake_readiness_baselines() -> None:
    baselines = expected_stage1_v2_baselines(_contract())

    assert len(baselines) == 20
    assert len(set(baselines)) == 20
    assert sum(item[1] == "cadquery_v1" for item in baselines) == 10
    assert sum(item[1] == "ocp_v1" for item in baselines) == 10


def test_stage1_v2_runner_continues_terminal_model_and_cad_failures() -> None:
    classifications = iter(
        ["generation", "geometry", "execution", "budget", "model_policy"] + ["pass"] * 75
    )
    visited = []

    def execute(identity, run_root):
        visited.append((identity, run_root))
        return Stage1V2RunOutcome(next(classifications), 1, 10, 0.001)

    result = run_stage1_v2_cohort(_contract(), Path("fresh-v2-root"), execute)

    assert result["status"] == "complete"
    assert result["completed_runs"] == 80
    assert len(visited) == 80
    assert result["stage2_authorized"] is False
    assert visited[0][1] == Path(
        "fresh-v2-root/cadquery_baseline/box/cadquery_v1/first_shot/replicate-1"
    )
    assert visited[-1][1] == Path(
        "fresh-v2-root/ocp_contrast/filleted_box/ocp_v1/bounded_repair/replicate-5"
    )


@pytest.mark.parametrize("fatal", ["artifact", "projection"])
def test_stage1_v2_runner_stops_immediately_on_integrity_failure(fatal: str) -> None:
    calls = 0

    def execute(identity, run_root):
        nonlocal calls
        calls += 1
        return Stage1V2RunOutcome(
            "geometry",
            1,
            10,
            0.001,
            artifact_valid=fatal != "artifact",
            projection_valid=fatal != "projection",
        )

    with pytest.raises(Stage1V2ValidationError, match=fatal):
        run_stage1_v2_cohort(_contract(), Path("fresh-v2-root"), execute)
    assert calls == 1


def test_stage1_v2_runner_stops_on_configuration_failure() -> None:
    calls = 0

    def execute(identity, run_root):
        nonlocal calls
        calls += 1
        raise RuntimeError("configuration failed")

    with pytest.raises(Stage1V2ValidationError, match="configuration"):
        run_stage1_v2_cohort(_contract(), Path("fresh-v2-root"), execute)
    assert calls == 1


def test_stage1_v2_runner_rejects_existing_root_and_aggregate_overrun(tmp_path: Path) -> None:
    existing = tmp_path / "existing"
    existing.mkdir()
    with pytest.raises(Stage1V2ValidationError, match="fresh"):
        run_stage1_v2_cohort(_contract(), existing, lambda identity, root: None)

    calls = 0

    def execute(identity, run_root):
        nonlocal calls
        calls += 1
        return Stage1V2RunOutcome("pass", 241, 1, 0.0)

    with pytest.raises(Stage1V2ValidationError, match="aggregate ceiling"):
        run_stage1_v2_cohort(_contract(), tmp_path / "fresh", execute)
    assert calls == 1


def test_stage1_v2_preflight_binds_prerequisite_backends_and_maximum_scope(
    tmp_path: Path,
) -> None:
    prerequisite = tmp_path / "stabilization-report.json"
    _write_stabilization_report(prerequisite)

    plan = build_stage1_v2_preflight(
        _contract(),
        prerequisite,
        tmp_path / "fresh-runs",
        lambda profile: (True, "ready", "2.8.0" if profile == "cadquery_v1" else "7.9.3.1.1"),
    )

    assert plan["status"] == "ready_for_authorization_review"
    assert plan["expected_runs"] == 80
    assert plan["maximum_scope"] == {
        "model_decisions": 120,
        "http_attempts": 240,
        "tokens": 1_280_000,
        "cost_usd": 1.6,
    }
    assert plan["authorization_granted"] is False
    assert plan["stage2_authorized"] is False
    assert "numeric_limits" in plan["outbound_projection"]["excluded"]


def test_stage1_v2_preflight_rejects_unstable_prerequisite(tmp_path: Path) -> None:
    prerequisite = tmp_path / "stabilization-report.json"
    _write_stabilization_report(prerequisite, stable=False)

    with pytest.raises(Stage1V2ValidationError, match="prerequisite"):
        build_stage1_v2_preflight(
            _contract(),
            prerequisite,
            tmp_path / "fresh-runs",
            lambda profile: (True, "ready", "version"),
        )


def test_stage1_v2_empty_report_exposes_all_missing_identities(tmp_path: Path) -> None:
    report = build_stage1_v2_report(_contract(), validate_catalog(Path("cases")), tmp_path / "runs")

    assert report["expected_runs"] == 80
    assert report["observed_runs"] == 0
    assert len(report["missing_runs"]) == 80
    assert report["phase_judgments"]["cadquery_baseline"]["complete"] is False
    assert report["phase_judgments"]["ocp_contrast"]["complete"] is False
    assert report["judgment"] == {
        "complete": False,
        "exit_ready": False,
        "stage2_authorized": False,
    }


def test_stage1_v2_result_validation_rejects_nonterminal_checkpoint(tmp_path: Path) -> None:
    root = tmp_path / "runs" / "partial"
    root.mkdir(parents=True)
    payload = {
        "stage1_identity": {
            "experiment_id": "stage1-no-knowledge-v2",
            "phase_id": "cadquery_baseline",
            "cohort": "first_shot",
            "replicate": 1,
        },
        "case_id": "box",
        "backend_profile": "cadquery_v1",
    }
    # A minimally discoverable checkpoint must never count as a terminal research result.
    (root / "result.json").write_text(json.dumps(payload), encoding="utf-8")

    report = build_stage1_v2_report(_contract(), validate_catalog(Path("cases")), tmp_path / "runs")

    assert report["artifact_validation_failures"]
    assert report["failure_classifications"] == {"controller_harness": 1}
    assert report["judgment"]["abort_status"] == "aborted_infrastructure_failure"
