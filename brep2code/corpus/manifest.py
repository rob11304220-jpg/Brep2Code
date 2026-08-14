"""Case corpus manifest loading and validation."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


VALID_TIERS = {"P0", "P1", "P2", "P3"}


@dataclass(frozen=True)
class CorpusCase:
    case_id: str
    tier: str
    input_step: Path
    expected_bbox: dict[str, list[float]] | None = None
    expected_counts: dict[str, int] | None = None
    expected_volume: float | None = None
    difficulty_tags: tuple[str, ...] = ()
    first_pass_script: Path | None = None
    reference_script: Path | None = None
    notes: str = ""


@dataclass(frozen=True)
class CaseManifest:
    path: Path
    schema_version: int
    cases: tuple[CorpusCase, ...]


def load_case_manifest(path: Path | str, *, repo_root: Path | str | None = None) -> CaseManifest:
    """Load a small local case manifest and resolve repository-relative paths."""

    manifest_path = Path(path)
    root = Path(repo_root) if repo_root is not None else Path.cwd()
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("case manifest must be a JSON object")
    schema_version = payload.get("schema_version")
    if schema_version != 1:
        raise ValueError("case manifest schema_version must be 1")
    raw_cases = payload.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise ValueError("case manifest must contain a non-empty cases list")

    cases = tuple(_load_case(raw_case, root, index) for index, raw_case in enumerate(raw_cases))
    case_ids = [case.case_id for case in cases]
    duplicates = sorted({case_id for case_id in case_ids if case_ids.count(case_id) > 1})
    if duplicates:
        raise ValueError(f"duplicate case_id values: {', '.join(duplicates)}")
    return CaseManifest(path=manifest_path, schema_version=schema_version, cases=cases)


def _load_case(raw_case: Any, repo_root: Path, index: int) -> CorpusCase:
    if not isinstance(raw_case, dict):
        raise ValueError(f"case at index {index} must be an object")
    case_id = _required_str(raw_case, "case_id", index)
    tier = _required_str(raw_case, "tier", index)
    if tier not in VALID_TIERS:
        raise ValueError(f"case {case_id} has unsupported tier: {tier}")
    input_step = _resolve_existing_file(repo_root, _required_str(raw_case, "input_step", index), case_id)
    reference_script = None
    if raw_case.get("reference_script") is not None:
        reference_script = _resolve_existing_file(repo_root, _required_str(raw_case, "reference_script", index), case_id)
    first_pass_script = None
    if raw_case.get("first_pass_script") is not None:
        first_pass_script = _resolve_existing_file(repo_root, _required_str(raw_case, "first_pass_script", index), case_id)
    return CorpusCase(
        case_id=case_id,
        tier=tier,
        input_step=input_step,
        expected_bbox=_optional_bbox(raw_case.get("expected_bbox"), case_id),
        expected_counts=_optional_counts(raw_case.get("expected_counts"), case_id),
        expected_volume=_optional_number(raw_case.get("expected_volume"), case_id, "expected_volume"),
        difficulty_tags=_optional_tags(raw_case.get("difficulty_tags"), case_id),
        first_pass_script=first_pass_script,
        reference_script=reference_script,
        notes=_optional_str(raw_case.get("notes"), case_id, "notes"),
    )


def _required_str(raw_case: dict, field: str, index: int) -> str:
    value = raw_case.get(field)
    if not isinstance(value, str) or not value:
        raise ValueError(f"case at index {index} must provide non-empty string field: {field}")
    return value


def _optional_str(value: Any, case_id: str, field: str) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError(f"case {case_id} field {field} must be a string")
    return value


def _resolve_existing_file(repo_root: Path, relative_path: str, case_id: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        raise ValueError(f"case {case_id} path must be repository-relative: {relative_path}")
    resolved = (repo_root / path).resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"case {case_id} file does not exist: {relative_path}")
    return resolved


def _optional_bbox(value: Any, case_id: str) -> dict[str, list[float]] | None:
    if value is None:
        return None
    if not isinstance(value, dict) or set(value) != {"min", "max"}:
        raise ValueError(f"case {case_id} expected_bbox must contain min and max")
    return {
        "min": _number_list(value["min"], case_id, "expected_bbox.min", 3),
        "max": _number_list(value["max"], case_id, "expected_bbox.max", 3),
    }


def _optional_counts(value: Any, case_id: str) -> dict[str, int] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError(f"case {case_id} expected_counts must be an object")
    counts: dict[str, int] = {}
    for key, count in value.items():
        if not isinstance(key, str) or not isinstance(count, int):
            raise ValueError(f"case {case_id} expected_counts must map strings to integers")
        counts[key] = count
    return counts


def _optional_number(value: Any, case_id: str, field: str) -> float | None:
    if value is None:
        return None
    if not isinstance(value, int | float):
        raise ValueError(f"case {case_id} field {field} must be numeric")
    return float(value)


def _optional_tags(value: Any, case_id: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"case {case_id} difficulty_tags must be a list of non-empty strings")
    return tuple(value)


def _number_list(value: Any, case_id: str, field: str, length: int) -> list[float]:
    if not isinstance(value, list) or len(value) != length:
        raise ValueError(f"case {case_id} field {field} must contain {length} numbers")
    if not all(isinstance(item, int | float) for item in value):
        raise ValueError(f"case {case_id} field {field} must contain only numbers")
    return [float(item) for item in value]
