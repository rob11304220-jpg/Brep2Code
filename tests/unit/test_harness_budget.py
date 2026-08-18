from __future__ import annotations

import json
from pathlib import Path

from brep2code.cases import validate_case
from brep2code.harness import RepairLoopRunner
from brep2code.providers import ProviderBudgetError


class BudgetExhaustedProvider:
    name = "test"
    model = "budget-test"

    def generate(self, request) -> None:
        del request
        raise ProviderBudgetError("provider token budget exceeded")


def test_provider_budget_error_is_recorded_as_budget_failure(tmp_path: Path) -> None:
    case = validate_case(Path("cases/smoke/box"), Path("cases"))

    result = RepairLoopRunner(BudgetExhaustedProvider()).run(
        case, tmp_path / "run", max_rounds=1
    )

    assert result.status == "budget_exhausted"
    assert result.stop_reason == "provider_budget"
    payload = json.loads(result.result_path.read_text(encoding="utf-8"))
    assert payload["revisions"][0]["error"] == {
        "stage": "budget",
        "scope": "provider",
        "message": "provider token budget exceeded",
    }
