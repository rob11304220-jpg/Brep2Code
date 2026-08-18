from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from brep2code.capabilities import CAPABILITY_LEVEL_SET
from brep2code.cases import ValidatedCase, validate_catalog
from brep2code.dossiers import DEVELOPMENT_COHORT


CAMPAIGN_SCHEMA_VERSION = 1
CAMPAIGN_CASE_KEYS = frozenset(
    {
        "case_id",
        "mode",
        "capability_level",
        "mechanism",
        "kernel_properties",
        "sequence",
        "difficulty",
    }
)
LADDER_KEYS = frozenset(
    {"capability_level", "label", "case_ids", "mechanisms", "minimum_cases"}
)
POLICY_KEYS = frozenset(
    {
        "provider",
        "model",
        "executor",
        "max_rounds",
        "build_timeout_seconds",
        "max_requests",
        "case_max_requests",
        "provider_timeout_seconds",
        "max_retries",
        "max_output_tokens",
        "max_total_tokens",
        "case_max_total_tokens",
        "max_cost_usd",
        "case_max_cost_usd",
        "input_cost_per_million",
        "output_cost_per_million",
    }
)
CONTROL_KEYS = frozenset({"case_id", "control_variant", "expected_result", "failure_class"})
CONTROL_RESULT_FAILURE_CLASSES = frozenset(
    {"pass", "generation", "execution", "geometry", "provider", "budget", "harness"}
)
CONTROL_POLICY_KEYS = frozenset(
    {
        "max_rounds",
        "build_timeout_seconds",
        "max_requests",
        "case_max_requests",
        "max_total_tokens",
        "case_max_total_tokens",
        "max_cost_usd",
        "case_max_cost_usd",
    }
)
HELD_OUT_KEYS = frozenset(
    {"case_id", "expected_result", "failure_class", "fixture_sha256", "expected", "gate_oracles"}
)
HELD_OUT_POLICY_KEYS = CONTROL_POLICY_KEYS
RESULT_FAILURE_CLASSES = frozenset(
    {"pass", "generation", "execution", "geometry", "provider", "budget", "harness"}
)


class CampaignValidationError(ValueError):
    """Raised when a campaign contract cannot be admitted."""


@dataclass(frozen=True)
class CampaignCase:
    case_id: str
    mode: str
    capability_level: str
    mechanism: str
    kernel_properties: tuple[str, ...]
    sequence: tuple[str, ...]
    difficulty: int


@dataclass(frozen=True)
class ControlCase:
    case_id: str
    control_variant: str
    expected_result: str
    failure_class: str


@dataclass(frozen=True)
class HeldOutCase:
    case_id: str
    expected_result: str
    failure_class: str
    fixture_sha256: str
    expected: dict[str, Any]
    gate_oracles: dict[str, Any]


@dataclass(frozen=True)
class CampaignContract:
    campaign_id: str
    objective: str
    provider_policy: dict[str, Any]
    capability_ladder: tuple[dict[str, Any], ...]
    cases: tuple[CampaignCase, ...]
    control_policy: dict[str, Any]
    control_matrix: tuple[ControlCase, ...]
    held_out_policy: dict[str, Any]
    held_out_matrix: tuple[HeldOutCase, ...]
    sha256: str

    @property
    def runtime_cases(self) -> tuple[CampaignCase, ...]:
        return tuple(item for item in self.cases if item.mode == "runtime")

    def select_case(self, case_id: str, *, runtime_only: bool = False) -> CampaignCase:
        matches = [item for item in self.cases if item.case_id == case_id]
        if runtime_only:
            matches = [item for item in matches if item.mode == "runtime"]
        if len(matches) != 1:
            scope = "runtime campaign" if runtime_only else "campaign"
            raise CampaignValidationError(f"expected exactly one case named {case_id!r} in {scope}")
        return matches[0]


def load_campaign_contract(path: Path, cases_root: Path) -> CampaignContract:
    payload = _load_json_object(path)
    manifests = validate_catalog(cases_root)
    catalog = {
        item.case.case_id: item
        for manifest in manifests
        for item in manifest.cases
    }
    return _validate_contract(payload, catalog)


