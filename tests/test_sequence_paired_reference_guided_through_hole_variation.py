import pytest

from tools.audit_sequence_paired_reference_guided_through_hole_variation import _assert_candidate_only, audit


def test_reference_guided_through_hole_variation_audit_passes() -> None:
    rows = audit()
    assert len(rows) == 6
    assert all(row["mutations"] == 3 for row in rows)


def test_candidate_metadata_rejects_a_provider_payload() -> None:
    entry = {"data_split": "development", "family_id": "development"}
    case = {
        "status": "experimental",
        "data_split": "development",
        "family_id": "development",
        "provider_payload": {"reference_answer": "forbidden"},
        "admission_boundary": "Absent from provider and runtime paths.",
    }
    with pytest.raises(ValueError, match="source leak"):
        _assert_candidate_only(case, entry)
