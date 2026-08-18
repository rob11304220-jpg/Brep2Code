from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from brep2code.capabilities import CAPABILITY_LEVEL_SET
from brep2code.mechanisms import MechanismRegistry


DOSSIER_NAME = "dossier.json"
DOSSIER_SCHEMA_VERSION = 1
DEVELOPMENT_COHORT = ("nominal", "parameter_variation", "failure_sensitive")
CONTROL_EXPECTED_RESULTS = frozenset({"pass", "fail"})
CONTROL_FAILURE_CLASSES = frozenset({"pass", "geometry", "execution"})
HELD_OUT_EXPECTED_RESULTS = frozenset({"pass", "fail"})
HELD_OUT_FAILURE_CLASSES = frozenset({"pass", "geometry", "execution"})
DOSSIER_KEYS = frozenset(
    {
        "schema_version",
        "case_id",
        "mechanism_id",
        "capability_level",
        "geometry_assets",
        "modeling_assets",
        "harness_assets",
    }
)


class CaseDossierError(ValueError):
    """Raised when a case's Harness-only dossier cannot be admitted."""


def validate_case_dossier(
    case_root: Path,
    case_metadata: dict[str, Any],
    registry: MechanismRegistry,
) -> dict[str, Any]:
    path = case_root / DOSSIER_NAME
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CaseDossierError(f"cannot read case dossier {path}: {exc}") from exc
    if not isinstance(payload, dict) or frozenset(payload) != DOSSIER_KEYS:
        raise CaseDossierError(f"case dossier keys must be {sorted(DOSSIER_KEYS)}")
    if payload["schema_version"] != DOSSIER_SCHEMA_VERSION:
        raise CaseDossierError("case dossier schema_version must equal 1")
    case_id = _required_string(payload, "case_id")
    if case_id != case_metadata["case_id"]:
        raise CaseDossierError("case dossier case_id does not match case metadata")
    mechanism_id = _required_string(payload, "mechanism_id")
    if mechanism_id != case_metadata["mechanism"]:
        raise CaseDossierError("case dossier mechanism_id does not match case metadata")
    definition = registry.get(mechanism_id)
    if payload["capability_level"] not in CAPABILITY_LEVEL_SET:
        raise CaseDossierError("case dossier capability_level is invalid")
    if payload["capability_level"] != definition["capability_level"]:
        raise CaseDossierError("case dossier capability_level does not match registry")

    geometry = _object(payload, "geometry_assets")
    _exact_keys(geometry, {"input_step", "expected_geometry", "topology_oracle"}, "geometry_assets")
    if geometry["input_step"] != case_metadata["input_step"]:
        raise CaseDossierError("geometry_assets.input_step does not match case metadata")
    if geometry["expected_geometry"] != "case.json.expected":
        raise CaseDossierError("geometry_assets.expected_geometry must be case.json.expected")
    if geometry["topology_oracle"] != "case.json.expected.counts":
        raise CaseDossierError("geometry_assets.topology_oracle must be case.json.expected.counts")

    modeling = _object(payload, "modeling_assets")
    _exact_keys(
        modeling,
        {
            "kernel_operations",
            "sequence_dependencies",
            "parameter_dimensions",
            "failure_modes",
            "parser_notes",
        },
        "modeling_assets",
    )
    for key in modeling:
        _string_array(modeling[key], f"modeling_assets.{key}")
    if set(modeling["kernel_operations"]) != set(definition["kernel_operations"]):
        raise CaseDossierError("modeling_assets.kernel_operations drift from registry")
    if not set(definition["required_gates"]).issuperset(
        set(_object(payload, "harness_assets").get("required_gates", []))
    ):
        raise CaseDossierError("harness required gates must be declared by the registry")

    harness = _object(payload, "harness_assets")
    _exact_keys(
        harness,
        {
            "prompt_mode",
            "repair_policy",
            "required_gates",
            "gate_oracles",
            "development_cohort",
            "controls",
            "held_out_fixture",
            "positive_control",
            "negative_control",
            "reference_policy",
            "hosted_budget_policy",
        },
        "harness_assets",
    )
    if harness["prompt_mode"] not in {"observation-only", "mechanism-conditioned"}:
        raise CaseDossierError("harness_assets.prompt_mode is invalid")
    if harness["reference_policy"] != "harness_only":
        raise CaseDossierError("harness_assets.reference_policy must be harness_only")
    repair_policy = _object(harness, "repair_policy")
    _exact_keys(repair_policy, {"max_rounds", "initial_script_allowed"}, "repair_policy")
    if not isinstance(repair_policy["max_rounds"], int) or repair_policy["max_rounds"] < 1:
        raise CaseDossierError("repair_policy.max_rounds must be positive")
    if not isinstance(repair_policy["initial_script_allowed"], bool):
        raise CaseDossierError("repair_policy.initial_script_allowed must be boolean")
    _string_array(harness["required_gates"], "harness_assets.required_gates")
    gate_oracles = _object(harness, "gate_oracles")
    if not set(gate_oracles) <= set(harness["required_gates"]):
        raise CaseDossierError("harness gate oracles must be declared by required_gates")
    for gate_id, oracle in gate_oracles.items():
        _validate_gate_oracle(gate_id, oracle)
    for gate_id in ("semantic", "adjacency"):
        if gate_id in harness["required_gates"] and gate_id not in gate_oracles:
            raise CaseDossierError(f"required {gate_id} gate needs a gate oracle")
    cohort = _string_array(harness["development_cohort"], "harness_assets.development_cohort")
    if cohort != DEVELOPMENT_COHORT:
        raise CaseDossierError(
            "harness_assets.development_cohort must declare nominal, parameter_variation, "
            "and failure_sensitive in that order"
        )
    _validate_controls(harness["controls"], case_root)
    _validate_held_out_fixture(harness["held_out_fixture"], case_root)
    for key in ("positive_control", "negative_control"):
        if not isinstance(harness[key], bool):
            raise CaseDossierError(f"harness_assets.{key} must be boolean")
    if not harness["positive_control"]:
        raise CaseDossierError("nominal development cohort requires positive_control")
    if not harness["negative_control"]:
        raise CaseDossierError("failure_sensitive development cohort requires negative_control")
    budget = _object(harness, "hosted_budget_policy")
    _exact_keys(budget, {"max_requests", "max_total_tokens", "max_cost_usd"}, "hosted_budget_policy")
    if (
        not isinstance(budget["max_requests"], int)
        or budget["max_requests"] < 1
        or not isinstance(budget["max_total_tokens"], int)
        or budget["max_total_tokens"] < 1
        or not isinstance(budget["max_cost_usd"], (int, float))
        or budget["max_cost_usd"] <= 0
    ):
        raise CaseDossierError("hosted_budget_policy values must be positive")
    return payload


