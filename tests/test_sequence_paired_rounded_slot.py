from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tools.audit_sequence_paired_rounded_slot import EXPANSION, assert_sequence_agreement, audit, canonical_sequence
from tools.build_m21_offset_rounded_slot_candidates import build


def _record() -> dict:
    return json.loads(EXPANSION.read_text(encoding="utf-8"))


def test_m21_producer_is_hash_stable_and_audit_passes() -> None:
    assert len(build()) == 3
    assert len(build()) == 3
    rows = audit()
    assert len(rows) == 6
    assert all(len(row["gates"]) == 3 and row["mutations"] == 3 for row in rows)


def test_m21_rejects_rectangular_slot_sequence() -> None:
    entry = _record()["cases"][0]
    candidate = copy.deepcopy(canonical_sequence(entry))
    candidate["operations"][2]["kind"] = "SketchRect"
    with pytest.raises(ValueError, match="differs"):
        assert_sequence_agreement(candidate, entry)


def test_m21_rejects_split_leak(tmp_path: Path) -> None:
    record = _record()
    record["cases"][0]["data_split"] = "held_out"
    path = tmp_path / "leak.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(ValueError, match="split leak|development count"):
        audit(path)
