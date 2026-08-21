from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from brep2code.backends import backend_profile
from brep2code.cases import CaseManifest, ValidatedCase
from brep2code.harness.active_results import ActiveResultValidationError, validate_active_result
from brep2code.providers.task_contract import build_provider_task_contract


class StabilizationValidationError(ValueError):
    pass


_TASK_FIELDS = {
    "case_id",
    "unit",
    "initial_observations",
    "allowed_actions",
    "available_tools",
    "session_phase",
    "retrieval_policy",
    "backend_profile",
    "current_revision",
    "feedback",
    "tool_results",
    "turn_index",
}
_INTERNAL_KEYS = {
    "authorization",
    "budgets",
    "campaign",
    "ceilings",
    "cost_usd",
    "host_path",
    "provider_accounting",
    "provider_limits",
    "task_contract",
    "task_contract_hash",
    "timeout_seconds",
    "tokens",
    "usage",
}


def load_stabilization_contract(
    path: Path, catalog: tuple[CaseManifest, ...]
) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StabilizationValidationError("stabilization contract is unreadable") from exc
    required = {
        "schema_version",
        "experiment_id",
        "purpose",
        "result_schema_version",
        "task_contract_version",
        "prompt_version",
        "provider",
        "model",
        "retrieval_policy",
        "cases",
        "backend_profiles",
        "cohorts",
        "hosted_limits",
        "phases",
    }
    if not isinstance(payload, dict) or set(payload) != required:
        raise StabilizationValidationError("stabilization contract fields are invalid")
    if (
        payload["schema_version"] != 1
        or payload["experiment_id"] != "stage1-active-v4-stabilization-v1"
        or payload["purpose"] != "protocol_stabilization"
        or payload["result_schema_version"] != 7
        or payload["task_contract_version"] != 2
        or payload["prompt_version"] != "active-v4-no-retrieval"
        or payload["retrieval_policy"] != "disabled"
    ):
        raise StabilizationValidationError("stabilization protocol identity is invalid")
    if payload["cases"] != ["box", "block_with_hole"]:
        raise StabilizationValidationError("stabilization case order is invalid")
    runtime_cases = {
        item.case.case_id
        for manifest in catalog
        if manifest.split in {"smoke", "train"}
        for item in manifest.cases
    }
    if not set(payload["cases"]) <= runtime_cases:
        raise StabilizationValidationError("stabilization case is not runtime-loadable")
    if payload["backend_profiles"] != ["ocp_v1"]:
        raise StabilizationValidationError("stabilization backend profile is invalid")
    backend_profile("ocp_v1")
    build_provider_task_contract("ocp_v1", "disabled", contract_version=2)
    _validate_cohorts(payload["cohorts"])
    _validate_hosted_limits(payload["hosted_limits"])
    expected_phase = {
        "phase_id": "hosted_protocol_confirmation",
        "cases": ["box", "block_with_hole"],
        "backend_profiles": ["ocp_v1"],
        "cohorts": ["first_shot", "bounded_repair"],
        "replicates": 3,
    }
    if payload["phases"] != [expected_phase]:
        raise StabilizationValidationError("stabilization phase is invalid")
    return payload


