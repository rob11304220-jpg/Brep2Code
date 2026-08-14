"""Validate the immutable selector-ambiguity admission record without held-out access."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/corpus/knowledge/admissions/selector-ambiguity-v1.json"
REQUIRED_SOURCE_PATHS = {
    "docs/corpus/knowledge/decisions/q01-selector-ambiguity-v1/decision.json",
    "docs/corpus/sequence-paired/selector-ambiguity-v1-preregistration.json",
    "docs/architecture/v1/m29-selector-ambiguity-controlled-production-review.md",
    "docs/architecture/v1/contracts/classified-repair-policy.md",
    "docs/corpus/knowledge/observables/planar-face-selector-cardinality-v1.json",
}
HELD_OUT_MARKERS = ("held_out", "twin_offset", "offset_nominal")
ALLOWED_HELD_OUT_TERMS = {"held_out", "reviewed_hash_pinned_documentary_evidence_only", "held_out_raw_reference"}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected object: {path}")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_no_held_out_raw_reference(value: Any, *, field: str = "record") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _assert_no_held_out_raw_reference(item, field=f"{field}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _assert_no_held_out_raw_reference(item, field=f"{field}[{index}]")
    elif isinstance(value, str) and any(marker in value.lower() for marker in HELD_OUT_MARKERS):
        if value not in ALLOWED_HELD_OUT_TERMS:
            raise ValueError(f"held-out raw reference is prohibited: {field}")


def _audit_sources(record: dict[str, Any]) -> None:
    sources = record.get("source_hashes")
    if not isinstance(sources, list):
        raise ValueError("source_hashes must be a list")
    declared = {item.get("path") for item in sources if isinstance(item, dict)}
    if declared != REQUIRED_SOURCE_PATHS:
        raise ValueError("source hash set drift")
    for item in sources:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str) or not isinstance(item.get("sha256"), str):
            raise ValueError("invalid source hash record")
        if _sha256(ROOT / item["path"]) != item["sha256"]:
            raise ValueError(f"source hash mismatch: {item['path']}")


def _audit_case(record: dict[str, Any], field: str, *, cardinality: int, terminal: str) -> None:
    case = record.get(field)
    if not isinstance(case, dict):
        raise ValueError(f"missing {field}")
    metadata_path = ROOT / str(case.get("case_metadata_path"))
    if _sha256(metadata_path) != case.get("case_metadata_sha256"):
        raise ValueError(f"case metadata hash mismatch: {field}")
    metadata = _load(metadata_path)
    if metadata.get("case_id") != case.get("case_id") or metadata.get("data_split") != "development":
        raise ValueError(f"development case identity or split drift: {field}")
    input_path = metadata_path.parent / str(metadata.get("input_step"))
    if _sha256(input_path) != case.get("input_sha256") or metadata.get("sha256") != case.get("input_sha256"):
        raise ValueError(f"input hash mismatch: {field}")
    expected = case.get("expected_selector")
    if not isinstance(expected, dict) or expected.get("cardinality") != cardinality or case.get("expected_terminal_operation") != terminal:
        raise ValueError(f"selector or terminal disposition drift: {field}")
    if field == "development_discriminating_case":
        sequence_path = ROOT / str(case.get("candidate_sequence_path"))
        if _sha256(sequence_path) != case.get("candidate_sequence_sha256"):
            raise ValueError("candidate sequence hash mismatch")
        sequence = _load(sequence_path).get("sequence", {}).get("operations", [])
        kinds = [operation.get("kind") for operation in sequence if isinstance(operation, dict)]
        if not kinds or kinds[-1] != "FailClosedAmbiguous" or any(item in kinds for item in case.get("required_absent_operations", [])):
            raise ValueError("ambiguous development sequence is not fail-closed")


def audit(record_path: Path = RECORD) -> dict[str, Any]:
    """Return a compact, deterministic audit summary without held-out access."""
    record = _load(record_path)
    if record.get("schema_version") != 1 or record.get("status") not in {"draft_pending_independent_review", "reviewed"}:
        raise ValueError("unsupported admission record status or schema")
    _assert_no_held_out_raw_reference(record)
    _audit_sources(record)
    _audit_case(record, "oracle", cardinality=1, terminal="CutCylinder")
    _audit_case(record, "development_discriminating_case", cardinality=2, terminal="FailClosedAmbiguous")
    held_out = record.get("held_out_split_isolation")
    if not isinstance(held_out, dict) or held_out.get("evidence_mode") != "reviewed_hash_pinned_documentary_evidence_only":
        raise ValueError("held-out split isolation is not documentary-only")
    controls = {item.get("id"): item.get("expected_rejection") for item in record.get("negative_controls", []) if isinstance(item, dict)}
    if controls != {"wrong-face-injection": "selector_ambiguity", "coordinate-tie-breaker-injection": "coordinate_only_support"}:
        raise ValueError("negative control taxonomy drift")
    signature = record.get("evidence_source_fields", {}).get("repair_signature", {})
    if signature != {"classification": "selector_ambiguous", "route": "stop", "terminal_reason": "stop_unsupported", "request_count": 0}:
        raise ValueError("M141 repair signature drift")
    prohibited = set(record.get("non_projection", {}).get("prohibited", []))
    if not record.get("non_projection", {}).get("evidence_only") or not {"manifest", "runtime card", "provider", "hosted execution"}.issubset(prohibited):
        raise ValueError("non-projection boundary drift")
    return {"admission_id": record["admission_id"], "record_sha256": _sha256(record_path), "source_hashes": len(record["source_hashes"]), "development_cases": 2, "held_out_access": "not_performed", "result": "pass"}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
