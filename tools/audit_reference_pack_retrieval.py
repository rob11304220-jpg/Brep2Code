"""Audit M19-002's fixed offline reference-pack retrieval preregistration."""

from __future__ import annotations

import json
from pathlib import Path

try:  # Supports both direct execution and package import from tests.
    from tools import audit_reference_pack_qualification
except ModuleNotFoundError:  # pragma: no cover - direct script entrypoint only
    import audit_reference_pack_qualification


ROOT = Path(__file__).resolve().parents[1]
EVALUATION = ROOT / "docs/corpus/reference-packs/m19-retrieval-evaluation-v1.json"
EXPECTED_CASES = {
    "cylinder": ("final primitive", "reference-pack-cylinder"),
    "block_with_hole": ("single boolean-cut tool", "reference-pack-block-with-hole"),
    "three_hole_plate": ("repeated boolean-cut tool", "reference-pack-three-hole-plate"),
}
REQUIRED_FIELDS = {
    "schema_version", "mechanism_id", "status", "development_only", "top_k",
    "baseline_policy", "treatment_policy", "stopping_rule", "cases",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def audit_evaluation(evaluation: dict | None = None) -> None:
    evaluation = load_json(EVALUATION) if evaluation is None else evaluation
    assert set(evaluation) == REQUIRED_FIELDS
    assert evaluation["schema_version"] == 1
    assert evaluation["mechanism_id"] == "vertical-cylinder-construction-v1"
    assert evaluation["status"] == "preregistered"
    assert evaluation["development_only"] is True
    assert evaluation["top_k"] == 1
    assert evaluation["baseline_policy"] == "return no cards"
    assert "vertical-cylinder-construction" in evaluation["treatment_policy"]
    assert "do not add or replace a case" in evaluation["stopping_rule"]

    audit_reference_pack_qualification.audit_qualification()
    rows = evaluation["cases"]
    assert len(rows) == 3
    assert {row["case_id"] for row in rows} == set(EXPECTED_CASES)
    for row in rows:
        expected_role, expected_pack = EXPECTED_CASES[row["case_id"]]
        assert set(row) == {"case_id", "role", "pack_id"}
        assert row["role"] == expected_role
        assert row["pack_id"] == expected_pack


def main() -> None:
    audit_evaluation()
    print("reference-pack retrieval preregistration passed: 3 fixed development cases, top-k=1")


if __name__ == "__main__":
    main()
