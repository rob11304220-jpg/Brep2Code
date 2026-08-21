from __future__ import annotations

import json
from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Any, Callable

from brep2code.backends import backend_profile
from brep2code.cases import CaseManifest, ValidatedCase
from brep2code.harness import ActiveBudgets, ActiveHarnessRunner, RetrievalPolicy
from brep2code.harness.active_results import ActiveResultValidationError, validate_active_result
from brep2code.providers import FakeActionProvider, ProviderExchangeArtifactError
from brep2code.providers.task_contract import build_provider_task_contract
from brep2code.stabilization import (
    StabilizationValidationError,
    classify_stabilization_result,
    validate_outbound_projection,
)


class Stage1V2ValidationError(ValueError):
    def __init__(self, message: str, *, category: str = "validation") -> None:
        super().__init__(message)
        self.category = category


@dataclass(frozen=True)
class Stage1V2RunOutcome:
    classification: str
    http_attempts: int
    tokens: int
    cost_usd: float
    artifact_valid: bool = True
    projection_valid: bool = True


CORE_CASES = (
    "box",
    "stage1_cylinder",
    "block_with_hole",
    "blind_hole_block",
    "filleted_box",
)
INFRASTRUCTURE_CLASSES = {
    "provider_transport",
    "provider_protocol",
    "controller_harness",
    "harness_infrastructure",
    "projection",
}


def load_stage1_v2_contract(path: Path, catalog: tuple[CaseManifest, ...]) -> dict[str, Any]:
    payload = _read_object(path, "Stage 1 v2 contract")
    return _validate_stage1_v2_payload(payload, catalog)


def _validate_stage1_v2_payload(
    payload: dict[str, Any], catalog: tuple[CaseManifest, ...]
) -> dict[str, Any]:
    required = {
        "schema_version",
        "experiment_id",
        "purpose",
        "prerequisite_experiment_id",
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
        "valid_attempt_threshold",
        "infrastructure_failure_rate_threshold",
    }
    if set(payload) != required:
        raise Stage1V2ValidationError("Stage 1 v2 contract fields are invalid")
    if (
        payload["schema_version"] != 1
        or payload["experiment_id"] != "stage1-no-knowledge-v2"
        or payload["purpose"] != "no_knowledge_baseline"
        or payload["prerequisite_experiment_id"] != "stage1-active-v4-stabilization-v1"
        or payload["result_schema_version"] != 7
        or payload["task_contract_version"] != 2
        or payload["prompt_version"] != "active-v4-no-retrieval"
        or payload["provider"] != "deepseek"
        or payload["model"] != "deepseek-v4-pro"
        or payload["retrieval_policy"] != "disabled"
    ):
        raise Stage1V2ValidationError("Stage 1 v2 protocol identity is invalid")
    if tuple(payload["cases"]) != CORE_CASES:
        raise Stage1V2ValidationError("Stage 1 v2 core case order is invalid")
    runtime_cases = {
        item.case.case_id
        for manifest in catalog
        if manifest.split in {"smoke", "train"}
        for item in manifest.cases
    }
    if not set(CORE_CASES) <= runtime_cases:
        raise Stage1V2ValidationError("Stage 1 v2 case is not runtime-loadable")
    if payload["backend_profiles"] != ["cadquery_v1", "ocp_v1"]:
        raise Stage1V2ValidationError("Stage 1 v2 backend profile order is invalid")
    for profile in payload["backend_profiles"]:
        backend_profile(profile)
        build_provider_task_contract(profile, "disabled", contract_version=2)
    _validate_cohorts(payload["cohorts"])
    _validate_limits(payload["hosted_limits"])
    _validate_phases(payload["phases"])
    if payload["valid_attempt_threshold"] != 0.9:
        raise Stage1V2ValidationError("Stage 1 v2 valid-attempt threshold is invalid")
    if payload["infrastructure_failure_rate_threshold"] != 0.1:
        raise Stage1V2ValidationError("Stage 1 v2 infrastructure threshold is invalid")
    return payload


