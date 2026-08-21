from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from brep2code.backends import backend_profile
from brep2code.cases import CaseManifest
from brep2code.providers.task_contract import build_provider_task_contract
from brep2code.harness.active_results import ActiveResultValidationError, validate_active_result


class Stage1ContractError(ValueError):
    pass


CORE_CASES = (
    "box",
    "stage1_cylinder",
    "block_with_hole",
    "blind_hole_block",
    "filleted_box",
)


def load_stage1_contract(path: Path, catalog: tuple[CaseManifest, ...]) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Stage1ContractError("Stage 1 contract is unreadable") from exc
    required = {
        "schema_version",
        "experiment_id",
        "provider",
        "model",
        "retrieval_policy",
        "cases",
        "backend_profiles",
        "cohorts",
        "hosted_limits",
        "phases",
        "valid_attempt_threshold",
        "infrastructure_failure_rate_threshold",
    }
    if not isinstance(payload, dict) or set(payload) != required:
        raise Stage1ContractError("Stage 1 contract fields are invalid")
    if payload["schema_version"] != 1 or payload["retrieval_policy"] != "disabled":
        raise Stage1ContractError("Stage 1 identity or retrieval policy is invalid")
    if tuple(payload["cases"]) != CORE_CASES:
        raise Stage1ContractError("Stage 1 core case order is invalid")
    runtime_cases = {
        item.case.case_id
        for manifest in catalog
        if manifest.split in {"smoke", "train"}
        for item in manifest.cases
    }
    if not set(CORE_CASES).issubset(runtime_cases):
        raise Stage1ContractError("Stage 1 core case is not runtime-loadable")
    profiles = payload["backend_profiles"]
    if profiles != ["cadquery_v1", "ocp_v1"]:
        raise Stage1ContractError("Stage 1 backend profile order is invalid")
    for profile_id in profiles:
        backend_profile(profile_id)
        build_provider_task_contract(profile_id, "disabled", contract_version=1)
    _validate_cohorts(payload["cohorts"])
    _validate_hosted_limits(payload["hosted_limits"])
    _validate_phases(payload["phases"])
    threshold = payload["valid_attempt_threshold"]
    if (
        not isinstance(threshold, (int, float))
        or isinstance(threshold, bool)
        or not 0.9 <= threshold <= 1
    ):
        raise Stage1ContractError("Stage 1 valid-attempt threshold is invalid")
    failure_threshold = payload["infrastructure_failure_rate_threshold"]
    if (
        not isinstance(failure_threshold, (int, float))
        or isinstance(failure_threshold, bool)
        or not 0 < failure_threshold <= 1
    ):
        raise Stage1ContractError("Stage 1 infrastructure-failure threshold is invalid")
    return payload


def _validate_cohorts(value: Any) -> None:
    if not isinstance(value, dict) or set(value) != {"first_shot", "bounded_repair"}:
        raise Stage1ContractError("Stage 1 cohorts are invalid")
    expected = {
        "first_shot": {"model_requests": 1, "script_submissions": 1, "executions": 1, "repairs": 0},
        "bounded_repair": {
            "model_requests": 2,
            "script_submissions": 2,
            "executions": 2,
            "repairs": 1,
        },
    }
    for name, required in expected.items():
        cohort = value[name]
        if not isinstance(cohort, dict) or any(
            cohort.get(key) != item for key, item in required.items()
        ):
            raise Stage1ContractError(f"Stage 1 {name} cohort bounds are invalid")
        if cohort.get("probes") != 0 or cohort.get("retrievals") != 0:
            raise Stage1ContractError(f"Stage 1 {name} knowledge surface is invalid")


def _validate_phases(value: Any) -> None:
    if not isinstance(value, list) or [
        item.get("phase_id") for item in value if isinstance(item, dict)
    ] != [
        "contract_diagnostic",
        "cadquery_baseline",
        "ocp_contrast",
    ]:
        raise Stage1ContractError("Stage 1 phase order is invalid")
    for phase in value:
        if not isinstance(phase.get("replicates"), int) or phase["replicates"] < 1:
            raise Stage1ContractError("Stage 1 phase replicate count is invalid")


