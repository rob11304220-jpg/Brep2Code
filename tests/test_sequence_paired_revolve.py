from tools.audit_sequence_paired_revolve import audit


def test_revolve_audit_passes() -> None:
    rows = audit()
    assert len(rows) == 6
    assert all(row["mutations"] == 6 for row in rows)