def load_stage1_v3_contract(path: Path, catalog: tuple[CaseManifest, ...]) -> dict[str, Any]:
    payload = _read_object(path, "Stage 1 v3 contract")
    extras = {
        "execution_protocol_version",
        "supersedes_experiment_id",
        "aborted_report_sha256",
    }
    if not extras <= set(payload):
        raise Stage1V2ValidationError("Stage 1 v3 execution identity is incomplete")
    if (
        payload.get("experiment_id") != "stage1-no-knowledge-v3"
        or payload.get("execution_protocol_version") != 3
        or payload.get("supersedes_experiment_id") != "stage1-no-knowledge-v2"
        or payload.get("aborted_report_sha256")
        != "ABAA99C33579402C54FFEA6CCF22EA868CCD010C1DA2E064F8B41C2309F39133"
    ):
        raise Stage1V2ValidationError("Stage 1 v3 execution identity is invalid")
    base = {key: value for key, value in payload.items() if key not in extras}
    base["experiment_id"] = "stage1-no-knowledge-v2"
    _validate_stage1_v2_payload(base, catalog)
    return payload


def build_stage1_v3_readiness(
    contract: dict[str, Any],
    catalog: tuple[CaseManifest, ...],
    stabilization_report: Path,
    aborted_report: Path,
    baseline_root: Path,
    run_root: Path,
    backend_status: Callable[[str], tuple[bool, str, str | None]],
) -> dict[str, Any]:
    try:
        digest = hashlib.sha256(aborted_report.read_bytes()).hexdigest().upper()
    except OSError as exc:
        raise Stage1V2ValidationError("Stage 1 v3 aborted prerequisite is unreadable") from exc
    aborted = _read_object(aborted_report, "Stage 1 v3 aborted prerequisite")
    if (
        digest != contract["aborted_report_sha256"]
        or aborted.get("experiment_id") != contract["supersedes_experiment_id"]
        or aborted.get("judgment", {}).get("abort_status")
        != "aborted_infrastructure_failure"
        or aborted.get("judgment", {}).get("stage2_authorized") is not False
    ):
        raise Stage1V2ValidationError("Stage 1 v3 aborted prerequisite is invalid")
    plan = build_stage1_v2_cohort_readiness(
        contract,
        catalog,
        stabilization_report,
        baseline_root,
        run_root,
        backend_status,
    )
    plan["status"] = "ready_for_new_experiment_authorization_review"
    plan["execution_protocol_version"] = contract["execution_protocol_version"]
    plan["supersedes_experiment_id"] = contract["supersedes_experiment_id"]
    plan["aborted_report_sha256"] = digest
    return plan


def build_stage1_v2_preflight(
    contract: dict[str, Any],
    stabilization_report: Path,
    run_root: Path,
    backend_status: Callable[[str], tuple[bool, str, str | None]],
) -> dict[str, Any]:
    prerequisite = _read_object(stabilization_report, "stabilization report")
    judgment = prerequisite.get("judgment")
    if (
        prerequisite.get("experiment_id") != contract["prerequisite_experiment_id"]
        or prerequisite.get("expected_runs") != 12
        or prerequisite.get("observed_runs") != 12
        or prerequisite.get("missing_runs") != []
        or prerequisite.get("artifact_validation_failures") != []
        or prerequisite.get("projection_validation_failures") != []
        or not isinstance(judgment, dict)
        or judgment.get("protocol_stable") is not True
        or judgment.get("stage1_exit_changed") is not False
        or judgment.get("stage2_authorized") is not False
    ):
        raise Stage1V2ValidationError("Stage 1 v2 stabilization prerequisite is invalid")
    if run_root.exists():
        raise Stage1V2ValidationError("Stage 1 v2 run root must be fresh")
    backend_versions: dict[str, str] = {}
    for profile in contract["backend_profiles"]:
        ready, reason, version = backend_status(profile)
        if not ready or version is None:
            raise Stage1V2ValidationError(f"Stage 1 v2 backend is not ready: {reason}")
        backend_versions[profile] = version
    identities = expected_stage1_v2_identities(contract)
    limits = contract["hosted_limits"]
    first_shot = sum(item[2] == "first_shot" for item in identities)
    bounded_repair = len(identities) - first_shot
    max_http_attempts = first_shot * 2 + bounded_repair * 4
    return {
        "status": "ready_for_authorization_review",
        "experiment_id": contract["experiment_id"],
        "prerequisite_experiment_id": contract["prerequisite_experiment_id"],
        "expected_runs": len(identities),
        "backend_versions": backend_versions,
        "run_root": str(run_root),
        "network_requests": 0,
        "provider_configuration_read": False,
        "artifacts_created": False,
        "authorization_granted": False,
        "stage2_authorized": False,
        "maximum_scope": {
            "model_decisions": first_shot + bounded_repair * 2,
            "http_attempts": max_http_attempts,
            "tokens": len(identities) * limits["max_total_tokens"],
            "cost_usd": len(identities) * limits["max_cost_usd"],
        },
        "outbound_projection": {
            "allowed": [
                "case_id",
                "unit",
                "initial_observations",
                "allowed_actions",
                "available_tools",
                "session_phase",
                "retrieval_policy",
                "backend_profile",
                "current_revision",
                "bounded_tool_results",
                "typed_feedback",
            ],
            "excluded": [
                "numeric_limits",
                "usage",
                "provider_accounting",
                "authorization",
                "executor_configuration",
                "eval_references",
                "target_solutions",
                "private_oracles",
                "repository_files",
                "host_paths",
                "secrets",
            ],
        },
        "authorization_requirements": [
            "provider_endpoint_model",
            "all_80_run_identities",
            "controller_and_provider_limits",
            "token_prices_and_cost_ceiling",
            "exact_outbound_projection",
            "fresh_run_root",
        ],
    }


