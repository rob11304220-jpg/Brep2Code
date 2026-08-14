from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tools.audit_sequence_paired_face_selected_dependent_cut import EXPANSION, assert_sequence_agreement, audit, build, canonical_sequence


def _record() -> dict:
    return json.loads(EXPANSION.read_text(encoding="utf-8"))


def test_m25_producer_is_hash_stable_and_audit_passes(tmp_path: Path) -> None:
    assert len(build(output_root=tmp_path)) == 6
    assert len(build(output_root=tmp_path)) == 6
    rows = audit()
    assert len(rows) == 6
    assert all(len(row["gates"]) == 3 and row["mutations"] == 5 for row in rows)


@pytest.mark.parametrize(
    ("operation", "field", "value"),
    [(4, "selector", {"normal": "+Z", "z_role": "maximum_output_z", "cardinality": "many"}), (5, "support", "base.top_face"), (4, "kind", "SelectVerticalFace")],
)
def test_m25_rejects_ambiguous_wrong_or_vertical_face_controls(operation: int, field: str, value: object) -> None:
    entry = _record()["cases"][0]
    candidate = copy.deepcopy(canonical_sequence(entry))
    candidate["operations"][operation][field] = value
    with pytest.raises(ValueError, match="differs"):
        assert_sequence_agreement(candidate, entry)


def test_m25_rejects_split_leak(tmp_path: Path) -> None:
    record = _record()
    record["cases"][0]["data_split"] = "held_out"
    path = tmp_path / "split-leak.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(ValueError, match="split leak"):
        audit(path)
