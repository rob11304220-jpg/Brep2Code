from __future__ import annotations

import json
from pathlib import Path

import pytest

from brep2code.campaigns import CampaignValidationError, load_campaign_contract
from brep2code.evaluation import build_mechanism_report
from brep2code.harness import CampaignRunner, CampaignRunResult, HarnessResult
from brep2code.providers import FakeProvider, ProviderLimits
from brep2code.providers.protocol import ProviderRequest
from brep2code.tools import dispatch_tool
from tests.support.pilot_artifacts import synthetic_pilot_artifacts


CONTRACT = load_campaign_contract(
    Path("cases/campaigns/g1-mechanism-coverage.json"), Path("cases")
)


class StubHostedProvider:
    def __init__(self, *, name: str = "deepseek", model: str = "deepseek-v4-pro", limits=None):
        self.name = name
        self.model = model
        self.limits = limits or ProviderLimits(
            max_requests=8,
            timeout_seconds=120,
            max_retries=0,
            max_output_tokens=4096,
            max_total_tokens=32768,
            max_cost_usd=0.4,
            input_cost_per_million=1.0,
            output_cost_per_million=2.0,
        )

    def generate(self, request):
        del request
        raise AssertionError("orchestration test must not make a hosted request")


def test_campaign_preflight_is_fresh_runtime_only_and_provider_free(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(
        "brep2code.harness.campaign.secure_backend_status",
        lambda: (True, "secure execution backend ready"),
    )
    runner = CampaignRunner(CONTRACT, Path("cases"))

    cases = runner.preflight(tmp_path / "campaign")

    assert [item[0].case_id for item in cases] == [
        "box",
        "block_with_hole",
        "blind_hole_block",
        "filleted_box",
    ]
    assert not (tmp_path / "campaign").exists()


def test_pilot_preflight_checks_all_scopes_once_without_reading_fake_scripts(
    tmp_path: Path, monkeypatch
) -> None:
    backend_calls = 0

    def ready_backend():
        nonlocal backend_calls
        backend_calls += 1
        return True, "secure execution backend ready"

    monkeypatch.setattr("brep2code.harness.campaign.secure_backend_status", ready_backend)
    runner = CampaignRunner(CONTRACT, Path("cases"))
    monkeypatch.setattr(
        runner,
        "control_scripts",
        lambda: (_ for _ in ()).throw(AssertionError("must not read control scripts")),
    )
    monkeypatch.setattr(
        runner,
        "held_out_scripts",
        lambda: (_ for _ in ()).throw(AssertionError("must not read held-out scripts")),
    )

    counts = runner.preflight_pilot(tmp_path / "pilot")

    assert counts == {"runtime": 4, "control_matrix": 30, "held_out": 6}
    assert backend_calls == 1
    assert not (tmp_path / "pilot").exists()


def test_hosted_pilot_orchestrates_mixed_providers_and_validates_aggregate(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(
        "brep2code.harness.campaign.secure_backend_status",
        lambda: (True, "secure execution backend ready"),
    )
    artifacts = synthetic_pilot_artifacts(hosted=True)
    runtime_payload = artifacts.runtime
    control_payload = artifacts.controls
    held_out_payload = artifacts.held_out
    calls: list[tuple[str, str]] = []
    runner = CampaignRunner(CONTRACT, Path("cases"))
    monkeypatch.setattr(runner, "control_scripts", lambda: ("control",) * 30)
    monkeypatch.setattr(runner, "held_out_scripts", lambda: ("held-out",) * 6)

    def write_result(label, payload, provider, root, *, preflighted):
        assert preflighted is True
        calls.append((label, provider.name))
        root.mkdir(parents=True)
        path = root / "result.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return CampaignRunResult(
            payload["status"], payload["stop_reason"], payload["provider_requests"], path
        )

    monkeypatch.setattr(
        runner,
        "run",
        lambda provider, root, *, preflighted: write_result(
            "runtime", runtime_payload, provider, root, preflighted=preflighted
        ),
    )
    monkeypatch.setattr(
        runner,
        "run_control_matrix",
        lambda provider, root, *, preflighted: write_result(
            "controls", control_payload, provider, root, preflighted=preflighted
        ),
    )
    monkeypatch.setattr(
        runner,
        "run_held_out",
        lambda provider, root, *, preflighted: write_result(
            "held-out", held_out_payload, provider, root, preflighted=preflighted
        ),
    )

    result = runner.run_hosted_pilot(StubHostedProvider(), tmp_path / "pilot")
    payload = json.loads(result.result_path.read_text(encoding="utf-8"))

    assert calls == [("runtime", "deepseek"), ("controls", "fake"), ("held-out", "fake")]
    assert result.status == "succeeded"
    assert result.provider_requests == 43
    assert payload["artifact"] == "l0_l2_hosted_pilot"
    assert payload["provider_routing"] == {
        "runtime": {"provider": "deepseek", "model": "deepseek-v4-pro"},
        "control_matrix": {"provider": "fake", "model": "fake-script-queue-v1"},
        "held_out": {"provider": "fake", "model": "fake-script-queue-v1"},
    }
    assert payload["cohorts"]["runtime"]["result_path"] == str(Path("runtime/result.json"))
    assert payload["cohorts"]["control_matrix"]["result_path"] == str(
        Path("controls/result.json")
    )
    assert payload["cohorts"]["held_out"]["result_path"] == str(
        Path("held-out/result.json")
    )

    runtime_payload["status"] = "failed"
    runtime_payload["stop_reason"] = "case_failed"
    runtime_payload["cases"][0]["status"] = "failed"
    runtime_payload["mechanism_report"] = build_mechanism_report(runtime_payload["cases"])
    failed = runner.run_hosted_pilot(
        StubHostedProvider(), tmp_path / "failed-pilot", preflighted=True
    )
    failed_payload = json.loads(failed.result_path.read_text(encoding="utf-8"))
    assert failed.status == "failed"
    assert failed.stop_reason == "cohort_failed"
    assert failed_payload["status"] == "failed"


@pytest.mark.parametrize(
    "provider",
    [
        StubHostedProvider(name="fake"),
        StubHostedProvider(model="wrong-model"),
        StubHostedProvider(
            limits=ProviderLimits(
                max_requests=7,
                timeout_seconds=120,
                max_retries=0,
                max_output_tokens=4096,
                max_total_tokens=32768,
                max_cost_usd=0.4,
                input_cost_per_million=1.0,
                output_cost_per_million=2.0,
            )
        ),
    ],
)
def test_hosted_pilot_rejects_provider_model_and_policy_before_creating_root(
    tmp_path: Path, provider
) -> None:
    run_root = tmp_path / "pilot"

    with pytest.raises(CampaignValidationError, match="provider|model|limits"):
        CampaignRunner(CONTRACT, Path("cases")).run_hosted_pilot(provider, run_root)

    assert not run_root.exists()


def test_held_out_preflight_is_separate_from_runtime_and_keeps_fixture_out_of_observations(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(
        "brep2code.harness.campaign.secure_backend_status",
        lambda: (True, "secure execution backend ready"),
    )
    runner = CampaignRunner(CONTRACT, Path("cases"))

    runtime = runner.preflight(tmp_path / "runtime")
    held_out = runner.preflight_held_out(tmp_path / "held-out")

    assert [item[0].case_id for item in runtime] == [
        "box",
        "block_with_hole",
        "blind_hole_block",
        "filleted_box",
    ]
    assert [item[0].case_id for item in held_out] == [
        "cylinder",
        "box_held_out",
        "cylinder_held_out",
        "through_cut_held_out",
        "blind_cut_held_out",
        "filleted_box_held_out",
    ]
    assert len(runner.held_out_scripts()) == 6
    observations = dispatch_tool("brep_observations", held_out[1][1])
    assert "expected" not in observations
    assert "dossier" not in observations
    assert "held_out_fixture" not in observations


def test_held_out_runner_keeps_case_continuation_and_accounting_isolated(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(
        "brep2code.harness.campaign.secure_backend_status",
        lambda: (True, "secure execution backend ready"),
    )
    provider = FakeProvider(["script"] * 12)
    calls: list[str] = []

    class StubLoop:
        def __init__(self, case_provider) -> None:
            self.case_provider = case_provider

        def run(self, case, run_root, **kwargs):
            del kwargs
            calls.append(case.case.case_id)
            for index in range(2):
                self.case_provider.generate(
                    ProviderRequest(
                        case_id=case.case.case_id,
                        round_index=index,
                        context={"brep": {}},
                        feedback={"stage": "geometry"} if index else None,
                        previous_script="script" if index else None,
                    )
                )
            run_root.mkdir(parents=True)
            result_path = run_root / "result.json"
            result_path.write_text(
                json.dumps(
                    {
                        "case_id": case.case.case_id,
                        "status": "succeeded",
                        "stop_reason": "passed",
                        "provider_requests": 2,
                        "provider_accounting": {
                            "http_attempts": 2,
                            "total_tokens": 0,
                            "cost_usd": 0.0,
                        },
                        "revisions": [{"gates": {"passed": True}}],
                    }
                ),
                encoding="utf-8",
            )
            return HarnessResult("succeeded", "passed", 2, result_path)

    result = CampaignRunner(CONTRACT, Path("cases"), loop_factory=StubLoop).run_held_out(
        provider, tmp_path / "held-out"
    )
    payload = json.loads(result.result_path.read_text(encoding="utf-8"))

    assert result.status == "succeeded"
    assert calls == [
        "cylinder",
        "box_held_out",
        "cylinder_held_out",
        "through_cut_held_out",
        "blind_cut_held_out",
        "filleted_box_held_out",
    ]
    assert [request.case_id for request in provider.requests] == [case_id for case_id in calls for _ in range(2)]
    assert payload["provider_requests"] == 12
    assert payload["provider_accounting"] == {
        "http_attempts": 12,
        "total_tokens": 0,
        "cost_usd": 0.0,
    }
    assert all(item["matches_expectation"] for item in payload["cases"])
    assert all(item["case_provider_accounting"]["http_attempts"] == 2 for item in payload["cases"])
    assert all(
        Path(item["result_path"]) == Path("cases") / item["case_id"] / "result.json"
        for item in payload["cases"]
    )


def test_campaign_runs_all_cases_and_checkpoints_after_each_case(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(
        "brep2code.harness.campaign.secure_backend_status",
        lambda: (True, "secure execution backend ready"),
    )
    outcomes = {
        "box": ("succeeded", "passed", 2),
        "block_with_hole": ("failed", "case_failed", 1),
        "blind_hole_block": ("succeeded", "passed", 2),
        "filleted_box": ("succeeded", "passed", 2),
    }
    calls: list[str] = []

    class StubLoop:
        def __init__(self, provider) -> None:
            del provider

        def run(self, case, run_root, **kwargs):
            del kwargs
            calls.append(case.case.case_id)
            status, stop_reason, requests = outcomes[case.case.case_id]
            run_root.mkdir(parents=True)
            result_path = run_root / "result.json"
            result_path.write_text(
                json.dumps(
                    {
                        "case_id": case.case.case_id,
                        "status": status,
                        "stop_reason": stop_reason,
                        "provider_requests": requests,
                        "revisions": [],
                    }
                ),
                encoding="utf-8",
            )
            return HarnessResult(status, stop_reason, requests, result_path)

    runner = CampaignRunner(CONTRACT, Path("cases"), loop_factory=StubLoop)
    result = runner.run(FakeProvider([]), tmp_path / "campaign")
    payload = json.loads(result.result_path.read_text(encoding="utf-8"))

    assert calls == ["box", "block_with_hole", "blind_hole_block", "filleted_box"]
    assert result.status == "failed"
    assert result.stop_reason == "case_failed"
    assert result.provider_requests == 7
    assert [item["case_id"] for item in payload["cases"]] == calls
    assert "cylinder" not in {item["case_id"] for item in payload["cases"]}
    assert payload["cases"][1]["classification"] == "provider"
    assert [item["capability_level"] for item in payload["cases"]] == ["L0", "L1", "L1", "L2"]
    assert [(item["mechanism"], item["capability_level"]) for item in payload["mechanism_report"]] == [
        ("boolean_cut", "L1"),
        ("fillet", "L2"),
        ("primitive", "L0"),
    ]
    assert all(
        Path(item["result_path"]) == Path("cases") / item["case_id"] / "result.json"
        for item in payload["cases"]
    )
    assert payload["provider_policy"]["max_requests"] == 8
    assert payload["accounting_scope"] == "campaign_aggregate"
    assert all("case_provider_accounting" in item for item in payload["cases"])
    assert payload["provider_accounting"] == {
        "http_attempts": 0,
        "total_tokens": 0,
        "cost_usd": 0.0,
    }


def test_campaign_runner_isolates_runner_exception_and_continues(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(
        "brep2code.harness.campaign.secure_backend_status",
        lambda: (True, "secure execution backend ready"),
    )

    class StubLoop:
        def __init__(self, provider) -> None:
            del provider

        def run(self, case, run_root, **kwargs):
            del kwargs
            if case.case.case_id == "block_with_hole":
                raise RuntimeError("simulated case failure")
            run_root.mkdir(parents=True)
            result_path = run_root / "result.json"
            result_path.write_text(
                json.dumps(
                    {
                        "case_id": case.case.case_id,
                        "status": "succeeded",
                        "stop_reason": "passed",
                        "provider_requests": 1,
                        "revisions": [],
                    }
                ),
                encoding="utf-8",
            )
            return HarnessResult("succeeded", "passed", 1, result_path)

    result = CampaignRunner(CONTRACT, Path("cases"), loop_factory=StubLoop).run(
        FakeProvider([]), tmp_path / "campaign"
    )
    payload = json.loads(result.result_path.read_text(encoding="utf-8"))

    assert result.status == "failed"
    assert len(payload["cases"]) == 4
    assert payload["cases"][1]["stop_reason"] == "runner_error"
    assert payload["cases"][2]["status"] == "succeeded"


def test_fake_provider_covers_case_local_continuation_and_aggregate_reporting(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(
        "brep2code.harness.campaign.secure_backend_status",
        lambda: (True, "secure execution backend ready"),
    )
    provider = FakeProvider(["script"] * 8)

    class FakeLoop:
        def __init__(self, case_provider) -> None:
            self.case_provider = case_provider

        def run(self, case, run_root, **kwargs):
            del kwargs
            previous_script = None
            revisions = []
            for index in range(2):
                response = self.case_provider.generate(
                    ProviderRequest(
                        case_id=case.case.case_id,
                        round_index=index,
                        context={"case_id": case.case.case_id},
                        feedback=(
                            {"stage": "geometry"} if index == 1 else None
                        ),
                        previous_script=previous_script,
                    )
                )
                previous_script = response.script
                revisions.append({"feedback": {"stage": "geometry"}} if index == 1 else {})
            status = "failed" if case.case.case_id == "block_with_hole" else "succeeded"
            stop_reason = "case_failed" if status == "failed" else "passed"
            run_root.mkdir(parents=True)
            result_path = run_root / "result.json"
            result_path.write_text(
                json.dumps(
                    {
                        "case_id": case.case.case_id,
                        "status": status,
                        "stop_reason": stop_reason,
                        "provider_requests": 2,
                        "revisions": revisions,
                    }
                ),
                encoding="utf-8",
            )
            return HarnessResult(status, stop_reason, 2, result_path)

    result = CampaignRunner(CONTRACT, Path("cases"), loop_factory=FakeLoop).run(
        provider, tmp_path / "campaign"
    )
    payload = json.loads(result.result_path.read_text(encoding="utf-8"))

    assert [request.case_id for request in provider.requests] == [
        "box",
        "box",
        "block_with_hole",
        "block_with_hole",
        "blind_hole_block",
        "blind_hole_block",
        "filleted_box",
        "filleted_box",
    ]
    assert payload["provider_requests"] == 8
    assert payload["provider_accounting"]["http_attempts"] == 8
    assert payload["cases"][1]["classification"] == "geometry"
    assert payload["mechanism_report"][0]["capability_level"] == "L1"


def test_campaign_continues_after_case_budget_exhaustion(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(
        "brep2code.harness.campaign.secure_backend_status",
        lambda: (True, "secure execution backend ready"),
    )
    calls: list[str] = []
    outcomes = {
        "box": ("budget_exhausted", "max_rounds"),
        "block_with_hole": ("succeeded", "passed"),
        "blind_hole_block": ("succeeded", "passed"),
        "filleted_box": ("succeeded", "passed"),
    }

    class StubLoop:
        def __init__(self, provider) -> None:
            del provider

        def run(self, case, run_root, **kwargs):
            del kwargs
            calls.append(case.case.case_id)
            status, stop_reason = outcomes[case.case.case_id]
            run_root.mkdir(parents=True)
            result_path = run_root / "result.json"
            result_path.write_text(
                json.dumps(
                    {
                        "case_id": case.case.case_id,
                        "status": status,
                        "stop_reason": stop_reason,
                        "provider_requests": 1,
                        "revisions": [],
                    }
                ),
                encoding="utf-8",
            )
            return HarnessResult(status, stop_reason, 1, result_path)

    result = CampaignRunner(CONTRACT, Path("cases"), loop_factory=StubLoop).run(
        FakeProvider([]), tmp_path / "campaign"
    )
    payload = json.loads(result.result_path.read_text(encoding="utf-8"))

    assert calls == ["box", "block_with_hole", "blind_hole_block", "filleted_box"]
    assert result.status == "budget_exhausted"
    assert result.stop_reason == "case_budget_exhausted"
    assert len(payload["cases"]) == 4
    assert payload["cases"][0]["classification"] == "budget"


def test_campaign_stops_after_aggregate_budget_exhaustion(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(
        "brep2code.harness.campaign.secure_backend_status",
        lambda: (True, "secure execution backend ready"),
    )
    calls: list[str] = []

    class StubLoop:
        def __init__(self, provider) -> None:
            del provider

        def run(self, case, run_root, **kwargs):
            del kwargs
            calls.append(case.case.case_id)
            run_root.mkdir(parents=True)
            result_path = run_root / "result.json"
            result_path.write_text(
                json.dumps(
                    {
                        "case_id": case.case.case_id,
                        "status": "budget_exhausted",
                        "stop_reason": "provider_budget",
                        "provider_requests": 1,
                        "revisions": [
                            {
                                "error": {
                                    "stage": "budget",
                                    "scope": "campaign_aggregate",
                                }
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            return HarnessResult("budget_exhausted", "provider_budget", 1, result_path)

    result = CampaignRunner(CONTRACT, Path("cases"), loop_factory=StubLoop).run(
        FakeProvider([]), tmp_path / "campaign"
    )
    payload = json.loads(result.result_path.read_text(encoding="utf-8"))

    assert calls == ["box"]
    assert result.status == "budget_exhausted"
    assert result.stop_reason == "budget_exhausted"
    assert len(payload["cases"]) == 1
