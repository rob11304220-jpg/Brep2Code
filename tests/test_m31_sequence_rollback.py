from __future__ import annotations

import pytest

from tools.run_sequence_rollback_experiment import run


@pytest.mark.parametrize(
    "case_id",
    [
        "param_additive_boss_dependent_cut_centered_nominal",
        "param_additive_boss_dependent_cut_offset_nominal",
    ],
)
def test_suffix_rollback_preserves_verified_prefix_and_restores_final_gates(tmp_path, case_id: str) -> None:
    result = run(case_id, tmp_path / case_id)
    assert result["suffix_defect"]["status"] == "failed_after_verified_prefix"
    assert result["suffix_defect"]["prefix_hash_before"] == result["baseline"]["artifacts"]["after_boss"]
    assert result["rollback"]["reused_prefix_hash"] == result["baseline"]["artifacts"]["after_boss"]
    assert all(gate["status"] == "pass" for gate in result["rollback"]["gates"])


def test_early_defect_is_not_eligible_for_rollback(tmp_path) -> None:
    result = run("param_additive_boss_dependent_cut_centered_nominal", tmp_path / "early")
    assert result["early_defect"] == {
        "status": "unsupported",
        "reason": "defect_precedes_verified_boss_prefix",
        "after_base_hash": result["early_defect"]["after_base_hash"],
        "after_boss_exists": False,
    }