def expected_stage1_v2_identities(
    contract: dict[str, Any],
) -> set[tuple[str, str, str, int, str]]:
    return {
        (case_id, backend, cohort, replicate, phase["phase_id"])
        for phase in contract["phases"]
        for case_id in phase["cases"]
        for backend in phase["backend_profiles"]
        for cohort in phase["cohorts"]
        for replicate in range(1, phase["replicates"] + 1)
    }


def expected_stage1_v2_baselines(
    contract: dict[str, Any],
) -> list[tuple[str, str, str]]:
    """Return the full case/backend/cohort execution-readiness matrix."""
    return [
        (case_id, backend, cohort)
        for case_id in contract["cases"]
        for backend in contract["backend_profiles"]
        for cohort in contract["cohorts"]
    ]


def build_stage1_v2_fake_baselines(
    contract: dict[str, Any],
    catalog: tuple[CaseManifest, ...],
    baseline_root: Path,
) -> dict[str, Any]:
    """Run the complete deterministic fake readiness matrix through secure CAD execution."""
    if baseline_root.exists():
        raise Stage1V2ValidationError("Stage 1 v2 fake baseline root must be fresh")
    cases = {item.case.case_id: item for manifest in catalog for item in manifest.cases}
    completed: list[dict[str, Any]] = []
    for case_id, backend, cohort in expected_stage1_v2_baselines(contract):
        case = cases[case_id]
        run_root = baseline_root / case_id / backend / cohort
        nominal = case.case.root / "controls" / "nominal.py"
        try:
            script = nominal.read_text(encoding="utf-8")
        except OSError as exc:
            raise Stage1V2ValidationError("Stage 1 v2 nominal control is unreadable") from exc
        if backend == "cadquery_v1":
            script = _cadquery_fake_baseline_script(case_id)
        actions = [{"action": "submit", "submit": {"script": script}}]
        if cohort == "bounded_repair":
            actions.insert(
                0,
                {
                    "action": "submit",
                    "submit": {"script": "raise RuntimeError('repair fixture')\n"},
                },
            )
        budgets = ActiveBudgets(**contract["cohorts"][cohort])
        result = ActiveHarnessRunner(FakeActionProvider(actions)).run(
            case,
            run_root,
            budgets=budgets,
            timeout_seconds=contract["hosted_limits"]["build_timeout_seconds"],
            retrieval_policy=RetrievalPolicy.DISABLED,
            backend=backend,
        )
        payload = _read_object(run_root / "result.json", "Stage 1 v2 fake baseline")
        validate_active_result(payload, case, run_root)
        if result.state != "succeeded" or payload.get("provider") != "fake":
            raise Stage1V2ValidationError("Stage 1 v2 fake baseline did not succeed")
        if cohort == "bounded_repair" and payload["usage"]["repairs"] != 1:
            raise Stage1V2ValidationError("Stage 1 v2 repair baseline did not exercise repair")
        completed.append(
            {
                "case_id": case_id,
                "backend_profile": backend,
                "cohort": cohort,
                "result": str(run_root / "result.json"),
            }
        )
    return {
        "status": "passed",
        "experiment_id": contract["experiment_id"],
        "expected_baselines": len(expected_stage1_v2_baselines(contract)),
        "observed_baselines": len(completed),
        "network_requests": 0,
        "provider_configuration_read": False,
        "baselines": completed,
    }


