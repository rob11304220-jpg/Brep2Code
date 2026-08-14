"""Audit M143's metadata-only case-library admission profile."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "docs/corpus/knowledge/admissions/case-library-admission-profile-v1.json"
REGISTRY = ROOT / "docs/corpus/registry/self-authored.json"
REQUIRED_SOURCES = {
    "docs/corpus/registry/self-authored.json",
    "docs/corpus/knowledge/coverage-matrix.json",
    "docs/corpus/knowledge/admissions/selector-ambiguity-v1.json",
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _profile_for(case: dict[str, Any]) -> str:
    grammar = case.get("sequence_pair", {}).get("grammar_version")
    if grammar == "face-selected-dependent-cut-v1":
        return "unique_planar_selector"
    if isinstance(grammar, str):
        return "family_scoped_sequence"
    return "baseline_or_unpaired"


def inventory() -> dict[str, Any]:
    """Return metadata-only inventory facts, including authoritative-record drift."""
    registry = _load(REGISTRY)
    rows = registry.get("cases")
    if not isinstance(rows, list) or not rows:
        raise ValueError("registry has no cases")
    counts: Counter[str] = Counter()
    splits: Counter[str] = Counter()
    conflicts: list[dict[str, str]] = []
    for row in rows:
        if not isinstance(row, dict) or row.get("status") != "active":
            raise ValueError("M143 inventory accepts active registry rows only")
        metadata = _load(ROOT / str(row.get("case_record")))
        if metadata.get("case_id") != row.get("case_id"):
            conflicts.append({"case_id": str(row.get("case_id")), "kind": "case_id_mismatch"})
            continue
        if metadata.get("status") != "active":
            conflicts.append({"case_id": str(row.get("case_id")), "kind": "registry_active_case_metadata_not_active"})
        counts[_profile_for(metadata)] += 1
        splits[str(metadata.get("data_split", "undeclared"))] += 1
    return {"active_case_count": len(rows), "profile_counts": dict(sorted(counts.items())), "declared_split_counts": dict(sorted(splits.items())), "inventory_conflicts": conflicts, "fixture_access": "not_performed"}


def audit(profile_path: Path = PROFILE) -> dict[str, Any]:
    """Read registry and case metadata only; never open fixture or script paths."""
    profile = _load(profile_path)
    if profile.get("schema_version") != 1 or profile.get("status") not in {"draft_pending_independent_review", "reviewed"}:
        raise ValueError("unsupported profile schema or status")
    sources = profile.get("source_hashes")
    if not isinstance(sources, list) or {item.get("path") for item in sources if isinstance(item, dict)} != REQUIRED_SOURCES:
        raise ValueError("profile source set drift")
    for source in sources:
        if not isinstance(source, dict) or _sha256(ROOT / str(source.get("path"))) != source.get("sha256"):
            raise ValueError(f"profile source hash mismatch: {source}")
    profiles = profile.get("profiles")
    if not isinstance(profiles, list) or {item.get("id") for item in profiles if isinstance(item, dict)} != {"baseline_or_unpaired", "family_scoped_sequence", "unique_planar_selector", "selector_ambiguity_counterexample"}:
        raise ValueError("profile taxonomy drift")
    if len(profile.get("recommendations", [])) > 3 or not profile.get("non_projection", {}).get("evidence_only"):
        raise ValueError("recommendation or non-projection boundary drift")
    result = inventory()
    if result["inventory_conflicts"]:
        raise ValueError(f"authoritative inventory conflict: {result['inventory_conflicts']}")
    crosswalk = profile.get("m142_crosswalk")
    if crosswalk != {"admission_id": "selector-ambiguity-v1-m142", "unique_binding_profile": "unique_planar_selector", "unique_binding_disposition": "admit", "twin_boss_profile": "selector_ambiguity_counterexample", "twin_boss_disposition": "fail_closed", "held_out_access": "documentary_evidence_only"}:
        raise ValueError("M142 crosswalk drift")
    return {"profile_id": profile["profile_id"], "profile_sha256": _sha256(profile_path), **result, "held_out_access": "metadata_and_documentary_only", "result": "pass"}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
