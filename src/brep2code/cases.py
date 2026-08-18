from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

from brep2code.capabilities import (
    CAPABILITY_LEVEL_SET,
    COMPATIBILITY_TIER_SET,
)
from brep2code.dossiers import validate_case_dossier
from brep2code.domain import Case
from brep2code.mechanisms import MechanismRegistry, load_mechanism_registry


SUPPORTED_SPLITS = frozenset({"smoke", "train", "eval"})
RUNTIME_SPLITS = frozenset({"smoke", "train"})
CASE_KEYS = frozenset(
    {
        "case_id",
        "input_step",
        "sha256",
        "unit",
        "summary",
        "tags",
        "mechanism",
        "capability_level",
        "compatibility_tier",
        "kernel_properties",
        "sequence",
        "difficulty",
        "expected",
    }
)
EXPECTED_KEYS = frozenset({"bbox", "volume", "counts"})
COUNT_KEYS = frozenset({"solid", "shell", "face", "edge"})
MECHANISMS = frozenset({"primitive", "analytic_surface", "boolean_cut"})


class CaseValidationError(ValueError):
    """Raised when a case or manifest does not satisfy the v2 contract."""


@dataclass(frozen=True)
class ValidatedCase:
    case: Case
    sha256: str
    metadata: dict[str, Any]
    dossier: dict[str, Any] | None = None


@dataclass(frozen=True)
class CaseManifest:
    split: str
    cases: tuple[ValidatedCase, ...]


def discover_cases(cases_root: Path) -> list[Path]:
    if not cases_root.is_dir():
        raise CaseValidationError(f"cases root does not exist: {cases_root}")
    return sorted(path.parent for path in cases_root.glob("*/*/case.json"))


def discover_manifests(cases_root: Path) -> list[Path]:
    manifests_root = cases_root / "manifests"
    if not manifests_root.is_dir():
        raise CaseValidationError(f"manifests root does not exist: {manifests_root}")
    return sorted(manifests_root.glob("*.json"))


def validate_case(
    case_root: Path,
    cases_root: Path,
    *,
    registry: MechanismRegistry | None = None,
) -> ValidatedCase:
    resolved_root = case_root.resolve()
    resolved_cases = cases_root.resolve()
    if not resolved_root.is_relative_to(resolved_cases):
        raise CaseValidationError(f"case is outside cases root: {case_root}")

    relative = resolved_root.relative_to(resolved_cases)
    if len(relative.parts) != 2:
        raise CaseValidationError(f"case must use cases/<split>/<case_id>: {case_root}")
    split, directory_id = relative.parts
    if split not in SUPPORTED_SPLITS:
        raise CaseValidationError(f"unsupported split {split!r}")

    metadata = _load_json_object(resolved_root / "case.json", "case metadata")
    _require_exact_keys(metadata, CASE_KEYS, "case metadata")
    case_id = _required_string(metadata, "case_id")
    if case_id != directory_id:
        raise CaseValidationError(
            f"case_id {case_id!r} does not match directory {directory_id!r}"
        )
    input_name = _required_string(metadata, "input_step")
    if Path(input_name).name != input_name:
        raise CaseValidationError("input_step must be a filename in the case directory")
    input_step = resolved_root / input_name
    if not input_step.is_file():
        raise CaseValidationError(f"missing STEP input: {input_step}")

    _required_string(metadata, "unit")
    _required_string(metadata, "summary")
    _validate_tags(metadata.get("tags"))
    registry = registry or _optional_registry(cases_root)
    _validate_mechanism_metadata(metadata, registry)
    _validate_expected(metadata.get("expected"))
    dossier = None
    if registry is not None:
        try:
            dossier = validate_case_dossier(resolved_root, metadata, registry)
        except ValueError as exc:
            raise CaseValidationError(str(exc)) from exc
    expected_hash = _required_sha256(metadata, "sha256")
    actual_hash = hashlib.sha256(input_step.read_bytes()).hexdigest()
    if actual_hash != expected_hash:
        raise CaseValidationError(
            f"sha256 mismatch for {case_id}: expected {expected_hash}, got {actual_hash}"
        )
    return ValidatedCase(
        case=Case(case_id=case_id, root=resolved_root, input_step=input_step, split=split),
        sha256=actual_hash,
        metadata=metadata,
        dossier=dossier,
    )


