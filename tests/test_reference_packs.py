from __future__ import annotations

import copy

import pytest

from tools import audit_reference_packs


def test_reference_pack_audit_passes() -> None:
    audit_reference_packs.main()


def test_reference_pack_rejects_raw_step_reference() -> None:
    contract = audit_reference_packs.load_json(audit_reference_packs.CONTRACT)
    unsafe_contract = copy.deepcopy(contract)
    unsafe_contract["packs"][0]["source_case_record"] = "case-library/self-authored/box/input.step"

    with pytest.raises(AssertionError):
        audit_reference_packs.audit_contract(unsafe_contract)
