"""Audit the metadata-only M175 cohort and annex qualification dossier."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER = ROOT / "docs/corpus/knowledge/m175-asymmetric-cohort-qualification-v1.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit() -> dict[str, object]:
    dossier = json.loads(DOSSIER.read_text(encoding="utf-8"))
    registry_path = ROOT / dossier["registry"]["path"]
    if _sha256(registry_path) != dossier["registry"]["sha256"]:
        raise ValueError("M175 registry hash drift")
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    records = {item["case_id"]: ROOT / item["case_record"] for item in registry["cases"]}
    main = dossier["main_cohort"]
    groups = main["groups"]
    ids = [case_id for rows in groups.values() for case_id in rows]
    if main["count"] != 30 or main["reference"] != {"mode": "none"} or len(groups) != 10 or len(ids) != 30 or len(set(ids)) != 30:
        raise ValueError("M175 main cohort cardinality is invalid")
    if any(len(rows) != 3 for rows in groups.values()):
        raise ValueError("M175 cohort groups must each have three rows")
    for case_id in ids:
        record = json.loads(records[case_id].read_text(encoding="utf-8"))
        if record.get("data_split") != "development" or record.get("reference_script_status") != "available":
            raise ValueError(f"M175 case is not an eligible development record: {case_id}")
        if not {"bbox", "counts", "volume"}.issubset(record.get("expected", {})):
            raise ValueError(f"M175 case lacks base oracle fields: {case_id}")
    annex = dossier["feasibility_annex"]
    guidance = annex["guidance"]
    if annex["count"] != 3 or annex["pooling"] != "forbidden" or len(annex["rows"]) != 3:
        raise ValueError("M175 annex boundary is invalid")
    if _sha256(ROOT / guidance["index"]) != guidance["index_sha256"] or _sha256(ROOT / guidance["card"]) != guidance["card_sha256"]:
        raise ValueError("M175 annex guidance hash drift")
    if [row["role"] for row in annex["rows"]] != ["final primitive", "single boolean-cut tool", "repeated boolean-cut tool"]:
        raise ValueError("M175 annex roles are invalid")
    return {"status": "pass", "main_rows": len(ids), "groups": sorted(groups), "annex_rows": 3}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
