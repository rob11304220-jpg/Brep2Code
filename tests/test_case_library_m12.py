from __future__ import annotations

import json
from pathlib import Path

import pytest

from brep2code.corpus import load_case_manifest
from tools import audit_case_library as library_audit
from tools.audit_case_library import main as audit_case_library


DEVELOPMENT_MANIFEST = Path("case-library/manifests/self-authored/parametric-development.json")
HELD_OUT_MANIFEST = Path("case-library/manifests/self-authored/parametric-held-out.json")


def test_m12_parameter_manifests_are_family_isolated_and_loadable() -> None:
    development = load_case_manifest(DEVELOPMENT_MANIFEST)
    held_out = load_case_manifest(HELD_OUT_MANIFEST)

    assert len(development.cases) == 12
    assert len(held_out.cases) == 6
    assert {case["family_id"] for case in json.loads(DEVELOPMENT_MANIFEST.read_text(encoding="utf-8"))["cases"]} == {
        "additive_boss", "through_hole", "rounded_slot", "fillet"
    }
    assert {case["family_id"] for case in json.loads(HELD_OUT_MANIFEST.read_text(encoding="utf-8"))["cases"]} == {
        "blind_hole", "chamfer"
    }
    assert all(case.tier == "P2" and case.reference_script is not None for case in development.cases + held_out.cases)


def test_m12_case_library_audit_passes() -> None:
    audit_case_library()


def test_m20_library_audit_rejects_sequence_pair_drift(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    expansion = {
        "grammar_version": "prismatic-hole-v1",
        "oracle_provenance": "self_authored_deterministic_reference",
        "cases": [{"case_id": "sample", "case_record": "case-library/self-authored/sample/case.json", "sequence": {"operations": [{"id": "sketch_1", "kind": "SketchRect", "plane": "XY", "length_x": 10.0, "length_y": 10.0}, {"id": "base_1", "kind": "ExtrudeBase", "profile": "sketch_1", "direction": "+Z", "distance": 5.0}, {"id": "hole_1", "kind": "CutCylinder", "target": "base_1", "variant": "through", "center_xy": [5.0, 5.0], "axis": "+Z", "radius": 1.0}], "mutations": []}}],
    }
    record_path = tmp_path / "expansion.json"
    record_path.write_text(json.dumps(expansion), encoding="utf-8")
    monkeypatch.setattr(library_audit, "M20_EXPANSION", record_path)
    records = {"sample": {"sequence_pair": {"grammar_version": "prismatic-hole-v1", "oracle_provenance": "self_authored_deterministic_reference", "sequence": {"operations": [{"id": "sketch_1", "kind": "SketchRect", "plane": "XY", "length_x": 10.0, "length_y": 10.0}, {"id": "base_1", "kind": "ExtrudeBase", "profile": "sketch_1", "direction": "+Z", "distance": 5.0}, {"id": "hole_1", "kind": "CutCylinder", "target": "base_1", "variant": "through", "center_xy": [5.0, 5.0], "axis": "+Z", "radius": 1.1}], "mutations": []}}}}
    with pytest.raises(ValueError, match="differs"):
        library_audit.assert_m20_sequence_pairs(records)


def test_m21_library_audit_rejects_sequence_pair_drift(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    expansion = json.loads(Path("docs/corpus/sequence-paired/rounded-slot-v1-expansion.json").read_text(encoding="utf-8"))
    path = tmp_path / "expansion.json"
    path.write_text(json.dumps(expansion), encoding="utf-8")
    monkeypatch.setattr(library_audit, "M21_EXPANSION", path)
    records = {
        entry["case_id"]: {
            "sequence_pair": {
                "grammar_version": "rounded-slot-v1",
                "oracle_provenance": "self_authored_deterministic_reference",
                "sequence": entry["parameters"],
            }
        }
        for entry in expansion["cases"]
        if "case_record" in entry
    }
    with pytest.raises(ValueError, match="differs"):
        library_audit.assert_m21_sequence_pairs(records)


def test_m21_library_audit_rejects_deregistered_candidate_as_active() -> None:
    records = {
        "param_offset_rounded_slot_low": {
            "sequence_pair": {"grammar_version": "rounded-slot-v1"}
        }
    }
    with pytest.raises(AssertionError):
        library_audit.assert_m21_sequence_pairs(records)


def test_m22_library_audit_rejects_sequence_pair_drift(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    expansion = json.loads(Path("docs/corpus/sequence-paired/multi-contour-pocket-v1-preregistration.json").read_text(encoding="utf-8"))
    path = tmp_path / "expansion.json"
    path.write_text(json.dumps(expansion), encoding="utf-8")
    monkeypatch.setattr(library_audit, "M22_EXPANSION", path)
    records = {entry["case_id"]: {"sequence_pair": {"grammar_version": "multi-contour-pocket-v1", "oracle_provenance": "self_authored_deterministic_reference", "sequence": {"operations": []}}} for entry in expansion["cases"]}
    with pytest.raises(ValueError, match="differs"):
        library_audit.assert_m22_sequence_pairs(records)