def canonical_json(payload: object) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def contract_sha256(payload: dict[str, Any]) -> str:
    return sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def _validate_contract(
    payload: dict[str, Any], catalog: dict[str, ValidatedCase]
) -> CampaignContract:
    expected_keys = frozenset(
        {
            "schema_version",
            "campaign_id",
            "objective",
            "provider_policy",
            "control_policy",
            "held_out_policy",
            "capability_ladder",
            "cases",
            "control_matrix",
            "held_out_matrix",
        }
    )
    _require_exact_keys(payload, expected_keys, "campaign contract")
    if payload["schema_version"] != CAMPAIGN_SCHEMA_VERSION:
        raise CampaignValidationError("campaign schema_version must equal 1")
    campaign_id = _required_string(payload, "campaign_id")
    objective = _required_string(payload, "objective")
    policy = _validate_policy(payload["provider_policy"])
    control_policy = _validate_control_policy(payload["control_policy"])
    held_out_policy = _validate_held_out_policy(payload["held_out_policy"])
    rows = _validate_cases(payload["cases"], catalog)
    ladder = _validate_ladder(payload["capability_ladder"], rows)
    control_matrix = _validate_control_matrix(payload["control_matrix"], rows, catalog)
    held_out_matrix = _validate_held_out_matrix(payload["held_out_matrix"], rows, catalog)
    if control_policy["max_requests"] < len(control_matrix) * control_policy["case_max_requests"]:
        raise CampaignValidationError("control policy max_requests must cover every control")
    if control_policy["max_total_tokens"] < len(control_matrix) * control_policy["case_max_total_tokens"]:
        raise CampaignValidationError("control policy max_total_tokens must cover every control")
    if control_policy["max_cost_usd"] + 1e-12 < len(control_matrix) * control_policy["case_max_cost_usd"]:
        raise CampaignValidationError("control policy max_cost_usd must cover every control")
    if held_out_policy["max_requests"] < len(held_out_matrix) * held_out_policy["case_max_requests"]:
        raise CampaignValidationError("held_out policy max_requests must cover every case")
    if held_out_policy["max_total_tokens"] < len(held_out_matrix) * held_out_policy["case_max_total_tokens"]:
        raise CampaignValidationError("held_out policy max_total_tokens must cover every case")
    if held_out_policy["max_cost_usd"] + 1e-12 < len(held_out_matrix) * held_out_policy["case_max_cost_usd"]:
        raise CampaignValidationError("held_out policy max_cost_usd must cover every case")
    runtime_count = len([row for row in rows if row.mode == "runtime"])
    required_requests = runtime_count * policy["case_max_requests"]
    if policy["max_requests"] < required_requests:
        raise CampaignValidationError("campaign max_requests must cover every case budget")
    if policy["max_total_tokens"] < runtime_count * policy["case_max_total_tokens"]:
        raise CampaignValidationError("campaign max_total_tokens must cover every case budget")
    required_cost = runtime_count * policy["case_max_cost_usd"]
    if policy["max_cost_usd"] + 1e-12 < required_cost:
        raise CampaignValidationError("campaign max_cost_usd must cover every case budget")
    return CampaignContract(
        campaign_id=campaign_id,
        objective=objective,
        provider_policy=policy,
        capability_ladder=tuple(ladder),
        cases=tuple(rows),
        control_policy=control_policy,
        control_matrix=tuple(control_matrix),
        held_out_policy=held_out_policy,
        held_out_matrix=tuple(held_out_matrix),
        sha256=contract_sha256(payload),
    )


