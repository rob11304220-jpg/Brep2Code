#!/usr/bin/env python3
"""Audit the metadata/documentary case-evidence companion mapping."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "docs/corpus/knowledge/case-evidence-relationships-v1.json"
FORBIDDEN = ("case-library/", "runtime_resources/", "fixtures/", ".step", ".py", "reference_script")
ROLES = {"oracle", "discriminating", "negative_control", "regression", "documentary"}
MODES = {"development_source_linked", "held_out_documentary_only", "documentary_external_source"}


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def declared_strings(value: object) -> set[str]:
    if isinstance(value, dict):
        return set().union(*(declared_strings(item) for item in value.values()))
    if isinstance(value, list):
        return set().union(*(declared_strings(item) for item in value))
    if isinstance(value, str):
        return {value}
    return set()


def main() -> int:
    errors: list[str] = []
    mapping = load(MAPPING_PATH)
    if mapping.get("schema_version") != 1 or mapping.get("mapping_id") != "case-evidence-relationships-v1":
        errors.append("mapping identity/schema_version is invalid")
    if not mapping.get("non_projection", {}).get("evidence_only"):
        errors.append("mapping must remain evidence_only")

    crosswalk = mapping.get("crosswalk", {})
    crosswalk_path = ROOT / crosswalk.get("path", "")
    if not crosswalk_path.is_file() or crosswalk.get("sha256") != digest(crosswalk_path):
        errors.append("crosswalk source is missing or has hash drift")
    else:
        hypothesis_ids = {item["id"] for item in load(crosswalk_path)["hypotheses"]}

    declared_sources: dict[str, Path] = {}
    for source in mapping.get("source_hashes", []):
        relative = source.get("path", "")
        if any(part in relative.lower() for part in FORBIDDEN):
            errors.append(f"forbidden declared source: {relative}")
            continue
        path = ROOT / relative
        declared_sources[relative] = path
        if not path.is_file() or source.get("sha256") != digest(path):
            errors.append(f"source hash drift: {relative}")

    seen: set[str] = set()
    for relation in mapping.get("relationships", []):
        relation_id = relation.get("id")
        if not isinstance(relation_id, str) or relation_id in seen:
            errors.append(f"missing or duplicate relationship ID: {relation_id}")
        seen.add(relation_id)
        if relation.get("hypothesis_id") not in hypothesis_ids:
            errors.append(f"unknown hypothesis: {relation_id}")
        if relation.get("evidence_role") not in ROLES or relation.get("evidence_mode") not in MODES:
            errors.append(f"invalid role or mode: {relation_id}")
        source_path = relation.get("source_path", "")
        source = declared_sources.get(source_path)
        if source is None:
            errors.append(f"relationship source is not hash-declared: {relation_id}")
            continue
        declared_case_ids = declared_strings(load(source))
        case_ids = relation.get("case_ids", [])
        if relation.get("evidence_mode") == "held_out_documentary_only" and case_ids:
            errors.append(f"held-out relationship must not contain case IDs: {relation_id}")
        if relation.get("evidence_mode") != "held_out_documentary_only" and not set(case_ids).issubset(declared_case_ids):
            errors.append(f"case IDs are not declared by source: {relation_id}")
        if any("held_out" in item.lower() for item in case_ids):
            errors.append(f"held-out case ID is forbidden in mapping: {relation_id}")
        if any(part in str(relation).lower() for part in FORBIDDEN):
            errors.append(f"forbidden relationship content: {relation_id}")

    if errors:
        print("Case-evidence relationship audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Case-evidence relationship audit passed: {len(seen)} relationships.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