def load_manifest(
    manifest_path: Path,
    cases_root: Path,
    *,
    runtime: bool = False,
    registry: MechanismRegistry | None = None,
) -> CaseManifest:
    payload = _load_json_object(manifest_path, "case manifest")
    _require_exact_keys(payload, frozenset({"schema_version", "split", "cases"}), "manifest")
    if payload["schema_version"] != 1:
        raise CaseValidationError("manifest schema_version must equal 1")
    split = _required_string(payload, "split")
    if split not in SUPPORTED_SPLITS:
        raise CaseValidationError(f"unsupported manifest split {split!r}")
    if runtime and split not in RUNTIME_SPLITS:
        raise CaseValidationError(f"split {split!r} is not visible to the runtime")
    case_ids = payload.get("cases")
    if not isinstance(case_ids, list) or not case_ids:
        raise CaseValidationError("manifest cases must be a non-empty array")
    if any(not isinstance(case_id, str) or not case_id for case_id in case_ids):
        raise CaseValidationError("manifest case IDs must be non-empty strings")
    if len(case_ids) != len(set(case_ids)):
        raise CaseValidationError("manifest contains duplicate case IDs")

    cases = tuple(
        validate_case(cases_root / split / case_id, cases_root, registry=registry)
        for case_id in case_ids
    )
    return CaseManifest(split=split, cases=cases)


def validate_catalog(cases_root: Path) -> tuple[CaseManifest, ...]:
    case_roots = discover_cases(cases_root)
    if not case_roots:
        raise CaseValidationError(f"no cases discovered under {cases_root}")
    try:
        registry = load_mechanism_registry(cases_root)
    except ValueError as exc:
        raise CaseValidationError(str(exc)) from exc
    manifests = tuple(
        load_manifest(path, cases_root, registry=registry) for path in discover_manifests(cases_root)
    )
    declared = [
        (manifest.split, item.case.case_id)
        for manifest in manifests
        for item in manifest.cases
    ]
    if len(declared) != len(set(declared)):
        raise CaseValidationError("a case is declared by more than one manifest")
    discovered = {
        (case_root.parent.name, case_root.name)
        for case_root in case_roots
    }
    if set(declared) != discovered:
        missing = sorted(discovered - set(declared))
        unknown = sorted(set(declared) - discovered)
        raise CaseValidationError(f"manifest/catalog mismatch: missing={missing}, unknown={unknown}")
    return manifests


