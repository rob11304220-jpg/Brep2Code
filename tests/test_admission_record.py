from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.audit_admission_record import RECORD, audit


def test_selector_ambiguity_admission_record_audits_without_held_out_access() -> None:
    result = audit()
    assert result["result"] == "pass"
    assert result["held_out_access"] == "not_performed"
    assert result["development_cases"] == 2


def test_admission_audit_rejects_held_out_raw_reference(tmp_path: Path) -> None:
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    record["held_out_split_isolation"]["raw_fixture_path"] = "case-library/self-authored/twin_offset/input.step"
    path = tmp_path / "record.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(ValueError, match="held-out raw reference"):
        audit(path)
