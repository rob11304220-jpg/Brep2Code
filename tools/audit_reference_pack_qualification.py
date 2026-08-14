"""Audit M84's fixed, source-linked cylinder-construction qualification."""

from __future__ import annotations

import ast
import json
from pathlib import Path

try:  # Supports both direct execution and package import from tests.
    from tools import audit_reference_packs
except ModuleNotFoundError:  # pragma: no cover - direct script entrypoint only
    import audit_reference_packs


ROOT = Path(__file__).resolve().parents[1]
QUALIFICATION = ROOT / "docs/corpus/reference-packs/m84-cylinder-construction-qualification-v1.json"
EXPECTED_CASES = {
    "cylinder": ("reference-pack-cylinder", "final primitive"),
    "block_with_hole": ("reference-pack-block-with-hole", "single boolean-cut tool"),
    "three_hole_plate": ("reference-pack-three-hole-plate", "repeated boolean-cut tool"),
}
REQUIRED_FIELDS = {
    "schema_version", "mechanism_id", "status", "development_only", "source_contract",
    "candidate_card", "recommended_action", "fixed_fixture_policy", "stopping_rule", "cases",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def script_calls_declared_action(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "BRepPrimAPI_MakeCylinder"
        for node in ast.walk(tree)
    )


def audit_qualification(qualification: dict | None = None) -> None:
    qualification = load_json(QUALIFICATION) if qualification is None else qualification
    assert set(qualification) == REQUIRED_FIELDS
    assert qualification["schema_version"] == 1
    assert qualification["mechanism_id"] == "vertical-cylinder-construction-v1"
    assert qualification["status"] == "qualified"
    assert qualification["development_only"] is True
    assert qualification["source_contract"] == audit_reference_packs.CONTRACT.relative_to(ROOT).as_posix()
    assert qualification["recommended_action"] == "OCP.BRepPrimAPI.BRepPrimAPI_MakeCylinder"
    assert "no fake provider" in qualification["fixed_fixture_policy"]
    assert "do not substitute or add a case" in qualification["stopping_rule"]

    audit_reference_packs.audit_contract()
    packs = {pack["id"]: pack for pack in audit_reference_packs.load_json(audit_reference_packs.CONTRACT)["packs"]}
    evidence_cases = qualification["cases"]
    assert len(evidence_cases) == 3
    assert {case["case_id"] for case in evidence_cases} == set(EXPECTED_CASES)
    assert len({case["role"] for case in evidence_cases}) == 3
    for evidence_case in evidence_cases:
        case_id = evidence_case["case_id"]
        expected_pack, expected_role = EXPECTED_CASES[case_id]
        assert evidence_case["pack_id"] == expected_pack
        assert evidence_case["role"] == expected_role
        assert evidence_case["counterexamples"] and all(evidence_case["counterexamples"])
        pack = packs[expected_pack]
        assert pack["source_case_record"] == evidence_case["source_case_record"]
        assert "OCP.BRepPrimAPI" in pack["allowed_ocp_modules"]
        case_record = load_json(ROOT / evidence_case["source_case_record"])
        assert case_record["reference_script_status"] == "available"
        assert script_calls_declared_action((ROOT / evidence_case["source_case_record"]).parent / case_record["reference_script"])

    card = load_json(ROOT / qualification["candidate_card"])
    assert card["id"] == "vertical-cylinder-construction"
    assert card["status"] == "experimental"
    assert card["evidence"]["level"] == "direct"
    assert len(card["evidence"]["supporting_cases"]) == 3
    assert qualification["recommended_action"] in card["claim"]
    assert qualification["recommended_action"] in card["runtime_action"]
    assert "cadquery" not in card["runtime_action"].lower()
    assert "occ.core" not in card["runtime_action"].lower()


def main() -> None:
    audit_qualification()
    print("reference-pack qualification passed: 3 independent direct cylinder-construction cases")


if __name__ == "__main__":
    main()
