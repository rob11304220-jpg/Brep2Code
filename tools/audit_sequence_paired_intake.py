"""Validate the reusable preregistration contract for a sequence-paired family.

This deliberately validates only governance invariants shared by every family.
Each family must still provide its own geometry, sequence, editability, and
semantic audit after candidate production.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {
    "schema_version",
    "expansion_id",
    "grammar_version",
    "oracle_provenance",
    "selection_status",
    "selection_rule",
    "canonical_sequence",
    "candidate_producer",
    "contract",
    "production_checks",
    "rejection_taxonomy",
    "cases",
}
VALID_SPLITS = {"development", "held_out"}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("preregistration must be a JSON object")
    return data


def _nonempty_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    if value.startswith("replace-with-"):
        raise ValueError(f"{label} still contains a template placeholder")


def _required_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not value:
        raise ValueError(f"{label} must be a non-empty object")
    return value


def _nonempty_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise ValueError(f"{label} must be a non-empty string list")
    return value


def audit_preregistration(record: dict[str, Any]) -> None:
    missing = REQUIRED_TOP_LEVEL - record.keys()
    if missing:
        raise ValueError(f"preregistration is missing required fields: {sorted(missing)}")
    if record.get("schema_version") != 1:
        raise ValueError("unsupported preregistration schema_version")
    for field in ("expansion_id", "grammar_version", "oracle_provenance", "selection_rule"):
        _nonempty_string(record.get(field), field)
    if record.get("selection_status") != "preregistered_before_candidate_production":
        raise ValueError("selection_status must freeze the record before candidate production")

    sequence = record["canonical_sequence"]
    if not isinstance(sequence, list) or not sequence:
        raise ValueError("canonical_sequence must be a non-empty operation list")
    operation_ids: set[str] = set()
    for operation in sequence:
        operation = _required_mapping(operation, "canonical_sequence operation")
        _nonempty_string(operation.get("id"), "canonical_sequence operation id")
        _nonempty_string(operation.get("kind"), "canonical_sequence operation kind")
        if operation["id"] in operation_ids:
            raise ValueError("canonical_sequence operation ids must be unique")
        operation_ids.add(operation["id"])

    producer = _required_mapping(record["candidate_producer"], "candidate_producer")
    _nonempty_string(producer.get("planned_path"), "candidate_producer.planned_path")
    _nonempty_string(producer.get("admission_boundary"), "candidate_producer.admission_boundary")
    if producer.get("output_status") != "planned_uncreated_candidate_only":
        raise ValueError("candidate producer must remain candidate-only at preregistration")

    contract = _required_mapping(record["contract"], "contract")
    _nonempty_string(contract.get("units"), "contract.units")
    for field in ("preconditions", "semantic_invariants", "unsupported_conditions"):
        _nonempty_string_list(contract.get(field), f"contract.{field}")
    checks = _required_mapping(record["production_checks"], "production_checks")
    for field in ("geometry", "sequence", "editability", "semantic", "hash_stability", "split_isolation"):
        _nonempty_string_list(checks.get(field), f"production_checks.{field}")
    _nonempty_string_list(record["rejection_taxonomy"], "rejection_taxonomy")

    cases = record["cases"]
    if not isinstance(cases, list) or len(cases) < 2:
        raise ValueError("preregistration requires at least two frozen cases")
    ids: set[str] = set()
    family_splits: dict[str, str] = {}
    splits: set[str] = set()
    for case in cases:
        case = _required_mapping(case, "case")
        for field in ("case_id", "family_id", "variant", "candidate_directory"):
            _nonempty_string(case.get(field), f"case.{field}")
        if case["case_id"] in ids:
            raise ValueError("case_ids must be unique")
        ids.add(case["case_id"])
        if Path(case["candidate_directory"]).is_absolute() or ".." in Path(
            case["candidate_directory"]
        ).parts:
            raise ValueError("candidate_directory must be a safe relative path")
        split = case.get("data_split")
        if split not in VALID_SPLITS:
            raise ValueError("case.data_split must be development or held_out")
        splits.add(split)
        previous = family_splits.setdefault(case["family_id"], split)
        if previous != split:
            raise ValueError("family split leak detected")
        _required_mapping(case.get("parameters"), "case.parameters")
        mutations = case.get("mutations")
        if not isinstance(mutations, list) or not mutations:
            raise ValueError("case.mutations must be a non-empty list")
        for mutation in mutations:
            mutation = _required_mapping(mutation, "mutation")
            _nonempty_string(mutation.get("kind"), "mutation.kind")
            if not isinstance(mutation.get("delta"), (int, float)) or mutation["delta"] == 0:
                raise ValueError("mutation.delta must be a non-zero number")
    if splits != VALID_SPLITS:
        raise ValueError("preregistration must include development and held_out cases")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path, help="frozen family preregistration JSON")
    args = parser.parse_args()
    audit_preregistration(load_json(args.record))
    print(f"sequence-paired intake audit passed: {args.record}")


if __name__ == "__main__":
    main()
