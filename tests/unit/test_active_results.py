import json
from pathlib import Path

import pytest

from brep2code.cases import validate_case
from brep2code.harness import ActiveResultValidationError, validate_active_result


def _write_active_result(root: Path) -> dict:
    root.mkdir()
    payload = {
        "schema_version": 3,
        "mode": "active",
        "case_id": "box",
        "provider": "fake",
        "model": "fake-action-queue-v1",
        "budgets": {
            "model_requests": 4,
            "probes": 1,
            "retrievals": 1,
            "script_submissions": 2,
            "executions": 2,
            "repairs": 1,
            "tokens": 0,
            "cost_usd": 0.0,
        },
        "timeout_seconds": 5,
        "checkpoint_index": 8,
        "terminal": True,
        "continuation_policy": {
            "eligible": False,
            "implemented": True,
            "requirements": [
                "same_case",
                "same_budgets",
                "remaining_model_requests",
                "existing_revision_root",
            ],
        },
        "state": "succeeded",
        "stop_reason": "passed",
        "usage": {
            "model_requests": 4,
            "probes": 1,
            "retrievals": 1,
            "script_submissions": 2,
            "executions": 2,
            "repairs": 1,
            "tokens": 0,
            "cost_usd": 0.0,
        },
        "trace": [
            {"action": "probe", "result": {"edges": []}},
            {"action": "retrieve", "result": {"symbol": "TopoDS.Edge_s"}},
            {"action": "submit", "passed": False, "feedback": {"stage": "geometry"}},
            {"action": "submit", "passed": True, "feedback": None},
        ],
    }
    for index, status in enumerate(("failed", "succeeded")):
        revision_id = f"revision-{index:03d}"
        revision = root / revision_id
        revision.mkdir()
        (revision / "build.py").write_text(f"revision = {index}\n", encoding="utf-8")
        (revision / "result.json").write_text(
            json.dumps(
                {
                    "revision_id": revision_id,
                    "workspace": revision_id,
                    "status": status,
                    "execution": {
                        "output_step": "output.step",
                        "sandboxed": True,
                    },
                }
            ),
            encoding="utf-8",
        )
    (root / "result.json").write_text(json.dumps(payload), encoding="utf-8")
    return payload


def _case():
    return validate_case(Path("cases/smoke/box"), Path("cases"))


def test_validate_active_result_cross_checks_trace_revisions_and_budgets(tmp_path: Path) -> None:
    root = tmp_path / "active"
    payload = _write_active_result(root)

    validate_active_result(payload, _case(), root)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda payload: payload["usage"].update(executions=1), "execution accounting drift"),
        (lambda payload: payload["usage"].update(model_requests=3), "request trace drift"),
        (
            lambda payload: payload["trace"][0]["result"].update(expected={}),
            "private field",
        ),
        (lambda payload: payload.update(stop_reason="provider_error"), "success terminal drift"),
    ],
)
def test_validate_active_result_rejects_artifact_drift(
    tmp_path: Path, mutation, message: str
) -> None:
    root = tmp_path / "active"
    payload = _write_active_result(root)
    mutation(payload)

    with pytest.raises(ActiveResultValidationError, match=message):
        validate_active_result(payload, _case(), root)


def test_validate_active_result_rejects_non_relative_output_artifact(tmp_path: Path) -> None:
    root = tmp_path / "active"
    payload = _write_active_result(root)
    revision_path = root / "revision-000/result.json"
    revision = json.loads(revision_path.read_text(encoding="utf-8"))
    revision["execution"]["output_step"] = str(tmp_path / "private.step")
    revision_path.write_text(json.dumps(revision), encoding="utf-8")

    with pytest.raises(ActiveResultValidationError, match="output path"):
        validate_active_result(payload, _case(), root)
