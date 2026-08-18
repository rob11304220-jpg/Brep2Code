from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from brep2code.cases import validate_case
from brep2code.campaigns import (
    CampaignValidationError,
    load_campaign_contract,
    validate_control_matrix_result,
    validate_hosted_pilot_result,
    validate_pilot_result,
)
from brep2code.evaluation import (
    build_control_report,
    build_hosted_pilot_report,
)
from brep2code.tools import dispatch_tool
from tests.support.pilot_artifacts import synthetic_pilot_artifacts


CONTRACT = Path("cases/campaigns/g1-mechanism-coverage.json")


def _synthetic_pilot_payloads():
    artifacts = synthetic_pilot_artifacts()
    return (
        artifacts.contract,
        artifacts.runtime,
        artifacts.controls,
        artifacts.held_out,
        artifacts.pilot,
    )


def test_g1_campaign_contract_binds_ladder_and_runtime_scope() -> None:
    contract = load_campaign_contract(CONTRACT, Path("cases"))

    assert contract.campaign_id == "g1-mechanism-coverage"
    assert [item.case_id for item in contract.runtime_cases] == [
        "box",
        "block_with_hole",
        "blind_hole_block",
        "filleted_box",
    ]
    assert contract.select_case("cylinder").mode == "held_out"
    assert contract.provider_policy["max_requests"] == 8
    assert contract.provider_policy["case_max_requests"] == 2
    assert contract.provider_policy["max_total_tokens"] == 32768
    assert contract.provider_policy["case_max_total_tokens"] == 8192
    assert contract.provider_policy["case_max_cost_usd"] == 0.1
    assert [item["capability_level"] for item in contract.capability_ladder] == ["L0", "L1", "L2"]
    assert [item.capability_level for item in contract.cases] == ["L0", "L0", "L1", "L1", "L2", "L0", "L0", "L1", "L1", "L2"]
    assert len(contract.cases) == 10
    assert len(contract.control_matrix) == 30
    assert {
        (item.case_id, item.control_variant) for item in contract.control_matrix
    } == {
        (case_id, variant)
        for case_id in (
            "box",
            "cylinder",
            "block_with_hole",
            "blind_hole_block",
            "box_held_out",
            "cylinder_held_out",
            "through_cut_held_out",
            "blind_cut_held_out",
            "filleted_box",
            "filleted_box_held_out",
        )
        for variant in ("nominal", "parameter_variation", "failure_sensitive")
    }
    assert [item.case_id for item in contract.held_out_matrix] == [
        "cylinder",
        "box_held_out",
        "cylinder_held_out",
        "through_cut_held_out",
        "blind_cut_held_out",
        "filleted_box_held_out",
    ]
    assert contract.held_out_policy["max_requests"] == 12
    assert contract.control_policy == {
        "max_rounds": 1,
        "build_timeout_seconds": 30,
        "max_requests": 30,
        "case_max_requests": 1,
        "max_total_tokens": 30,
        "case_max_total_tokens": 1,
        "max_cost_usd": 0.3,
        "case_max_cost_usd": 0.01,
    }


def test_pilot_result_validator_rejects_scope_accounting_and_report_drift() -> None:
    contract, runtime, controls, held_out, pilot = _synthetic_pilot_payloads()
    validate_pilot_result(
        pilot,
        contract,
        runtime_payload=runtime,
        control_matrix_payload=controls,
        held_out_payload=held_out,
    )

    tampered = deepcopy(pilot)
    tampered["runtime_case_ids"] = ["cylinder"]
    with pytest.raises(CampaignValidationError, match="runtime case scope drift"):
        validate_pilot_result(tampered, contract)

    tampered = deepcopy(pilot)
    tampered["provider_accounting"]["http_attempts"] = 42
    with pytest.raises(CampaignValidationError, match="aggregate provider accounting drift"):
        validate_pilot_result(tampered, contract)

    tampered = deepcopy(pilot)
    tampered["capability_report"][0]["control_count"] = 99
    with pytest.raises(CampaignValidationError, match="terminal status drift|report drift"):
        validate_pilot_result(
            tampered,
            contract,
            runtime_payload=runtime,
            control_matrix_payload=controls,
            held_out_payload=held_out,
        )

    tampered_controls = deepcopy(controls)
    tampered_controls["cases"][0], tampered_controls["cases"][1] = (
        tampered_controls["cases"][1],
        tampered_controls["cases"][0],
    )
    with pytest.raises(CampaignValidationError, match="control order drift"):
        validate_pilot_result(
            pilot,
            contract,
            runtime_payload=runtime,
            control_matrix_payload=tampered_controls,
            held_out_payload=held_out,
        )


