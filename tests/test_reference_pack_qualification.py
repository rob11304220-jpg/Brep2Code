from __future__ import annotations

import copy

import pytest

from tools import audit_reference_pack_qualification


def test_reference_pack_qualification_passes() -> None:
    audit_reference_pack_qualification.main()


def test_reference_pack_qualification_rejects_duplicate_role() -> None:
    qualification = audit_reference_pack_qualification.load_json(
        audit_reference_pack_qualification.QUALIFICATION
    )
    invalid = copy.deepcopy(qualification)
    invalid["cases"][2]["role"] = "single boolean-cut tool"

    with pytest.raises(AssertionError):
        audit_reference_pack_qualification.audit_qualification(invalid)
