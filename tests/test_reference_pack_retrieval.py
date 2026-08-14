from __future__ import annotations

import copy

import pytest

from tools import audit_reference_pack_retrieval
from tools import evaluate_reference_pack_retrieval


@pytest.mark.fast
def test_reference_pack_retrieval_preregistration_passes() -> None:
    audit_reference_pack_retrieval.main()


@pytest.mark.fast
def test_reference_pack_selection_is_fixed_and_bounded() -> None:
    assert evaluate_reference_pack_retrieval.select_cards("baseline", "cylinder", "final primitive") == []
    assert evaluate_reference_pack_retrieval.select_cards("treatment", "cylinder", "final primitive") == [
        "vertical-cylinder-construction"
    ]
    with pytest.raises(AssertionError):
        evaluate_reference_pack_retrieval.select_cards("treatment", "box", "baseline primitive")


@pytest.mark.fast
def test_reference_pack_retrieval_rejects_case_substitution() -> None:
    evaluation = audit_reference_pack_retrieval.load_json(audit_reference_pack_retrieval.EVALUATION)
    invalid = copy.deepcopy(evaluation)
    invalid["cases"][2]["case_id"] = "box"

    with pytest.raises(AssertionError):
        audit_reference_pack_retrieval.audit_evaluation(invalid)
