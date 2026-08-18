from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from brep2code.capabilities import (
    CAPABILITY_LEVEL_SET,
    COMPATIBILITY_TIER_SET,
)


REGISTRY_RELATIVE_PATH = Path("registry") / "mechanisms.json"
REGISTRY_SCHEMA_VERSION = 1
MECHANISM_KEYS = frozenset(
    {
        "mechanism_id",
        "label",
        "capability_level",
        "compatibility_tier",
        "kernel_operations",
        "sequence_dependencies",
        "difficulty_dimensions",
        "required_gates",
        "failure_modes",
        "parser_notes",
    }
)


class MechanismRegistryError(ValueError):
    """Raised when the mechanism registry cannot be admitted."""


@dataclass(frozen=True)
class MechanismRegistry:
    schema_version: int
    definitions: dict[str, dict[str, Any]]

    def get(self, mechanism_id: str) -> dict[str, Any]:
        try:
            return self.definitions[mechanism_id]
        except KeyError as exc:
            raise MechanismRegistryError(
                f"unknown mechanism {mechanism_id!r} in case metadata"
            ) from exc


def load_mechanism_registry(cases_root: Path) -> MechanismRegistry:
    path = cases_root / REGISTRY_RELATIVE_PATH
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MechanismRegistryError(f"cannot read mechanism registry {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise MechanismRegistryError("mechanism registry must be a JSON object")
    if frozenset(payload) != frozenset({"schema_version", "mechanisms"}):
        raise MechanismRegistryError(
            "mechanism registry keys must be ['mechanisms', 'schema_version']"
        )
    if payload["schema_version"] != REGISTRY_SCHEMA_VERSION:
        raise MechanismRegistryError("mechanism registry schema_version must equal 1")
    raw_mechanisms = payload["mechanisms"]
    if not isinstance(raw_mechanisms, list) or not raw_mechanisms:
        raise MechanismRegistryError("mechanisms must be a non-empty array")

    definitions: dict[str, dict[str, Any]] = {}
    for raw in raw_mechanisms:
        if not isinstance(raw, dict) or frozenset(raw) != MECHANISM_KEYS:
            raise MechanismRegistryError(
                f"mechanism entry keys must be {sorted(MECHANISM_KEYS)}"
            )
        mechanism_id = raw.get("mechanism_id")
        if not isinstance(mechanism_id, str) or not mechanism_id:
            raise MechanismRegistryError("mechanism_id must be a non-empty string")
        if mechanism_id in definitions:
            raise MechanismRegistryError(f"duplicate mechanism_id {mechanism_id!r}")
        _required_string(raw, "label")
        _required_enum(raw, "capability_level", CAPABILITY_LEVEL_SET)
        _required_enum(raw, "compatibility_tier", COMPATIBILITY_TIER_SET)
        for key in (
            "kernel_operations",
            "sequence_dependencies",
            "difficulty_dimensions",
            "required_gates",
            "failure_modes",
            "parser_notes",
        ):
            _string_array(raw.get(key), key)
        definitions[mechanism_id] = dict(raw)
    return MechanismRegistry(schema_version=payload["schema_version"], definitions=definitions)


def _required_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise MechanismRegistryError(f"{key} must be a non-empty string")
    return value


def _required_enum(payload: dict[str, Any], key: str, values: set[str]) -> str:
    value = _required_string(payload, key)
    if value not in values:
        raise MechanismRegistryError(f"{key} must be one of {sorted(values)}")
    return value


def _string_array(value: Any, key: str) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item for item in value)
        or len(value) != len(set(value))
    ):
        raise MechanismRegistryError(f"{key} must contain unique non-empty strings")
    return tuple(value)