def validate_stage1_v2_fake_baselines(
    contract: dict[str, Any],
    catalog: tuple[CaseManifest, ...],
    baseline_root: Path,
) -> dict[str, Any]:
    cases = {item.case.case_id: item for manifest in catalog for item in manifest.cases}
    failures: list[dict[str, str]] = []
    for case_id, backend, cohort in expected_stage1_v2_baselines(contract):
        result_path = baseline_root / case_id / backend / cohort / "result.json"
        try:
            payload = _read_object(result_path, "Stage 1 v2 fake baseline")
            validate_active_result(payload, cases[case_id], result_path.parent)
            expected_contract = build_provider_task_contract(
                backend, "disabled", contract_version=2
            )
            if (
                payload.get("provider") != "fake"
                or payload.get("state") != "succeeded"
                or payload.get("terminal") is not True
                or payload.get("backend_profile") != backend
                or payload.get("task_contract_hash") != expected_contract.identity
                or payload.get("budgets") != contract["cohorts"][cohort]
            ):
                raise Stage1V2ValidationError("fake baseline identity or outcome drift")
            if cohort == "bounded_repair" and payload["usage"]["repairs"] != 1:
                raise Stage1V2ValidationError("fake repair baseline did not exercise repair")
        except (ActiveResultValidationError, OSError, Stage1V2ValidationError) as exc:
            failures.append(
                {
                    "case_id": case_id,
                    "backend_profile": backend,
                    "cohort": cohort,
                    "error": str(exc),
                }
            )
    return {
        "expected": len(expected_stage1_v2_baselines(contract)),
        "passed": len(expected_stage1_v2_baselines(contract)) - len(failures),
        "failures": failures,
    }


def build_stage1_v2_cohort_readiness(
    contract: dict[str, Any],
    catalog: tuple[CaseManifest, ...],
    stabilization_report: Path,
    baseline_root: Path,
    run_root: Path,
    backend_status: Callable[[str], tuple[bool, str, str | None]],
) -> dict[str, Any]:
    plan = build_stage1_v2_preflight(
        contract,
        stabilization_report,
        run_root,
        backend_status,
    )
    baselines = validate_stage1_v2_fake_baselines(contract, catalog, baseline_root)
    if baselines["passed"] != baselines["expected"]:
        raise Stage1V2ValidationError("Stage 1 v2 fake baseline matrix is incomplete")
    identities = sorted(expected_stage1_v2_identities(contract), key=_identity_sort_key)
    if len(identities) != 80:
        raise Stage1V2ValidationError("Stage 1 v2 identity enumeration is incomplete")
    return {
        **plan,
        "status": "ready_for_provider_config_check_and_authorization",
        "fake_baselines": baselines,
        "identity_readiness": {
            "expected": 80,
            "ready": len(identities),
            "identities": [_identity_row(item) for item in identities],
        },
    }


