from pathlib import Path

import pytest

from brep2code.domain import Case, Session


def test_session_enforces_revision_budget() -> None:
    case = Case("box", Path("cases/smoke/box"), Path("input.step"))
    session = Session(case=case, max_rounds=1)

    assert session.new_revision().index == 0
    with pytest.raises(RuntimeError, match="budget exhausted"):
        session.new_revision()
