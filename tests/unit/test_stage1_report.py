from __future__ import annotations

import json
from pathlib import Path

import pytest

import brep2code.stage1 as stage1_module
from brep2code.cases import validate_catalog
from brep2code.stage1 import Stage1ContractError, build_stage1_report


def _contract() -> dict:
    payload = json.loads(
        Path("cases/campaigns/stage1-backend-baseline.json").read_text(encoding="utf-8")
    )
    payload["phases"] = [{
        "phase_id": "test_phase",
        "cases": ["box"],
        "backend_profiles": ["cadquery_v1"],
        "cohorts": ["first_shot"],
        "replicates": 2,
    }]
    return payload


def _write_result(root: Path, replicate: int, *, provider: str = "deepseek") -> None:
    run = root / f"run-{replicate}"
    run.mkdir(parents=True)
    contract = _contract()
    payload = {
        "schema_version": 6,
        "case_id": "box",
        "provider": provider,
        "model": contract["model"],
        "retrieval_policy": "disabled",
        "backend_profile": "cadquery_v1",
        "task_contract_hash": stage1_module.build_provider_task_contract(
            "cadquery_v1", "disabled", contract_version=1
        ).identity,
        "budgets": contract["cohorts"]["first_shot"],
        "timeout_seconds": 20,
        "state": "succeeded",
        "stop_reason": "passed",
        "usage": {
            "model_requests": 1, "probes": 0, "retrievals": 0,
            "script_submissions": 1, "executions": 1, "repairs": 0,
            "tokens": 100, "cost_usd": 0.001,
        },
        "trace": [{"action": "submit", "passed": True}],
        "stage1_identity": {
            "experiment_id": contract["experiment_id"],
            "phase_id": "test_phase",
            "cohort": "first_shot",
            "replicate": replicate,
        },
    }
    (run / "result.json").write_text(json.dumps(payload), encoding="utf-8")


@pytest.fixture(autouse=True)
def _skip_artifact_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(stage1_module, "validate_active_result", lambda *args: None)


def _report(root: Path) -> dict:
    return build_stage1_report(
        _contract(), validate_catalog(Path("cases")), root, "test_phase"
    )


def test_stage1_report_accepts_complete_identity_set(tmp_path: Path) -> None:
    _write_result(tmp_path, 1)
    _write_result(tmp_path, 2)

    report = _report(tmp_path)

    assert report["totals"]["runs"] == 2
    assert report["judgment"]["phase_ready"] is True
    assert report["groups"]["first_shot/box/cadquery_v1"]["passed"] == 2


def test_stage1_report_exposes_missing_run(tmp_path: Path) -> None:
    _write_result(tmp_path, 1)

    report = _report(tmp_path)

    assert report["judgment"]["complete"] is False
    assert report["missing_runs"][0]["replicate"] == 2


def test_stage1_report_rejects_duplicate_identity(tmp_path: Path) -> None:
    _write_result(tmp_path / "a", 1)
    _write_result(tmp_path / "b", 1)

    with pytest.raises(Stage1ContractError, match="duplicate"):
        _report(tmp_path)


def test_stage1_report_rejects_frozen_identity_drift(tmp_path: Path) -> None:
    _write_result(tmp_path, 1, provider="other")

    with pytest.raises(Stage1ContractError, match="frozen identity drift"):
        _report(tmp_path)


def test_stage1_report_applies_infrastructure_failure_threshold(tmp_path: Path) -> None:
    _write_result(tmp_path, 1)
    _write_result(tmp_path, 2)
    path = tmp_path / "run-2" / "result.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload.update(state="failed", stop_reason="provider_error")
    path.write_text(json.dumps(payload), encoding="utf-8")

    report = _report(tmp_path)

    assert report["failure_classifications"] == {"pass": 1, "provider": 1}
    assert report["judgment"]["phase_ready"] is False


def test_stage1_report_counts_artifact_validation_failure_as_harness(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _write_result(tmp_path, 1)
    _write_result(tmp_path, 2)

    def fail_one(payload, *_args) -> None:
        if payload["stage1_identity"]["replicate"] == 1:
            raise stage1_module.ActiveResultValidationError("request trace drift")

    monkeypatch.setattr(stage1_module, "validate_active_result", fail_one)

    report = _report(tmp_path)

    assert report["failure_classifications"] == {"harness": 1, "pass": 1}
    assert report["artifact_validation_failures"] == [
        {
            "case_id": "box",
            "backend_profile": "cadquery_v1",
            "cohort": "first_shot",
            "replicate": 1,
            "error": "request trace drift",
        }
    ]
    assert report["judgment"]["phase_ready"] is False
