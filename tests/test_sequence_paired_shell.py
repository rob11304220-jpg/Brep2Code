from tools.audit_sequence_paired_shell import audit


def test_shell_audit_passes() -> None:
    rows = audit()
    assert len(rows) == 6
    assert all(row["mutations"] == 2 for row in rows)
