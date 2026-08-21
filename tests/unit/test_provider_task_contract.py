import pytest

from brep2code.providers.task_contract import (
    build_provider_task_contract,
    validate_task_contract_projection,
)


def test_no_retrieval_cadquery_contract_is_bounded_and_stable() -> None:
    contract = build_provider_task_contract("cadquery_v1", "disabled")

    assert contract.backend_profile == "cadquery_v1"
    assert contract.allowed_import_roots == ("cadquery",)
    assert contract.actions == ("probe", "submit", "finish")
    assert contract.available_tools == ("edge_candidates",)
    assert contract.output_file == "output.step"
    assert len(contract.identity) == 64


def test_task_contract_validation_rejects_projection_drift() -> None:
    contract = build_provider_task_contract("ocp_v1", "disabled")
    projection = contract.projection()
    projection["output_file"] = "other.step"

    with pytest.raises(ValueError, match="projection drift"):
        validate_task_contract_projection(projection, backend="ocp_v1", retrieval_policy="disabled")


def test_retrieval_contract_exposes_retrieval_only_when_enabled() -> None:
    contract = build_provider_task_contract("ocp_v1", "bounded_seed")

    assert "retrieve" in contract.actions
    assert "ocp_symbol" in contract.available_tools
    assert contract.prompt_version == "active-v4-retrieval"


def test_provider_task_contract_preserves_frozen_v1_identity() -> None:
    contract = build_provider_task_contract(
        "ocp_v1", "bounded_seed", contract_version=1
    )

    assert contract.contract_version == 1
    assert contract.prompt_version == "active-v3-retrieval"
