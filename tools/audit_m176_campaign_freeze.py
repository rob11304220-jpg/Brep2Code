"""Audit M176's offline campaign freeze without constructing a provider."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/corpus/knowledge/m176-asymmetric-campaign-freeze-v1.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fingerprint(case_ids: list[str], records: dict[str, Path]) -> str:
    rows = []
    for case_id in sorted(case_ids):
        record_path = records[case_id]
        record = json.loads(record_path.read_text(encoding="utf-8"))
        rows.append({"case_id": case_id, "input_sha256": record["sha256"], "case_json_sha256": _sha256(record_path)})
    return hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def audit() -> dict[str, object]:
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    qualification_path = ROOT / spec["qualification"]["path"]
    if _sha256(qualification_path) != spec["qualification"]["sha256"]:
        raise ValueError("M176 qualification hash drift")
    qualification = json.loads(qualification_path.read_text(encoding="utf-8"))
    registry = json.loads((ROOT / qualification["registry"]["path"]).read_text(encoding="utf-8"))
    records = {item["case_id"]: ROOT / item["case_record"] for item in registry["cases"]}
    main_ids = [case_id for rows in qualification["main_cohort"]["groups"].values() for case_id in rows]
    annex_ids = [row["case_id"] for row in qualification["feasibility_annex"]["rows"]]
    if _fingerprint(main_ids, records) != spec["main_cohort"]["input_fingerprint_sha256"]:
        raise ValueError("M176 main input fingerprint drift")
    if _fingerprint(annex_ids, records) != spec["feasibility_annex"]["input_fingerprint_sha256"]:
        raise ValueError("M176 annex input fingerprint drift")
    provider = spec["provider"]
    if provider != {"name": "deepseek", "model": "deepseek-v4-pro", "max_output_tokens": 4096, "provider_timeout_seconds": 120, "serial_only": True, "retry": "forbidden"}:
        raise ValueError("M176 provider bounds drift")
    if spec["executor"] != {"name": "wsl-bwrap", "input_mount": "no-input"}:
        raise ValueError("M176 executor boundary drift")
    if spec["completion_cap"] != spec["main_cohort"]["completion_cap"] + spec["feasibility_annex"]["completion_cap"] != 102:
        raise ValueError("M176 completion arithmetic drift")
    identities = spec["report_identities"]
    if len(set(identities.values())) != 4 or any((ROOT / value).exists() for value in identities.values()):
        raise ValueError("M176 report identities are not fresh and distinct")
    return {"status": "prepared_offline", "completion_cap": 102, "main_cases": len(main_ids), "annex_cases": len(annex_ids)}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
