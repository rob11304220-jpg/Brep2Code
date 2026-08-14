"""Validate ADR-0023 lifecycle metadata without opening fixtures or scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CASE_IDS = (
    "param_offset_rounded_slot_low",
    "param_offset_rounded_slot_nominal",
    "param_offset_rounded_slot_high",
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def audit() -> dict[str, Any]:
    """Read only registry and case JSON metadata; never open a fixture or script."""
    registry = _load(ROOT / "docs/corpus/registry/self-authored.json")
    registry_rows = {row.get("case_id"): row for row in registry.get("cases", []) if isinstance(row, dict)}
    for case_id in CASE_IDS:
        row = registry_rows.get(case_id)
        if not isinstance(row, dict) or row.get("status") != "active":
            raise ValueError(f"registry lifecycle drift: {case_id}")
        case = _load(ROOT / str(row.get("case_record")))
        if case.get("case_id") != case_id or case.get("status") != "active":
            raise ValueError(f"case lifecycle drift: {case_id}")
        if case.get("data_split") != "held_out":
            raise ValueError(f"split drift: {case_id}")
        if case.get("reference_script_status") != "available" or case.get("reference_script") != "reference_build_sequence.py":
            raise ValueError(f"reference-script declaration drift: {case_id}")
        if case.get("admission_boundary") != "Active self-authored governance asset; absent from executable manifests, provider, training, and runtime paths.":
            raise ValueError(f"admission boundary drift: {case_id}")
    return {"case_ids": list(CASE_IDS), "fixture_access": "not_performed", "script_access": "not_performed", "result": "pass"}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