def run_stage1_v2_cohort(
    contract: dict[str, Any],
    run_root: Path,
    execute: Callable[[tuple[str, str, str, int, str], Path], Stage1V2RunOutcome],
) -> dict[str, Any]:
    """Execute every frozen identity once, continuing only through terminal run failures."""
    if run_root.exists():
        raise Stage1V2ValidationError("Stage 1 v2 cohort run root must be fresh")
    identities = sorted(expected_stage1_v2_identities(contract), key=_identity_sort_key)
    completed: list[dict[str, Any]] = []
    totals = {"http_attempts": 0, "tokens": 0, "cost_usd": 0.0}
    maximum = {
        "http_attempts": 240,
        "tokens": 1_280_000,
        "cost_usd": 1.6,
    }
    terminal = {
        "pass",
        "generation",
        "geometry",
        "execution",
        "budget",
        "model_policy",
        "provider_transport",
        "provider_protocol",
        "controller_harness",
        "harness_infrastructure",
    }
    def record(identity, outcome):
        if not outcome.artifact_valid:
            raise Stage1V2ValidationError(
                f"Stage 1 v2 cohort artifact failure at {_identity_row(identity)!r}",
                category="artifact",
            )
        if not outcome.projection_valid:
            raise Stage1V2ValidationError(
                f"Stage 1 v2 cohort projection failure at {_identity_row(identity)!r}",
                category="projection",
            )
        if outcome.classification not in terminal:
            raise Stage1V2ValidationError("Stage 1 v2 cohort classification is invalid")
        if outcome.http_attempts < 0 or outcome.tokens < 0 or outcome.cost_usd < 0:
            raise Stage1V2ValidationError("Stage 1 v2 cohort accounting is invalid")
        totals["http_attempts"] += outcome.http_attempts
        totals["tokens"] += outcome.tokens
        totals["cost_usd"] += outcome.cost_usd
        if any(totals[name] > maximum[name] for name in maximum):
            raise Stage1V2ValidationError("Stage 1 v2 cohort aggregate ceiling exceeded")
        completed.append({**_identity_row(identity), "classification": outcome.classification})

    for identity in identities:
        identity_root = stage1_v2_identity_root(run_root, identity)
        try:
            outcome = execute(identity, identity_root)
        except Exception as exc:
            raise Stage1V2ValidationError(
                f"Stage 1 v2 cohort configuration failure at {_identity_row(identity)!r}",
                category=(
                    "artifact" if isinstance(exc, ProviderExchangeArtifactError) else "configuration"
                ),
            ) from exc
        record(identity, outcome)
    return {
        "status": "complete",
        "expected_runs": len(identities),
        "completed_runs": len(completed),
        "runs": completed,
        "accounting": totals,
        "maximum_scope": maximum,
        "stage2_authorized": False,
    }


def stage1_v2_identity_root(
    run_root: Path, identity: tuple[str, str, str, int, str]
) -> Path:
    case_id, backend, cohort, replicate, phase_id = identity
    return run_root / phase_id / case_id / backend / cohort / f"replicate-{replicate}"


def ordered_stage1_v2_identities(
    contract: dict[str, Any],
) -> list[tuple[str, str, str, int, str]]:
    return sorted(expected_stage1_v2_identities(contract), key=_identity_sort_key)


def _identity_sort_key(item: tuple[str, str, str, int, str]) -> tuple[int, int, int, int]:
    phase_order = {"cadquery_baseline": 0, "ocp_contrast": 1}
    case_order = {case_id: index for index, case_id in enumerate(CORE_CASES)}
    cohort_order = {"first_shot": 0, "bounded_repair": 1}
    return (phase_order[item[4]], case_order[item[0]], cohort_order[item[2]], item[3])


def _cadquery_fake_baseline_script(case_id: str) -> str:
    bodies = {
        "box": "shape = cq.Workplane('XY').box(10, 20, 30, centered=(False, False, False))",
        "stage1_cylinder": "shape = cq.Workplane('XY').circle(4).extrude(15)",
        "block_with_hole": (
            "block = cq.Workplane('XY').box(20, 20, 8, centered=(False, False, False))\n"
            "tool = cq.Workplane('XY').center(10, 10).circle(4).extrude(8)\n"
            "shape = block.cut(tool)"
        ),
        "blind_hole_block": (
            "block = cq.Workplane('XY').box(24, 18, 10, centered=(False, False, False))\n"
            "tool = cq.Workplane('XY').workplane(offset=4).center(12, 9).circle(3).extrude(6)\n"
            "shape = block.cut(tool)"
        ),
        "filleted_box": (
            "shape = cq.Workplane('XY').box(20, 16, 12, centered=(False, False, False))"
            ".edges('|X and <Y and <Z').fillet(2)"
        ),
    }
    try:
        body = bodies[case_id]
    except KeyError as exc:
        raise Stage1V2ValidationError("Stage 1 v2 CadQuery baseline case is unsupported") from exc
    return f"import cadquery as cq\n\n{body}\ncq.exporters.export(shape, 'output.step')\n"


