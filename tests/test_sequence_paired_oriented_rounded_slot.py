from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tools.audit_sequence_paired_oriented_rounded_slot import EXPANSION, assert_sequence_agreement, canonical_sequence
from tools.build_m27_oriented_rounded_slot_candidates import build


def _record() -> dict:
    return json.loads(EXPANSION.read_text(encoding="utf-8"))


def test_m27_producer_is_hash_stable(tmp_path: Path) -> None:
    assert len(build(output_root=tmp_path)) == 6
    assert len(build(output_root=tmp_path)) == 6


def test_m27_rejects_wrong_axis_for_orientation() -> None:
    entry = copy.deepcopy(_record()["cases"][0])
    entry["parameters"]["local_axis"] = "+Y"
    with pytest.raises(ValueError, match="local axis"):
        canonical_sequence(entry)


def test_m27_rejects_arbitrary_angle() -> None:
    entry = copy.deepcopy(_record()["cases"][0])
    entry["parameters"]["orientation_degrees"] = 45
    with pytest.raises(ValueError, match="local axis"):
        canonical_sequence(entry)


def test_m27_rejects_wrong_sequence_frame() -> None:
    entry = _record()["cases"][3]
    candidate = copy.deepcopy(canonical_sequence(entry))
    candidate["operations"][2]["local_axis"] = "+X"
    with pytest.raises(ValueError, match="differs"):
        assert_sequence_agreement(candidate, entry)
