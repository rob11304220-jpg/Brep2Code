from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.audit_admission_profile import PROFILE, audit, inventory


def test_admission_profile_inventory_is_consistent_after_m144_reconciliation() -> None:
    result = inventory()
    assert result["fixture_access"] == "not_performed"
    assert result["active_case_count"] == 84
    assert result["inventory_conflicts"] == []


def test_admission_profile_rejects_a_fourth_recommendation(tmp_path: Path) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["recommendations"].append(profile["recommendations"][0])
    path = tmp_path / "profile.json"
    path.write_text(json.dumps(profile), encoding="utf-8")
    with pytest.raises(ValueError, match="recommendation"):
        audit(path)


def test_admission_profile_audits_after_m144_reconciliation() -> None:
    assert audit()["result"] == "pass"
