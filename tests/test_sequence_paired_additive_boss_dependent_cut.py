from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tools.audit_sequence_paired_additive_boss_dependent_cut import EXPANSION, assert_sequence_agreement, audit, canonical_sequence
from tools.build_m23_additive_boss_dependent_cut_candidates import build


def _record() -> dict:
    return json.loads(EXPANSION.read_text(encoding="utf-8"))


def test_m23_producer_is_hash_stable_and_audit_passes(tmp_path: Path) -> None:
    assert len(build(output_root=tmp_path)) == 6
    assert len(build(output_root=tmp_path)) == 6
    assert len(audit()) == 6


def test_m23_rejects_base_targeted_cut() -> None:
    entry = _record()["cases"][0]
    candidate = copy.deepcopy(canonical_sequence(entry))
    candidate["operations"][5]["target"] = "base"
    with pytest.raises(ValueError, match="differs"):
        assert_sequence_agreement(candidate, entry)


def test_m23_rejects_no_boss_or_disconnected_boss_controls() -> None:
    entry = _record()["cases"][0]
    no_boss = copy.deepcopy(canonical_sequence(entry))
    no_boss["operations"][3]["kind"] = "NoBoss"
    disconnected = copy.deepcopy(canonical_sequence(entry))
    disconnected["operations"][3]["operation"] = "new_body"
    with pytest.raises(ValueError, match="differs"):
        assert_sequence_agreement(no_boss, entry)
    with pytest.raises(ValueError, match="differs"):
        assert_sequence_agreement(disconnected, entry)


def test_m23_rejects_through_cut() -> None:
    entry = copy.deepcopy(_record()["cases"][0])
    entry["parameters"]["cut_depth"] = entry["parameters"]["boss_height"]
    with pytest.raises(ValueError, match="blind"):
        canonical_sequence(entry)


def test_m23_rejects_split_leak(tmp_path: Path) -> None:
    record = _record()
    record["cases"][0]["data_split"] = "held_out"
    path = tmp_path / "split-leak.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(ValueError, match="split leak"):
        audit(path)