def build_stage1_v2_report(
    contract: dict[str, Any], catalog: tuple[CaseManifest, ...], runs_root: Path
) -> dict[str, Any]:
    expected = expected_stage1_v2_identities(contract)
    cases = {item.case.case_id: item for manifest in catalog for item in manifest.cases}
    rows: dict[tuple[str, str, str, int, str], dict[str, Any]] = {}
    classifications: dict[str, int] = {}
    phases = {item["phase_id"]: _empty_summary() for item in contract["phases"]}
    totals = _empty_summary()
    artifact_failures: list[dict[str, Any]] = []
    projection_failures: list[dict[str, Any]] = []
    for result_path in runs_root.rglob("result.json"):
        payload = _read_object(result_path, "Stage 1 v2 result")
        identity = payload.get("stage1_identity")
        if (
            not isinstance(identity, dict)
            or identity.get("experiment_id") != contract["experiment_id"]
        ):
            continue
        key = (
            payload.get("case_id"),
            payload.get("backend_profile"),
            identity.get("cohort"),
            identity.get("replicate"),
            identity.get("phase_id"),
        )
        if key not in expected:
            raise Stage1V2ValidationError(f"Stage 1 v2 result identity drift: {key!r}")
        if key in rows:
            raise Stage1V2ValidationError(f"duplicate Stage 1 v2 identity: {key!r}")
        try:
            _validate_result(payload, cases[key[0]], result_path.parent, contract, key[2])
        except (ActiveResultValidationError, KeyError, Stage1V2ValidationError) as exc:
            classification = "controller_harness"
            artifact_failures.append(_failure_row(key, str(exc)))
        else:
            try:
                validate_outbound_projection(result_path.parent)
            except StabilizationValidationError as exc:
                classification = "projection"
                projection_failures.append(_failure_row(key, str(exc)))
            else:
                classification = classify_stabilization_result(payload)
        classifications[classification] = classifications.get(classification, 0) + 1
        _add_summary(phases[key[4]], payload, classification)
        _add_summary(totals, payload, classification)
        rows[key] = payload
    missing = sorted(expected - set(rows))
    phase_judgments = {
        phase_id: _judgment(
            summary, contract, complete=not any(item[4] == phase_id for item in missing)
        )
        for phase_id, summary in phases.items()
    }
    complete = not missing and len(rows) == len(expected)
    exit_ready = complete and all(item["thresholds_pass"] for item in phase_judgments.values())
    judgment = {
        "complete": complete,
        "exit_ready": exit_ready,
        "stage2_authorized": False,
    }
    if artifact_failures or projection_failures:
        judgment.update(
            {
                "aborted": True,
                "abort_status": "aborted_infrastructure_failure",
                "abort_reason": (
                    "nonterminal_provider_exchange_failure"
                    if any("must be terminal" in item["error"] for item in artifact_failures)
                    else "artifact_or_projection_validation_failure"
                ),
            }
        )
    return {
        "schema_version": 1,
        "experiment_id": contract["experiment_id"],
        "expected_runs": len(expected),
        "observed_runs": len(rows),
        "missing_runs": [_identity_row(item) for item in missing],
        "phases": phases,
        "phase_judgments": phase_judgments,
        "totals": totals,
        "failure_classifications": classifications,
        "artifact_validation_failures": artifact_failures,
        "projection_validation_failures": projection_failures,
        "judgment": judgment,
    }


def validate_stage1_v2_result(
    payload: dict[str, Any],
    case: ValidatedCase,
    run_root: Path,
    contract: dict[str, Any],
    cohort: str,
) -> None:
    _validate_result(payload, case, run_root, contract, cohort)


