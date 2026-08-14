"""Replay one promoted M23 deterministic reference into a STEP file."""

from __future__ import annotations

from pathlib import Path

from tools.audit_sequence_paired_additive_boss_dependent_cut import EXPANSION, build_shape
from tools.audit_sequence_paired_prismatic_hole import load_json, write_step


def replay(case_id: str, output: Path) -> None:
    entry = next(entry for entry in load_json(EXPANSION)["cases"] if entry["case_id"] == case_id)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_step(build_shape(entry), output)
