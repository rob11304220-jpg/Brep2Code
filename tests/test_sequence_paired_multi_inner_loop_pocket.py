from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tools.audit_sequence_paired_multi_inner_loop_pocket import EXPANSION, assert_sequence_agreement, canonical_sequence
from tools.build_m26_multi_inner_loop_pocket_candidates import build


def _record() -> dict:
    return json.loads(EXPANSION.read_text(encoding="utf-8"))


def test_m26_producer_is_hash_stable(tmp_path: Path) -> None:
    assert len(build(output_root=tmp_path)) == 6
    assert len(build(output_root=tmp_path)) == 6


def test_m26_rejects_single_inner_loop_sequence() -> None:
    entry = _record()["cases"][0]
    candidate = copy.deepcopy(canonical_sequence(entry))
    candidate["operations"][2].pop("inner_right_center_xy")
    with pytest.raises(ValueError, match="differs"):
        assert_sequence_agreement(candidate, entry)


def test_m26_rejects_overlapping_inner_loops() -> None:
    entry = copy.deepcopy(_record()["cases"][0])
    entry["parameters"]["inner_right_center_xy"] = entry["parameters"]["inner_left_center_xy"]
    with pytest.raises(ValueError, match="overlap"):
        canonical_sequence(entry)


def test_m26_rejects_noncontained_inner_loop() -> None:
    entry = copy.deepcopy(_record()["cases"][0])
    entry["parameters"]["inner_left_center_xy"] = [1.0, 1.0]
    with pytest.raises(ValueError, match="contained"):
        canonical_sequence(entry)