def _validate_policy(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CampaignValidationError("provider_policy must be an object")
    _require_exact_keys(value, POLICY_KEYS, "provider_policy")
    if value["provider"] != "deepseek":
        raise CampaignValidationError("campaign provider must be deepseek")
    if not isinstance(value["model"], str) or not value["model"]:
        raise CampaignValidationError("campaign model must be a non-empty string")
    if value["executor"] != "wsl-bwrap":
        raise CampaignValidationError("campaign executor must be wsl-bwrap")
    for key in (
        "max_rounds",
        "build_timeout_seconds",
        "max_requests",
        "case_max_requests",
        "provider_timeout_seconds",
        "max_output_tokens",
        "max_total_tokens",
        "case_max_total_tokens",
    ):
        if not isinstance(value[key], int) or isinstance(value[key], bool) or value[key] < 1:
            raise CampaignValidationError(f"provider_policy.{key} must be a positive integer")
    if not isinstance(value["max_retries"], int) or isinstance(value["max_retries"], bool) or value["max_retries"] < 0:
        raise CampaignValidationError("provider_policy.max_retries must be a non-negative integer")
    for key in (
        "max_cost_usd",
        "case_max_cost_usd",
        "input_cost_per_million",
        "output_cost_per_million",
    ):
        if not isinstance(value[key], int | float) or isinstance(value[key], bool) or value[key] <= 0:
            raise CampaignValidationError(f"provider_policy.{key} must be positive")
    if value["case_max_requests"] != value["max_rounds"]:
        raise CampaignValidationError("case_max_requests must equal max_rounds")
    return dict(value)


def _validate_control_policy(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CampaignValidationError("control_policy must be an object")
    _require_exact_keys(value, CONTROL_POLICY_KEYS, "control_policy")
    for key in (
        "max_rounds",
        "build_timeout_seconds",
        "max_requests",
        "case_max_requests",
        "max_total_tokens",
        "case_max_total_tokens",
    ):
        if not isinstance(value[key], int) or isinstance(value[key], bool) or value[key] < 1:
            raise CampaignValidationError(f"control_policy.{key} must be a positive integer")
    for key in ("max_cost_usd", "case_max_cost_usd"):
        if not isinstance(value[key], int | float) or isinstance(value[key], bool) or value[key] <= 0:
            raise CampaignValidationError(f"control_policy.{key} must be positive")
    if value["case_max_requests"] != value["max_rounds"]:
        raise CampaignValidationError("control_policy.case_max_requests must equal max_rounds")
    if value["max_total_tokens"] < value["case_max_total_tokens"]:
        raise CampaignValidationError("control_policy.max_total_tokens must cover one control")
    if value["max_cost_usd"] < value["case_max_cost_usd"]:
        raise CampaignValidationError("control_policy.max_cost_usd must cover one control")
    return dict(value)


def _validate_held_out_policy(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CampaignValidationError("held_out_policy must be an object")
    _require_exact_keys(value, HELD_OUT_POLICY_KEYS, "held_out_policy")
    for key in (
        "max_rounds",
        "build_timeout_seconds",
        "max_requests",
        "case_max_requests",
        "max_total_tokens",
        "case_max_total_tokens",
    ):
        if not isinstance(value[key], int) or isinstance(value[key], bool) or value[key] < 1:
            raise CampaignValidationError(f"held_out_policy.{key} must be a positive integer")
    for key in ("max_cost_usd", "case_max_cost_usd"):
        if not isinstance(value[key], int | float) or isinstance(value[key], bool) or value[key] <= 0:
            raise CampaignValidationError(f"held_out_policy.{key} must be positive")
    if value["case_max_requests"] != value["max_rounds"]:
        raise CampaignValidationError("held_out_policy.case_max_requests must equal max_rounds")
    if value["max_total_tokens"] < value["case_max_total_tokens"]:
        raise CampaignValidationError("held_out_policy.max_total_tokens must cover one case")
    if value["max_cost_usd"] < value["case_max_cost_usd"]:
        raise CampaignValidationError("held_out_policy.max_cost_usd must cover one case")
    return dict(value)


def _validate_cases(value: Any, catalog: dict[str, ValidatedCase]) -> list[CampaignCase]:
    if not isinstance(value, list) or not value:
        raise CampaignValidationError("campaign cases must be a non-empty array")
    rows: list[CampaignCase] = []
    seen: set[str] = set()
    for raw in value:
        if not isinstance(raw, dict):
            raise CampaignValidationError("campaign case entries must be objects")
        _require_exact_keys(raw, CAMPAIGN_CASE_KEYS, "campaign case")
        case_id = _required_string(raw, "case_id")
        if case_id in seen:
            raise CampaignValidationError(f"campaign contains duplicate case ID {case_id!r}")
        seen.add(case_id)
        validated = catalog.get(case_id)
        if validated is None:
            raise CampaignValidationError(f"campaign references unknown case {case_id!r}")
        mode = raw.get("mode")
        expected_mode = "held_out" if validated.case.split == "eval" else "runtime"
        if mode != expected_mode:
            raise CampaignValidationError(f"campaign mode for {case_id!r} must be {expected_mode!r}")
        for key in ("capability_level", "mechanism"):
            if raw[key] != validated.metadata[key]:
                raise CampaignValidationError(f"campaign {key} drift for {case_id!r}")
        properties = _string_array(raw["kernel_properties"], f"campaign {case_id}.kernel_properties")
        sequence = _string_array(raw["sequence"], f"campaign {case_id}.sequence")
        if properties != tuple(validated.metadata["kernel_properties"]):
            raise CampaignValidationError(f"campaign kernel_properties drift for {case_id!r}")
        if sequence != tuple(validated.metadata["sequence"]):
            raise CampaignValidationError(f"campaign sequence drift for {case_id!r}")
        difficulty = raw["difficulty"]
        if difficulty != validated.metadata["difficulty"]:
            raise CampaignValidationError(f"campaign difficulty drift for {case_id!r}")
        rows.append(
            CampaignCase(
                case_id=case_id,
                mode=mode,
                capability_level=raw["capability_level"],
                mechanism=raw["mechanism"],
                kernel_properties=properties,
                sequence=sequence,
                difficulty=difficulty,
            )
        )
    if not any(row.mode == "runtime" for row in rows):
        raise CampaignValidationError("campaign must contain at least one runtime case")
    return rows


def _validate_control_matrix(
    value: Any,
    rows: list[CampaignCase],
    catalog: dict[str, ValidatedCase],
) -> list[ControlCase]:
    if not isinstance(value, list) or not value:
        raise CampaignValidationError("control_matrix must be a non-empty array")
    expected_keys = {
        (row.case_id, variant)
        for row in rows
        for variant in DEVELOPMENT_COHORT
    }
    seen: set[tuple[str, str]] = set()
    controls: list[ControlCase] = []
    for raw in value:
        if not isinstance(raw, dict):
            raise CampaignValidationError("control_matrix entries must be objects")
        _require_exact_keys(raw, CONTROL_KEYS, "control_matrix entry")
        case_id = _required_string(raw, "case_id")
        variant = _required_string(raw, "control_variant")
        key = (case_id, variant)
        if key in seen:
            raise CampaignValidationError(f"control_matrix contains duplicate control {key!r}")
        seen.add(key)
        validated = catalog.get(case_id)
        if validated is None:
            raise CampaignValidationError(f"control_matrix references unknown case {case_id!r}")
        if variant not in DEVELOPMENT_COHORT:
            raise CampaignValidationError(f"control variant {variant!r} is invalid")
        dossier = validated.dossier or {}
        harness = dossier.get("harness_assets") if isinstance(dossier, dict) else None
        dossier_controls = harness.get("controls") if isinstance(harness, dict) else None
        matching = [item for item in dossier_controls or [] if item.get("variant") == variant]
        if len(matching) != 1:
            raise CampaignValidationError(f"dossier has no unique {variant!r} control for {case_id!r}")
        control = matching[0]
        if raw["expected_result"] != control["expected_result"]:
            raise CampaignValidationError(f"control expected_result drift for {case_id!r}/{variant}")
        if raw["failure_class"] != control["failure_class"]:
            raise CampaignValidationError(f"control failure_class drift for {case_id!r}/{variant}")
        controls.append(
            ControlCase(
                case_id=case_id,
                control_variant=variant,
                expected_result=raw["expected_result"],
                failure_class=raw["failure_class"],
            )
        )
    if seen != expected_keys:
        missing = sorted(expected_keys - seen)
        extra = sorted(seen - expected_keys)
        raise CampaignValidationError(
            f"control_matrix must cover every campaign case and cohort exactly once; "
            f"missing={missing}, extra={extra}"
        )
    return controls


def _validate_held_out_matrix(
    value: Any,
    rows: list[CampaignCase],
    catalog: dict[str, ValidatedCase],
) -> list[HeldOutCase]:
    if not isinstance(value, list) or not value:
        raise CampaignValidationError("held_out_matrix must be a non-empty array")
    expected_ids = {row.case_id for row in rows if row.mode == "held_out"}
    seen: set[str] = set()
    matrix: list[HeldOutCase] = []
    for raw in value:
        if not isinstance(raw, dict):
            raise CampaignValidationError("held_out_matrix entries must be objects")
        _require_exact_keys(raw, HELD_OUT_KEYS, "held_out_matrix entry")
        case_id = _required_string(raw, "case_id")
        if case_id in seen:
            raise CampaignValidationError(f"held_out_matrix contains duplicate case {case_id!r}")
        seen.add(case_id)
        campaign_case = next((row for row in rows if row.case_id == case_id), None)
        if campaign_case is None:
            raise CampaignValidationError(f"held_out_matrix references unknown case {case_id!r}")
        if campaign_case.mode != "held_out":
            raise CampaignValidationError(f"held_out_matrix case {case_id!r} is not held out")
        validated = catalog[case_id]
        harness = (validated.dossier or {}).get("harness_assets", {})
        fixture = harness.get("held_out_fixture")
        if not isinstance(fixture, dict):
            raise CampaignValidationError(f"held-out dossier fixture is missing for {case_id!r}")
        if raw["fixture_sha256"] != fixture["sha256"]:
            raise CampaignValidationError(f"held-out fixture hash drift for {case_id!r}")
        if raw["expected_result"] != fixture["expected_result"]:
            raise CampaignValidationError(f"held-out expected_result drift for {case_id!r}")
        if raw["failure_class"] != fixture["failure_class"]:
            raise CampaignValidationError(f"held-out failure_class drift for {case_id!r}")
        if raw["expected"] != validated.metadata["expected"]:
            raise CampaignValidationError(f"held-out expected geometry drift for {case_id!r}")
        if raw["gate_oracles"] != harness["gate_oracles"]:
            raise CampaignValidationError(f"held-out gate oracle drift for {case_id!r}")
        matrix.append(
            HeldOutCase(
                case_id=case_id,
                expected_result=raw["expected_result"],
                failure_class=raw["failure_class"],
                fixture_sha256=raw["fixture_sha256"],
                expected=raw["expected"],
                gate_oracles=raw["gate_oracles"],
            )
        )
    if seen != expected_ids:
        raise CampaignValidationError(
            "held_out_matrix must cover every held-out campaign case exactly once; "
            f"missing={sorted(expected_ids - seen)}, extra={sorted(seen - expected_ids)}"
        )
    return matrix


def validate_control_matrix_result(
    payload: dict[str, Any], contract: CampaignContract
) -> None:
    """Validate a completed control-matrix artifact against its frozen contract."""
    required = {
        "artifact",
        "campaign_id",
        "contract_sha256",
        "provider",
        "control_policy",
        "accounting_scope",
        "provider_accounting",
        "provider_requests",
        "status",
        "stop_reason",
        "cases",
        "control_report",
    }
    if not isinstance(payload, dict) or not required <= set(payload):
        raise CampaignValidationError("control matrix result is missing required fields")
    if payload["artifact"] != "control_matrix":
        raise CampaignValidationError("control matrix result artifact is invalid")
    if payload["campaign_id"] != contract.campaign_id:
        raise CampaignValidationError("control matrix result campaign_id drift")
    if payload["contract_sha256"] != contract.sha256:
        raise CampaignValidationError("control matrix result contract_sha256 drift")
    if payload["provider"] != "fake":
        raise CampaignValidationError("control matrix result must use the fake provider")
    if payload["control_policy"] != contract.control_policy:
        raise CampaignValidationError("control matrix result control_policy drift")
    if payload["accounting_scope"] != "control_matrix_aggregate":
        raise CampaignValidationError("control matrix result accounting scope is invalid")
    rows = payload["cases"]
    if not isinstance(rows, list) or len(rows) != len(contract.control_matrix):
        raise CampaignValidationError("control matrix result must contain every control exactly once")
    expected_keys = {
        (control.case_id, control.control_variant) for control in contract.control_matrix
    }
    seen: set[tuple[str, str]] = set()
    for row, control in zip(rows, contract.control_matrix, strict=True):
        if not isinstance(row, dict):
            raise CampaignValidationError("control matrix result rows must be objects")
        row_key = (row.get("case_id"), row.get("control_variant"))
        if row_key in seen or row_key not in expected_keys:
            raise CampaignValidationError("control matrix result contains duplicate or unknown control")
        seen.add(row_key)
        if row_key != (control.case_id, control.control_variant):
            raise CampaignValidationError("control matrix result control order drift")
        if row.get("expected_result") != control.expected_result:
            raise CampaignValidationError(f"control result expected_result drift for {row_key!r}")
        if row.get("expected_failure_class") != control.failure_class:
            raise CampaignValidationError(f"control result failure class drift for {row_key!r}")
        if row.get("actual_result") not in {"pass", "fail"}:
            raise CampaignValidationError(f"control result actual_result is invalid for {row_key!r}")
        actual_failure_class = row.get("actual_failure_class")
        if actual_failure_class not in CONTROL_RESULT_FAILURE_CLASSES:
            raise CampaignValidationError(f"control result failure class is invalid for {row_key!r}")
        expected_match = (
            row["actual_result"] == control.expected_result
            and actual_failure_class == control.failure_class
        )
        if not isinstance(row.get("matches_expectation"), bool) or row["matches_expectation"] != expected_match:
            raise CampaignValidationError(f"control result expectation flag is invalid for {row_key!r}")
        if not isinstance(row.get("provider_requests"), int) or isinstance(row["provider_requests"], bool):
            raise CampaignValidationError(f"control result provider_requests is invalid for {row_key!r}")
        if not 0 <= row["provider_requests"] <= contract.control_policy["case_max_requests"]:
            raise CampaignValidationError(f"control result provider_requests exceeds case bound for {row_key!r}")
        expected_path = str(Path("cases") / control.case_id / control.control_variant / "result.json")
        if row.get("result_path") != expected_path:
            raise CampaignValidationError(f"control result path drift for {row_key!r}")
        _validate_accounting(
            row.get("case_provider_accounting"),
            row["provider_requests"],
            contract.control_policy["case_max_total_tokens"],
            contract.control_policy["case_max_cost_usd"],
            f"control {row_key!r}",
        )
    if seen != expected_keys:
        raise CampaignValidationError("control matrix result does not cover the contract matrix")
    if payload["provider_requests"] != sum(row["provider_requests"] for row in rows):
        raise CampaignValidationError("control matrix result provider_requests accounting drift")
    if not isinstance(payload["provider_requests"], int) or not 0 <= payload["provider_requests"] <= contract.control_policy["max_requests"]:
        raise CampaignValidationError("control matrix result exceeds aggregate request bound")
    _validate_accounting(
        payload["provider_accounting"],
        payload["provider_requests"],
        contract.control_policy["max_total_tokens"],
        contract.control_policy["max_cost_usd"],
        "control matrix aggregate",
    )
    from brep2code.evaluation import build_control_report

    if payload["control_report"] != build_control_report(rows):
        raise CampaignValidationError("control matrix report drift")
    all_matched = all(row["matches_expectation"] for row in rows)
    expected_terminal = (
        ("succeeded", "control_matrix_passed")
        if all_matched
        else ("failed", "control_expectation_failed")
    )
    if (payload["status"], payload["stop_reason"]) != expected_terminal:
        raise CampaignValidationError("control matrix terminal status drift")


def validate_held_out_result(payload: dict[str, Any], contract: CampaignContract) -> None:
    """Validate an offline held-out generalization artifact against its frozen contract."""
    required = {
        "artifact",
        "campaign_id",
        "contract_sha256",
        "provider",
        "held_out_policy",
        "accounting_scope",
        "provider_accounting",
        "provider_requests",
        "status",
        "stop_reason",
        "cases",
        "held_out_report",
    }
    if not isinstance(payload, dict) or not required <= set(payload):
        raise CampaignValidationError("held-out result is missing required fields")
    if payload["artifact"] != "held_out_generalization":
        raise CampaignValidationError("held-out result artifact is invalid")
    if payload["campaign_id"] != contract.campaign_id:
        raise CampaignValidationError("held-out result campaign_id drift")
    if payload["contract_sha256"] != contract.sha256:
        raise CampaignValidationError("held-out result contract_sha256 drift")
    if payload["provider"] != "fake":
        raise CampaignValidationError("held-out result must use the fake provider")
    if payload["held_out_policy"] != contract.held_out_policy:
        raise CampaignValidationError("held-out result policy drift")
    if payload["accounting_scope"] != "held_out_aggregate":
        raise CampaignValidationError("held-out result accounting scope is invalid")
    rows = payload["cases"]
    if not isinstance(rows, list) or len(rows) != len(contract.held_out_matrix):
        raise CampaignValidationError("held-out result must contain every case exactly once")
    for row, expected in zip(rows, contract.held_out_matrix, strict=True):
        if not isinstance(row, dict):
            raise CampaignValidationError("held-out result rows must be objects")
        if row.get("case_id") != expected.case_id:
            raise CampaignValidationError("held-out result case order drift")
        if row.get("expected_result") != expected.expected_result:
            raise CampaignValidationError(f"held-out expected_result drift for {expected.case_id!r}")
        if row.get("expected_failure_class") != expected.failure_class:
            raise CampaignValidationError(f"held-out failure class drift for {expected.case_id!r}")
        if row.get("fixture_sha256") != expected.fixture_sha256:
            raise CampaignValidationError(f"held-out fixture hash drift for {expected.case_id!r}")
        if row.get("expected") != expected.expected:
            raise CampaignValidationError(f"held-out expected geometry drift for {expected.case_id!r}")
        if row.get("gate_oracles") != expected.gate_oracles:
            raise CampaignValidationError(f"held-out gate oracle drift for {expected.case_id!r}")
        actual_failure_class = row.get("actual_failure_class")
        if actual_failure_class not in RESULT_FAILURE_CLASSES:
            raise CampaignValidationError(f"held-out result failure class is invalid for {expected.case_id!r}")
        actual_result = row.get("actual_result")
        if actual_result not in {"pass", "fail"}:
            raise CampaignValidationError(f"held-out result actual_result is invalid for {expected.case_id!r}")
        matches = actual_result == expected.expected_result and actual_failure_class == expected.failure_class
        if row.get("matches_expectation") is not matches:
            raise CampaignValidationError(f"held-out result expectation flag is invalid for {expected.case_id!r}")
        provider_requests = row.get("provider_requests")
        if not isinstance(provider_requests, int) or isinstance(provider_requests, bool):
            raise CampaignValidationError(f"held-out result provider_requests is invalid for {expected.case_id!r}")
        if not 0 <= provider_requests <= contract.held_out_policy["case_max_requests"]:
            raise CampaignValidationError(f"held-out result exceeds case request bound for {expected.case_id!r}")
        expected_path = str(Path("cases") / expected.case_id / "result.json")
        if row.get("result_path") != expected_path:
            raise CampaignValidationError(f"held-out result path drift for {expected.case_id!r}")
        _validate_accounting(
            row.get("case_provider_accounting"),
            provider_requests,
            contract.held_out_policy["case_max_total_tokens"],
            contract.held_out_policy["case_max_cost_usd"],
            f"held-out case {expected.case_id!r}",
        )
    if payload["provider_requests"] != sum(row["provider_requests"] for row in rows):
        raise CampaignValidationError("held-out result provider_requests accounting drift")
    if not isinstance(payload["provider_requests"], int) or not 0 <= payload["provider_requests"] <= contract.held_out_policy["max_requests"]:
        raise CampaignValidationError("held-out result exceeds aggregate request bound")
    _validate_accounting(
        payload["provider_accounting"],
        payload["provider_requests"],
        contract.held_out_policy["max_total_tokens"],
        contract.held_out_policy["max_cost_usd"],
        "held-out aggregate",
    )
    from brep2code.evaluation import build_held_out_report

    if payload["held_out_report"] != build_held_out_report(rows):
        raise CampaignValidationError("held-out report drift")
    all_matched = all(row["matches_expectation"] for row in rows)
    expected_terminal = (
        ("succeeded", "held_out_passed")
        if all_matched
        else ("failed", "held_out_expectation_failed")
    )
    if (payload["status"], payload["stop_reason"]) != expected_terminal:
        raise CampaignValidationError("held-out terminal status drift")


def validate_pilot_result(
    payload: dict[str, Any],
    contract: CampaignContract,
    *,
    runtime_payload: dict[str, Any] | None = None,
    control_matrix_payload: dict[str, Any] | None = None,
    held_out_payload: dict[str, Any] | None = None,
) -> None:
    """Validate an aggregate fake-only pilot and, when supplied, its cohorts."""
    required = {
        "schema_version",
        "artifact",
        "campaign_id",
        "contract_sha256",
        "provider",
        "accounting_scope",
        "provider_accounting",
        "provider_requests",
        "status",
        "stop_reason",
        "runtime_case_ids",
        "held_out_case_ids",
        "control_count",
        "cohorts",
        "capability_report",
    }
    if not isinstance(payload, dict) or not required <= set(payload):
        raise CampaignValidationError("pilot result is missing required fields")
    if payload["schema_version"] != 1:
        raise CampaignValidationError("pilot result schema_version is invalid")
    if payload["artifact"] != "l0_l2_fake_pilot":
        raise CampaignValidationError("pilot result artifact is invalid")
    if payload["campaign_id"] != contract.campaign_id:
        raise CampaignValidationError("pilot result campaign_id drift")
    if payload["contract_sha256"] != contract.sha256:
        raise CampaignValidationError("pilot result contract_sha256 drift")
    if payload["provider"] != "fake":
        raise CampaignValidationError("pilot result must use the fake provider")
    if payload["accounting_scope"] != "pilot_cohort_aggregate":
        raise CampaignValidationError("pilot result accounting scope is invalid")

    runtime_ids = [case.case_id for case in contract.runtime_cases]
    held_out_ids = [case.case_id for case in contract.held_out_matrix]
    if payload["runtime_case_ids"] != runtime_ids:
        raise CampaignValidationError("pilot runtime case scope drift")
    if payload["held_out_case_ids"] != held_out_ids:
        raise CampaignValidationError("pilot held-out case scope drift")
    if set(runtime_ids) & set(held_out_ids):
        raise CampaignValidationError("pilot runtime and held-out scopes overlap")
    if payload["control_count"] != len(contract.control_matrix):
        raise CampaignValidationError("pilot control count drift")

    cohorts = payload["cohorts"]
    if not isinstance(cohorts, dict) or set(cohorts) != {"runtime", "control_matrix", "held_out"}:
        raise CampaignValidationError("pilot cohort set is invalid")
    expected_paths = {
        "runtime": str(Path("runtime") / "result.json"),
        "control_matrix": str(Path("controls") / "result.json"),
        "held_out": str(Path("held-out") / "result.json"),
    }
    cohort_payloads = {
        "runtime": runtime_payload,
        "control_matrix": control_matrix_payload,
        "held_out": held_out_payload,
    }
    for cohort, cohort_summary in cohorts.items():
        if not isinstance(cohort_summary, dict):
            raise CampaignValidationError(f"pilot {cohort} cohort summary is invalid")
        required_summary = {
            "status",
            "stop_reason",
            "case_count",
            "case_ids",
            "provider_requests",
            "provider_accounting",
            "result_path",
        }
        if not required_summary <= set(cohort_summary):
            raise CampaignValidationError(f"pilot {cohort} cohort summary is incomplete")
        if cohort_summary["result_path"] != expected_paths[cohort]:
            raise CampaignValidationError(f"pilot {cohort} result path drift")
        child = cohort_payloads[cohort]
        if child is not None:
            if child.get("campaign_id") != contract.campaign_id:
                raise CampaignValidationError(f"pilot {cohort} campaign_id drift")
            if child.get("contract_sha256") != contract.sha256 or child.get("provider") != "fake":
                raise CampaignValidationError(f"pilot {cohort} contract/provider drift")
            if cohort_summary["status"] != child.get("status"):
                raise CampaignValidationError(f"pilot {cohort} status drift")
            if cohort_summary["stop_reason"] != child.get("stop_reason"):
                raise CampaignValidationError(f"pilot {cohort} stop_reason drift")
            if cohort_summary["case_count"] != len(child.get("cases", [])):
                raise CampaignValidationError(f"pilot {cohort} case count drift")
            if cohort_summary["case_ids"] != [row.get("case_id") for row in child.get("cases", [])]:
                raise CampaignValidationError(f"pilot {cohort} case order drift")
            if cohort_summary["provider_requests"] != child.get("provider_requests"):
                raise CampaignValidationError(f"pilot {cohort} request accounting drift")
            if cohort_summary["provider_accounting"] != child.get("provider_accounting"):
                raise CampaignValidationError(f"pilot {cohort} provider accounting drift")

    if not isinstance(payload["provider_requests"], int) or isinstance(payload["provider_requests"], bool):
        raise CampaignValidationError("pilot provider_requests is invalid")
    expected_requests = sum(
        int(cohorts[cohort]["provider_requests"])
        for cohort in ("runtime", "control_matrix", "held_out")
    )
    if payload["provider_requests"] != expected_requests:
        raise CampaignValidationError("pilot aggregate request accounting drift")
    expected_accounting = _sum_accounting(
        cohorts[cohort]["provider_accounting"]
        for cohort in ("runtime", "control_matrix", "held_out")
    )
    if payload["provider_accounting"] != expected_accounting:
        raise CampaignValidationError("pilot aggregate provider accounting drift")
    _validate_pilot_terminal_status(payload, cohorts)

    if runtime_payload is not None and control_matrix_payload is not None and held_out_payload is not None:
        _validate_runtime_result(runtime_payload, contract)
        validate_control_matrix_result(control_matrix_payload, contract)
        validate_held_out_result(held_out_payload, contract)
        from brep2code.evaluation import build_pilot_report

        expected = build_pilot_report(runtime_payload, control_matrix_payload, held_out_payload)
        for key in (
            "campaign_id",
            "contract_sha256",
            "provider",
            "accounting_scope",
            "provider_accounting",
            "provider_requests",
            "status",
            "stop_reason",
            "runtime_case_ids",
            "held_out_case_ids",
            "control_count",
            "capability_report",
        ):
            if payload[key] != expected[key]:
                raise CampaignValidationError(f"pilot {key} report drift")


def validate_hosted_pilot_result(
    payload: dict[str, Any],
    contract: CampaignContract,
    *,
    runtime_payload: dict[str, Any],
    control_matrix_payload: dict[str, Any],
    held_out_payload: dict[str, Any],
) -> None:
    """Validate a mixed-provider pilot and all three bound cohort results."""
    if not isinstance(payload, dict):
        raise CampaignValidationError("hosted pilot result must be an object")
    if payload.get("artifact") != "l0_l2_hosted_pilot":
        raise CampaignValidationError("hosted pilot result artifact is invalid")
    if payload.get("campaign_id") != contract.campaign_id:
        raise CampaignValidationError("hosted pilot campaign_id drift")
    if payload.get("contract_sha256") != contract.sha256:
        raise CampaignValidationError("hosted pilot contract_sha256 drift")
    if payload.get("provider") != "mixed":
        raise CampaignValidationError("hosted pilot provider must be mixed")
    expected_routing = {
        "runtime": {"provider": contract.provider_policy["provider"], "model": contract.provider_policy["model"]},
        "control_matrix": {"provider": "fake", "model": "fake-script-queue-v1"},
        "held_out": {"provider": "fake", "model": "fake-script-queue-v1"},
    }
    if payload.get("provider_routing") != expected_routing:
        raise CampaignValidationError("hosted pilot provider routing drift")

    _validate_runtime_result(
        runtime_payload,
        contract,
        expected_provider=contract.provider_policy["provider"],
        expected_model=contract.provider_policy["model"],
    )
    validate_control_matrix_result(control_matrix_payload, contract)
    validate_held_out_result(held_out_payload, contract)

    from brep2code.evaluation import build_hosted_pilot_report

    expected = build_hosted_pilot_report(
        runtime_payload, control_matrix_payload, held_out_payload
    )
    if payload != expected:
        raise CampaignValidationError("hosted pilot report drift")


def _validate_runtime_result(
    payload: dict[str, Any],
    contract: CampaignContract,
    *,
    expected_provider: str = "fake",
    expected_model: str | None = None,
) -> None:
    required = {
        "artifact",
        "campaign_id",
        "contract_sha256",
        "provider",
        "provider_policy",
        "accounting_scope",
        "provider_accounting",
        "provider_requests",
        "status",
        "stop_reason",
        "cases",
        "mechanism_report",
    }
    if not isinstance(payload, dict) or not required <= set(payload):
        raise CampaignValidationError("runtime result is missing required fields")
    if payload["artifact"] != "campaign":
        raise CampaignValidationError("runtime result artifact is invalid")
    if payload["campaign_id"] != contract.campaign_id or payload["contract_sha256"] != contract.sha256:
        raise CampaignValidationError("runtime result contract drift")
    if payload["provider"] != expected_provider or payload["provider_policy"] != contract.provider_policy:
        raise CampaignValidationError("runtime result provider policy drift")
    if expected_model is not None and payload.get("model") != expected_model:
        raise CampaignValidationError("runtime result model drift")
    if payload["accounting_scope"] != "campaign_aggregate":
        raise CampaignValidationError("runtime result accounting scope is invalid")
    rows = payload["cases"]
    if not isinstance(rows, list) or len(rows) != len(contract.runtime_cases):
        raise CampaignValidationError("runtime result must contain every runtime case exactly once")
    for row, expected in zip(rows, contract.runtime_cases, strict=True):
        if not isinstance(row, dict) or row.get("case_id") != expected.case_id:
            raise CampaignValidationError("runtime result case order drift")
        if row.get("mechanism") != expected.mechanism or row.get("capability_level") != expected.capability_level:
            raise CampaignValidationError(f"runtime result metadata drift for {expected.case_id!r}")
        provider_requests = row.get("provider_requests")
        if not isinstance(provider_requests, int) or isinstance(provider_requests, bool):
            raise CampaignValidationError(f"runtime result provider_requests is invalid for {expected.case_id!r}")
        if not 0 <= provider_requests <= contract.provider_policy["case_max_requests"]:
            raise CampaignValidationError(f"runtime result exceeds case request bound for {expected.case_id!r}")
        if row.get("result_path") != str(Path("cases") / expected.case_id / "result.json"):
            raise CampaignValidationError(f"runtime result path drift for {expected.case_id!r}")
        _validate_accounting(
            row.get("case_provider_accounting"),
            provider_requests,
            contract.provider_policy["case_max_total_tokens"],
            contract.provider_policy["case_max_cost_usd"],
            f"runtime case {expected.case_id!r}",
        )
    if payload["provider_requests"] != sum(row["provider_requests"] for row in rows):
        raise CampaignValidationError("runtime result provider_requests accounting drift")
    if not isinstance(payload["provider_requests"], int) or not 0 <= payload["provider_requests"] <= contract.provider_policy["max_requests"]:
        raise CampaignValidationError("runtime result exceeds aggregate request bound")
    _validate_accounting(
        payload["provider_accounting"],
        payload["provider_requests"],
        contract.provider_policy["max_total_tokens"],
        contract.provider_policy["max_cost_usd"],
        "runtime aggregate",
    )
    from brep2code.evaluation import build_mechanism_report

    if payload["mechanism_report"] != build_mechanism_report(rows):
        raise CampaignValidationError("runtime mechanism report drift")


def _validate_pilot_terminal_status(payload: dict[str, Any], cohorts: dict[str, Any]) -> None:
    statuses = [cohorts[name]["status"] for name in ("runtime", "control_matrix", "held_out")]
    expected = (
        ("succeeded", "completed")
        if all(status == "succeeded" for status in statuses)
        else ("budget_exhausted", "cohort_budget_exhausted")
        if "budget_exhausted" in statuses
        else ("failed", "cohort_failed")
    )
    if (payload["status"], payload["stop_reason"]) != expected:
        raise CampaignValidationError("pilot terminal status drift")


def _sum_accounting(accountings: Any) -> dict[str, int | float]:
    totals: dict[str, int | float] = {
        "http_attempts": 0,
        "total_tokens": 0,
        "cost_usd": 0.0,
    }
    for accounting in accountings:
        if not isinstance(accounting, dict) or set(accounting) != set(totals):
            raise CampaignValidationError("pilot provider accounting is incomplete")
        totals["http_attempts"] += accounting["http_attempts"]
        totals["total_tokens"] += accounting["total_tokens"]
        totals["cost_usd"] += accounting["cost_usd"]
    return totals


def _validate_accounting(
    value: Any,
    requests: int,
    max_total_tokens: int,
    max_cost_usd: float,
    label: str,
) -> None:
    if not isinstance(value, dict) or set(value) != {"http_attempts", "total_tokens", "cost_usd"}:
        raise CampaignValidationError(f"{label} accounting is incomplete")
    if value["http_attempts"] != requests:
        raise CampaignValidationError(f"{label} http accounting drift")
    if (
        not isinstance(value["total_tokens"], int)
        or isinstance(value["total_tokens"], bool)
        or value["total_tokens"] < 0
        or value["total_tokens"] > max_total_tokens
    ):
        raise CampaignValidationError(f"{label} token accounting exceeds bound")
    if (
        not isinstance(value["cost_usd"], int | float)
        or isinstance(value["cost_usd"], bool)
        or value["cost_usd"] < 0
        or value["cost_usd"] > max_cost_usd + 1e-12
    ):
        raise CampaignValidationError(f"{label} cost accounting exceeds bound")


def _validate_ladder(value: Any, rows: list[CampaignCase]) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        raise CampaignValidationError("capability_ladder must be a non-empty array")
    row_ids = {row.case_id for row in rows}
    ladder_ids: set[str] = set()
    levels: list[str] = []
    result: list[dict[str, Any]] = []
    for raw in value:
        if not isinstance(raw, dict):
            raise CampaignValidationError("capability ladder entries must be objects")
        _require_exact_keys(raw, LADDER_KEYS, "capability ladder entry")
        level = _required_string(raw, "capability_level")
        if level not in CAPABILITY_LEVEL_SET:
            raise CampaignValidationError(f"capability ladder level {level!r} is invalid")
        if level in levels:
            raise CampaignValidationError(
                f"capability ladder contains duplicate level {level!r}"
            )
        levels.append(level)
        case_ids = _string_array(raw["case_ids"], f"capability ladder {level}.case_ids")
        if not case_ids or len(case_ids) != len(set(case_ids)):
            raise CampaignValidationError(
                f"capability ladder {level} case_ids must be unique and non-empty"
            )
        if not set(case_ids) <= row_ids:
            raise CampaignValidationError(
                f"capability ladder {level} references a case outside the campaign"
            )
        mechanisms = _string_array(raw["mechanisms"], f"capability ladder {level}.mechanisms")
        if not isinstance(raw["minimum_cases"], int) or isinstance(raw["minimum_cases"], bool) or raw["minimum_cases"] < 1:
            raise CampaignValidationError(
                f"capability ladder {level}.minimum_cases must be positive"
            )
        if raw["minimum_cases"] > len(case_ids):
            raise CampaignValidationError(
                f"capability ladder {level}.minimum_cases exceeds its cases"
            )
        for case_id in case_ids:
            row = next(row for row in rows if row.case_id == case_id)
            if row.capability_level != level or row.mechanism not in mechanisms:
                raise CampaignValidationError(f"capability ladder assignment drift for {case_id!r}")
        ladder_ids.update(case_ids)
        result.append(dict(raw))
    if ladder_ids != row_ids:
        raise CampaignValidationError("capability ladder must cover every campaign case exactly once")
    return result


def _load_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CampaignValidationError(f"cannot read campaign contract {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise CampaignValidationError("campaign contract must be a JSON object")
    return payload


def _require_exact_keys(payload: dict[str, Any], expected: frozenset[str], label: str) -> None:
    keys = frozenset(payload)
    if keys != expected:
        raise CampaignValidationError(
            f"{label} keys must be {sorted(expected)}; missing={sorted(expected - keys)}, "
            f"unknown={sorted(keys - expected)}"
        )


def _required_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise CampaignValidationError(f"{key} must be a non-empty string")
    return value


def _string_array(value: Any, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item for item in value):
        raise CampaignValidationError(f"{label} must be a non-empty string array")
    if len(value) != len(set(value)):
        raise CampaignValidationError(f"{label} must contain unique strings")
    return tuple(value)
