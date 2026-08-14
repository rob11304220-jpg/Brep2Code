"""Build only the preregistered M21 offset-rounded-slot candidates offline."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from brep2code.brep.probes import load_model, probe_summary
from tools.audit_sequence_paired_prismatic_hole import load_json, write_step
from tools.build_m20_counterbore_candidates import normalize_step_header
from tools.audit_sequence_paired_rounded_slot import EXPANSION, ROOT, build_shape, canonical_sequence


def build(expansion_path: Path = EXPANSION) -> list[str]:
    expansion = load_json(expansion_path)
    rows = [row for row in expansion["cases"] if row["family_id"] == "offset_rounded_slot"]
    if len(rows) != 3 or any(row["data_split"] != "held_out" for row in rows):
        raise ValueError("expected exactly three held-out offset-rounded-slot rows")
    produced = []
    for row in rows:
        directory = ROOT / row["candidate_directory"]
        directory.mkdir(parents=True, exist_ok=True)
        target = directory / "input.step"
        write_step(build_shape(row), target)
        normalize_step_header(target)
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        expected = probe_summary(load_model(target))
        sequence = canonical_sequence(row)
        (directory / "candidate_sequence.json").write_text(json.dumps({"grammar_version": expansion["grammar_version"], "sequence": sequence}, indent=2) + "\n", encoding="utf-8")
        metadata: dict[str, Any] = {"case_id": row["case_id"], "status": "experimental", "origin": "self_authored", "tier": "P2", "fixture_version": 1, "family_id": row["family_id"], "data_split": row["data_split"], "variant": row["variant"], "parameters": row["parameters"], "input_step": "input.step", "reference_script_status": "unavailable", "sha256": digest, "unit": "mm", "expected": expected, "sequence_pair": {"grammar_version": expansion["grammar_version"], "oracle_provenance": expansion["oracle_provenance"], "sequence": sequence, "candidate_sequence": "candidate_sequence.json"}, "admission_boundary": "Experimental candidate only; absent from registry, manifest, provider, training, and runtime paths."}
        (directory / "case.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        produced.append(row["case_id"])
    return produced
