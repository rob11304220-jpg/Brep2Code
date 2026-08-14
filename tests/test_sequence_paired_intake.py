from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tools.audit_sequence_paired_intake import audit_preregistration, load_json


ROOT = Path(__file__).resolve().parents[1]
M23 = ROOT / "docs/corpus/sequence-paired/additive-boss-dependent-cut-v1-preregistration.json"


def _record() -> dict:
    record = json.loads(M23.read_text(encoding="utf-8"))
    record["production_checks"] = {
        "geometry": ["existing replay gates"],
        "sequence": ["exact canonical sequence"],
        "editability": ["declared mutations"],
        "semantic": ["one solid and blind-cut volume"],
        "hash_stability": ["two clean-directory normalized STEP hashes"],
        "split_isolation": ["family remains in one split"],
    }
    record["rejection_taxonomy"] = ["split_leak", "sequence_mismatch", "semantic_degeneration"]
    return record


def test_existing_m23_preregistration_satisfies_reusable_intake_contract() -> None:
    audit_preregistration(_record())


def test_intake_rejects_family_split_leak() -> None:
    record = _record()
    record["cases"][0]["data_split"] = "held_out"
    with pytest.raises(ValueError, match="split leak"):
        audit_preregistration(record)


def test_intake_rejects_missing_negative_evidence() -> None:
    record = _record()
    record["rejection_taxonomy"] = []
    with pytest.raises(ValueError, match="rejection_taxonomy"):
        audit_preregistration(record)


def test_intake_rejects_duplicate_operation_ids() -> None:
    record = copy.deepcopy(_record())
    record["canonical_sequence"][1]["id"] = record["canonical_sequence"][0]["id"]
    with pytest.raises(ValueError, match="unique"):
        audit_preregistration(record)


def test_load_json_rejects_a_non_object(tmp_path: Path) -> None:
    path = tmp_path / "record.json"
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="JSON object"):
        load_json(path)
