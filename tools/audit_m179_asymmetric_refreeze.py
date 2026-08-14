"""Audit M179's fresh local identities without provider construction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/corpus/knowledge/m179-asymmetric-campaign-refreeze-v1.json"
M176 = ROOT / "docs/corpus/knowledge/m176-asymmetric-campaign-freeze-v1.json"


def audit() -> dict[str, object]:
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    if spec.get("policy") != "m179-asymmetric-hosted-campaign-v1":
        raise ValueError("M179 policy drift")
    if spec.get("m176_spec_sha256") != hashlib.sha256(M176.read_bytes()).hexdigest():
        raise ValueError("M179 inherited M176 hash drift")
    identities = spec.get("report_identities")
    if not isinstance(identities, dict) or len(identities) != 4 or len(set(identities.values())) != 4:
        raise ValueError("M179 report identities are not distinct")
    if any((ROOT / value).exists() for value in identities.values()):
        raise ValueError("M179 report identities are not fresh")
    return {"status": "prepared_offline", "policy": spec["policy"], "identities": 4}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
