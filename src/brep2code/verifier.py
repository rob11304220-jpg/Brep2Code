from __future__ import annotations

import json
from pathlib import Path
from typing import Any


VERIFIER_NAME = "verifier.json"
VERIFIER_SCHEMA_VERSION = 1
VERIFIER_KEYS = frozenset(
    {"schema_version", "case_id", "target", "gates", "repair_policy", "reference_policy"}
)


class VerifierPackError(ValueError):
    """Raised when a generic verifier pack cannot be admitted."""


def load_verifier_pack(
    case_root: Path, case_metadata: dict[str, Any]
) -> dict[str, Any] | None:
    """Load an optional construction-strategy-independent verifier contract."""

    path = case_root / VERIFIER_NAME
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise VerifierPackError(f"cannot read verifier pack {path}: {exc}") from exc
    if not isinstance(payload, dict) or frozenset(payload) != VERIFIER_KEYS:
        raise VerifierPackError(f"verifier pack keys must be {sorted(VERIFIER_KEYS)}")
    if payload["schema_version"] != VERIFIER_SCHEMA_VERSION:
        raise VerifierPackError("verifier pack schema_version must equal 1")
    if payload["case_id"] != case_metadata["case_id"]:
        raise VerifierPackError("verifier pack case_id does not match case metadata")

    target = _object(payload, "target")
    _exact_keys(target, {"expected_geometry", "topology_oracle"}, "target")
    if target["expected_geometry"] != "case.json.expected":
        raise VerifierPackError("target.expected_geometry must be case.json.expected")
    if target["topology_oracle"] != "case.json.expected.counts":
        raise VerifierPackError("target.topology_oracle must be case.json.expected.counts")

    gates = _object(payload, "gates")
    _exact_keys(gates, {"required", "oracles"}, "gates")
    required = _string_array(gates["required"], "gates.required")
    oracles = _object(gates, "oracles")
    if not set(oracles) <= set(required):
        raise VerifierPackError("gates.oracles must refer to required gates")
    for gate_id in ("semantic", "adjacency"):
        if gate_id in required and gate_id not in oracles:
            raise VerifierPackError(f"required {gate_id} gate needs an oracle")

    repair = _object(payload, "repair_policy")
    _exact_keys(repair, {"max_rounds", "initial_script_allowed"}, "repair_policy")
    if not isinstance(repair["max_rounds"], int) or repair["max_rounds"] < 1:
        raise VerifierPackError("repair_policy.max_rounds must be positive")
    if not isinstance(repair["initial_script_allowed"], bool):
        raise VerifierPackError("repair_policy.initial_script_allowed must be boolean")
    if payload["reference_policy"] not in {"projected_only", "harness_only"}:
        raise VerifierPackError("reference_policy must be projected_only or harness_only")
    return payload


def _object(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise VerifierPackError(f"{key} must be an object")
    return value


def _exact_keys(payload: dict[str, Any], expected: set[str], label: str) -> None:
    if set(payload) != expected:
        raise VerifierPackError(
            f"{label} keys must be {sorted(expected)}; "
            f"missing={sorted(expected - set(payload))}, "
            f"unknown={sorted(set(payload) - expected)}"
        )


def _string_array(value: Any, label: str) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item for item in value)
        or len(value) != len(set(value))
    ):
        raise VerifierPackError(f"{label} must be a non-empty unique string array")
    return tuple(value)