def validate_outbound_projection(run_root: Path) -> dict[str, Any]:
    try:
        result = json.loads((run_root / "result.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StabilizationValidationError("stabilization result is unreadable") from exc
    if not isinstance(result, dict) or result.get("schema_version") != 7:
        raise StabilizationValidationError("outbound projection requires schema-v7 result")
    request_paths = sorted((run_root / "provider-exchanges").glob("attempt-*/request.json"))
    if not request_paths:
        raise StabilizationValidationError("provider request artifacts are missing")
    retry_requests = 0
    for request_path in request_paths:
        request_payload = _read_object(request_path)
        body = request_payload.get("body")
        if not isinstance(body, dict) or not isinstance(body.get("messages"), list):
            raise StabilizationValidationError("provider request body is invalid")
        messages = body["messages"]
        if len(messages) not in {2, 3}:
            raise StabilizationValidationError("provider message count is invalid")
        if [item.get("role") for item in messages[:2]] != ["system", "user"]:
            raise StabilizationValidationError("provider message roles are invalid")
        if len(messages) == 3:
            if messages[2].get("role") != "user" or "action JSON contract" not in str(
                messages[2].get("content")
            ):
                raise StabilizationValidationError("provider retry projection is invalid")
            retry_requests += 1
        try:
            task = json.loads(messages[1]["content"])
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise StabilizationValidationError("provider task projection is invalid") from exc
        _validate_task_projection(task, str(messages[0].get("content", "")))
    accounting = result.get("provider_accounting")
    if not isinstance(accounting, dict):
        raise StabilizationValidationError("provider accounting is missing")
    if accounting.get("http_attempts") != len(request_paths):
        raise StabilizationValidationError("provider request artifact count drift")
    if accounting.get("protocol_retries", 0) != retry_requests:
        raise StabilizationValidationError("provider protocol retry artifact drift")
    return {
        "status": "valid",
        "schema_version": 7,
        "http_attempts": len(request_paths),
        "protocol_retries": retry_requests,
        "model_visible_internal_fields": [],
    }


def build_stabilization_report(
    contract: dict[str, Any], catalog: tuple[CaseManifest, ...], runs_root: Path
) -> dict[str, Any]:
    phase = contract["phases"][0]
    expected = {
        (case_id, backend, cohort, replicate)
        for case_id in phase["cases"]
        for backend in phase["backend_profiles"]
        for cohort in phase["cohorts"]
        for replicate in range(1, phase["replicates"] + 1)
    }
    cases = {
        item.case.case_id: item
        for manifest in catalog
        for item in manifest.cases
    }
    rows: dict[tuple[str, str, str, int], dict[str, Any]] = {}
    classifications: dict[str, int] = {}
    groups: dict[str, dict[str, int | float]] = {}
    totals = _empty_summary()
    validation_failures: list[dict[str, Any]] = []
    projection_failures: list[dict[str, Any]] = []
    for result_path in runs_root.rglob("result.json"):
        payload = _read_object(result_path)
        identity = payload.get("stage1_identity")
        if not isinstance(identity, dict) or identity.get("experiment_id") != contract[
            "experiment_id"
        ]:
            continue
        key = (
            payload.get("case_id"),
            payload.get("backend_profile"),
            identity.get("cohort"),
            identity.get("replicate"),
        )
        if key not in expected or identity.get("phase_id") != phase["phase_id"]:
            raise StabilizationValidationError(f"stabilization result identity drift: {key!r}")
        if key in rows:
            raise StabilizationValidationError(f"duplicate stabilization identity: {key!r}")
        error = _validate_run(payload, cases[key[0]], result_path.parent, contract, key[2])
        if error is not None:
            validation_failures.append(_failure_row(key, error))
            classification = "controller_harness"
        else:
            try:
                validate_outbound_projection(result_path.parent)
            except StabilizationValidationError as exc:
                projection_failures.append(_failure_row(key, str(exc)))
                classification = "projection"
            else:
                classification = classify_stabilization_result(payload)
        classifications[classification] = classifications.get(classification, 0) + 1
        group_key = f"{key[2]}/{key[0]}"
        _add_summary(groups.setdefault(group_key, _empty_summary()), payload, classification)
        _add_summary(totals, payload, classification)
        rows[key] = payload
    missing = sorted(expected - set(rows))
    complete = not missing and len(rows) == len(expected)
    return {
        "schema_version": 1,
        "experiment_id": contract["experiment_id"],
        "phase_id": phase["phase_id"],
        "expected_runs": len(expected),
        "observed_runs": len(rows),
        "missing_runs": [_identity_row(item) for item in missing],
        "groups": groups,
        "totals": totals,
        "failure_classifications": classifications,
        "artifact_validation_failures": validation_failures,
        "projection_validation_failures": projection_failures,
        "judgment": {
            "complete": complete,
            "artifacts_valid": not validation_failures,
            "projections_valid": not projection_failures,
            "protocol_stable": complete and not validation_failures and not projection_failures,
            "stage1_exit_changed": False,
            "stage2_authorized": False,
        },
    }


def classify_stabilization_result(payload: dict[str, Any]) -> str:
    if payload.get("state") == "succeeded":
        return "pass"
    stop_reason = payload.get("stop_reason")
    if stop_reason == "provider_error":
        errors = " ".join(
            str(item.get("error", "")) for item in payload.get("trace", [])
        )
        return "provider_protocol" if "JSON contract" in errors else "provider_transport"
    if stop_reason in {"finish_without_verifier", "harness_policy"}:
        return "model_policy"
    if stop_reason == "sandbox_unavailable":
        return "harness_infrastructure"
    feedback = next(
        (
            item.get("feedback")
            for item in reversed(payload.get("trace", []))
            if item.get("feedback")
        ),
        {},
    )
    stage = feedback.get("stage") if isinstance(feedback, dict) else None
    if stage in {"geometry", "validation"}:
        return "geometry"
    if stage == "execution":
        return "generation" if "SyntaxError" in str(feedback.get("stderr", "")) else "execution"
    if stage == "generation":
        return "generation"
    if payload.get("state") == "exhausted":
        return "budget"
    return "controller_harness"


def _validate_task_projection(task: Any, prompt: str) -> None:
    if not isinstance(task, dict) or set(task) - _TASK_FIELDS:
        raise StabilizationValidationError("provider task fields are invalid")
    if set(task) & _INTERNAL_KEYS:
        raise StabilizationValidationError("provider task exposes internal fields")
    _reject_internal_keys(task)
    actions = task.get("allowed_actions")
    tools = task.get("available_tools")
    if not isinstance(actions, list) or not isinstance(tools, list):
        raise StabilizationValidationError("provider capability projection is invalid")
    if not actions or actions[-1] != "finish" or len(actions) != len(set(actions)):
        raise StabilizationValidationError("provider action projection is invalid")
    examples = {
        action
        for action in ("probe", "retrieve", "submit", "finish")
        if f'{{"action":"{action}"' in prompt
    }
    if examples != set(actions):
        raise StabilizationValidationError("provider prompt action projection drift")
    expected_tools = []
    if "probe" in actions:
        expected_tools.append("edge_candidates")
    if "retrieve" in actions:
        expected_tools.extend(("knowledge_search", "ocp_symbol"))
    if tools != expected_tools:
        raise StabilizationValidationError("provider tool projection drift")


def _reject_internal_keys(value: Any) -> None:
    if isinstance(value, dict):
        if set(value) & _INTERNAL_KEYS:
            raise StabilizationValidationError("provider task exposes internal fields")
        for item in value.values():
            _reject_internal_keys(item)
    elif isinstance(value, list):
        for item in value:
            _reject_internal_keys(item)


def _validate_run(
    payload: dict[str, Any],
    case: ValidatedCase,
    run_root: Path,
    contract: dict[str, Any],
    cohort: str,
) -> str | None:
    try:
        validate_active_result(payload, case, run_root)
        expected_contract = build_provider_task_contract("ocp_v1", "disabled")
        limits = contract["hosted_limits"]
        if (
            payload["schema_version"] != contract["result_schema_version"]
            or payload["prompt_version"] != contract["prompt_version"]
            or payload["task_contract_hash"] != expected_contract.identity
            or payload["provider"] != contract["provider"]
            or payload["model"] != contract["model"]
            or payload["retrieval_policy"] != contract["retrieval_policy"]
            or payload["backend_profile"] != "ocp_v1"
            or payload["budgets"] != contract["cohorts"][cohort]
            or payload["timeout_seconds"] != limits["build_timeout_seconds"]
        ):
            raise StabilizationValidationError("stabilization frozen identity drift")
        accounting = payload["provider_accounting"]
        expected_requests = contract["cohorts"][cohort]["model_requests"] * (
            1 + limits["max_retries"]
        )
        if accounting["ceilings"] != {
            "max_requests": expected_requests,
            "timeout_seconds": limits["provider_timeout_seconds"],
            "max_retries": limits["max_retries"],
            "max_output_tokens": limits["max_output_tokens"],
            "max_total_tokens": limits["max_total_tokens"],
            "max_cost_usd": limits["max_cost_usd"],
        } or accounting["pricing"] != {
            "input_cost_per_million": limits["input_cost_per_million"],
            "output_cost_per_million": limits["output_cost_per_million"],
        }:
            raise StabilizationValidationError("stabilization provider limits drift")
    except (ActiveResultValidationError, KeyError, StabilizationValidationError) as exc:
        return str(exc)
    return None


def _validate_cohorts(value: Any) -> None:
    expected = {
        "first_shot": {
            "model_requests": 1,
            "probes": 0,
            "retrievals": 0,
            "script_submissions": 1,
            "executions": 1,
            "repairs": 0,
            "tokens": 16000,
            "cost_usd": 0.02,
        },
        "bounded_repair": {
            "model_requests": 2,
            "probes": 0,
            "retrievals": 0,
            "script_submissions": 2,
            "executions": 2,
            "repairs": 1,
            "tokens": 16000,
            "cost_usd": 0.02,
        },
    }
    if value != expected:
        raise StabilizationValidationError("stabilization cohorts are invalid")


def _validate_hosted_limits(value: Any) -> None:
    expected = {
        "build_timeout_seconds": 20,
        "provider_timeout_seconds": 120,
        "max_retries": 1,
        "max_output_tokens": 4096,
        "max_total_tokens": 16000,
        "max_cost_usd": 0.02,
        "input_cost_per_million": 0.435,
        "output_cost_per_million": 0.87,
    }
    if value != expected:
        raise StabilizationValidationError("stabilization hosted limits are invalid")


def _read_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StabilizationValidationError(f"JSON artifact is unreadable: {path}") from exc
    if not isinstance(payload, dict):
        raise StabilizationValidationError(f"JSON artifact must be an object: {path}")
    return payload


def _identity_row(item: tuple[Any, Any, Any, Any]) -> dict[str, Any]:
    return {
        "case_id": item[0],
        "backend_profile": item[1],
        "cohort": item[2],
        "replicate": item[3],
    }


def _failure_row(item: tuple[Any, Any, Any, Any], error: str) -> dict[str, Any]:
    return {**_identity_row(item), "error": error}


def _empty_summary() -> dict[str, int | float]:
    return {
        "runs": 0,
        "passed": 0,
        "model_requests": 0,
        "http_attempts": 0,
        "protocol_retries": 0,
        "submissions": 0,
        "executions": 0,
        "repairs": 0,
        "tokens": 0,
        "cost_usd": 0.0,
    }


def _add_summary(
    summary: dict[str, int | float], payload: dict[str, Any], classification: str
) -> None:
    usage = payload.get("usage", {})
    accounting = payload.get("provider_accounting", {})
    summary["runs"] += 1
    summary["passed"] += classification == "pass"
    summary["model_requests"] += int(usage.get("model_requests", 0))
    summary["http_attempts"] += int(accounting.get("http_attempts", 0))
    summary["protocol_retries"] += int(accounting.get("protocol_retries", 0))
    summary["submissions"] += int(usage.get("script_submissions", 0))
    summary["executions"] += int(usage.get("executions", 0))
    summary["repairs"] += int(usage.get("repairs", 0))
    summary["tokens"] += int(usage.get("tokens", 0))
    summary["cost_usd"] += float(usage.get("cost_usd", 0.0))
