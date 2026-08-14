from tools.audit_m159_offset_rounded_slot_deregistration import audit


def test_m159_deregisters_experimental_offset_rounded_slot_metadata_without_asset_access() -> None:
    assert audit() == {
        "case_ids": [
            "param_offset_rounded_slot_low",
            "param_offset_rounded_slot_nominal",
            "param_offset_rounded_slot_high",
        ],
        "fixture_access": "not_performed",
        "script_access": "not_performed",
        "result": "pass",
    }
