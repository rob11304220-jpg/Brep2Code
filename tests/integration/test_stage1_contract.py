from pathlib import Path
import json

import pytest

from brep2code.cases import validate_catalog
from brep2code.stage1 import CORE_CASES, Stage1ContractError, load_stage1_contract


def test_stage1_backend_baseline_contract_binds_runtime_cases_and_profiles() -> None:
    contract = load_stage1_contract(
        Path("cases/campaigns/stage1-backend-baseline.json"),
        validate_catalog(Path("cases")),
    )

    assert tuple(contract["cases"]) == CORE_CASES
    assert contract["backend_profiles"] == ["cadquery_v1", "ocp_v1"]
    assert contract["retrieval_policy"] == "disabled"
    assert contract["hosted_limits"]["max_total_tokens"] == 16000
    assert contract["cohorts"]["first_shot"]["cost_usd"] == 0.02
    assert contract["infrastructure_failure_rate_threshold"] == 0.1


def test_stage1_contract_rejects_invalid_infrastructure_failure_threshold(
    tmp_path: Path,
) -> None:
    source = Path("cases/campaigns/stage1-backend-baseline.json")
    payload = json.loads(source.read_text(encoding="utf-8"))
    payload["infrastructure_failure_rate_threshold"] = 0
    contract = tmp_path / "contract.json"
    contract.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(Stage1ContractError, match="infrastructure-failure threshold"):
        load_stage1_contract(contract, validate_catalog(Path("cases")))
