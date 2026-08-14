"""Audit the M83 development-only candidate reference-pack contract."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/corpus/reference-packs/reference-pack-contract-v1.json"
MANIFESTS = ROOT / "case-library/manifests/self-authored"
ID_PATTERN = re.compile(r"^reference-pack-[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_TEXT = ("input.step", "reference_build_sequence.py", "runtime_resources")
REQUIRED_PACK_FIELDS = {
    "id", "version", "content_sha256", "case_id", "tier", "mechanism", "difficulty",
    "evidence_role", "applicability_observations", "allowed_ocp_modules",
    "parameter_placeholders", "sequence_outline", "output_requirement", "counterexamples",
    "source_case_record", "source_input_sha256",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_digest(pack: dict) -> str:
    payload = dict(pack)
    payload.pop("content_sha256", None)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def assert_no_forbidden_text(value: object) -> None:
    if isinstance(value, str):
        assert not any(forbidden in value for forbidden in FORBIDDEN_TEXT), value
    elif isinstance(value, list):
        for item in value:
            assert_no_forbidden_text(item)
    elif isinstance(value, dict):
        for item in value.values():
            assert_no_forbidden_text(item)


def selected_cases() -> dict[str, str]:
    selected: dict[str, str] = {}
    for manifest_name in ("p0.json", "p1.json"):
        for case in load_json(MANIFESTS / manifest_name)["cases"]:
            selected[case["case_id"]] = case["tier"]
    return selected


def audit_pack(pack: dict, selected: dict[str, str]) -> None:
    assert set(pack) == REQUIRED_PACK_FIELDS, pack.get("id")
    assert isinstance(pack["id"], str) and ID_PATTERN.fullmatch(pack["id"])
    assert pack["version"] == 1
    assert pack["id"] == f"reference-pack-{pack['case_id'].replace('_', '-')}"
    assert pack["case_id"] in selected and pack["tier"] == selected[pack["case_id"]]
    assert pack["content_sha256"] == canonical_digest(pack)
    assert SHA256_PATTERN.fullmatch(pack["source_input_sha256"])
    assert all(isinstance(pack[field], str) and pack[field] for field in ("mechanism", "difficulty", "evidence_role", "output_requirement"))
    for field in ("applicability_observations", "allowed_ocp_modules", "parameter_placeholders", "sequence_outline", "counterexamples"):
        assert isinstance(pack[field], list) and pack[field] and all(isinstance(item, str) and item for item in pack[field])
    assert all(module.startswith("OCP.") for module in pack["allowed_ocp_modules"])
    assert all(re.fullmatch(r"[a-z][a-z0-9_]*", parameter) for parameter in pack["parameter_placeholders"])
    source_record = ROOT / pack["source_case_record"]
    assert source_record.is_file()
    source = load_json(source_record)
    assert source["case_id"] == pack["case_id"]
    assert source["tier"] == pack["tier"]
    assert source["sha256"] == pack["source_input_sha256"]
    assert_no_forbidden_text(pack)


def audit_contract(contract: dict | None = None) -> None:
    contract = load_json(CONTRACT) if contract is None else contract
    assert set(contract) == {"schema_version", "status", "development_only", "runtime_visible", "packs"}
    assert contract["schema_version"] == 1
    assert contract["status"] == "experimental"
    assert contract["development_only"] is True
    assert contract["runtime_visible"] is False
    selected = selected_cases()
    packs = contract["packs"]
    assert isinstance(packs, list) and len(packs) == 7
    assert {pack["case_id"] for pack in packs} == set(selected)
    assert len({pack["id"] for pack in packs}) == len(packs)
    for pack in packs:
        audit_pack(pack, selected)


def main() -> None:
    audit_contract()
    print("reference-pack audit passed: 7 development-only candidate packs")


if __name__ == "__main__":
    main()
