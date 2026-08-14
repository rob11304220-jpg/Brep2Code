"""Build only the six preregistered M22 multi-contour pocket candidates offline."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from brep2code.brep.probes import load_model, probe_summary
from tools.audit_sequence_paired_multi_contour_pocket import EXPANSION, ROOT, build_shape, canonical_sequence
from tools.audit_sequence_paired_prismatic_hole import load_json, write_step
from tools.build_m20_counterbore_candidates import normalize_step_header


def _write_normalized(entry: dict[str, Any], path: Path) -> str:
    write_step(build_shape(entry), path)
    normalize_step_header(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_stable(entry: dict[str, Any]) -> None:
    with tempfile.TemporaryDirectory(prefix="brep2code-m22-stable-a-") as first, tempfile.TemporaryDirectory(prefix="brep2code-m22-stable-b-") as second:
        first_path, second_path = Path(first) / "model.step", Path(second) / "model.step"
        first_digest = _write_normalized(entry, first_path)
        second_digest = _write_normalized(entry, second_path)
        if first_digest != second_digest or first_path.read_bytes() != second_path.read_bytes():
            raise RuntimeError(f"hash nondeterminism: {entry['case_id']}")


def _metadata(entry: dict[str, Any], digest: str, expected: dict[str, Any], grammar_version: str, provenance: str) -> dict[str, Any]:
    return {
        "case_id": entry["case_id"],
        "status": "experimental",
        "origin": "self_authored",
        "tier": "P2",
        "fixture_version": 1,
        "family_id": entry["family_id"],
        "data_split": entry["data_split"],
        "variant": entry["variant"],
        "parameters": entry["parameters"],
        "input_step": "input.step",
        "reference_script_status": "unavailable",
        "sha256": digest,
        "unit": "mm",
        "expected": expected,
        "sequence_pair": {"grammar_version": grammar_version, "oracle_provenance": provenance, "sequence": canonical_sequence(entry), "candidate_sequence": "candidate_sequence.json"},
        "admission_boundary": "Experimental candidate only; absent from registry, manifest, provider, training, and runtime paths.",
    }


def build(expansion_path: Path = EXPANSION, output_root: Path = ROOT) -> list[str]:
    expansion = load_json(expansion_path)
    entries = expansion.get("cases")
    if expansion.get("selection_status") != "preregistered_before_candidate_production" or not isinstance(entries, list) or len(entries) != 6:
        raise ValueError("M22 production requires exactly six preregistered rows")
    if {entry.get("family_id") for entry in entries if entry.get("data_split") == "development"} != {"multi_contour_pocket_centered"} or {entry.get("family_id") for entry in entries if entry.get("data_split") == "held_out"} != {"multi_contour_pocket_offset"}:
        raise ValueError("M22 preregistration split drift")
    produced: list[str] = []
    for entry in entries:
        canonical_sequence(entry)
        _assert_stable(entry)
        directory = output_root / entry["candidate_directory"]
        directory.mkdir(parents=True, exist_ok=True)
        target = directory / "input.step"
        digest = _write_normalized(entry, target)
        expected = probe_summary(load_model(target))
        (directory / "candidate_sequence.json").write_text(json.dumps({"grammar_version": expansion["grammar_version"], "sequence": canonical_sequence(entry)}, indent=2) + "\n", encoding="utf-8")
        (directory / "case.json").write_text(json.dumps(_metadata(entry, digest, expected, expansion["grammar_version"], expansion["oracle_provenance"]), indent=2) + "\n", encoding="utf-8")
        produced.append(entry["case_id"])
    return produced


if __name__ == "__main__":
    print(json.dumps({"produced": build(), "status": "experimental_candidates"}, indent=2))
