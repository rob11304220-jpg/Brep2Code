"""Verify M159 deregisters downgraded offset-rounded-slot metadata only."""

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
    """Read only registry and case JSON metadata; never open fixtures or scripts."""

    registry = _load(ROOT / "docs/corpus/registry/self-authored.json")
    registered_ids = {
        row.get("case_id")
        for row in registry.get("cases", [])
        if isinstance(row, dict)
    }
    for case_id in CASE_IDS:
        if case_id in registered_ids:
            raise ValueError(f"active registry row remains: {case_id}")
        case = _load(ROOT / "case-library/self-authored" / case_id / "case.json")
        if case.get("case_id") != case_id or case.get("status") != "experimental":
            raise ValueError(f"experimental lifecycle drift: {case_id}")
        if case.get("reference_script_status") != "unavailable" or "reference_script" in case:
            raise ValueError(f"reference-script deregistration drift: {case_id}")
        if case.get("admission_boundary") != "Experimental candidate only; absent from registry, manifest, provider, training, and runtime paths.":
            raise ValueError(f"admission boundary drift: {case_id}")
    return {
        "case_ids": list(CASE_IDS),
        "fixture_access": "not_performed",
        "script_access": "not_performed",
        "result": "pass",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
