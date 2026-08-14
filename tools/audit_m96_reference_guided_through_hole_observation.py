"""Derive a path-free, bounded M96 observation transcript from development B-Reps."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from brep2code.agent.m97_observation import derive_m96_development_context
from tools.audit_sequence_paired_prismatic_hole import load_json


ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "docs/corpus/sequence-paired/reference-guided-through-hole-variation-v1-preregistration.json"


def derive_transcript(entry: dict[str, Any], *, root: Path = ROOT) -> str:
    """Return only measured M96 facts; never serialize local oracle material."""

    if entry.get("data_split") != "development":
        raise ValueError("M96 derives transcripts from development rows only")
    return derive_m96_development_context(entry, root=root)


def audit(record_path: Path = EXPANSION) -> list[dict[str, Any]]:
    record = load_json(record_path)
    rows = record.get("cases")
    if not isinstance(rows, list) or len(rows) != 6:
        raise ValueError("M96 requires the frozen six-row M94 record")
    development = [entry for entry in rows if entry.get("data_split") == "development"]
    held_out = [entry for entry in rows if entry.get("data_split") == "held_out"]
    if len(development) != 3 or len(held_out) != 3:
        raise ValueError("M96 requires the frozen 3/3 split")
    result = []
    for entry in development:
        transcript = json.loads(derive_transcript(entry))
        facts = transcript["observation_transcript"][0]["data"]["cylindrical_cut"]
        if set(facts) != {"radius", "axis", "center_xy", "extent"} or facts["axis"] != "+Z" or facts["extent"] != "through":
            raise ValueError("M96 transcript lacks required cylinder facts")
        result.append({"case_id": entry["case_id"], "transcript_bytes": len(derive_transcript(entry).encode("utf-8"))})
    return result


if __name__ == "__main__":
    print(json.dumps({"cases": audit(), "status": "pass"}, indent=2))
