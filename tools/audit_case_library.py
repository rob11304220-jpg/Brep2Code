"""Offline consistency audit for self-authored case-library records and manifests."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/corpus/registry/self-authored.json"
MANIFESTS = ROOT / "case-library/manifests/self-authored"
M20_EXPANSION = ROOT / "docs/corpus/sequence-paired/prismatic-hole-v1-expansion.json"
M21_EXPANSION = ROOT / "docs/corpus/sequence-paired/rounded-slot-v1-expansion.json"
M22_EXPANSION = ROOT / "docs/corpus/sequence-paired/multi-contour-pocket-v1-preregistration.json"
M23_EXPANSION = ROOT / "docs/corpus/sequence-paired/additive-boss-dependent-cut-v1-preregistration.json"
M25_EXPANSION = ROOT / "docs/corpus/sequence-paired/face-selected-dependent-cut-v1-preregistration.json"
M26_EXPANSION = ROOT / "docs/corpus/sequence-paired/multi-inner-loop-pocket-v1-preregistration.json"
M27_EXPANSION = ROOT / "docs/corpus/sequence-paired/oriented-rounded-slot-v1-preregistration.json"
M108_EXPANSION = ROOT / "docs/corpus/sequence-paired/revolve-v1-preregistration.json"

try:  # Supports both direct execution and package import from tests.
    from tools.audit_sequence_paired_prismatic_hole import assert_sequence_agreement, canonical_sequence
    from tools.audit_sequence_paired_rounded_slot import assert_sequence_agreement as assert_rounded_slot_sequence_agreement
    from tools.audit_sequence_paired_multi_contour_pocket import assert_sequence_agreement as assert_multi_contour_pocket_sequence_agreement
    from tools.audit_sequence_paired_additive_boss_dependent_cut import assert_sequence_agreement as assert_additive_boss_sequence_agreement
    from tools.audit_sequence_paired_face_selected_dependent_cut import assert_sequence_agreement as assert_face_selected_sequence_agreement
    from tools.audit_sequence_paired_multi_inner_loop_pocket import assert_sequence_agreement as assert_multi_inner_loop_sequence_agreement
    from tools.audit_sequence_paired_oriented_rounded_slot import assert_sequence_agreement as assert_oriented_rounded_slot_sequence_agreement
    from tools.audit_sequence_paired_revolve import canonical_sequence as canonical_revolve_sequence
except ModuleNotFoundError:  # pragma: no cover - direct script entrypoint only
    from audit_sequence_paired_prismatic_hole import assert_sequence_agreement, canonical_sequence
    from audit_sequence_paired_rounded_slot import assert_sequence_agreement as assert_rounded_slot_sequence_agreement
    from audit_sequence_paired_multi_contour_pocket import assert_sequence_agreement as assert_multi_contour_pocket_sequence_agreement
    from audit_sequence_paired_additive_boss_dependent_cut import assert_sequence_agreement as assert_additive_boss_sequence_agreement
    from audit_sequence_paired_face_selected_dependent_cut import assert_sequence_agreement as assert_face_selected_sequence_agreement
    from audit_sequence_paired_multi_inner_loop_pocket import assert_sequence_agreement as assert_multi_inner_loop_sequence_agreement
    from audit_sequence_paired_oriented_rounded_slot import assert_sequence_agreement as assert_oriented_rounded_slot_sequence_agreement
    from audit_sequence_paired_revolve import canonical_sequence as canonical_revolve_sequence


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_m20_sequence_pairs(records: dict[str, dict]) -> None:
    """Validate the ADR-0019-scoped sequence metadata without widening its scope."""

    expansion = load_json(M20_EXPANSION)
    entries = {entry["case_id"]: entry for entry in expansion["cases"]}
    paired_ids = {
        case_id
        for case_id, record in records.items()
        if record.get("sequence_pair", {}).get("grammar_version") == "prismatic-hole-v1"
    }
    assert paired_ids == set(entries), paired_ids
    for case_id, entry in entries.items():
        record = records[case_id]
        pair = record["sequence_pair"]
        assert pair["grammar_version"] == expansion["grammar_version"]
        assert pair["oracle_provenance"] == expansion["oracle_provenance"]
        canonical_sequence(pair["sequence"])
        assert_sequence_agreement(pair["sequence"], entry["sequence"])
        candidate_path = pair.get("candidate_sequence")
        if candidate_path is not None:
            candidate_file = ROOT / entry["case_record"]
            candidate_sequence = load_json(candidate_file.parent / candidate_path)
            assert candidate_sequence["grammar_version"] == pair["grammar_version"]
            assert_sequence_agreement(candidate_sequence["sequence"], pair["sequence"])


def assert_m21_sequence_pairs(records: dict[str, dict]) -> None:
    """Validate active M21 rows while retaining deregistered candidates as history."""

    expansion = load_json(M21_EXPANSION)
    entries = {entry["case_id"]: entry for entry in expansion["cases"]}
    active_entries = {
        case_id: entry
        for case_id, entry in entries.items()
        if "case_record" in entry
    }
    experimental_entries = {
        case_id: entry
        for case_id, entry in entries.items()
        if "candidate_directory" in entry
    }
    paired_ids = {
        case_id
        for case_id, record in records.items()
        if record.get("sequence_pair", {}).get("grammar_version") == "rounded-slot-v1"
    }
    assert paired_ids == set(active_entries), paired_ids
    assert not (set(records) & set(experimental_entries))
    for case_id, entry in active_entries.items():
        record = records[case_id]
        pair = record["sequence_pair"]
        assert pair["grammar_version"] == expansion["grammar_version"]
        assert pair["oracle_provenance"] == expansion["oracle_provenance"]
        assert_rounded_slot_sequence_agreement(pair["sequence"], entry)
        candidate_file = ROOT / entry["case_record"]
        candidate_sequence = load_json(candidate_file.parent / pair["candidate_sequence"])
        assert candidate_sequence["grammar_version"] == pair["grammar_version"]
        assert_rounded_slot_sequence_agreement(candidate_sequence["sequence"], entry)


def assert_m22_sequence_pairs(records: dict[str, dict]) -> None:
    """Validate the ADR-0024-scoped multi-contour-pocket metadata only."""

    expansion = load_json(M22_EXPANSION)
    entries = {entry["case_id"]: entry for entry in expansion["cases"]}
    paired_ids = {case_id for case_id, record in records.items() if record.get("sequence_pair", {}).get("grammar_version") == "multi-contour-pocket-v1"}
    assert paired_ids == set(entries), paired_ids
    for case_id, entry in entries.items():
        record = records[case_id]
        pair = record["sequence_pair"]
        assert pair["grammar_version"] == expansion["grammar_version"]
        assert pair["oracle_provenance"] == expansion["oracle_provenance"]
        assert_multi_contour_pocket_sequence_agreement(pair["sequence"], entry)
        candidate_file = ROOT / entry["candidate_directory"] / pair["candidate_sequence"]
        candidate_sequence = load_json(candidate_file)
        assert candidate_sequence["grammar_version"] == pair["grammar_version"]
        assert_multi_contour_pocket_sequence_agreement(candidate_sequence["sequence"], entry)


def assert_m23_sequence_pairs(records: dict[str, dict]) -> None:
    """Validate the ADR-0027-scoped additive-boss sequence metadata only."""

    expansion = load_json(M23_EXPANSION)
    entries = {entry["case_id"]: entry for entry in expansion["cases"]}
    paired_ids = {case_id for case_id, record in records.items() if record.get("sequence_pair", {}).get("grammar_version") == "additive-boss-dependent-cut-v1"}
    assert paired_ids == set(entries), paired_ids
    for case_id, entry in entries.items():
        record = records[case_id]
        pair = record["sequence_pair"]
        assert pair["grammar_version"] == expansion["grammar_version"]
        assert pair["oracle_provenance"] == expansion["oracle_provenance"]
        assert_additive_boss_sequence_agreement(pair["sequence"], entry)
        candidate_file = ROOT / entry["candidate_directory"] / pair["candidate_sequence"]
        candidate_sequence = load_json(candidate_file)
        assert candidate_sequence["grammar_version"] == pair["grammar_version"]
        assert_additive_boss_sequence_agreement(candidate_sequence["sequence"], entry)


def assert_m25_sequence_pairs(records: dict[str, dict]) -> None:
    """Validate the ADR-0029-scoped face-selected sequence metadata only."""

    expansion = load_json(M25_EXPANSION)
    entries = {entry["case_id"]: entry for entry in expansion["cases"]}
    paired_ids = {case_id for case_id, record in records.items() if record.get("sequence_pair", {}).get("grammar_version") == "face-selected-dependent-cut-v1"}
    assert paired_ids == set(entries), paired_ids
    for case_id, entry in entries.items():
        record = records[case_id]
        pair = record["sequence_pair"]
        assert pair["grammar_version"] == expansion["grammar_version"]
        assert pair["oracle_provenance"] == expansion["oracle_provenance"]
        assert_face_selected_sequence_agreement(pair["sequence"], entry)
        candidate_sequence = load_json(ROOT / entry["candidate_directory"] / pair["candidate_sequence"])
        assert candidate_sequence["grammar_version"] == pair["grammar_version"]
        assert_face_selected_sequence_agreement(candidate_sequence["sequence"], entry)


def assert_m26_sequence_pairs(records: dict[str, dict]) -> None:
    """Validate the ADR-0031-scoped multi-inner-loop metadata only."""

    expansion = load_json(M26_EXPANSION)
    entries = {entry["case_id"]: entry for entry in expansion["cases"]}
    paired_ids = {case_id for case_id, record in records.items() if record.get("sequence_pair", {}).get("grammar_version") == "multi-inner-loop-pocket-v1"}
    assert paired_ids == set(entries), paired_ids
    for case_id, entry in entries.items():
        record = records[case_id]
        pair = record["sequence_pair"]
        assert pair["grammar_version"] == expansion["grammar_version"]
        assert pair["oracle_provenance"] == expansion["oracle_provenance"]
        assert_multi_inner_loop_sequence_agreement(pair["sequence"], entry)
        candidate_sequence = load_json(ROOT / entry["candidate_directory"] / pair["candidate_sequence"])
        assert candidate_sequence["grammar_version"] == pair["grammar_version"]
        assert_multi_inner_loop_sequence_agreement(candidate_sequence["sequence"], entry)


def assert_m27_sequence_pairs(records: dict[str, dict]) -> None:
    """Validate the ADR-0033-scoped oriented rounded-slot metadata only."""
    expansion = load_json(M27_EXPANSION)
    entries = {entry["case_id"]: entry for entry in expansion["cases"]}
    paired_ids = {case_id for case_id, record in records.items() if record.get("sequence_pair", {}).get("grammar_version") == "oriented-rounded-slot-v1"}
    assert paired_ids == set(entries), paired_ids
    for case_id, entry in entries.items():
        pair = records[case_id]["sequence_pair"]
        assert pair["oracle_provenance"] == expansion["oracle_provenance"]
        assert_oriented_rounded_slot_sequence_agreement(pair["sequence"], entry)
        candidate = load_json(ROOT / entry["candidate_directory"] / pair["candidate_sequence"])
        assert candidate["grammar_version"] == pair["grammar_version"]
        assert_oriented_rounded_slot_sequence_agreement(candidate["sequence"], entry)


def assert_m108_sequence_pairs(records: dict[str, dict]) -> None:
    """Validate the ADR-0064-scoped revolve metadata only."""
    expansion = load_json(M108_EXPANSION)
    entries = {entry["case_id"]: entry for entry in expansion["cases"]}
    paired_ids = {case_id for case_id, record in records.items() if record.get("sequence_pair", {}).get("grammar_version") == "revolve-v1"}
    assert paired_ids == set(entries), paired_ids
    for case_id, entry in entries.items():
        pair = records[case_id]["sequence_pair"]
        assert pair["oracle_provenance"] == expansion["oracle_provenance"]
        assert pair["sequence"] == canonical_revolve_sequence(entry)
        candidate = load_json(ROOT / entry["candidate_directory"] / pair["candidate_sequence"])
        assert candidate["grammar_version"] == pair["grammar_version"]
        assert candidate["sequence"] == canonical_revolve_sequence(entry)


def assert_replay(record_path: Path, record: dict) -> None:
    """Replay one local reference script and compare the existing geometry baseline."""

    with tempfile.TemporaryDirectory(prefix="brep2code-case-replay-") as temp_dir:
        workdir = Path(temp_dir)
        subprocess.run(
            [sys.executable, str(record_path.parent / record["reference_script"])],
            cwd=workdir,
            check=True,
        )
        from brep2code.brep.probes import load_model, probe_summary

        summary = probe_summary(load_model(workdir / "output" / "model.step"))
        baseline = record["expected"]
        assert summary["counts"] == baseline["counts"], record["case_id"]
        for actual, expected in zip(summary["bbox"]["min"], baseline["bbox"]["min"], strict=True):
            assert abs(actual - expected) < 1e-5, record["case_id"]
        for actual, expected in zip(summary["bbox"]["max"], baseline["bbox"]["max"], strict=True):
            assert abs(actual - expected) < 1e-5, record["case_id"]
        assert abs(summary["volume"] - baseline["volume"]) < 1e-5, record["case_id"]


def main(replay: bool = False) -> None:
    registry = load_json(REGISTRY)
    records = {}
    families: dict[str, set[str]] = {}
    for entry in registry["cases"]:
        record_path = ROOT / entry["case_record"]
        record = load_json(record_path)
        case_id = record["case_id"]
        assert entry["case_id"] == case_id
        assert (record_path.parent / record["input_step"]).is_file()
        assert (record_path.parent / record["reference_script"]).is_file() if record["reference_script_status"] == "available" else True
        digest = hashlib.sha256((record_path.parent / record["input_step"]).read_bytes()).hexdigest()
        assert digest == record["sha256"], case_id
        records[case_id] = record
        if "family_id" in record:
            families.setdefault(record["family_id"], set()).add(record["data_split"])
            if replay and record.get("reference_script"):
                assert_replay(record_path, record)
    assert all(len(splits) == 1 for splits in families.values()), families
    assert_m20_sequence_pairs(records)
    assert_m21_sequence_pairs(records)
    assert_m22_sequence_pairs(records)
    assert_m23_sequence_pairs(records)
    assert_m25_sequence_pairs(records)
    assert_m26_sequence_pairs(records)
    assert_m27_sequence_pairs(records)
    assert_m108_sequence_pairs(records)

    parametric_ids: set[str] = set()
    for name in ("parametric-development.json", "parametric-held-out.json"):
        manifest = load_json(MANIFESTS / name)
        expected_split = "held_out" if "held-out" in name else "development"
        for case in manifest["cases"]:
            record = records[case["case_id"]]
            assert case["family_id"] == record["family_id"]
            assert case["data_split"] == record["data_split"] == expected_split
            assert case["parameters"] == record["parameters"]
            assert case["expected_bbox"] == record["expected"]["bbox"]
            assert case["expected_counts"] == record["expected"]["counts"]
            assert case["expected_volume"] == record["expected"]["volume"]
            parametric_ids.add(case["case_id"])
    assert len(parametric_ids) == 18
    assert not any(case_id.startswith("param_counterbore_") for case_id in parametric_ids)
    print(f"case-library audit passed: {len(records)} records, {len(parametric_ids)} M12 parameter cases")


if __name__ == "__main__":
    main(replay="--replay" in sys.argv[1:])
