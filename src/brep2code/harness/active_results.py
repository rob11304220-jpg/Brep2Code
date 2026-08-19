from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from brep2code.cases import ValidatedCase
from brep2code.harness.active import ActiveBudgets
from brep2code.providers import ProviderLimits


class ActiveResultValidationError(ValueError):
    pass


_USAGE_KEYS = {
    "model_requests",
    "probes",
    "retrievals",
    "script_submissions",
    "executions",
    "repairs",
    "tokens",
    "cost_usd",
}
_FORBIDDEN_KEYS = {
    "api_key",
    "authorization",
    "dossier",
    "expected",
    "host_path",
    "input_step",
    "oracle",
    "reference_solution",
    "registry",
    "secret",
    "sha256",
}
_ACCOUNTING_FIELDS = {
    "http_attempts",
    "in_flight_requests",
    "tokens",
    "cost_usd",
    "pricing",
    "ceilings",
}


def validate_provider_accounting(
    value: Any,
    provider_limits: ProviderLimits,
    *,
    allow_terminal_overrun: bool = False,
) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _ACCOUNTING_FIELDS:
        raise ActiveResultValidationError("provider accounting fields are invalid")
    attempts = value["http_attempts"]
    in_flight = value["in_flight_requests"]
    if (
        not isinstance(attempts, int)
        or isinstance(attempts, bool)
        or attempts < 0
        or not isinstance(in_flight, int)
        or isinstance(in_flight, bool)
        or in_flight not in {0, 1}
        or in_flight > attempts
    ):
        raise ActiveResultValidationError("provider request accounting is invalid")
    tokens = value["tokens"]
    if not isinstance(tokens, dict) or set(tokens) != {"prompt", "completion", "total"}:
        raise ActiveResultValidationError("provider token accounting fields are invalid")
    if any(
        not isinstance(item, int) or isinstance(item, bool) or item < 0
        for item in tokens.values()
    ) or tokens["prompt"] + tokens["completion"] != tokens["total"]:
        raise ActiveResultValidationError("provider token accounting drift")
    cost = value["cost_usd"]
    if not isinstance(cost, (int, float)) or isinstance(cost, bool) or cost < 0:
        raise ActiveResultValidationError("provider cost accounting is invalid")
    expected_pricing = {
        "input_cost_per_million": provider_limits.input_cost_per_million,
        "output_cost_per_million": provider_limits.output_cost_per_million,
    }
    if value["pricing"] != expected_pricing:
        raise ActiveResultValidationError("provider pricing drift")
    expected_ceilings = {
        "max_requests": provider_limits.max_requests,
        "timeout_seconds": provider_limits.timeout_seconds,
        "max_retries": provider_limits.max_retries,
        "max_output_tokens": provider_limits.max_output_tokens,
        "max_total_tokens": provider_limits.max_total_tokens,
        "max_cost_usd": provider_limits.max_cost_usd,
    }
    if value["ceilings"] != expected_ceilings:
        raise ActiveResultValidationError("provider ceiling drift")
    if attempts > provider_limits.max_requests:
        raise ActiveResultValidationError("provider request accounting exceeds ceiling")
    if tokens["total"] > provider_limits.max_total_tokens and not allow_terminal_overrun:
        raise ActiveResultValidationError("provider token accounting exceeds ceiling")
    if cost > provider_limits.max_cost_usd and not allow_terminal_overrun:
        raise ActiveResultValidationError("provider cost accounting exceeds ceiling")
    expected_cost = (
        tokens["prompt"] * provider_limits.input_cost_per_million
        + tokens["completion"] * provider_limits.output_cost_per_million
    ) / 1_000_000
    if abs(float(cost) - expected_cost) > 1e-12:
        raise ActiveResultValidationError("provider cost accounting drift")
    return value


