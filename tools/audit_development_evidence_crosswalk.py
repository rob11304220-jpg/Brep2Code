#!/usr/bin/env python3
"""Audit the metadata-only development-evidence crosswalk."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CROSSWALK = REPO_ROOT / "docs/corpus/knowledge/development-evidence-crosswalk-v1.json"
FORBIDDEN_PATH_PARTS = ("case-library/", "runtime_resources/", "fixtures/", ".step", ".py", "reference_script")
REQUIRED_RELATIONS = {
    "observable_units", "operation_units", "execution_units", "patterns",
    "admission_ids", "evidence_dispositions", "coverage_dimensions",
}


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def error(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    crosswalk = load_json(CROSSWALK)
    if crosswalk.get("schema_version") != 1:
        error(errors, "crosswalk schema_version must be 1")
    if crosswalk.get("primary_node") != "bounded_modeling_hypothesis":
        error(errors, "crosswalk primary_node must be bounded_modeling_hypothesis")
    if not crosswalk.get("non_projection", {}).get("evidence_only"):
        error(errors, "crosswalk must remain evidence_only")

    for source in crosswalk.get("source_hashes", []):
        relative = source.get("path", "")
        if any(part in relative.lower() for part in FORBIDDEN_PATH_PARTS):
            error(errors, f"forbidden source path: {relative}")
            continue
        path = REPO_ROOT / relative
        if not path.is_file():
            error(errors, f"missing source: {relative}")
        elif source.get("sha256") != sha256(path):
            error(errors, f"source hash drift: {relative}")

    decisions = load_json(REPO_ROOT / "docs/corpus/knowledge/decisions/index.json")
    decision_paths = {item["decision_id"]: REPO_ROOT / item["path"] for item in decisions["packages"]}
    unit_ids: dict[str, set[str]] = {"observable_units": set(), "operation_units": set(), "execution_units": set(), "patterns": set()}
    for relation, directory in (("observable_units", "observables"), ("operation_units", "operations"), ("execution_units", "execution"), ("patterns", "patterns")):
        for path in (REPO_ROOT / "docs/corpus/knowledge" / directory).glob("*.json"):
            payload = load_json(path)
            unit_id = payload.get("unit_id")
            if isinstance(unit_id, str):
                unit_ids[relation].add(unit_id)
    dispositions = {item["id"] for item in load_json(REPO_ROOT / "docs/corpus/knowledge/evidence-disposition.json")["dispositions"]}
    admission_payload = load_json(REPO_ROOT / "docs/corpus/knowledge/admissions/selector-ambiguity-v1.json")
    admission_ids = {admission_payload["admission_id"]}
    coverage = load_json(REPO_ROOT / "docs/corpus/knowledge/coverage-matrix.json")
    coverage_dimensions = {item["id"] for item in coverage["dimensions"]}

    seen: set[str] = set()
    for hypothesis in crosswalk.get("hypotheses", []):
        hypothesis_id = hypothesis.get("id")
        if not isinstance(hypothesis_id, str) or hypothesis_id in seen:
            error(errors, f"hypothesis ID is missing or duplicated: {hypothesis_id}")
        seen.add(hypothesis_id)
        decision_id = hypothesis.get("capability_question", "")
        if isinstance(decision_id, str) and decision_id.startswith("q") and decision_id not in decision_paths:
            error(errors, f"unknown decision ID: {decision_id}")
        relations = hypothesis.get("relations", {})
        if set(relations) != REQUIRED_RELATIONS:
            error(errors, f"relations must have exactly the required keys: {hypothesis_id}")
            continue
        for relation in ("observable_units", "operation_units", "execution_units", "patterns"):
            unknown = set(relations[relation]) - unit_ids[relation]
            if unknown:
                error(errors, f"unknown {relation} for {hypothesis_id}: {sorted(unknown)}")
        if unknown := set(relations["admission_ids"]) - admission_ids:
            error(errors, f"unknown admission IDs for {hypothesis_id}: {sorted(unknown)}")
        if unknown := set(relations["evidence_dispositions"]) - dispositions:
            error(errors, f"unknown dispositions for {hypothesis_id}: {sorted(unknown)}")
        if unknown := set(relations["coverage_dimensions"]) - coverage_dimensions:
            error(errors, f"unknown coverage dimensions for {hypothesis_id}: {sorted(unknown)}")
        if "runtime" not in hypothesis.get("adoption_boundary", "").lower() and "no " not in hypothesis.get("adoption_boundary", "").lower():
            error(errors, f"adoption boundary is not explicit: {hypothesis_id}")

    if errors:
        print("Development-evidence crosswalk audit failed:")
        for item in errors:
            print(f"- {item}")
        return 1
    print(f"Development-evidence crosswalk audit passed: {len(seen)} hypotheses.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