def _validate_hosted_limits(value: Any) -> None:
    expected = {
        "build_timeout_seconds": 20,
        "provider_timeout_seconds": 120,
        "max_retries": 0,
        "max_output_tokens": 4096,
        "max_total_tokens": 16000,
        "max_cost_usd": 0.02,
        "input_cost_per_million": 0.435,
        "output_cost_per_million": 0.87,
    }
    if value != expected:
        raise Stage1ContractError("Stage 1 hosted limits are invalid")


def build_stage1_report(
    contract: dict[str, Any],
    catalog: tuple[CaseManifest, ...],
    runs_root: Path,
    phase_id: str,
) -> dict[str, Any]:
    phase = next((item for item in contract["phases"] if item["phase_id"] == phase_id), None)
    if phase is None:
        raise Stage1ContractError("Stage 1 report phase is invalid")
    cases = {
        item.case.case_id: item
        for manifest in catalog
        for item in manifest.cases
    }
    expected = {
        (case_id, backend, cohort, replicate)
        for case_id in phase["cases"]
        for backend in phase["backend_profiles"]
        for cohort in phase["cohorts"]
        for replicate in range(1, phase["replicates"] + 1)
    }
    rows: dict[tuple[str, str, str, int], tuple[dict[str, Any], str | None]] = {}
    legacy_schema_v6 = 0
    for result_path in runs_root.rglob("result.json"):
        try:
            payload = json.loads(result_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise Stage1ContractError(f"Stage 1 result is unreadable: {result_path}") from exc
        if not isinstance(payload, dict) or payload.get("schema_version") != 6:
            continue
        identity = payload.get("stage1_identity")
        if identity is None:
            legacy_schema_v6 += 1
            continue
        if identity.get("experiment_id") != contract["experiment_id"]:
            continue
        if identity.get("phase_id") != phase_id:
            continue
        case_id = payload.get("case_id")
        if case_id not in cases:
            raise Stage1ContractError("Stage 1 result case identity drift")
        key = (case_id, payload["backend_profile"], identity["cohort"], identity["replicate"])
        if key not in expected:
            raise Stage1ContractError(f"Stage 1 result identity drift: {key!r}")
        if key in rows:
            raise Stage1ContractError(f"duplicate Stage 1 run identity: {key!r}")
        _validate_report_identity(payload, contract, identity["cohort"])
        validation_error = None
        try:
            validate_active_result(payload, cases[case_id], result_path.parent)
        except ActiveResultValidationError as exc:
            validation_error = str(exc)
        rows[key] = (payload, validation_error)
    missing = sorted(expected - set(rows))
    grouped: dict[str, dict[str, Any]] = {}
    classifications: dict[str, int] = {}
    totals = _empty_stage1_summary()
    validation_failures = []
    for key, (payload, validation_error) in sorted(rows.items()):
        classification = "harness" if validation_error is not None else _classify_stage1_result(payload)
        if validation_error is not None:
            validation_failures.append(
                {
                    "case_id": key[0],
                    "backend_profile": key[1],
                    "cohort": key[2],
                    "replicate": key[3],
                    "error": validation_error,
                }
            )
        classifications[classification] = classifications.get(classification, 0) + 1
        group_key = "/".join((key[2], key[0], key[1]))
        summary = grouped.setdefault(group_key, _empty_stage1_summary())
        _add_stage1_result(summary, payload, classification)
        _add_stage1_result(totals, payload, classification)
    run_count = totals["runs"]
    valid_rate = totals["valid_attempts"] / run_count if run_count else 0.0
    infra_failures = classifications.get("provider", 0) + classifications.get("harness", 0)
    failure_rate = infra_failures / run_count if run_count else 0.0
    complete = not missing and run_count == len(expected)
    thresholds_pass = (
        complete
        and valid_rate >= contract["valid_attempt_threshold"]
        and failure_rate < contract["infrastructure_failure_rate_threshold"]
    )
    return {
        "schema_version": 1,
        "experiment_id": contract["experiment_id"],
        "phase_id": phase_id,
        "expected_runs": len(expected),
        "missing_runs": [
            {"case_id": item[0], "backend_profile": item[1], "cohort": item[2], "replicate": item[3]}
            for item in missing
        ],
        "legacy_schema_v6_without_stage1_identity": legacy_schema_v6,
        "groups": grouped,
        "totals": totals,
        "stop_reasons": _counts(payload["stop_reason"] for payload, _ in rows.values()),
        "failure_classifications": classifications,
        "artifact_validation_failures": validation_failures,
        "judgment": {
            "complete": complete,
            "valid_attempt_rate": valid_rate,
            "infrastructure_failure_rate": failure_rate,
            "thresholds_pass": thresholds_pass,
            "phase_ready": thresholds_pass,
        },
    }


def _validate_report_identity(payload: dict[str, Any], contract: dict[str, Any], cohort: str) -> None:
    expected_contract = build_provider_task_contract(
        payload["backend_profile"], "disabled", contract_version=1
    )
    if (
        payload["provider"] != contract["provider"]
        or payload["model"] != contract["model"]
        or payload["retrieval_policy"] != contract["retrieval_policy"]
        or payload["budgets"] != contract["cohorts"][cohort]
        or payload["timeout_seconds"] != contract["hosted_limits"]["build_timeout_seconds"]
        or payload.get("task_contract_hash") != expected_contract.identity
    ):
        raise Stage1ContractError("Stage 1 result frozen identity drift")
    limits = contract["hosted_limits"]
    accounting = payload.get("provider_accounting")
    if accounting is not None and (
        accounting["ceilings"] != {
            "max_requests": contract["cohorts"][cohort]["model_requests"],
            "timeout_seconds": limits["provider_timeout_seconds"],
            "max_retries": limits["max_retries"],
            "max_output_tokens": limits["max_output_tokens"],
            "max_total_tokens": limits["max_total_tokens"],
            "max_cost_usd": limits["max_cost_usd"],
        }
        or accounting["pricing"] != {
            "input_cost_per_million": limits["input_cost_per_million"],
            "output_cost_per_million": limits["output_cost_per_million"],
        }
    ):
        raise Stage1ContractError("Stage 1 provider limits drift")


def _empty_stage1_summary() -> dict[str, Any]:
    return {name: 0 for name in (
        "runs", "valid_attempts", "passed", "requests", "repairs", "tokens"
    )} | {"cost_usd": 0.0}


def _add_stage1_result(summary: dict[str, Any], payload: dict[str, Any], classification: str) -> None:
    usage = payload["usage"]
    summary["runs"] += 1
    summary["valid_attempts"] += classification not in {"provider", "harness"}
    summary["passed"] += payload["state"] == "succeeded"
    summary["requests"] += usage["model_requests"]
    summary["repairs"] += usage["repairs"]
    summary["tokens"] += usage["tokens"]
    summary["cost_usd"] += usage["cost_usd"]


def _classify_stage1_result(payload: dict[str, Any]) -> str:
    if payload["state"] == "succeeded":
        return "pass"
    if payload["stop_reason"] == "provider_error":
        return "provider"
    if payload["stop_reason"] == "sandbox_unavailable":
        return "harness"
    feedback = next((item.get("feedback") for item in reversed(payload["trace"]) if item.get("feedback")), {})
    stage = feedback.get("stage") if isinstance(feedback, dict) else None
    if stage in {"geometry", "validation"}:
        return "geometry"
    if stage == "execution":
        return "generation" if "SyntaxError" in str(feedback.get("stderr", "")) else "execution"
    if stage == "generation":
        return "generation"
    if payload["state"] == "exhausted":
        return "budget"
    return "harness"


def _counts(values: Any) -> dict[str, int]:
    result: dict[str, int] = {}
    for value in values:
        result[value] = result.get(value, 0) + 1
    return result
