from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CROSSWALK = ROOT / "docs/corpus/knowledge/development-evidence-crosswalk-v1.json"
MAPPING = ROOT / "docs/corpus/knowledge/implementation-contract-relationships-v1.json"
COVERAGE = ROOT / "docs/corpus/knowledge/implementation-contract-coverage-v1.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_m154_coverage_includes_every_reviewed_hypothesis() -> None:
    crosswalk = _load(CROSSWALK)
    coverage = _load(COVERAGE)

    assert coverage["schema_version"] == 1
    assert coverage["coverage_id"] == "implementation-contract-coverage-v1"

    expected = {item["id"] for item in crosswalk["hypotheses"]}
    actual = {item["hypothesis_id"] for item in coverage["hypothesis_coverage"]}

    assert actual == expected


def test_m154_coverage_tracks_existing_mapping_status_without_widening() -> None:
    mapping_payload = _load(MAPPING)
    coverage_payload = _load(COVERAGE)

    mapping_by_hypothesis = {
        item["hypothesis_id"]: item for item in mapping_payload["mappings"]
    }
    coverage_by_hypothesis = {
        item["hypothesis_id"]: item for item in coverage_payload["hypothesis_coverage"]
    }

    selector = coverage_by_hypothesis["hm-q01-selector-cardinality-v1"]
    assert selector["coverage_status"] == "contract_only"
    assert selector["mapping_ids"] == ["selector-cardinality-contract-alignment-v1"]
    assert selector["represented_stages"] == ["Q01", "Q02", "Q03", "Q04"]
    assert selector["missing_stages"] == []
    assert mapping_by_hypothesis["hm-q01-selector-cardinality-v1"]["implementation_status"] == "contract_only"

    blind_through = coverage_by_hypothesis["hm-q01-blind-through-observability-v1"]
    assert blind_through["coverage_status"] == "contract_only"
    assert blind_through["mapping_ids"] == ["blind-through-observability-contract-alignment-v1"]
    assert blind_through["represented_stages"] == ["Q01", "Q02"]
    assert blind_through["missing_stages"] == []
    assert mapping_by_hypothesis["hm-q01-blind-through-observability-v1"]["implementation_status"] == "contract_only"


def test_m154_coverage_marks_only_unmapped_hypotheses_as_missing_link() -> None:
    mapping_payload = _load(MAPPING)
    coverage_payload = _load(COVERAGE)

    mapped = {item["hypothesis_id"] for item in mapping_payload["mappings"]}
    for item in coverage_payload["hypothesis_coverage"]:
        if item["hypothesis_id"] in mapped:
            continue
        assert item["coverage_status"] == "missing_link"
        assert item["mapping_ids"] == []
        assert item["represented_stages"] == []
        assert item["missing_stages"] == item["declared_stages"]
