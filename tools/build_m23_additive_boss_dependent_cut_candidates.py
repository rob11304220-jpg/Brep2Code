"""Build only the six preregistered M23 experimental candidates offline."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from brep2code.brep.probes import load_model, probe_summary
from tools.audit_sequence_paired_additive_boss_dependent_cut import EXPANSION, ROOT, build_shape, canonical_sequence
from tools.audit_sequence_paired_prismatic_hole import load_json, write_step
from tools.build_m20_counterbore_candidates import normalize_step_header


def _write(entry: dict[str, Any], path: Path) -> str:
    write_step(build_shape(entry), path)
    normalize_step_header(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_stable(entry: dict[str, Any]) -> None:
    with tempfile.TemporaryDirectory(prefix="brep2code-m23-a-") as first, tempfile.TemporaryDirectory(prefix="brep2code-m23-b-") as second:
        first_path, second_path = Path(first) / "model.step", Path(second) / "model.step"
        if _write(entry, first_path) != _write(entry, second_path) or first_path.read_bytes() != second_path.read_bytes():
            raise RuntimeError(f"hash nondeterminism: {entry['case_id']}")


def build(expansion_path: Path = EXPANSION, output_root: Path = ROOT) -> list[str]:
    expansion = load_json(expansion_path)
    entries = expansion.get("cases")
    if expansion.get("selection_status") != "preregistered_before_candidate_production" or not isinstance(entries, list) or len(entries) != 6:
        raise ValueError("M23 production requires exactly six preregistered rows")
    produced = []
    for entry in entries:
        canonical_sequence(entry)
        _assert_stable(entry)
        directory = output_root / entry["candidate_directory"]
        directory.mkdir(parents=True, exist_ok=True)
        target = directory / "input.step"
        digest = _write(entry, target)
        expected = probe_summary(load_model(target))
        sequence = {"grammar_version": expansion["grammar_version"], "sequence": canonical_sequence(entry)}
        metadata = {"case_id": entry["case_id"], "status": "experimental", "origin": "self_authored", "tier": "P2", "fixture_version": 1, "family_id": entry["family_id"], "data_split": entry["data_split"], "variant": entry["variant"], "parameters": entry["parameters"], "input_step": "input.step", "reference_script_status": "unavailable", "sha256": digest, "unit": "mm", "expected": expected, "sequence_pair": {"grammar_version": expansion["grammar_version"], "oracle_provenance": expansion["oracle_provenance"], "sequence": canonical_sequence(entry), "candidate_sequence": "candidate_sequence.json"}, "admission_boundary": "Experimental candidate only; absent from registry, manifest, provider, training, and runtime paths."}
        (directory / "candidate_sequence.json").write_text(json.dumps(sequence, indent=2) + "\n", encoding="utf-8")
        (directory / "case.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        produced.append(entry["case_id"])
    return produced


if __name__ == "__main__":
    print(json.dumps({"produced": build(), "status": "experimental_candidates"}, indent=2))
