from tools.audit_sequence_paired_repeated_feature_pattern import audit


def test_repeated_feature_pattern_audit_passes() -> None:
    rows = audit()
    assert len(rows) == 6
    assert all(row["mutations"] == 5 for row in rows)
