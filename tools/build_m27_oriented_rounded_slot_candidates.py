"""Build only the six preregistered M27 candidates offline."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from brep2code.brep.probes import load_model, probe_summary
try:  # Supports both package import and direct script execution.
    from tools.audit_sequence_paired_oriented_rounded_slot import EXPANSION, ROOT, build_shape, canonical_sequence
    from tools.audit_sequence_paired_prismatic_hole import load_json, write_step
    from tools.build_m20_counterbore_candidates import normalize_step_header
except ModuleNotFoundError:  # pragma: no cover - direct script entrypoint only
    from audit_sequence_paired_oriented_rounded_slot import EXPANSION, ROOT, build_shape, canonical_sequence
    from audit_sequence_paired_prismatic_hole import load_json, write_step
    from build_m20_counterbore_candidates import normalize_step_header


def _write(entry: dict[str, Any], path: Path) -> str:
    write_step(build_shape(entry), path)
    normalize_step_header(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _stable(entry: dict[str, Any]) -> None:
    with tempfile.TemporaryDirectory(prefix="brep2code-m27-a-") as first, tempfile.TemporaryDirectory(prefix="brep2code-m27-b-") as second:
        left, right = Path(first) / "model.step", Path(second) / "model.step"
        if _write(entry, left) != _write(entry, right) or left.read_bytes() != right.read_bytes():
            raise RuntimeError(f"hash nondeterminism: {entry['case_id']}")


def build(expansion_path: Path = EXPANSION, output_root: Path = ROOT) -> list[str]:
    expansion = load_json(expansion_path)
    rows = expansion.get("cases")
    if expansion.get("selection_status") != "preregistered_before_candidate_production" or not isinstance(rows, list) or len(rows) != 6:
        raise ValueError("M27 production requires exactly six preregistered rows")
    produced = []
    for entry in rows:
        sequence = canonical_sequence(entry)
        _stable(entry)
        directory = output_root / entry["candidate_directory"]
        directory.mkdir(parents=True, exist_ok=True)
        target = directory / "input.step"
        digest = _write(entry, target)
        metadata = {"case_id": entry["case_id"], "status": "experimental", "origin": "self_authored", "tier": "P2", "fixture_version": 1, "family_id": entry["family_id"], "data_split": entry["data_split"], "variant": entry["variant"], "parameters": entry["parameters"], "input_step": "input.step", "reference_script_status": "unavailable", "sha256": digest, "unit": "mm", "expected": probe_summary(load_model(target)), "sequence_pair": {"grammar_version": expansion["grammar_version"], "oracle_provenance": expansion["oracle_provenance"], "sequence": sequence, "candidate_sequence": "candidate_sequence.json"}, "admission_boundary": "Experimental candidate only; absent from registry, manifest, provider, training, and runtime paths."}
        (directory / "candidate_sequence.json").write_text(json.dumps({"grammar_version": expansion["grammar_version"], "sequence": sequence}, indent=2) + "\n", encoding="utf-8")
        (directory / "case.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        produced.append(entry["case_id"])
    return produced


if __name__ == "__main__":
    print(json.dumps({"produced": build(), "status": "experimental_candidates"}, indent=2))
