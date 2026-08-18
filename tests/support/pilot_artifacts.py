from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from brep2code.campaigns import CampaignContract, load_campaign_contract
from brep2code.evaluation import (
    build_control_report,
    build_held_out_report,
    build_hosted_pilot_report,
    build_mechanism_report,
    build_pilot_report,
)


DEFAULT_CONTRACT = Path("cases/campaigns/g1-mechanism-coverage.json")


@dataclass(frozen=True)
class PilotArtifacts:
    contract: CampaignContract
    pilot: dict
    runtime: dict
    controls: dict
    held_out: dict

    def write_tree(self, root: Path) -> Path:
        """Write the aggregate and three cohort results as a pilot artifact tree."""
        paths = {
            root / "result.json": self.pilot,
            root / "runtime" / "result.json": self.runtime,
            root / "controls" / "result.json": self.controls,
            root / "held-out" / "result.json": self.held_out,
        }
        for path, payload in paths.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload), encoding="utf-8")
        return root / "result.json"


def synthetic_pilot_artifacts(
    *,
    hosted: bool = False,
    contract_path: Path = DEFAULT_CONTRACT,
    cases_root: Path = Path("cases"),
) -> PilotArtifacts:
    """Build internally consistent fake or hosted pilot artifacts from a contract."""
    contract = load_campaign_contract(contract_path, cases_root)
    common = {
        "campaign_id": contract.campaign_id,
        "contract_sha256": contract.sha256,
        "provider": "fake",
        "model": "fake-script-queue-v1",
    }
    runtime_rows = []
    for case in contract.runtime_cases:
        requests = min(case.difficulty, contract.provider_policy["case_max_requests"])
        runtime_rows.append(
            {
                "case_id": case.case_id,
                "mechanism": case.mechanism,
                "capability_level": case.capability_level,
                "difficulty": case.difficulty,
                "status": "succeeded",
                "stop_reason": "passed",
                "classification": "pass",
                "gate_report": {},
                "case_provider_accounting": _accounting(requests),
                "provider_requests": requests,
                "result_path": str(Path("cases") / case.case_id / "result.json"),
            }
        )
    runtime = {
        **common,
        "artifact": "campaign",
        "provider_policy": contract.provider_policy,
        "accounting_scope": "campaign_aggregate",
        "provider_accounting": _accounting(sum(row["provider_requests"] for row in runtime_rows)),
        "provider_requests": sum(row["provider_requests"] for row in runtime_rows),
        "status": "succeeded",
        "stop_reason": "completed",
        "cases": runtime_rows,
        "mechanism_report": build_mechanism_report(runtime_rows),
    }

    cases_by_id = {case.case_id: case for case in contract.cases}
    control_rows = []
    for control in contract.control_matrix:
        case = cases_by_id[control.case_id]
        control_rows.append(
            {
                "case_id": control.case_id,
                "control_variant": control.control_variant,
                "mechanism": case.mechanism,
                "capability_level": case.capability_level,
                "expected_result": control.expected_result,
                "expected_failure_class": control.failure_class,
                "actual_result": "pass" if control.failure_class == "pass" else "fail",
                "actual_failure_class": control.failure_class,
                "matches_expectation": True,
                "status": "succeeded",
                "stop_reason": "passed",
                "gate_report": {},
                "case_provider_accounting": _accounting(1),
                "provider_requests": 1,
                "result_path": str(
                    Path("cases") / control.case_id / control.control_variant / "result.json"
                ),
            }
        )
    controls = {
        **common,
        "artifact": "control_matrix",
        "control_policy": contract.control_policy,
        "accounting_scope": "control_matrix_aggregate",
        "provider_accounting": _accounting(len(control_rows)),
        "provider_requests": len(control_rows),
        "status": "succeeded",
        "stop_reason": "control_matrix_passed",
        "cases": control_rows,
        "control_report": build_control_report(control_rows),
    }

    held_out_rows = []
    for expected in contract.held_out_matrix:
        case = cases_by_id[expected.case_id]
        held_out_rows.append(
            {
                "case_id": expected.case_id,
                "mechanism": case.mechanism,
                "capability_level": case.capability_level,
                "expected_result": expected.expected_result,
                "expected_failure_class": expected.failure_class,
                "fixture_sha256": expected.fixture_sha256,
                "expected": expected.expected,
                "gate_oracles": expected.gate_oracles,
                "actual_result": "pass" if expected.failure_class == "pass" else "fail",
                "actual_failure_class": expected.failure_class,
                "matches_expectation": True,
                "status": "succeeded",
                "stop_reason": "passed",
                "gate_report": {},
                "case_provider_accounting": _accounting(1),
                "provider_requests": 1,
                "result_path": str(Path("cases") / expected.case_id / "result.json"),
            }
        )
    held_out = {
        **common,
        "artifact": "held_out_generalization",
        "held_out_policy": contract.held_out_policy,
        "accounting_scope": "held_out_aggregate",
        "provider_accounting": _accounting(len(held_out_rows)),
        "provider_requests": len(held_out_rows),
        "status": "succeeded",
        "stop_reason": "held_out_passed",
        "cases": held_out_rows,
        "held_out_report": build_held_out_report(held_out_rows),
    }

    if hosted:
        runtime["provider"] = contract.provider_policy["provider"]
        runtime["model"] = contract.provider_policy["model"]
        pilot = build_hosted_pilot_report(runtime, controls, held_out)
    else:
        pilot = build_pilot_report(runtime, controls, held_out)
        pilot["cohorts"]["runtime"]["result_path"] = str(Path("runtime") / "result.json")
        pilot["cohorts"]["control_matrix"]["result_path"] = str(Path("controls") / "result.json")
        pilot["cohorts"]["held_out"]["result_path"] = str(Path("held-out") / "result.json")
    return PilotArtifacts(contract, pilot, runtime, controls, held_out)


def _accounting(requests: int) -> dict[str, int | float]:
    return {"http_attempts": requests, "total_tokens": 0, "cost_usd": 0.0}