def _validate_result(
    payload: dict[str, Any],
    case: ValidatedCase,
    run_root: Path,
    contract: dict[str, Any],
    cohort: str,
) -> None:
    validate_active_result(payload, case, run_root)
    if payload.get("terminal") is not True:
        raise Stage1V2ValidationError("Stage 1 v2 result must be terminal")
    expected_contract = build_provider_task_contract(
        payload["backend_profile"], "disabled", contract_version=2
    )
    limits = contract["hosted_limits"]
    if (
        payload["schema_version"] != 7
        or payload["prompt_version"] != contract["prompt_version"]
        or payload["task_contract_hash"] != expected_contract.identity
        or payload["provider"] != contract["provider"]
        or payload["model"] != contract["model"]
        or payload["retrieval_policy"] != "disabled"
        or payload["budgets"] != contract["cohorts"][cohort]
        or payload["timeout_seconds"] != limits["build_timeout_seconds"]
    ):
        raise Stage1V2ValidationError("Stage 1 v2 frozen identity drift")
    expected_requests = contract["cohorts"][cohort]["model_requests"] * (1 + limits["max_retries"])
    accounting = payload["provider_accounting"]
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
        raise Stage1V2ValidationError("Stage 1 v2 provider limits drift")


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
        raise Stage1V2ValidationError("Stage 1 v2 cohorts are invalid")


def _validate_limits(value: Any) -> None:
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
        raise Stage1V2ValidationError("Stage 1 v2 hosted limits are invalid")


def _validate_phases(value: Any) -> None:
    expected = [
        {
            "phase_id": "cadquery_baseline",
            "cases": list(CORE_CASES),
            "backend_profiles": ["cadquery_v1"],
            "cohorts": ["first_shot", "bounded_repair"],
            "replicates": 5,
        },
        {
            "phase_id": "ocp_contrast",
            "cases": ["box", "block_with_hole", "filleted_box"],
            "backend_profiles": ["ocp_v1"],
            "cohorts": ["first_shot", "bounded_repair"],
            "replicates": 5,
        },
    ]
    if value != expected:
        raise Stage1V2ValidationError("Stage 1 v2 phases are invalid")


def _empty_summary() -> dict[str, int | float]:
    return {
        "runs": 0,
        "valid_attempts": 0,
        "passed": 0,
        "model_requests": 0,
        "http_attempts": 0,
        "protocol_retries": 0,
        "executions": 0,
        "repairs": 0,
        "tokens": 0,
        "cost_usd": 0.0,
        "infrastructure_failures": 0,
    }


def _add_summary(
    summary: dict[str, int | float], payload: dict[str, Any], classification: str
) -> None:
    usage = payload.get("usage", {})
    accounting = payload.get("provider_accounting", {})
    summary["runs"] += 1
    summary["valid_attempts"] += classification not in INFRASTRUCTURE_CLASSES
    summary["passed"] += classification == "pass"
    summary["model_requests"] += int(usage.get("model_requests", 0))
    summary["http_attempts"] += int(accounting.get("http_attempts", 0))
    summary["protocol_retries"] += int(accounting.get("protocol_retries", 0))
    summary["executions"] += int(usage.get("executions", 0))
    summary["repairs"] += int(usage.get("repairs", 0))
    summary["tokens"] += int(usage.get("tokens", 0))
    summary["cost_usd"] += float(usage.get("cost_usd", 0.0))
    summary["infrastructure_failures"] += classification in INFRASTRUCTURE_CLASSES


def _judgment(
    summary: dict[str, int | float], contract: dict[str, Any], *, complete: bool
) -> dict[str, Any]:
    runs = int(summary["runs"])
    valid_rate = float(summary["valid_attempts"]) / runs if runs else 0.0
    failure_rate = float(summary["infrastructure_failures"]) / runs if runs else 0.0
    thresholds_pass = (
        complete
        and valid_rate >= contract["valid_attempt_threshold"]
        and failure_rate < contract["infrastructure_failure_rate_threshold"]
    )
    return {
        "complete": complete,
        "valid_attempt_rate": valid_rate,
        "infrastructure_failure_rate": failure_rate,
        "thresholds_pass": thresholds_pass,
    }


def _read_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Stage1V2ValidationError(f"{label} is unreadable") from exc
    if not isinstance(payload, dict):
        raise Stage1V2ValidationError(f"{label} must be an object")
    return payload


def _identity_row(item: tuple[Any, Any, Any, Any, Any]) -> dict[str, Any]:
    return {
        "case_id": item[0],
        "backend_profile": item[1],
        "cohort": item[2],
        "replicate": item[3],
        "phase_id": item[4],
    }


def _failure_row(item: tuple[Any, Any, Any, Any, Any], error: str) -> dict[str, Any]:
    return {**_identity_row(item), "error": error}