def test_hosted_pilot_validator_binds_provider_routing_policy_and_children() -> None:
    contract, runtime, controls, held_out, _ = _synthetic_pilot_payloads()
    runtime["provider"] = contract.provider_policy["provider"]
    runtime["model"] = contract.provider_policy["model"]
    controls["model"] = "fake-script-queue-v1"
    held_out["model"] = "fake-script-queue-v1"
    pilot = build_hosted_pilot_report(runtime, controls, held_out)

    validate_hosted_pilot_result(
        pilot,
        contract,
        runtime_payload=runtime,
        control_matrix_payload=controls,
        held_out_payload=held_out,
    )

    tampered = deepcopy(pilot)
    tampered["provider_routing"]["held_out"]["provider"] = "deepseek"
    with pytest.raises(CampaignValidationError, match="provider routing drift"):
        validate_hosted_pilot_result(
            tampered,
            contract,
            runtime_payload=runtime,
            control_matrix_payload=controls,
            held_out_payload=held_out,
        )

    tampered_runtime = deepcopy(runtime)
    tampered_runtime["model"] = "wrong-model"
    with pytest.raises(CampaignValidationError, match="runtime result model drift"):
        validate_hosted_pilot_result(
            pilot,
            contract,
            runtime_payload=tampered_runtime,
            control_matrix_payload=controls,
            held_out_payload=held_out,
        )

    tampered = deepcopy(pilot)
    tampered["provider_accounting"]["total_tokens"] += 1
    with pytest.raises(CampaignValidationError, match="report drift"):
        validate_hosted_pilot_result(
            tampered,
            contract,
            runtime_payload=runtime,
            control_matrix_payload=controls,
            held_out_payload=held_out,
        )

def test_campaign_contract_rejects_case_metadata_drift(tmp_path: Path) -> None:
    payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
    payload["cases"][0]["mechanism"] = "boolean_cut"
    path = tmp_path / "campaign.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(CampaignValidationError, match="mechanism drift"):
        load_campaign_contract(path, Path("cases"))


def test_control_matrix_result_validator_rejects_drift_and_accounting_errors() -> None:
    contract = load_campaign_contract(CONTRACT, Path("cases"))
    rows = []
    for control in contract.control_matrix:
        actual_failure_class = control.failure_class
        rows.append(
            {
                "case_id": control.case_id,
                "control_variant": control.control_variant,
                "mechanism": next(item.mechanism for item in contract.cases if item.case_id == control.case_id),
                "capability_level": next(
                    item.capability_level for item in contract.cases if item.case_id == control.case_id
                ),
                "expected_result": control.expected_result,
                "expected_failure_class": control.failure_class,
                "actual_result": "pass" if actual_failure_class == "pass" else "fail",
                "actual_failure_class": actual_failure_class,
                "matches_expectation": True,
                "status": "succeeded" if actual_failure_class == "pass" else "budget_exhausted",
                "stop_reason": "passed" if actual_failure_class == "pass" else "max_rounds",
                "gate_report": {},
                "case_provider_accounting": {
                    "http_attempts": 1,
                    "total_tokens": 0,
                    "cost_usd": 0.0,
                },
                "provider_requests": 1,
                "result_path": str(Path("cases") / control.case_id / control.control_variant / "result.json"),
            }
        )
    result = {
        "artifact": "control_matrix",
        "campaign_id": contract.campaign_id,
        "contract_sha256": contract.sha256,
        "provider": "fake",
        "control_policy": contract.control_policy,
        "accounting_scope": "control_matrix_aggregate",
        "provider_accounting": {"http_attempts": 30, "total_tokens": 0, "cost_usd": 0.0},
        "provider_requests": 30,
        "status": "succeeded",
        "stop_reason": "control_matrix_passed",
        "cases": rows,
        "control_report": build_control_report(rows),
    }

    validate_control_matrix_result(result, contract)

    result["cases"][1]["control_variant"] = "failure_sensitive"
    with pytest.raises(CampaignValidationError, match="order drift"):
        validate_control_matrix_result(result, contract)
    result["cases"][1]["control_variant"] = contract.control_matrix[1].control_variant
    result["provider_accounting"]["http_attempts"] = 11
    with pytest.raises(CampaignValidationError, match="http accounting drift"):
        validate_control_matrix_result(result, contract)


def test_mechanism_metadata_stays_out_of_runtime_observations() -> None:
    case = validate_case(Path("cases/smoke/block_with_hole"), Path("cases"))

    observations = dispatch_tool("brep_observations", case)

    assert "mechanism" not in observations
    assert "kernel_properties" not in observations
    assert "sequence" not in observations
    assert "expected" not in observations
    assert "dossier" not in observations
