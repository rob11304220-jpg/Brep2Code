from __future__ import annotations

import json
from pathlib import Path

from brep2code.agent.repair_policy import classify_terminal_feedback


ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "docs/corpus/knowledge/implementation-contract-relationships-v1.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _selector_mapping() -> dict:
    return next(
        item
        for item in _load(MAPPING)["mappings"]
        if item["hypothesis_id"] == "hm-q01-selector-cardinality-v1"
    )


def test_m152_mapping_tracks_selector_cardinality_as_contract_only() -> None:
    payload = _load(MAPPING)

    assert payload["schema_version"] == 1
    assert payload["mapping_id"] == "implementation-contract-relationships-v1"
    assert payload["crosswalk"]["id"] == "development-evidence-crosswalk-v1"
    assert payload["case_evidence_mapping"]["id"] == "case-evidence-relationships-v1"

    mapping = _selector_mapping()
    assert mapping["hypothesis_id"] == "hm-q01-selector-cardinality-v1"
    assert mapping["implementation_status"] == "contract_only"
    assert mapping["relationship_ids"] == [
        "selector-cardinality-development-oracle",
        "selector-cardinality-development-discriminating",
        "selector-cardinality-held-out-documentary-control",
    ]


def test_m152_mapping_points_to_reviewed_q01_q02_sources() -> None:
    mapping = _selector_mapping()
    q01 = _load(ROOT / mapping["q01"]["source_path"])
    q02 = _load(ROOT / mapping["q02"]["source_path"])

    assert q01["unit_id"] == "planar-face-selector-cardinality-v1"
    assert "candidate cardinality" in q01["measurement"]["reported_fields"]
    assert q02["unit_id"] == "face-selected-dependent-cut-v1"
    assert "SelectPlanarFace(unique +Z maximum-Z)" in q02["sequence"]["canonical_pattern"]


def test_m152_mapping_q04_route_remains_fail_closed() -> None:
    mapping = _selector_mapping()
    q04 = mapping["q04"]

    assert (ROOT / q04["contract_path"]).is_file()
    assert (ROOT / q04["code_path"]).is_file()
    for path in q04["test_paths"]:
        assert (ROOT / path).is_file()

    decision = classify_terminal_feedback({"status": "fail", "repair_classification": "selector_ambiguous"})
    assert decision.route == "stop"
    assert decision.allowed is False
    assert decision.stop_reason == "stop_unsupported"


def test_m152_validation_evidence_paths_exist() -> None:
    mapping = _selector_mapping()
    for relative in mapping["validation_evidence"]:
        assert (ROOT / relative).is_file(), relative