def validate_active_result(
    payload: dict[str, Any], case: ValidatedCase, result_root: Path
) -> None:
    required = {
        "schema_version",
        "mode",
        "case_id",
        "provider",
        "model",
        "budgets",
        "timeout_seconds",
        "checkpoint_index",
        "terminal",
        "continuation_policy",
        "state",
        "stop_reason",
        "usage",
        "trace",
    }
    schema_version = payload.get("schema_version") if isinstance(payload, dict) else None
    if schema_version == 4:
        required.add("provider_accounting")
    if schema_version == 5:
        required.update({"retrieval_policy", "catalog_id", "prompt_version"})
        if payload.get("provider") != "fake":
            required.add("provider_accounting")
    if not isinstance(payload, dict) or set(payload) != required:
        raise ActiveResultValidationError("active result fields are invalid")
    if schema_version not in {3, 4, 5} or payload["mode"] != "active":
        raise ActiveResultValidationError("active result identity is invalid")
    if schema_version == 3 and payload["provider"] != "fake":
        raise ActiveResultValidationError("hosted active result requires provider accounting")
    if payload["case_id"] != case.case.case_id:
        raise ActiveResultValidationError("active result case_id drift")
    if not isinstance(payload["provider"], str) or not payload["provider"]:
        raise ActiveResultValidationError("active result provider is invalid")
    if not isinstance(payload["model"], str) or not payload["model"]:
        raise ActiveResultValidationError("active result model is invalid")
    if not isinstance(payload["timeout_seconds"], int) or payload["timeout_seconds"] < 1:
        raise ActiveResultValidationError("active result timeout is invalid")
    if not isinstance(payload["checkpoint_index"], int) or payload["checkpoint_index"] < 0:
        raise ActiveResultValidationError("active result checkpoint index is invalid")
    terminal = payload["terminal"]
    if not isinstance(terminal, bool):
        raise ActiveResultValidationError("active result terminal marker is invalid")
    _validate_continuation_policy(
        payload["continuation_policy"], terminal, schema_version=schema_version
    )
    budgets = _validated_budgets(payload["budgets"])
    allow_terminal_overrun = (
        schema_version in {4, 5}
        and terminal
        and payload["state"] == "failed"
        and payload["stop_reason"] == "provider_error"
    )
    usage = _validated_usage(
        payload["usage"], budgets, allow_provider_overrun=allow_terminal_overrun
    )
    if schema_version == 5:
        _validate_retrieval_identity(payload)
    if schema_version in {4, 5} and "provider_accounting" in payload:
        accounting = payload["provider_accounting"]
        if not isinstance(accounting, dict):
            raise ActiveResultValidationError("provider accounting fields are invalid")
        try:
            limits = ProviderLimits(**accounting["ceilings"], **accounting["pricing"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ActiveResultValidationError("provider accounting limits are invalid") from exc
        validate_provider_accounting(
            accounting, limits, allow_terminal_overrun=allow_terminal_overrun
        )
        if accounting["tokens"]["total"] != usage["tokens"]:
            raise ActiveResultValidationError("provider/controller token accounting drift")
        if abs(float(accounting["cost_usd"]) - float(usage["cost_usd"])) > 1e-12:
            raise ActiveResultValidationError("provider/controller cost accounting drift")
        incomplete_request = not payload["terminal"] and payload["state"] == "synthesizing"
        minimum_attempts = usage["model_requests"] - (1 if incomplete_request else 0)
        if accounting["http_attempts"] < minimum_attempts:
            raise ActiveResultValidationError("provider request accounting drift")
    trace = payload["trace"]
    if not isinstance(trace, list) or not all(isinstance(item, dict) for item in trace):
        raise ActiveResultValidationError("active result trace is invalid")
    _reject_private_keys(payload)
    _validate_trace(trace, usage, payload["state"], payload["stop_reason"], terminal)
    _validate_revisions(result_root, usage, payload["state"], terminal)
    _validate_terminal(payload["state"], payload["stop_reason"], trace, terminal)


def _validate_retrieval_identity(payload: dict[str, Any]) -> None:
    policy = payload["retrieval_policy"]
    if policy == "disabled":
        if payload["catalog_id"] is not None or payload["prompt_version"] != "active-v2-no-retrieval":
            raise ActiveResultValidationError("disabled retrieval identity is invalid")
        if payload["budgets"].get("retrievals") != 0 or payload["usage"].get("retrievals") != 0:
            raise ActiveResultValidationError("disabled retrieval policy requires zero retrievals")
        if any(item.get("action") == "retrieve" for item in payload["trace"]):
            raise ActiveResultValidationError("disabled retrieval result contains retrieval trace")
    elif policy == "bounded_seed":
        if payload["catalog_id"] != "bounded-seed-v1" or payload["prompt_version"] != "active-v2-retrieval":
            raise ActiveResultValidationError("bounded retrieval identity is invalid")
    else:
        raise ActiveResultValidationError("active retrieval policy is invalid")


def _validated_budgets(value: Any) -> ActiveBudgets:
    if not isinstance(value, dict) or set(value) != _USAGE_KEYS:
        raise ActiveResultValidationError("active result budgets are invalid")
    try:
        return ActiveBudgets(**value)
    except (TypeError, ValueError) as exc:
        raise ActiveResultValidationError("active result budgets are invalid") from exc


def _validated_usage(
    value: Any,
    budgets: ActiveBudgets,
    *,
    allow_provider_overrun: bool = False,
) -> dict[str, int | float]:
    if not isinstance(value, dict) or set(value) != _USAGE_KEYS:
        raise ActiveResultValidationError("active result usage fields are invalid")
    for name in _USAGE_KEYS - {"cost_usd"}:
        item = value[name]
        if not isinstance(item, int) or isinstance(item, bool) or item < 0:
            raise ActiveResultValidationError(f"active result {name} usage is invalid")
    cost = value["cost_usd"]
    if not isinstance(cost, (int, float)) or isinstance(cost, bool) or cost < 0:
        raise ActiveResultValidationError("active result cost usage is invalid")
    for name in _USAGE_KEYS:
        if allow_provider_overrun and name in {"tokens", "cost_usd"}:
            continue
        if value[name] > getattr(budgets, name):
            raise ActiveResultValidationError(f"active result exceeds {name} budget")
    return value


def _validate_trace(
    trace: list[dict[str, Any]],
    usage: dict[str, int | float],
    state: Any,
    stop_reason: Any,
    terminal: bool,
) -> None:
    allowed_actions = {"probe", "retrieve", "submit", "finish", "provider"}
    if any(item.get("action") not in allowed_actions for item in trace):
        raise ActiveResultValidationError("active result trace action is invalid")
    counts = {
        "probes": sum(item.get("action") == "probe" for item in trace),
        "retrievals": sum(item.get("action") == "retrieve" for item in trace),
        "script_submissions": sum(item.get("action") == "submit" for item in trace),
    }
    for name, count in counts.items():
        progress_state = {"probes": "probing", "retrievals": "retrieving"}.get(name)
        if not terminal and state == progress_state and usage[name] - count in {0, 1}:
            continue
        if name == "script_submissions" and not terminal and state == "executing":
            if usage[name] - count != 1:
                raise ActiveResultValidationError(f"active result {name} trace drift")
            continue
        if count != usage[name]:
            raise ActiveResultValidationError(f"active result {name} trace drift")
    request_gap = usage["model_requests"] - len(trace)
    allowed_terminal_gap = (
        terminal and state == "exhausted" and stop_reason in {"token_budget", "cost_budget"}
    )
    valid_request_gap = request_gap == 0
    if allowed_terminal_gap:
        valid_request_gap = request_gap == 1
    elif not terminal and state in {"probing", "retrieving"}:
        valid_request_gap = request_gap in {0, 1}
    elif not terminal and state in {"synthesizing", "executing"}:
        valid_request_gap = request_gap == 1
    if not valid_request_gap:
        raise ActiveResultValidationError("active result model request trace drift")
    failed_submissions = sum(
        item.get("action") == "submit" and item.get("passed") is False for item in trace
    )
    repair_gap = failed_submissions - usage["repairs"]
    allowed_repair_gap = terminal and state == "exhausted" and stop_reason == "repair_budget"
    if repair_gap != (1 if allowed_repair_gap else 0):
        raise ActiveResultValidationError("active result repair accounting drift")


def _validate_revisions(
    result_root: Path,
    usage: dict[str, int | float],
    state: Any,
    terminal: bool,
) -> None:
    expected_count = int(usage["script_submissions"])
    revision_dirs = sorted(
        path for path in result_root.glob("revision-*") if path.is_dir()
    )
    expected_names = [f"revision-{index:03d}" for index in range(expected_count)]
    actual_names = [path.name for path in revision_dirs]
    allowed_names = [expected_names]
    if not terminal and state == "executing" and expected_names:
        allowed_names.append(expected_names[:-1])
    if actual_names not in allowed_names:
        raise ActiveResultValidationError("active result revision set drift")
    execution_count = 0
    for revision, expected_name in zip(
        revision_dirs, expected_names[: len(revision_dirs)], strict=True
    ):
        script = revision / "build.py"
        result = revision / "result.json"
        if not script.is_file() or not script.read_text(encoding="utf-8").strip():
            raise ActiveResultValidationError("active revision script is missing")
        artifact = _read_object(result)
        _reject_private_keys(artifact)
        if artifact.get("revision_id") != expected_name or artifact.get("workspace") != expected_name:
            raise ActiveResultValidationError("active revision identity drift")
        error = artifact.get("error")
        if artifact.get("status") == "execution" or "execution" in artifact or (
            isinstance(error, dict) and error.get("stage") == "sandbox"
        ):
            execution_count += 1
        execution = artifact.get("execution")
        if execution is not None:
            if not isinstance(execution, dict) or execution.get("output_step") not in {
                None,
                "output.step",
            }:
                raise ActiveResultValidationError("active revision output path is invalid")
    execution_gap = execution_count - usage["executions"]
    if execution_gap != (1 if not terminal and state == "executing" and execution_gap == 1 else 0):
        raise ActiveResultValidationError("active result execution accounting drift")


def _validate_terminal(
    state: Any, stop_reason: Any, trace: list[dict[str, Any]], terminal: bool
) -> None:
    terminal_states = {"succeeded", "failed", "exhausted"}
    progress_states = {"observing", "probing", "retrieving", "synthesizing", "executing", "repairing"}
    if not terminal:
        if state not in progress_states or stop_reason is not None:
            raise ActiveResultValidationError("active result progress state is invalid")
        return
    if state not in terminal_states or not isinstance(stop_reason, str):
        raise ActiveResultValidationError("active result terminal state is invalid")
    if state == "succeeded":
        if stop_reason != "passed" or not trace or trace[-1].get("passed") is not True:
            raise ActiveResultValidationError("active result success terminal drift")
    elif stop_reason == "passed":
        raise ActiveResultValidationError("active result failure terminal drift")


def _validate_continuation_policy(value: Any, terminal: bool, *, schema_version: int) -> None:
    if not isinstance(value, dict) or set(value) != {
        "eligible",
        "implemented",
        "requirements",
    }:
        raise ActiveResultValidationError("active result continuation policy is invalid")
    expected_requirements = [
        "same_case",
        "same_budgets",
    ]
    if schema_version == 5:
        expected_requirements.append("same_retrieval_policy")
    expected_requirements.extend(["remaining_model_requests", "existing_revision_root"])
    if (
        value["eligible"] is not (not terminal)
        or value["implemented"] is not True
        or value["requirements"] != expected_requirements
    ):
        raise ActiveResultValidationError("active result continuation policy drift")


def _reject_private_keys(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() in _FORBIDDEN_KEYS:
                raise ActiveResultValidationError("active result contains a private field")
            _reject_private_keys(item)
    elif isinstance(value, list):
        for item in value:
            _reject_private_keys(item)


def _read_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ActiveResultValidationError("active revision result is unreadable") from exc
    if not isinstance(value, dict):
        raise ActiveResultValidationError("active revision result must be an object")
    return value