def _load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CaseValidationError(f"cannot read {label} {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise CaseValidationError(f"{label} must be a JSON object: {path}")
    return payload


def _require_exact_keys(payload: dict[str, Any], expected: frozenset[str], label: str) -> None:
    keys = frozenset(payload)
    if keys != expected:
        raise CaseValidationError(
            f"{label} keys must be {sorted(expected)}; missing={sorted(expected - keys)}, "
            f"unknown={sorted(keys - expected)}"
        )


def _required_string(metadata: dict[str, Any], key: str) -> str:
    value = metadata.get(key)
    if not isinstance(value, str) or not value:
        raise CaseValidationError(f"{key} must be a non-empty string")
    return value


def _required_sha256(metadata: dict[str, Any], key: str) -> str:
    value = _required_string(metadata, key).lower()
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise CaseValidationError(f"{key} must be a lowercase SHA-256 hex digest")
    return value


def _validate_tags(value: Any) -> None:
    if not isinstance(value, list) or not value:
        raise CaseValidationError("tags must be a non-empty array")
    if any(not isinstance(tag, str) or not tag for tag in value) or len(value) != len(set(value)):
        raise CaseValidationError("tags must contain unique non-empty strings")


def _validate_mechanism_metadata(
    metadata: dict[str, Any], registry: MechanismRegistry | None = None
) -> None:
    mechanism = metadata.get("mechanism")
    if registry is None:
        if mechanism not in MECHANISMS:
            raise CaseValidationError(f"mechanism must be one of {sorted(MECHANISMS)}")
    else:
        try:
            definition = registry.get(mechanism)
        except ValueError as exc:
            raise CaseValidationError(str(exc)) from exc
    capability_level = metadata.get("capability_level")
    if capability_level not in CAPABILITY_LEVEL_SET:
        raise CaseValidationError(
            f"capability_level must be one of {sorted(CAPABILITY_LEVEL_SET)}"
        )
    compatibility_tier = metadata.get("compatibility_tier")
    if compatibility_tier not in COMPATIBILITY_TIER_SET:
        raise CaseValidationError(
            f"compatibility_tier must be one of {sorted(COMPATIBILITY_TIER_SET)}"
        )
    if registry is not None:
        if capability_level != definition["capability_level"]:
            raise CaseValidationError(
                f"capability_level for {mechanism!r} must be {definition['capability_level']!r}"
            )
        if compatibility_tier != definition["compatibility_tier"]:
            raise CaseValidationError(
                f"compatibility_tier for {mechanism!r} must be {definition['compatibility_tier']!r}"
            )
    properties = metadata.get("kernel_properties")
    if not isinstance(properties, list) or not properties:
        raise CaseValidationError("kernel_properties must be a non-empty array")
    if any(not isinstance(item, str) or not item for item in properties):
        raise CaseValidationError("kernel_properties must contain non-empty strings")
    if len(properties) != len(set(properties)):
        raise CaseValidationError("kernel_properties must contain unique strings")
    sequence = metadata.get("sequence")
    if not isinstance(sequence, list) or not sequence:
        raise CaseValidationError("sequence must be a non-empty array")
    if any(not isinstance(item, str) or not item for item in sequence):
        raise CaseValidationError("sequence must contain non-empty strings")
    difficulty = metadata.get("difficulty")
    if not isinstance(difficulty, int) or isinstance(difficulty, bool) or not 1 <= difficulty <= 3:
        raise CaseValidationError("difficulty must be an integer from 1 to 3")


def _validate_expected(value: Any) -> None:
    if not isinstance(value, dict):
        raise CaseValidationError("expected must be an object")
    _require_exact_keys(value, EXPECTED_KEYS, "expected")
    bbox = value["bbox"]
    if not isinstance(bbox, dict) or frozenset(bbox) != frozenset({"min", "max"}):
        raise CaseValidationError("expected.bbox must contain min and max")
    for key in ("min", "max"):
        vector = bbox[key]
        if not isinstance(vector, list) or len(vector) != 3 or not all(_is_number(v) for v in vector):
            raise CaseValidationError(f"expected.bbox.{key} must be a three-number array")
    if any(low > high for low, high in zip(bbox["min"], bbox["max"], strict=True)):
        raise CaseValidationError("expected.bbox min must not exceed max")
    if not _is_number(value["volume"]) or value["volume"] <= 0:
        raise CaseValidationError("expected.volume must be positive")
    counts = value["counts"]
    if not isinstance(counts, dict):
        raise CaseValidationError("expected.counts must be an object")
    _require_exact_keys(counts, COUNT_KEYS, "expected.counts")
    if any(not isinstance(count, int) or isinstance(count, bool) or count < 0 for count in counts.values()):
        raise CaseValidationError("expected counts must be non-negative integers")


def _is_number(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool)


def _optional_registry(cases_root: Path) -> MechanismRegistry | None:
    path = cases_root / "registry" / "mechanisms.json"
    if not path.is_file():
        return None
    try:
        return load_mechanism_registry(cases_root)
    except ValueError as exc:
        raise CaseValidationError(str(exc)) from exc
