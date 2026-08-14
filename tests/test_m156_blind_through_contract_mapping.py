from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "docs/corpus/knowledge/implementation-contract-relationships-v1.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _mapping() -> dict:
    return next(
        item
        for item in _load(MAPPING)["mappings"]
        if item["hypothesis_id"] == "hm-q01-blind-through-observability-v1"
    )


def test_m156_mapping_tracks_only_the_reviewed_declared_stages() -> None:
    mapping = _mapping()

    assert mapping["implementation_status"] == "contract_only"
    assert mapping["relationship_ids"] == [
        "blind-through-development-observable",
        "blind-through-held-out-documentary-observable",
        "blind-through-negative-control",
    ]
    assert set(mapping) >= {"q01", "q02", "validation_evidence", "boundary"}
    assert "q03" not in mapping
    assert "q04" not in mapping
    assert "no repair route" in mapping["boundary"]


def test_m156_mapping_points_to_reviewed_q01_q02_sources() -> None:
    mapping = _mapping()
    q01 = _load(ROOT / mapping["q01"]["source_path"])
    q02 = _load(ROOT / mapping["q02"]["source_path"])

    assert q01["unit_id"] == "blind-through-cylindrical-extent-v1"
    assert q01["measurement"]["scope"].startswith("single cylindrical face")
    assert q02["unit_id"] == "prismatic-hole-v1"
    assert q02["sequence"]["canonical_pattern"] == ["SketchRect", "ExtrudeBase", "CutCylinder"]


def test_m156_mapping_validation_evidence_and_non_projection_paths_exist() -> None:
    mapping = _mapping()

    for relative in mapping["validation_evidence"]:
        assert (ROOT / relative).is_file(), relative
    assert "No runtime observation helper" in mapping["non_generalization"][-1]
