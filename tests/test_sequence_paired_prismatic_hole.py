from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tools.audit_sequence_paired_prismatic_hole import (
    EXPANSION,
    SEED,
    apply_mutation,
    assert_sequence_agreement,
    audit,
    canonical_sequence,
)
from tools.build_m20_counterbore_candidates import build


def _seed() -> dict:
    return json.loads(SEED.read_text(encoding="utf-8"))


def test_m20_expansion_audit_passes_all_three_layers() -> None:
    rows = audit()
    assert [row["case_id"] for row in rows] == [
        "param_through_hole_low",
        "param_through_hole_nominal",
        "param_through_hole_high",
        "param_counterbore_low",
        "param_counterbore_nominal",
        "param_counterbore_high",
        "param_blind_hole_low",
        "param_blind_hole_nominal",
        "param_blind_hole_high",
    ]
    assert all(len(row["gates"]) == 3 and row["mutations"] == 2 for row in rows)


def test_m20_sequence_comparison_rejects_parameter_drift() -> None:
    oracle = _seed()["cases"][0]["sequence"]
    candidate = copy.deepcopy(oracle)
    candidate["operations"][2]["radius"] = 4.1
    with pytest.raises(ValueError, match="differs"):
        assert_sequence_agreement(candidate, oracle)


def test_m20_sequence_normalization_rejects_extra_operation() -> None:
    sequence = copy.deepcopy(_seed()["cases"][0]["sequence"])
    sequence["operations"].append({"id": "extra", "kind": "Fillet"})
    with pytest.raises(ValueError, match="exactly three"):
        canonical_sequence(sequence)


def test_m20_mutation_rejects_incompatible_variant() -> None:
    sequence = _seed()["cases"][0]["sequence"]
    with pytest.raises(ValueError, match="incompatible"):
        apply_mutation(sequence, {"kind": "hole_depth", "delta": 1.0})


def test_m20_seed_file_is_preregistered_and_family_isolated() -> None:
    seed = _seed()
    assert seed["selection_status"] == "preregistered"
    assert {entry["data_split"] for entry in seed["cases"]} == {"development", "held_out"}
    assert len({entry["family_id"] for entry in seed["cases"]}) == len(seed["cases"])


def test_m20_expansion_is_preregistered_with_family_isolated_split() -> None:
    expansion = json.loads(EXPANSION.read_text(encoding="utf-8"))
    assert expansion["selection_status"] == "preregistered"
    assert len(expansion["cases"]) == 9
    assert sum(entry["data_split"] == "development" for entry in expansion["cases"]) == 6
    assert sum(entry["data_split"] == "held_out" for entry in expansion["cases"]) == 3
    assert {entry["family_id"] for entry in expansion["cases"] if entry["data_split"] == "development"} == {
        "through_hole", "counterbore"
    }
    assert {entry["family_id"] for entry in expansion["cases"] if entry["data_split"] == "held_out"} == {"blind_hole"}


def test_m20_counterbore_producer_is_hash_stable_and_unmanifested() -> None:
    before = {
        entry["case_id"]: json.loads((Path(entry["case_record"]).read_text(encoding="utf-8")))["sha256"]
        for entry in json.loads(EXPANSION.read_text(encoding="utf-8"))["cases"]
        if entry["family_id"] == "counterbore"
    }
    assert build() == list(before)
    after = {
        case_id: json.loads((Path("case-library/self-authored") / case_id / "case.json").read_text(encoding="utf-8"))
        for case_id in before
    }
    assert {case_id: record["sha256"] for case_id, record in after.items()} == before
    assert all(record["status"] == "active" and "sequence_pair" in record for record in after.values())


def test_m20_expansion_rejects_mismatched_candidate_sequence() -> None:
    expansion = json.loads(EXPANSION.read_text(encoding="utf-8"))
    entry = next(entry for entry in expansion["cases"] if entry["family_id"] == "counterbore")
    candidate = json.loads(Path(entry["candidate_sequence"]).read_text(encoding="utf-8"))
    candidate["sequence"]["operations"][2]["bore_depth"] += 0.1
    with pytest.raises(ValueError, match="differs"):
        assert_sequence_agreement(candidate["sequence"], entry["sequence"])


def test_m20_expansion_rejects_family_split_leak(tmp_path: Path) -> None:
    expansion = json.loads(EXPANSION.read_text(encoding="utf-8"))
    expansion["cases"][0]["data_split"] = "held_out"
    leaked_record = tmp_path / "split-leak.json"
    leaked_record.write_text(json.dumps(expansion), encoding="utf-8")
    with pytest.raises(ValueError, match="split leak"):
        audit(leaked_record)