def _required_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise CaseDossierError(f"{key} must be a non-empty string")
    return value


def _required_sha256(payload: dict[str, Any], key: str) -> str:
    value = _required_string(payload, key).lower()
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise CaseDossierError(f"{key} must be a lowercase SHA-256 hex digest")
    return value


def _object(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise CaseDossierError(f"{key} must be an object")
    return value


def _exact_keys(payload: dict[str, Any], expected: set[str], label: str) -> None:
    if set(payload) != expected:
        raise CaseDossierError(f"{label} keys must be {sorted(expected)}")


def _string_array(value: Any, label: str) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item for item in value)
        or len(value) != len(set(value))
    ):
        raise CaseDossierError(f"{label} must contain unique non-empty strings")
    return tuple(value)


def _validate_gate_oracle(gate_id: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise CaseDossierError(f"harness_assets.gate_oracles.{gate_id} must be an object")
    oracle = value
    if gate_id == "semantic":
        _exact_keys(oracle, {"surface", "radius", "axis_direction"}, f"{gate_id} gate oracle")
        _required_string(oracle, "surface")
        if not isinstance(oracle["radius"], (int, float)) or oracle["radius"] <= 0:
            raise CaseDossierError("semantic gate oracle radius must be positive")
        _vector(oracle["axis_direction"], "semantic gate oracle axis_direction")
    elif gate_id == "adjacency":
        _exact_keys(
            oracle,
            {"surface", "axis", "extent_min", "extent_max"},
            f"{gate_id} gate oracle",
        )
        _required_string(oracle, "surface")
        if oracle["axis"] not in {0, 1, 2}:
            raise CaseDossierError("adjacency gate oracle axis must be 0, 1, or 2")
        if not all(
            isinstance(oracle[key], (int, float))
            for key in ("extent_min", "extent_max")
        ):
            raise CaseDossierError("adjacency gate oracle extents must be numbers")
        if oracle["extent_min"] > oracle["extent_max"]:
            raise CaseDossierError("adjacency gate oracle extent_min must not exceed extent_max")
    else:
        raise CaseDossierError(f"unknown gate oracle {gate_id!r}")


def _validate_controls(value: Any, case_root: Path) -> None:
    if not isinstance(value, list) or len(value) != len(DEVELOPMENT_COHORT):
        raise CaseDossierError("harness_assets.controls must contain the three development controls")
    variants = []
    root = case_root.resolve()
    for raw, expected_variant in zip(value, DEVELOPMENT_COHORT, strict=True):
        if not isinstance(raw, dict) or set(raw) != {
            "variant", "asset", "sha256", "expected_result", "failure_class"
        }:
            raise CaseDossierError(
                "harness_assets.controls entries must contain variant, asset, sha256, expected_result, and failure_class"
            )
        variant = _required_string(raw, "variant")
        if variant != expected_variant or variant in variants:
            raise CaseDossierError("harness_assets.controls must follow the development cohort order")
        variants.append(variant)
        asset = _required_string(raw, "asset")
        asset_path = Path(asset)
        if asset_path.is_absolute() or ".." in asset_path.parts:
            raise CaseDossierError("harness control assets must be relative to the case directory")
        resolved_asset = (root / asset_path).resolve()
        if not resolved_asset.is_relative_to(root) or not resolved_asset.is_file():
            raise CaseDossierError(f"missing harness control asset: {asset}")
        if not resolved_asset.read_text(encoding="utf-8").strip():
            raise CaseDossierError(f"harness control asset must be non-empty: {asset}")
        asset_hash = _required_sha256(raw, "sha256")
        actual_hash = hashlib.sha256(resolved_asset.read_bytes()).hexdigest()
        if asset_hash != actual_hash:
            raise CaseDossierError(
                f"harness control asset sha256 mismatch for {variant}: expected {asset_hash}, got {actual_hash}"
            )
        expected_result = _required_string(raw, "expected_result")
        failure_class = _required_string(raw, "failure_class")
        if expected_result not in CONTROL_EXPECTED_RESULTS:
            raise CaseDossierError("harness control expected_result must be pass or fail")
        if failure_class not in CONTROL_FAILURE_CLASSES:
            raise CaseDossierError(
                "harness control failure_class must be pass, geometry, or execution"
            )
        if variant == "failure_sensitive" and expected_result != "fail":
            raise CaseDossierError("failure_sensitive control must expect fail")
        if variant != "failure_sensitive" and expected_result != "pass":
            raise CaseDossierError(f"{variant} control must expect pass")
        if expected_result == "pass" and failure_class != "pass":
            raise CaseDossierError("passing controls must use failure_class pass")
        if expected_result == "fail" and failure_class == "pass":
            raise CaseDossierError("failing controls must declare a failure class")


def _validate_held_out_fixture(value: Any, case_root: Path) -> None:
    if case_root.parent.name != "eval":
        if value is not None:
            raise CaseDossierError("runtime cases must not declare a held-out fixture")
        return
    if not isinstance(value, dict) or set(value) != {
        "asset", "sha256", "expected_result", "failure_class"
    }:
        raise CaseDossierError(
            "eval cases must declare held_out_fixture asset, sha256, expected_result, and failure_class"
        )
    asset = _required_string(value, "asset")
    asset_path = Path(asset)
    if asset_path.is_absolute() or ".." in asset_path.parts:
        raise CaseDossierError("held-out fixture assets must be relative to the case directory")
    root = case_root.resolve()
    resolved_asset = (root / asset_path).resolve()
    if not resolved_asset.is_relative_to(root) or not resolved_asset.is_file():
        raise CaseDossierError(f"missing held-out fixture asset: {asset}")
    if not resolved_asset.read_text(encoding="utf-8").strip():
        raise CaseDossierError(f"held-out fixture asset must be non-empty: {asset}")
    asset_hash = _required_sha256(value, "sha256")
    actual_hash = hashlib.sha256(resolved_asset.read_bytes()).hexdigest()
    if asset_hash != actual_hash:
        raise CaseDossierError(
            f"held-out fixture asset sha256 mismatch: expected {asset_hash}, got {actual_hash}"
        )
    expected_result = _required_string(value, "expected_result")
    failure_class = _required_string(value, "failure_class")
    if expected_result not in HELD_OUT_EXPECTED_RESULTS:
        raise CaseDossierError("held-out fixture expected_result must be pass or fail")
    if failure_class not in HELD_OUT_FAILURE_CLASSES:
        raise CaseDossierError(
            "held-out fixture failure_class must be pass, geometry, or execution"
        )
    if expected_result == "pass" and failure_class != "pass":
        raise CaseDossierError("passing held-out fixtures must use failure_class pass")
    if expected_result == "fail" and failure_class == "pass":
        raise CaseDossierError("failing held-out fixtures must declare a failure class")


def _vector(value: Any, label: str) -> None:
    if not isinstance(value, list) or len(value) != 3 or not all(
        isinstance(item, (int, float)) and not isinstance(item, bool) for item in value
    ):
        raise CaseDossierError(f"{label} must be a three-number array")
