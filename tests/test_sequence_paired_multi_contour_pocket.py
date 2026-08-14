from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tools.audit_sequence_paired_multi_contour_pocket import EXPANSION, assert_sequence_agreement, audit, canonical_sequence
from tools.build_m22_multi_contour_pocket_candidates import build


def _record() -> dict:
    return json.loads(EXPANSION.read_text(encoding="utf-8"))


def test_m22_producer_is_hash_stable_and_audit_passes(tmp_path: Path) -> None:
    assert len(build(output_root=tmp_path)) == 6
    assert len(build(output_root=tmp_path)) == 6
    rows = audit()
    assert len(rows) == 6
    assert all(len(row["gates"]) == 3 and row["mutations"] == 4 for row in rows)


def test_m22_rejects_single_loop_sequence() -> None:
    entry = _record()["cases"][0]
    candidate = copy.deepcopy(canonical_sequence(entry))
    candidate["operations"][2]["kind"] = "SketchRect"
    with pytest.raises(ValueError, match="differs"):
        assert_sequence_agreement(candidate, entry)


def test_m22_rejects_noncontained_inner_loop() -> None:
    entry = copy.deepcopy(_record()["cases"][0])
    entry["parameters"]["inner_center_xy"] = [1.0, 1.0]
    with pytest.raises(ValueError, match="contained"):
        canonical_sequence(entry)


def test_m22_rejects_split_leak(tmp_path: Path) -> None:
    record = _record()
    record["cases"][0]["data_split"] = "held_out"
    path = tmp_path / "split-leak.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(ValueError, match="split counts|split leak"):
        audit(path)
