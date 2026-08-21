from __future__ import annotations

import json
from pathlib import Path

import brep2code.cli as cli_module
import pytest

from brep2code.cli import main
from brep2code.campaigns import CampaignValidationError
from brep2code.execution import ExecutionResult
from brep2code.geometry.inspect import GeometryMetrics
from brep2code.harness import (
    ActiveHarnessRunner,
    ActiveHarnessResult,
    ActiveState,
    ActiveSubmissionVerifier,
    CampaignRunResult,
    HarnessResult,
)
from brep2code.providers import (
    ActionRequest,
    OpenAICompatibleConfig,
    ProviderConfigurationError,
    ProviderResponse,
)
from tests.support.pilot_artifacts import synthetic_pilot_artifacts


def test_cases_validate_command(capsys) -> None:
    assert main(["cases", "validate"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "valid"
    assert payload["count"] == 11
    assert {item["case_id"] for item in payload["cases"]} == {
        "box",
        "block_with_hole",
        "stage1_cylinder",
        "blind_hole_block",
        "cylinder",
        "box_held_out",
        "cylinder_held_out",
        "through_cut_held_out",
        "blind_cut_held_out",
        "filleted_box",
        "filleted_box_held_out",
    }


def test_stage1_validate_command_is_offline(capsys) -> None:
    assert (
        main(
            [
                "stage1",
                "validate",
                "--contract",
                "cases/campaigns/stage1-backend-baseline.json",
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "valid"
    assert payload["backend_profiles"] == ["cadquery_v1", "ocp_v1"]
    assert payload["network_requests"] == 0


def test_stabilization_report_can_persist_one_fresh_aggregate(tmp_path: Path, capsys) -> None:
    output = tmp_path / "stabilization-report.json"
    argv = [
        "stage1",
        "stabilization-report",
        "--contract",
        "cases/campaigns/stage1-active-v4-stabilization.json",
        "--runs-root",
        str(tmp_path / "runs"),
        "--output",
        str(output),
    ]

    assert main(argv) == 1
    assert json.loads(output.read_text(encoding="utf-8"))["expected_runs"] == 12
    capsys.readouterr()

    assert main(argv) == 1
    assert json.loads(capsys.readouterr().out) == {
        "status": "invalid",
        "error": "stabilization report output must be fresh",
    }


def test_stage1_v2_preflight_is_read_only_and_requires_later_authorization(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    prerequisite = tmp_path / "stabilization-report.json"
    prerequisite.write_text(
        json.dumps(
            {
                "experiment_id": "stage1-active-v4-stabilization-v1",
                "expected_runs": 12,
                "observed_runs": 12,
                "missing_runs": [],
                "artifact_validation_failures": [],
                "projection_validation_failures": [],
                "judgment": {
                    "protocol_stable": True,
                    "stage1_exit_changed": False,
                    "stage2_authorized": False,
                },
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        cli_module,
        "secure_backend_profile_status",
        lambda profile: (True, "ready", "version"),
    )

    assert (
        main(
            [
                "stage1",
                "v2-preflight",
                "--contract",
                "cases/campaigns/stage1-no-knowledge-v2.json",
                "--stabilization-report",
                str(prerequisite),
                "--run-root",
                str(tmp_path / "fresh"),
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "ready_for_authorization_review"
    assert payload["expected_runs"] == 80
    assert payload["maximum_scope"]["cost_usd"] == 1.6
    assert payload["network_requests"] == 0
    assert payload["provider_configuration_read"] is False
    assert payload["artifacts_created"] is False
    assert payload["authorization_granted"] is False
    assert payload["stage2_authorized"] is False


def test_campaign_validate_command(capsys) -> None:
    assert (
        main(
            [
                "campaign",
                "validate",
                "--contract",
                "cases/campaigns/g1-mechanism-coverage.json",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "valid"
    assert payload["runtime_case_count"] == 4
    assert payload["budget"]["campaign_aggregate"]["max_total_tokens"] == 32768
    assert payload["budget"]["per_case"]["max_total_tokens"] == 8192
    assert payload["capability_ladder"][-1]["capability_level"] == "L2"


def test_campaign_preflight_command_is_local_only(tmp_path: Path, capsys, monkeypatch) -> None:
    class StubCampaignRunner:
        def __init__(self, contract, cases_root) -> None:
            assert contract.campaign_id == "g1-mechanism-coverage"
            assert cases_root == Path("cases")

        def preflight(self, run_root):
            assert run_root == tmp_path / "campaign"
            return ()

    monkeypatch.setattr(cli_module, "CampaignRunner", StubCampaignRunner)
    assert (
        main(
            [
                "campaign",
                "preflight",
                "--contract",
                "cases/campaigns/g1-mechanism-coverage.json",
                "--run-root",
                str(tmp_path / "campaign"),
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "ready"
    assert payload["runtime_case_count"] == 4


def test_campaign_run_binds_fake_provider_queue_and_result_path(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    observed = {}

    class StubCampaignRunner:
        def __init__(self, contract, cases_root) -> None:
            del contract, cases_root

        def preflight(self, run_root):
            observed["preflight_root"] = run_root
            return ()

        def run(self, provider, run_root, *, preflighted):
            observed["provider"] = provider
            observed["run_root"] = run_root
            observed["preflighted"] = preflighted
            return CampaignRunResult("succeeded", "completed", 8, run_root / "result.json")

    monkeypatch.setattr(cli_module, "CampaignRunner", StubCampaignRunner)
    scripts = ["tests/fixtures/fixed_box.py"] * 8
    argv = [
        "campaign",
        "run",
        "--contract",
        "cases/campaigns/g1-mechanism-coverage.json",
        "--run-root",
        str(tmp_path / "campaign"),
    ]
    for script in scripts:
        argv.extend(["--fake-script", script])

    assert main(argv) == 0
    capsys.readouterr()
    assert observed["provider"].name == "fake"
    assert observed["preflight_root"] == tmp_path / "campaign"
    assert observed["preflighted"] is True


def test_campaign_pilot_binds_fake_provider_and_run_root(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    observed = {}

    class StubCampaignRunner:
        def __init__(self, contract, cases_root) -> None:
            del contract, cases_root

        def run_pilot(self, provider, run_root):
            observed["provider"] = provider
            observed["run_root"] = run_root
            return CampaignRunResult("succeeded", "completed", 50, run_root / "result.json")

    monkeypatch.setattr(cli_module, "CampaignRunner", StubCampaignRunner)
    scripts = ["tests/fixtures/fixed_box.py"] * 8
    argv = [
        "campaign",
        "pilot",
        "--contract",
        "cases/campaigns/g1-mechanism-coverage.json",
        "--run-root",
        str(tmp_path / "pilot"),
    ]
    for script in scripts:
        argv.extend(["--fake-script", script])

    assert main(argv) == 0
    capsys.readouterr()
    assert observed["provider"].name == "fake"
    assert observed["run_root"] == tmp_path / "pilot"


def _copy_pilot_results(tmp_path: Path) -> Path:
    return synthetic_pilot_artifacts().write_tree(tmp_path / "pilot")


def test_campaign_pilot_validate_reads_saved_cohorts_without_running_provider(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    result_path = _copy_pilot_results(tmp_path)

    def reject_provider(*args, **kwargs):
        del args, kwargs
        raise AssertionError("pilot validation must not construct a provider")

    monkeypatch.setattr(cli_module, "FakeProvider", reject_provider)
    assert (
        main(
            [
                "campaign",
                "pilot-validate",
                "--contract",
                "cases/campaigns/g1-mechanism-coverage.json",
                "--result",
                str(result_path),
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "valid"
    assert payload["provider_requests"] == 43
    assert payload["result_path"] == str(result_path)


@pytest.mark.parametrize(
    ("relative_path", "field", "value", "error"),
    [
        ("result.json", "runtime_case_ids", ["box"], "runtime case scope drift"),
        (
            "result.json",
            "cohorts.runtime.result_path",
            "elsewhere/result.json",
            "runtime result path drift",
        ),
        ("runtime/result.json", "contract_sha256", "wrong", "contract/provider drift"),
        (
            "result.json",
            "provider_accounting.http_attempts",
            42,
            "aggregate provider accounting drift",
        ),
        (
            "result.json",
            "capability_report.0.control_count",
            99,
            "report drift",
        ),
    ],
)
def test_campaign_pilot_validate_rejects_saved_result_drift(
    tmp_path: Path,
    capsys,
    relative_path: str,
    field: str,
    value,
    error: str,
) -> None:
    result_path = _copy_pilot_results(tmp_path)
    artifact_path = result_path.parent / relative_path
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    target = payload
    parts = field.split(".")
    for part in parts[:-1]:
        target = target[int(part)] if part.isdigit() else target[part]
    target[parts[-1]] = value
    artifact_path.write_text(json.dumps(payload), encoding="utf-8")

    assert (
        main(
            [
                "campaign",
                "pilot-validate",
                "--contract",
                "cases/campaigns/g1-mechanism-coverage.json",
                "--result",
                str(result_path),
            ]
        )
        == 1
    )
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "invalid"
    assert error in output["error"]


def _write_hosted_pilot_results(tmp_path: Path) -> Path:
    return synthetic_pilot_artifacts(hosted=True).write_tree(tmp_path / "pilot")


def test_campaign_hosted_pilot_validate_reads_mixed_provider_results_only(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    result_path = _write_hosted_pilot_results(tmp_path)

    def reject_provider(*args, **kwargs):
        del args, kwargs
        raise AssertionError("hosted pilot validation must not construct a provider")

    monkeypatch.setattr(cli_module, "FakeProvider", reject_provider)
    monkeypatch.setattr(cli_module, "OpenAICompatibleProvider", reject_provider)
    monkeypatch.setattr(cli_module, "deepseek_config_from_env", reject_provider)

    assert (
        main(
            [
                "campaign",
                "hosted-pilot-validate",
                "--contract",
                "cases/campaigns/g1-mechanism-coverage.json",
                "--result",
                str(result_path),
            ]
        )
        == 0
    )
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "valid"
    assert output["provider_routing"]["runtime"] == {
        "provider": "deepseek",
        "model": "deepseek-v4-pro",
    }
    assert output["provider_requests"] == 43


@pytest.mark.parametrize(
    ("relative_path", "field", "value", "error"),
    [
        ("result.json", "provider_routing.runtime.model", "wrong", "provider routing drift"),
        ("runtime/result.json", "model", "wrong", "runtime result model drift"),
        ("controls/result.json", "provider", "deepseek", "provider"),
        ("result.json", "runtime_case_ids", ["box"], "report drift"),
        ("result.json", "provider_requests", 42, "report drift"),
        ("result.json", "capability_report.0.control_count", 99, "report drift"),
    ],
)
def test_campaign_hosted_pilot_validate_rejects_routing_and_report_drift(
    tmp_path: Path,
    capsys,
    relative_path: str,
    field: str,
    value,
    error: str,
) -> None:
    result_path = _write_hosted_pilot_results(tmp_path)
    artifact_path = result_path.parent / relative_path
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    target = payload
    parts = field.split(".")
    for part in parts[:-1]:
        target = target[int(part)] if part.isdigit() else target[part]
    target[parts[-1]] = value
    artifact_path.write_text(json.dumps(payload), encoding="utf-8")

    assert (
        main(
            [
                "campaign",
                "hosted-pilot-validate",
                "--contract",
                "cases/campaigns/g1-mechanism-coverage.json",
                "--result",
                str(result_path),
            ]
        )
        == 1
    )
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "invalid"
    assert error in output["error"]


def _pilot_preflight_argv(tmp_path: Path) -> list[str]:
    return [
        "campaign",
        "pilot-preflight",
        "--contract",
        "cases/campaigns/g1-mechanism-coverage.json",
        "--run-root",
        str(tmp_path / "pilot"),
        "--provider",
        "deepseek",
        "--model",
        "deepseek-v4-pro",
        "--thinking-mode",
        "disabled",
        "--authorize-hosted",
        "--max-requests",
        "8",
        "--provider-timeout",
        "120",
        "--max-retries",
        "0",
        "--max-output-tokens",
        "4096",
        "--max-total-tokens",
        "32768",
        "--max-cost-usd",
        "0.4",
        "--input-cost-per-million",
        "1",
        "--output-cost-per-million",
        "2",
    ]


def _hosted_pilot_argv(tmp_path: Path) -> list[str]:
    argv = _pilot_preflight_argv(tmp_path)
    argv[1] = "hosted-pilot"
    return argv


def _hosted_pilot_config_check_argv(tmp_path: Path) -> list[str]:
    argv = _pilot_preflight_argv(tmp_path)
    argv[1] = "hosted-pilot-config-check"
    return argv


def _hosted_readiness_argv(tmp_path: Path, baseline: Path) -> list[str]:
    argv = _pilot_preflight_argv(tmp_path)
    argv[1] = "hosted-readiness"
    argv.remove("--authorize-hosted")
    argv.extend(["--baseline-result", str(baseline)])
    return argv


def test_campaign_hosted_readiness_is_read_only_and_provider_free(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    baseline = synthetic_pilot_artifacts().write_tree(tmp_path / "baseline")
    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))
    monkeypatch.setattr(
        "brep2code.harness.campaign.secure_backend_status",
        lambda: (True, "secure execution backend ready"),
    )
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: (_ for _ in ()).throw(
            AssertionError("default readiness must not read provider configuration")
        ),
    )

    assert main(_hosted_readiness_argv(tmp_path, baseline)) == 0
    raw = capsys.readouterr().out
    output = json.loads(raw)
    assert output["status"] == "ready"
    assert output["gates"] == {
        "campaign_contract": "passed",
        "fake_pilot_baseline": "passed",
        "scope_validation": "passed",
        "fresh_run_root": "passed",
        "secure_backend": "passed",
        "provider_configuration": "skipped",
    }
    assert output["cohort_counts"] == {"runtime": 4, "control_matrix": 30, "held_out": 6}
    assert output["thinking_mode"] == "disabled"
    assert output["network_requests"] == 0
    assert output["artifacts_created"] is False
    assert "Brep2Code_new" not in raw
    assert sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*")) == before
    assert not (tmp_path / "pilot").exists()


@pytest.mark.parametrize(
    ("relative_path", "field", "value", "error"),
    [
        ("result.json", "contract_sha256", "wrong", "contract_sha256 drift"),
        ("runtime/result.json", "contract_sha256", "wrong", "contract/provider drift"),
        ("result.json", "runtime_case_ids", ["box"], "runtime case scope drift"),
    ],
)
def test_campaign_hosted_readiness_rejects_baseline_drift(
    tmp_path: Path, capsys, monkeypatch, relative_path: str, field: str, value, error: str
) -> None:
    baseline = synthetic_pilot_artifacts().write_tree(tmp_path / "baseline")
    path = baseline.parent / relative_path
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload[field] = value
    path.write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(
        "brep2code.harness.campaign.secure_backend_status",
        lambda: (True, "secure execution backend ready"),
    )

    assert main(_hosted_readiness_argv(tmp_path, baseline)) == 1
    output = json.loads(capsys.readouterr().out)
    assert output["failed_gate"] == "fake_pilot_baseline"
    assert error in output["error"]


def test_campaign_hosted_readiness_reports_missing_baseline(tmp_path: Path, capsys) -> None:
    baseline = tmp_path / "missing" / "result.json"
    assert main(_hosted_readiness_argv(tmp_path, baseline)) == 1
    output = json.loads(capsys.readouterr().out)
    assert output["failed_gate"] == "fake_pilot_baseline"
    assert output["error"] == "required saved result is missing"
    assert str(tmp_path) not in json.dumps(output)


def test_campaign_hosted_readiness_reports_existing_root(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    baseline = synthetic_pilot_artifacts().write_tree(tmp_path / "baseline")
    (tmp_path / "pilot").mkdir()
    monkeypatch.setattr(
        "brep2code.harness.campaign.secure_backend_status",
        lambda: (True, "secure execution backend ready"),
    )

    assert main(_hosted_readiness_argv(tmp_path, baseline)) == 1
    output = json.loads(capsys.readouterr().out)
    assert output["failed_gate"] == "fresh_run_root"
    assert "fresh" in output["error"]


@pytest.mark.parametrize(
    ("reason", "gate"),
    [
        ("runtime case metadata drift", "scope_validation"),
        ("secure execution backend unavailable: test blocker", "secure_backend"),
    ],
)
def test_campaign_hosted_readiness_reports_preflight_gate(
    tmp_path: Path, capsys, monkeypatch, reason: str, gate: str
) -> None:
    baseline = synthetic_pilot_artifacts().write_tree(tmp_path / "baseline")

    class BlockedRunner:
        def __init__(self, contract, cases_root) -> None:
            del contract, cases_root

        def validate_pilot_scope(self):
            if gate != "scope_validation":
                return {"runtime": 4, "control_matrix": 30, "held_out": 6}
            raise CampaignValidationError(reason)

        def validate_secure_backend(self):
            if gate == "secure_backend":
                raise CampaignValidationError(reason)

    monkeypatch.setattr(cli_module, "CampaignRunner", BlockedRunner)
    assert main(_hosted_readiness_argv(tmp_path, baseline)) == 1
    output = json.loads(capsys.readouterr().out)
    assert output["failed_gate"] == gate
    assert reason in output["error"]


def test_campaign_hosted_readiness_config_check_is_offline_and_redacted(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    baseline = synthetic_pilot_artifacts().write_tree(tmp_path / "baseline")
    secret = "readiness-secret-must-not-leak"
    generate_calls = 0

    class NoNetworkProvider:
        def __init__(self, config, limits) -> None:
            self.config = config
            self.limits = limits
            self.name = config.provider
            self.model = config.model

        def generate(self, request):
            nonlocal generate_calls
            del request
            generate_calls += 1

    monkeypatch.setattr(
        "brep2code.harness.campaign.secure_backend_status",
        lambda: (True, "secure execution backend ready"),
    )
    monkeypatch.setattr(cli_module, "OpenAICompatibleProvider", NoNetworkProvider)
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: OpenAICompatibleConfig(
            provider="deepseek",
            base_url="https://api.deepseek.com/v1/chat/completions",
            api_key=secret,
            model="deepseek-v4-pro",
        ),
    )
    argv = _hosted_readiness_argv(tmp_path, baseline)
    argv.extend(["--check-provider-config", "--authorize-hosted"])

    assert main(argv) == 0
    raw = capsys.readouterr().out
    output = json.loads(raw)
    assert output["endpoint_host"] == "api.deepseek.com"
    assert output["provider"] == "deepseek"
    assert output["model"] == "deepseek-v4-pro"
    assert output["thinking_mode"] == "disabled"
    assert output["gates"]["provider_configuration"] == "passed"
    assert generate_calls == 0
    assert secret not in raw
    assert "/v1/chat/completions" not in raw
    assert not (tmp_path / "pilot").exists()


@pytest.mark.parametrize(
    ("mutate", "error"),
    [
        (lambda argv: None, "authorize-hosted"),
        (lambda argv: argv.__setitem__(argv.index("--model") + 1, "wrong"), "--model"),
        (
            lambda argv: argv.__setitem__(argv.index("--max-total-tokens") + 1, "1"),
            "--max-total-tokens",
        ),
    ],
)
def test_campaign_hosted_readiness_config_check_rejects_authorization_and_drift(
    tmp_path: Path, capsys, monkeypatch, mutate, error: str
) -> None:
    baseline = synthetic_pilot_artifacts().write_tree(tmp_path / "baseline")
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: (_ for _ in ()).throw(
            AssertionError("invalid arguments must fail before configuration")
        ),
    )
    argv = _hosted_readiness_argv(tmp_path, baseline)
    argv.append("--check-provider-config")
    if error != "authorize-hosted":
        argv.append("--authorize-hosted")
    mutate(argv)

    assert main(argv) == 1
    output = json.loads(capsys.readouterr().out)
    assert output["failed_gate"] == "campaign_contract"
    assert error in output["error"]


@pytest.mark.parametrize(
    ("config_factory", "error"),
    [
        (
            lambda: (_ for _ in ()).throw(
                ProviderConfigurationError("provider and API key are required")
            ),
            "required",
        ),
        (
            lambda: OpenAICompatibleConfig(
                provider="deepseek",
                base_url="http://api.deepseek.com/v1",
                api_key="hidden-readiness-secret",
                model="deepseek-v4-pro",
            ),
            "HTTPS",
        ),
        (
            lambda: OpenAICompatibleConfig(
                provider="deepseek",
                base_url="https://api.deepseek.com/v1",
                api_key="hidden-readiness-secret",
                model="wrong",
            ),
            "identity",
        ),
        (
            lambda: (_ for _ in ()).throw(
                ProviderConfigurationError("invalid key hidden-readiness-secret")
            ),
            "configuration is invalid",
        ),
    ],
)
def test_campaign_hosted_readiness_rejects_provider_configuration_safely(
    tmp_path: Path, capsys, monkeypatch, config_factory, error: str
) -> None:
    baseline = synthetic_pilot_artifacts().write_tree(tmp_path / "baseline")
    monkeypatch.setattr(
        "brep2code.harness.campaign.secure_backend_status",
        lambda: (True, "secure execution backend ready"),
    )
    monkeypatch.setattr(cli_module, "deepseek_config_from_env", lambda **kwargs: config_factory())
    argv = _hosted_readiness_argv(tmp_path, baseline)
    argv.extend(["--check-provider-config", "--authorize-hosted"])

    assert main(argv) == 1
    raw = capsys.readouterr().out
    output = json.loads(raw)
    assert output["failed_gate"] == "provider_configuration"
    assert error in output["error"]
    assert "hidden-readiness-secret" not in raw


def test_campaign_hosted_pilot_config_check_is_network_free_and_redacted(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    events: list[str] = []

    class ReadyRunner:
        def __init__(self, contract, cases_root) -> None:
            del contract, cases_root

        def preflight_pilot(self, root):
            assert root == tmp_path / "pilot"
            events.append("preflight")
            return {"runtime": 4, "control_matrix": 30, "held_out": 6}

    class NoNetworkProvider:
        def __init__(self, config, limits) -> None:
            events.append("provider")
            self.config = config
            self.limits = limits
            self.name = config.provider
            self.model = config.model

        def generate(self, request):
            del request
            raise AssertionError("configuration check must not make a network request")

    secret = "never-print-this-secret"
    monkeypatch.setattr(cli_module, "CampaignRunner", ReadyRunner)
    monkeypatch.setattr(cli_module, "OpenAICompatibleProvider", NoNetworkProvider)
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: (
            events.append("config"),
            OpenAICompatibleConfig(
                provider="deepseek",
                base_url="https://api.deepseek.com/v1",
                api_key=secret,
                model="deepseek-v4-pro",
            ),
        )[1],
    )

    assert main(_hosted_pilot_config_check_argv(tmp_path)) == 0
    raw_output = capsys.readouterr().out
    output = json.loads(raw_output)
    assert events == ["preflight", "config", "provider"]
    assert output["status"] == "ready"
    assert output["endpoint_host"] == "api.deepseek.com"
    assert output["cohort_counts"] == {"runtime": 4, "control_matrix": 30, "held_out": 6}
    assert secret not in raw_output
    assert not (tmp_path / "pilot").exists()


@pytest.mark.parametrize(
    ("config_factory", "error"),
    [
        (
            lambda: (_ for _ in ()).throw(
                ProviderConfigurationError("provider and API key are required")
            ),
            "required",
        ),
        (
            lambda: OpenAICompatibleConfig(
                provider="deepseek",
                base_url="http://api.deepseek.com",
                api_key="hidden-secret",
                model="deepseek-v4-pro",
            ),
            "HTTPS",
        ),
        (
            lambda: OpenAICompatibleConfig(
                provider="deepseek",
                base_url="https://api.deepseek.com",
                api_key="hidden-secret",
                model="wrong-model",
            ),
            "identity",
        ),
    ],
)
def test_campaign_hosted_pilot_config_check_rejects_invalid_configuration_without_secrets(
    tmp_path: Path, capsys, monkeypatch, config_factory, error: str
) -> None:
    class ReadyRunner:
        def __init__(self, contract, cases_root) -> None:
            del contract, cases_root

        def preflight_pilot(self, root):
            del root
            return {"runtime": 4, "control_matrix": 30, "held_out": 6}

    monkeypatch.setattr(cli_module, "CampaignRunner", ReadyRunner)
    monkeypatch.setattr(cli_module, "deepseek_config_from_env", lambda **kwargs: config_factory())

    assert main(_hosted_pilot_config_check_argv(tmp_path)) == 1
    raw_output = capsys.readouterr().out
    assert error in json.loads(raw_output)["error"]
    assert "hidden-secret" not in raw_output
    assert not (tmp_path / "pilot").exists()


def test_campaign_hosted_pilot_config_check_rejects_limit_drift_before_configuration(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: (_ for _ in ()).throw(
            AssertionError("configuration must not be read for limit drift")
        ),
    )
    argv = _hosted_pilot_config_check_argv(tmp_path)
    argv[argv.index("--max-total-tokens") + 1] = "1"

    assert main(argv) == 1
    assert "--max-total-tokens" in json.loads(capsys.readouterr().out)["error"]
    assert not (tmp_path / "pilot").exists()


def test_campaign_hosted_pilot_binds_provider_only_after_preflight(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    events: list[str] = []
    run_root = tmp_path / "pilot"

    class StubConfig:
        provider = "deepseek"
        model = "deepseek-v4-pro"

    class StubHostedProvider:
        def __init__(self, config, limits) -> None:
            events.append("provider")
            self.name = config.provider
            self.model = config.model
            self.limits = limits

        def generate(self, request):
            del request
            raise AssertionError("CLI binding test must not make a hosted request")

    class StubCampaignRunner:
        def __init__(self, contract, cases_root) -> None:
            del contract, cases_root

        def preflight_pilot(self, root):
            assert root == run_root
            events.append("preflight")
            return {"runtime": 4, "control_matrix": 30, "held_out": 6}

        def run_hosted_pilot(self, provider, root, *, preflighted):
            assert provider.name == "deepseek"
            assert root == run_root
            assert preflighted is True
            events.append("run")
            root.mkdir(parents=True)
            result_path = root / "result.json"
            result_path.write_text(
                json.dumps(
                    {
                        "provider_accounting": {
                            "http_attempts": 43,
                            "total_tokens": 100,
                            "cost_usd": 0.02,
                        }
                    }
                ),
                encoding="utf-8",
            )
            return CampaignRunResult("succeeded", "completed", 43, result_path)

    monkeypatch.setattr(cli_module, "CampaignRunner", StubCampaignRunner)
    monkeypatch.setattr(cli_module, "OpenAICompatibleProvider", StubHostedProvider)
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: (events.append("config"), StubConfig())[1],
    )

    assert main(_hosted_pilot_argv(tmp_path)) == 0
    output = json.loads(capsys.readouterr().out)
    assert events == ["preflight", "config", "provider", "run"]
    assert output["status"] == "succeeded"
    assert output["provider_accounting"]["http_attempts"] == 43
    assert output["result_path"] == str(run_root / "result.json")


def test_campaign_hosted_pilot_refuses_before_configuration_without_authorization(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: (_ for _ in ()).throw(
            AssertionError("configuration must not be read before authorization")
        ),
    )
    argv = _hosted_pilot_argv(tmp_path)
    argv.remove("--authorize-hosted")

    assert main(argv) == 2
    assert "authorize-hosted" in json.loads(capsys.readouterr().out)["error"]
    assert not (tmp_path / "pilot").exists()


def test_campaign_hosted_pilot_refuses_secure_blocker_before_configuration(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    class BlockedRunner:
        def __init__(self, contract, cases_root) -> None:
            del contract, cases_root

        def preflight_pilot(self, root):
            del root
            raise CampaignValidationError("secure execution backend unavailable: test blocker")

    monkeypatch.setattr(cli_module, "CampaignRunner", BlockedRunner)
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: (_ for _ in ()).throw(
            AssertionError("configuration must not be read after failed preflight")
        ),
    )

    assert main(_hosted_pilot_argv(tmp_path)) == 2
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "configuration_error"
    assert "secure execution backend unavailable" in output["error"]
    assert not (tmp_path / "pilot").exists()


def test_campaign_hosted_pilot_rejects_configured_provider_identity(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    class StubConfig:
        provider = "deepseek"
        model = "wrong-model"

    class StubProvider:
        def __init__(self, config, limits) -> None:
            self.name = config.provider
            self.model = config.model
            self.limits = limits

    class ReadyRunner:
        def __init__(self, contract, cases_root) -> None:
            del contract, cases_root

        def preflight_pilot(self, root):
            del root
            return {"runtime": 4, "control_matrix": 30, "held_out": 6}

    monkeypatch.setattr(cli_module, "CampaignRunner", ReadyRunner)
    monkeypatch.setattr(cli_module, "OpenAICompatibleProvider", StubProvider)
    monkeypatch.setattr(cli_module, "deepseek_config_from_env", lambda **kwargs: StubConfig())

    assert main(_hosted_pilot_argv(tmp_path)) == 2
    assert "identity" in json.loads(capsys.readouterr().out)["error"]
    assert not (tmp_path / "pilot").exists()


def test_campaign_hosted_pilot_rejects_existing_root_before_configuration(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    run_root = tmp_path / "pilot"
    run_root.mkdir()
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: (_ for _ in ()).throw(
            AssertionError("configuration must not be read for an existing run root")
        ),
    )

    assert main(_hosted_pilot_argv(tmp_path)) == 2
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "configuration_error"
    assert "fresh" in output["error"]


def test_campaign_pilot_preflight_is_provider_free_and_reports_cohort_routes(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    class StubCampaignRunner:
        def __init__(self, contract, cases_root) -> None:
            del contract, cases_root

        def preflight_pilot(self, run_root):
            assert run_root == tmp_path / "pilot"
            return {"runtime": 4, "control_matrix": 30, "held_out": 6}

    def reject_provider(*args, **kwargs):
        del args, kwargs
        raise AssertionError("pilot preflight must not construct a provider")

    monkeypatch.setattr(cli_module, "CampaignRunner", StubCampaignRunner)
    monkeypatch.setattr(cli_module, "FakeProvider", reject_provider)
    monkeypatch.setattr(cli_module, "OpenAICompatibleProvider", reject_provider)
    monkeypatch.setattr(cli_module, "deepseek_config_from_env", reject_provider)

    assert main(_pilot_preflight_argv(tmp_path)) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "ready"
    assert payload["cohorts"] == {
        "runtime": {"provider": "deepseek", "case_count": 4},
        "control_matrix": {"provider": "fake", "case_count": 30},
        "held_out": {"provider": "fake", "case_count": 6},
    }
    assert not (tmp_path / "pilot").exists()


@pytest.mark.parametrize(
    ("option", "value", "error"),
    [
        ("--provider", "fake", "--provider"),
        ("--model", "wrong-model", "--model"),
        ("--max-requests", "7", "--max-requests"),
        ("--max-total-tokens", "1", "--max-total-tokens"),
        ("--max-cost-usd", "0.3", "--max-cost-usd"),
    ],
)
def test_campaign_pilot_preflight_rejects_contract_policy_drift(
    tmp_path: Path, capsys, monkeypatch, option: str, value: str, error: str
) -> None:
    class RejectRunner:
        def __init__(self, *args, **kwargs) -> None:
            del args, kwargs
            raise AssertionError("invalid policy must fail before runner construction")

    monkeypatch.setattr(cli_module, "CampaignRunner", RejectRunner)
    argv = _pilot_preflight_argv(tmp_path)
    argv[argv.index(option) + 1] = value

    assert main(argv) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "not_ready"
    assert error in payload["error"]


def test_campaign_pilot_preflight_requires_hosted_authorization(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    class RejectRunner:
        def __init__(self, *args, **kwargs) -> None:
            del args, kwargs
            raise AssertionError("missing authorization must fail before runner construction")

    monkeypatch.setattr(cli_module, "CampaignRunner", RejectRunner)
    argv = _pilot_preflight_argv(tmp_path)
    argv.remove("--authorize-hosted")

    assert main(argv) == 1
    assert "authorize-hosted" in json.loads(capsys.readouterr().out)["error"]


def test_campaign_pilot_preflight_reports_secure_backend_blocker(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    monkeypatch.setattr(
        "brep2code.harness.campaign.secure_backend_status",
        lambda: (False, "secure execution backend unavailable: test blocker"),
    )

    assert main(_pilot_preflight_argv(tmp_path)) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "not_ready"
    assert payload["error"] == "secure execution backend unavailable: test blocker"
    assert not (tmp_path / "pilot").exists()


@pytest.mark.secure
def test_campaign_controls_run_complete_dossier_matrix(tmp_path: Path, capsys) -> None:
    run_root = tmp_path / "controls"
    exit_code = main(
        [
            "campaign",
            "controls",
            "--contract",
            "cases/campaigns/g1-mechanism-coverage.json",
            "--run-root",
            str(run_root),
        ]
    )

    assert exit_code == 0, capsys.readouterr().out
    summary = json.loads(capsys.readouterr().out)
    assert summary["provider_requests"] == 30
    payload = json.loads((run_root / "result.json").read_text(encoding="utf-8"))
    assert payload["status"] == "succeeded"
    assert payload["stop_reason"] == "control_matrix_passed"
    assert len(payload["cases"]) == 30
    assert all(item["matches_expectation"] for item in payload["cases"])
    assert payload["provider_accounting"] == {
        "http_attempts": 30,
        "total_tokens": 0,
        "cost_usd": 0.0,
    }
    assert {
        (item["mechanism"], item["capability_level"], item["control_variant"])
        for item in payload["control_report"]
    } == {
        ("primitive", "L0", "nominal"),
        ("primitive", "L0", "parameter_variation"),
        ("primitive", "L0", "failure_sensitive"),
        ("analytic_surface", "L0", "nominal"),
        ("analytic_surface", "L0", "parameter_variation"),
        ("analytic_surface", "L0", "failure_sensitive"),
        ("boolean_cut", "L1", "nominal"),
        ("boolean_cut", "L1", "parameter_variation"),
        ("boolean_cut", "L1", "failure_sensitive"),
        ("fillet", "L2", "nominal"),
        ("fillet", "L2", "parameter_variation"),
        ("fillet", "L2", "failure_sensitive"),
    }


@pytest.mark.secure
def test_campaign_held_out_runs_isolated_fake_generalization_cohort(tmp_path: Path, capsys) -> None:
    run_root = tmp_path / "held-out"
    exit_code = main(
        [
            "campaign",
            "held-out",
            "--contract",
            "cases/campaigns/g1-mechanism-coverage.json",
            "--run-root",
            str(run_root),
        ]
    )

    assert exit_code == 0, capsys.readouterr().out
    summary = json.loads(capsys.readouterr().out)
    assert summary["provider_requests"] == 6
    payload = json.loads((run_root / "result.json").read_text(encoding="utf-8"))
    assert payload["artifact"] == "held_out_generalization"
    assert payload["status"] == "succeeded"
    assert payload["stop_reason"] == "held_out_passed"
    assert len(payload["cases"]) == 6
    assert all(item["matches_expectation"] for item in payload["cases"])
    assert payload["provider_accounting"] == {
        "http_attempts": 6,
        "total_tokens": 0,
        "cost_usd": 0.0,
    }


def test_run_binds_campaign_projection_without_leaking_it_to_provider(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    observed = {}

    class StubRunner:
        def __init__(self, provider) -> None:
            del provider

        def run(self, case, run_root, **kwargs):
            observed["case_id"] = case.case.case_id
            observed["run_root"] = run_root
            observed["campaign"] = kwargs["campaign"]
            return HarnessResult("succeeded", "passed", 1, run_root / "result.json")

    monkeypatch.setattr(cli_module, "RepairLoopRunner", StubRunner)
    assert (
        main(
            [
                "run",
                "--case-id",
                "box",
                "--run-root",
                str(tmp_path / "run"),
                "--campaign-contract",
                "cases/campaigns/g1-mechanism-coverage.json",
                "--fake-script",
                "tests/fixtures/fixed_box.py",
                "--fake-script",
                "tests/fixtures/fixed_box.py",
                "--max-rounds",
                "2",
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert observed["case_id"] == "box"
    assert observed["campaign"]["campaign_id"] == "g1-mechanism-coverage"
    assert observed["campaign"]["case"]["mechanism"] == "primitive"


def test_active_run_binds_fake_actions_and_typed_budgets(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    action_path = tmp_path / "action.json"
    action_path.write_text(
        json.dumps({"action": "finish", "finish": {"reason": "test"}}),
        encoding="utf-8",
    )
    observed = {}

    class StubActiveRunner:
        def __init__(self, provider) -> None:
            observed["action"] = provider.choose_action(
                ActionRequest("box", 0, {"case_id": "box"})
            ).action

        def run(self, case, run_root, *, budgets, timeout_seconds, retrieval_policy, backend):
            observed["case_id"] = case.case.case_id
            observed["run_root"] = run_root
            observed["budgets"] = budgets
            observed["timeout_seconds"] = timeout_seconds
            observed["retrieval_policy"] = retrieval_policy
            observed["backend"] = backend
            return ActiveHarnessResult(
                ActiveState.SUCCEEDED,
                "passed",
                {"model_requests": 1},
                (),
            )

    monkeypatch.setattr(cli_module, "ActiveHarnessRunner", StubActiveRunner)
    exit_code = main(
        [
            "active-run",
            "--case-id",
            "box",
            "--run-root",
            str(tmp_path / "run"),
            "--fake-action",
            str(action_path),
            "--max-model-requests",
            "1",
            "--max-probes",
            "1",
            "--max-retrievals",
            "1",
            "--max-script-submissions",
            "1",
            "--max-executions",
            "1",
            "--max-repairs",
            "0",
            "--max-total-tokens",
            "0",
            "--max-cost-usd",
            "0",
            "--timeout",
            "7",
        ]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "succeeded"
    assert observed["action"]["action"] == "finish"
    assert observed["case_id"] == "box"
    assert observed["budgets"].model_requests == 1
    assert observed["budgets"].repairs == 0
    assert observed["timeout_seconds"] == 7


def test_active_preflight_is_local_and_creates_no_artifacts(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    action_path = tmp_path / "action.json"
    action_path.write_text(
        json.dumps({"action": "finish", "finish": {"reason": "test"}}),
        encoding="utf-8",
    )

    def reject_runner(*args, **kwargs):
        raise AssertionError("active preflight must not construct a runner")

    monkeypatch.setattr(cli_module, "ActiveHarnessRunner", reject_runner)
    run_root = tmp_path / "active"
    exit_code = main(
        [
            "active-preflight",
            "--case-id",
            "box",
            "--run-root",
            str(run_root),
            "--fake-action",
            str(action_path),
            "--max-model-requests",
            "1",
            "--max-probes",
            "0",
            "--max-retrievals",
            "0",
            "--max-script-submissions",
            "0",
            "--max-executions",
            "0",
            "--max-repairs",
            "0",
            "--max-total-tokens",
            "0",
            "--max-cost-usd",
            "0",
        ]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "ready"
    assert payload["network_requests"] == 0
    assert payload["artifacts_created"] is False
    assert not run_root.exists()


def test_active_preflight_accepts_held_out_case_for_fake_cohort(tmp_path: Path, capsys) -> None:
    action_path = tmp_path / "action.json"
    action_path.write_text(
        json.dumps({"action": "finish", "finish": {"reason": "expected control"}}),
        encoding="utf-8",
    )

    exit_code = main(
        [
            "active-preflight",
            "--case-id",
            "filleted_box_held_out",
            "--run-root",
            str(tmp_path / "active"),
            "--fake-action",
            str(action_path),
            "--max-model-requests",
            "1",
            "--max-probes",
            "0",
            "--max-retrievals",
            "0",
            "--max-script-submissions",
            "0",
            "--max-executions",
            "0",
            "--max-repairs",
            "0",
            "--max-total-tokens",
            "0",
            "--max-cost-usd",
            "0",
        ]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "ready"
    assert payload["case_id"] == "filleted_box_held_out"
    assert payload["provider"] == "fake"


def test_active_preflight_rejects_action_sequence_over_tool_budget(tmp_path: Path, capsys) -> None:
    action_path = tmp_path / "action.json"
    action_path.write_text(
        json.dumps({"action": "probe", "probe": {"tool": "edge_candidates", "arguments": {}}}),
        encoding="utf-8",
    )
    exit_code = main(
        [
            "active-preflight",
            "--case-id",
            "box",
            "--run-root",
            str(tmp_path / "active"),
            "--fake-action",
            str(action_path),
            "--max-model-requests",
            "1",
            "--max-probes",
            "0",
            "--max-retrievals",
            "0",
            "--max-script-submissions",
            "0",
            "--max-executions",
            "0",
            "--max-repairs",
            "0",
            "--max-total-tokens",
            "0",
            "--max-cost-usd",
            "0",
        ]
    )

    assert exit_code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "not_ready"
    assert "exceeds probes budget" in payload["error"]


def test_active_validate_reads_saved_result_without_running_provider(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    result_root = tmp_path / "active"
    result_root.mkdir()
    result_path = result_root / "result.json"
    result_path.write_text(
        json.dumps(
            {
                "case_id": "box",
                "state": "succeeded",
                "stop_reason": "passed",
            }
        ),
        encoding="utf-8",
    )
    observed = {}

    def validator(payload, case, root):
        observed["payload"] = payload
        observed["case_id"] = case.case.case_id
        observed["root"] = root

    monkeypatch.setattr(cli_module, "validate_active_result", validator)
    monkeypatch.setattr(
        cli_module,
        "FakeActionProvider",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("active validation must not construct a provider")
        ),
    )

    assert main(["active-validate", "--result", str(result_path)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "valid"
    assert observed["case_id"] == "box"
    assert observed["root"] == result_root


def test_active_continue_binds_only_remaining_fake_actions(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    run_root = tmp_path / "active"
    run_root.mkdir()
    (run_root / "result.json").write_text(
        json.dumps(
            {
                "case_id": "box",
                "usage": {
                    "model_requests": 1,
                    "probes": 0,
                    "retrievals": 0,
                    "script_submissions": 0,
                    "executions": 0,
                    "repairs": 0,
                    "tokens": 0,
                    "cost_usd": 0.0,
                },
            }
        ),
        encoding="utf-8",
    )
    actions = []
    for index in range(2):
        path = tmp_path / f"action-{index}.json"
        path.write_text(
            json.dumps({"action": "finish", "finish": {"reason": str(index)}}),
            encoding="utf-8",
        )
        actions.append(path)
    observed = {}

    class StubRunner:
        def __init__(self, provider):
            observed["first_action"] = provider.choose_action(
                ActionRequest("box", 1, {"case_id": "box"})
            ).action

        def continue_run(self, case, root, *, budgets, timeout_seconds, retrieval_policy, backend):
            observed["case_id"] = case.case.case_id
            observed["root"] = root
            observed["budgets"] = budgets
            observed["timeout"] = timeout_seconds
            observed["retrieval_policy"] = retrieval_policy
            observed["backend"] = backend
            return ActiveHarnessResult(
                ActiveState.SUCCEEDED,
                "passed",
                {"model_requests": 2},
                (),
            )

    monkeypatch.setattr(cli_module, "validate_active_result", lambda *args: None)
    monkeypatch.setattr(cli_module, "ActiveHarnessRunner", StubRunner)
    argv = [
        "active-continue",
        "--case-id",
        "box",
        "--run-root",
        str(run_root),
        "--max-model-requests",
        "3",
        "--max-probes",
        "0",
        "--max-retrievals",
        "0",
        "--max-script-submissions",
        "0",
        "--max-executions",
        "0",
        "--max-repairs",
        "0",
        "--max-total-tokens",
        "0",
        "--max-cost-usd",
        "0",
        "--timeout",
        "9",
    ]
    for path in actions:
        argv.extend(["--fake-action", str(path)])

    assert main(argv) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "succeeded"
    assert observed["first_action"]["finish"]["reason"] == "0"
    assert observed["case_id"] == "box"
    assert observed["budgets"].model_requests == 3
    assert observed["timeout"] == 9


def _active_hosted_argv(tmp_path: Path, command: str) -> list[str]:
    return [
        command,
        "--case-id",
        "box",
        "--run-root",
        str(tmp_path / "active-hosted"),
        "--provider",
        "deepseek",
        "--model",
        "deepseek-v4-pro",
        "--thinking-mode",
        "disabled",
        "--authorize-hosted",
        "--authorize-observations",
        "--authorize-tool-results",
        "--authorize-revision-source",
        "--authorize-feedback",
        "--max-model-requests",
        "2",
        "--max-probes",
        "1",
        "--max-retrievals",
        "1",
        "--max-script-submissions",
        "2",
        "--max-executions",
        "2",
        "--max-repairs",
        "1",
        "--session-max-total-tokens",
        "100",
        "--session-max-cost-usd",
        "1",
        "--build-timeout",
        "5",
        "--provider-max-requests",
        "2",
        "--provider-timeout",
        "30",
        "--provider-max-retries",
        "0",
        "--provider-max-output-tokens",
        "50",
        "--provider-max-total-tokens",
        "200",
        "--provider-max-cost-usd",
        "2",
        "--input-cost-per-million",
        "1",
        "--output-cost-per-million",
        "2",
    ]


def _write_fake_active_baseline(tmp_path: Path) -> Path:
    root = tmp_path / "fake-baseline"
    root.mkdir()
    result = root / "result.json"
    result.write_text(
        json.dumps(
            {
                "schema_version": 3,
                "mode": "active",
                "case_id": "box",
                "provider": "fake",
                "model": "fake-action-queue-v1",
                "budgets": {
                    "model_requests": 1,
                    "probes": 0,
                    "retrievals": 0,
                    "script_submissions": 0,
                    "executions": 0,
                    "repairs": 0,
                    "tokens": 0,
                    "cost_usd": 0.0,
                },
                "timeout_seconds": 5,
                "checkpoint_index": 2,
                "terminal": True,
                "continuation_policy": {
                    "eligible": False,
                    "implemented": True,
                    "requirements": [
                        "same_case",
                        "same_budgets",
                        "remaining_model_requests",
                        "existing_revision_root",
                    ],
                },
                "state": "succeeded",
                "stop_reason": "passed",
                "usage": {
                    "model_requests": 1,
                    "probes": 0,
                    "retrievals": 0,
                    "script_submissions": 0,
                    "executions": 0,
                    "repairs": 0,
                    "tokens": 0,
                    "cost_usd": 0.0,
                },
                "trace": [{"action": "finish", "passed": True, "result": {"reason": "done"}}],
            }
        ),
        encoding="utf-8",
    )
    return result


def _write_active_pilot_case_result(
    root: Path, case_id: str, *, passed: bool, exercise_tools: bool = False
) -> Path:
    root.mkdir(parents=True)
    model_requests = 3 if passed and exercise_tools else 1
    probes = int(passed and exercise_tools)
    retrievals = int(passed and exercise_tools)
    submissions = int(passed)
    executions = int(passed)
    trace = []
    if exercise_tools:
        trace.extend(
            [
                {"action": "probe", "result": {"edges": []}},
                {"action": "retrieve", "result": {"symbol": "TopoDS.Edge_s"}},
            ]
        )
    trace.append(
        {
            "action": "submit" if passed else "finish",
            "passed": True if passed else None,
            "request": {"reason": "deterministic cohort terminal"},
        }
    )
    if passed:
        revision = root / "revision-000"
        revision.mkdir()
        (revision / "build.py").write_text("candidate = True\n", encoding="utf-8")
        (revision / "result.json").write_text(
            json.dumps(
                {
                    "revision_id": "revision-000",
                    "workspace": "revision-000",
                    "status": "succeeded",
                    "execution": {
                        "output_step": "output.step",
                        "sandboxed": True,
                    },
                }
            ),
            encoding="utf-8",
        )
    result = root / "result.json"
    result.write_text(
        json.dumps(
            {
                "schema_version": 3,
                "mode": "active",
                "case_id": case_id,
                "provider": "fake",
                "model": "fake-action-queue-v1",
                "budgets": {
                    "model_requests": model_requests,
                    "probes": probes,
                    "retrievals": retrievals,
                    "script_submissions": submissions,
                    "executions": executions,
                    "repairs": 0,
                    "tokens": 0,
                    "cost_usd": 0.0,
                },
                "timeout_seconds": 5,
                "checkpoint_index": 2,
                "terminal": True,
                "continuation_policy": {
                    "eligible": False,
                    "implemented": True,
                    "requirements": [
                        "same_case",
                        "same_budgets",
                        "remaining_model_requests",
                        "existing_revision_root",
                    ],
                },
                "state": "succeeded" if passed else "failed",
                "stop_reason": "passed" if passed else "finish_without_verifier",
                "usage": {
                    "model_requests": model_requests,
                    "probes": probes,
                    "retrievals": retrievals,
                    "script_submissions": submissions,
                    "executions": executions,
                    "repairs": 0,
                    "tokens": 0,
                    "cost_usd": 0.0,
                },
                "trace": trace,
            }
        ),
        encoding="utf-8",
    )
    return result


def test_active_pilot_report_builds_fake_l2_decision_gate(tmp_path: Path, capsys) -> None:
    fixed = synthetic_pilot_artifacts()
    fixed_result = fixed.write_tree(tmp_path / "fixed-pilot")
    cases = {
        "nominal": ("filleted_box", True),
        "parameter_variation": ("filleted_box", True),
        "failure_sensitive": ("filleted_box", False),
        "controls": ("box", True),
        "held_out": ("filleted_box_held_out", True),
    }
    results = {
        label: _write_active_pilot_case_result(
            tmp_path / "active-results" / label,
            case_id,
            passed=passed,
            exercise_tools=label == "nominal",
        )
        for label, (case_id, passed) in cases.items()
    }
    output = tmp_path / "active-pilot" / "result.json"
    argv = [
        "active-pilot-report",
        "--contract",
        "cases/campaigns/g1-mechanism-coverage.json",
        "--fixed-pilot-result",
        str(fixed_result),
        "--output",
        str(output),
    ]
    for label, path in results.items():
        argv.extend([f"--{label.replace('_', '-')}-result", str(path)])

    assert main(argv) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "succeeded"
    assert payload["eligible_to_request_single_pilot_authorization"] is True
    assert payload["authorization_granted"] is False
    assert payload["network_requests"] == 0
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["cohort_order"] == list(cases)
    assert report["cohorts"][2]["terminal_classification"] == "harness"
    assert report["comparison"]["active_loop"]["model_requests"] == 7


def _active_hosted_readiness_argv(tmp_path: Path, baseline: Path) -> list[str]:
    argv = _active_hosted_argv(tmp_path, "active-hosted-readiness")
    argv.extend(["--baseline-result", str(baseline)])
    return argv


def _active_hosted_run_argv(tmp_path: Path, baseline: Path, stub_response: Path) -> list[str]:
    argv = _active_hosted_argv(tmp_path, "active-hosted-run")
    argv.extend(
        [
            "--baseline-result",
            str(baseline),
            "--http-stub-response",
            str(stub_response),
        ]
    )
    return argv


def _active_hosted_live_run_argv(tmp_path: Path, baseline: Path) -> list[str]:
    argv = _active_hosted_argv(tmp_path, "active-hosted-live-run")
    argv.extend(["--baseline-result", str(baseline)])
    return argv


def _write_hosted_active_checkpoint(tmp_path: Path) -> Path:
    root = tmp_path / "active-hosted"
    root.mkdir()
    result = root / "result.json"
    result.write_text(
        json.dumps(
            {
                "schema_version": 4,
                "mode": "active",
                "case_id": "box",
                "provider": "deepseek",
                "model": "deepseek-v4-pro",
                "budgets": {
                    "model_requests": 2,
                    "probes": 1,
                    "retrievals": 1,
                    "script_submissions": 2,
                    "executions": 2,
                    "repairs": 1,
                    "tokens": 100,
                    "cost_usd": 1.0,
                },
                "timeout_seconds": 5,
                "checkpoint_index": 3,
                "terminal": False,
                "continuation_policy": {
                    "eligible": True,
                    "implemented": True,
                    "requirements": [
                        "same_case",
                        "same_budgets",
                        "remaining_model_requests",
                        "existing_revision_root",
                    ],
                },
                "state": "synthesizing",
                "stop_reason": None,
                "usage": {
                    "model_requests": 1,
                    "probes": 0,
                    "retrievals": 0,
                    "script_submissions": 0,
                    "executions": 0,
                    "repairs": 0,
                    "tokens": 15,
                    "cost_usd": 0.00002,
                },
                "trace": [],
                "provider_accounting": {
                    "http_attempts": 1,
                    "in_flight_requests": 1,
                    "tokens": {"prompt": 10, "completion": 5, "total": 15},
                    "cost_usd": 0.00002,
                    "pricing": {
                        "input_cost_per_million": 1.0,
                        "output_cost_per_million": 2.0,
                    },
                    "ceilings": {
                        "max_requests": 2,
                        "timeout_seconds": 30.0,
                        "max_retries": 0,
                        "max_output_tokens": 50,
                        "max_total_tokens": 200,
                        "max_cost_usd": 2.0,
                    },
                },
            }
        ),
        encoding="utf-8",
    )
    return result


def _active_hosted_continue_argv(
    tmp_path: Path, baseline: Path, checkpoint: Path, stub_response: Path
) -> list[str]:
    argv = _active_hosted_argv(tmp_path, "active-hosted-continue")
    argv.extend(
        [
            "--baseline-result",
            str(baseline),
            "--continuation-result",
            str(checkpoint),
            "--http-stub-response",
            str(stub_response),
        ]
    )
    return argv


def test_active_hosted_continue_restores_accounting_and_uses_remaining_turn(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    baseline = _write_fake_active_baseline(tmp_path)
    checkpoint = _write_hosted_active_checkpoint(tmp_path)
    stub_response = tmp_path / "continue-response.json"
    stub_response.write_text(
        json.dumps(
            {
                "model": "deepseek-v4-pro",
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {
                                    "action": "submit",
                                    "submit": {"script": "candidate = True"},
                                }
                            )
                        }
                    }
                ],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 5,
                    "total_tokens": 15,
                },
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        cli_module, "secure_backend_profile_status", lambda backend: (True, "ready", "7.9.3.1.1")
    )
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: OpenAICompatibleConfig(
            provider="deepseek",
            base_url="https://provider.invalid/v1",
            api_key="continuation-secret",
            model="deepseek-v4-pro",
            thinking_mode=kwargs["thinking_mode"],
        ),
    )

    def submission_factory(case, run_root, timeout_seconds):
        return ActiveSubmissionVerifier(
            case,
            run_root,
            timeout_seconds,
            executor=lambda workspace, **kwargs: ExecutionResult(
                exit_code=0,
                stdout="",
                stderr="",
                duration_seconds=0.01,
                output_step=workspace / "output.step",
                sandboxed=True,
                sandbox_backend="fake-secure",
            ),
            inspector=lambda path: GeometryMetrics(
                bbox_min=(0.0, 0.0, 0.0),
                bbox_max=(10.0, 20.0, 30.0),
                volume=6000.0,
                counts={"solid": 1, "shell": 1, "face": 6, "edge": 24},
            ),
            observer=lambda path: {},
        )

    monkeypatch.setattr(
        cli_module,
        "ActiveHarnessRunner",
        lambda provider: ActiveHarnessRunner(provider, submission_factory=submission_factory),
    )

    assert main(_active_hosted_continue_argv(tmp_path, baseline, checkpoint, stub_response)) == 0
    output = capsys.readouterr().out
    payload = json.loads(output)
    assert payload["status"] == "succeeded"
    assert payload["usage"]["model_requests"] == 2
    assert payload["usage"]["tokens"] == 30
    assert payload["provider_accounting"]["http_attempts"] == 2
    assert payload["provider_accounting"]["in_flight_requests"] == 0
    assert payload["remaining_model_requests"] == 0
    assert payload["fresh_authorization"] is True
    assert payload["network_requests"] == 0
    assert "continuation-secret" not in output
    artifact = json.loads(checkpoint.read_text(encoding="utf-8"))
    assert artifact["trace"][0] == {"action": "provider", "state": "interrupted"}


def test_active_hosted_continue_requires_new_authorization_and_stable_pricing(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    baseline = _write_fake_active_baseline(tmp_path)
    checkpoint = _write_hosted_active_checkpoint(tmp_path)
    original = checkpoint.read_bytes()
    stub_response = tmp_path / "unused-response.json"
    monkeypatch.setattr(
        cli_module, "secure_backend_profile_status", lambda backend: (True, "ready", "7.9.3.1.1")
    )
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: (_ for _ in ()).throw(
            AssertionError("rejected continuation must not read provider configuration")
        ),
    )
    argv = _active_hosted_continue_argv(tmp_path, baseline, checkpoint, stub_response)
    argv.remove("--authorize-feedback")

    assert main(argv) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["failed_gate"] == "outbound_projection_authorization"
    assert checkpoint.read_bytes() == original

    argv = _active_hosted_continue_argv(tmp_path, baseline, checkpoint, stub_response)
    argv[argv.index("--input-cost-per-million") + 1] = "1.5"
    assert main(argv) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["failed_gate"] == "budget_binding"
    assert "pricing drift" in payload["error"]
    assert checkpoint.read_bytes() == original


def test_active_hosted_run_executes_stubbed_vertical_slice(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    baseline = _write_fake_active_baseline(tmp_path)
    stub_response = tmp_path / "stub-response.json"
    stub_response.write_text(
        json.dumps(
            {
                "model": "deepseek-v4-pro",
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {
                                    "action": "submit",
                                    "submit": {"script": "candidate = True"},
                                }
                            )
                        }
                    }
                ],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 5,
                    "total_tokens": 15,
                },
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        cli_module, "secure_backend_profile_status", lambda backend: (True, "ready", "7.9.3.1.1")
    )
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: OpenAICompatibleConfig(
            provider="deepseek",
            base_url="https://provider.invalid/v1",
            api_key="stub-secret",
            model="deepseek-v4-pro",
            thinking_mode=kwargs["thinking_mode"],
        ),
    )

    def submission_factory(case, run_root, timeout_seconds):
        return ActiveSubmissionVerifier(
            case,
            run_root,
            timeout_seconds,
            executor=lambda workspace, **kwargs: ExecutionResult(
                exit_code=0,
                stdout="",
                stderr="",
                duration_seconds=0.01,
                output_step=workspace / "output.step",
                sandboxed=True,
                sandbox_backend="fake-secure",
            ),
            inspector=lambda path: GeometryMetrics(
                bbox_min=(0.0, 0.0, 0.0),
                bbox_max=(10.0, 20.0, 30.0),
                volume=6000.0,
                counts={"solid": 1, "shell": 1, "face": 6, "edge": 24},
            ),
            observer=lambda path: {},
        )

    monkeypatch.setattr(
        cli_module,
        "ActiveHarnessRunner",
        lambda provider: ActiveHarnessRunner(provider, submission_factory=submission_factory),
    )

    assert main(_active_hosted_run_argv(tmp_path, baseline, stub_response)) == 0
    output = capsys.readouterr().out
    payload = json.loads(output)
    assert payload["status"] == "succeeded"
    assert payload["network_requests"] == 0
    assert payload["http_stub"] is True
    assert payload["provider_accounting"]["http_attempts"] == 1
    assert payload["provider_accounting"]["tokens"]["total"] == 15
    assert "stub-secret" not in output
    artifact = json.loads((tmp_path / "active-hosted/result.json").read_text(encoding="utf-8"))
    assert artifact["schema_version"] == 7
    assert artifact["state"] == "succeeded"


def test_active_hosted_live_run_uses_bounded_https_and_redacted_exchange_artifacts(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    baseline = _write_fake_active_baseline(tmp_path)
    response = {
        "model": "deepseek-v4-pro",
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "action": "submit",
                            "submit": {"script": "candidate = True"},
                        }
                    )
                }
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }
    observed = {}

    def opener(http_request, *, timeout):
        observed["authorization"] = http_request.headers["Authorization"]
        observed["timeout"] = timeout
        return cli_module._StubHTTPResponse(response)

    real_provider = cli_module.OpenAICompatibleProvider

    def provider_factory(config, limits, **kwargs):
        return real_provider(config, limits, opener=opener, **kwargs)

    monkeypatch.setattr(
        cli_module, "secure_backend_profile_status", lambda backend: (True, "ready", "7.9.3.1.1")
    )
    monkeypatch.setattr(cli_module, "OpenAICompatibleProvider", provider_factory)
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: OpenAICompatibleConfig(
            provider="deepseek",
            base_url="https://provider.invalid/v1",
            api_key="live-secret",
            model="deepseek-v4-pro",
            thinking_mode=kwargs["thinking_mode"],
        ),
    )

    def submission_factory(case, run_root, timeout_seconds):
        return ActiveSubmissionVerifier(
            case,
            run_root,
            timeout_seconds,
            executor=lambda workspace, **kwargs: ExecutionResult(
                exit_code=0,
                stdout="",
                stderr="",
                duration_seconds=0.01,
                output_step=workspace / "output.step",
                sandboxed=True,
                sandbox_backend="fake-secure",
            ),
            inspector=lambda path: GeometryMetrics(
                bbox_min=(0.0, 0.0, 0.0),
                bbox_max=(10.0, 20.0, 30.0),
                volume=6000.0,
                counts={"solid": 1, "shell": 1, "face": 6, "edge": 24},
            ),
            observer=lambda path: {},
        )

    monkeypatch.setattr(
        cli_module,
        "ActiveHarnessRunner",
        lambda provider: ActiveHarnessRunner(provider, submission_factory=submission_factory),
    )

    assert main(_active_hosted_live_run_argv(tmp_path, baseline)) == 0
    output = capsys.readouterr().out
    payload = json.loads(output)
    assert payload["status"] == "succeeded"
    assert payload["network_requests"] == 1
    assert payload["http_stub"] is False
    assert payload["fresh_authorization"] is True
    assert observed == {"authorization": "Bearer live-secret", "timeout": 30.0}
    exchange_root = tmp_path / "active-hosted/provider-exchanges/attempt-001"
    request_artifact = (exchange_root / "request.json").read_text(encoding="utf-8")
    response_artifact = (exchange_root / "response.json").read_text(encoding="utf-8")
    assert "live-secret" not in request_artifact
    assert "Authorization" not in request_artifact
    assert "reasoning_content" not in response_artifact
    assert "candidate = True" in response_artifact


def test_active_hosted_run_stops_before_stub_when_readiness_fails(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    baseline = _write_fake_active_baseline(tmp_path)
    missing_stub = tmp_path / "missing-stub.json"
    monkeypatch.setattr(
        cli_module,
        "secure_backend_profile_status",
        lambda backend: (
            False,
            "secure execution backend unavailable: WSL2 probe failed",
            None,
        ),
    )
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: (_ for _ in ()).throw(
            AssertionError("provider configuration must follow secure readiness")
        ),
    )

    assert main(_active_hosted_run_argv(tmp_path, baseline, missing_stub)) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["failed_gate"] == "secure_backend"
    assert not (tmp_path / "active-hosted").exists()


def test_active_hosted_readiness_is_provider_free_and_read_only(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    baseline = _write_fake_active_baseline(tmp_path)
    monkeypatch.setattr(
        cli_module, "secure_backend_profile_status", lambda backend: (True, "ready", "7.9.3.1.1")
    )
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: (_ for _ in ()).throw(
            AssertionError("default readiness must not read provider configuration")
        ),
    )

    assert main(_active_hosted_readiness_argv(tmp_path, baseline)) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "ready"
    assert payload["gates"]["provider_configuration"] == "skipped"
    assert payload["provider_configuration_read"] is False
    assert payload["network_requests"] == 0
    assert payload["artifacts_created"] is False
    assert not (tmp_path / "active-hosted").exists()


def test_active_hosted_readiness_reports_gate_failures(tmp_path: Path, capsys, monkeypatch) -> None:
    baseline = _write_fake_active_baseline(tmp_path)
    monkeypatch.setattr(
        cli_module,
        "secure_backend_profile_status",
        lambda backend: (
            False,
            "secure execution backend unavailable: WSL2 probe failed",
            None,
        ),
    )

    assert main(_active_hosted_readiness_argv(tmp_path, baseline)) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["failed_gate"] == "secure_backend"
    assert payload["gates"]["saved_result_validation"] == "passed"
    assert payload["gates"]["provider_configuration"] == "skipped"


def test_active_hosted_readiness_config_check_is_offline_and_redacted(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    baseline = _write_fake_active_baseline(tmp_path)
    monkeypatch.setattr(
        cli_module, "secure_backend_profile_status", lambda backend: (True, "ready", "7.9.3.1.1")
    )
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: OpenAICompatibleConfig(
            provider="deepseek",
            base_url="https://key-value@api.deepseek.com/path",
            api_key="readiness-secret",
            model="deepseek-v4-pro",
            thinking_mode=kwargs["thinking_mode"],
        ),
    )
    argv = _active_hosted_readiness_argv(tmp_path, baseline)
    argv.append("--check-provider-config")

    assert main(argv) == 0
    output = capsys.readouterr().out
    payload = json.loads(output)
    assert payload["endpoint_host"] == "api.deepseek.com"
    assert payload["gates"]["provider_configuration"] == "passed"
    assert payload["network_requests"] == 0
    assert "readiness-secret" not in output
    assert "key-value" not in output


def test_active_hosted_readiness_requires_baseline_and_fresh_authorization(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    monkeypatch.setattr(
        cli_module, "secure_backend_profile_status", lambda backend: (True, "ready", "7.9.3.1.1")
    )
    missing = tmp_path / "missing" / "result.json"
    assert main(_active_hosted_readiness_argv(tmp_path, missing)) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["failed_gate"] == "fake_active_baseline"

    baseline = _write_fake_active_baseline(tmp_path)
    argv = _active_hosted_readiness_argv(tmp_path, baseline)
    argv.remove("--authorize-feedback")
    assert main(argv) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["failed_gate"] == "outbound_projection_authorization"
    assert "feedback" in payload["error"]


def test_active_hosted_readiness_rejects_invalid_baseline_and_existing_initial_root(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    monkeypatch.setattr(
        cli_module, "secure_backend_profile_status", lambda backend: (True, "ready", "7.9.3.1.1")
    )
    baseline = _write_fake_active_baseline(tmp_path)
    payload = json.loads(baseline.read_text(encoding="utf-8"))
    payload["usage"]["model_requests"] = 0
    baseline.write_text(json.dumps(payload), encoding="utf-8")

    assert main(_active_hosted_readiness_argv(tmp_path, baseline)) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["failed_gate"] == "saved_result_validation"

    baseline.unlink()
    baseline.parent.rmdir()
    baseline = _write_fake_active_baseline(tmp_path)
    (tmp_path / "active-hosted").mkdir()
    assert main(_active_hosted_readiness_argv(tmp_path, baseline)) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["failed_gate"] == "run_root"


def test_active_hosted_readiness_classifies_budget_binding_drift(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    baseline = _write_fake_active_baseline(tmp_path)
    monkeypatch.setattr(
        cli_module, "secure_backend_profile_status", lambda backend: (True, "ready", "7.9.3.1.1")
    )
    argv = _active_hosted_readiness_argv(tmp_path, baseline)
    argv[argv.index("--provider-max-total-tokens") + 1] = "50"

    assert main(argv) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["failed_gate"] == "budget_binding"
    assert "token budget" in payload["error"]


def test_active_hosted_preflight_does_not_read_config_or_create_artifacts(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    def reject_config(*args, **kwargs):
        raise AssertionError("active hosted preflight must not read provider configuration")

    monkeypatch.setattr(cli_module, "deepseek_config_from_env", reject_config)
    run_root = tmp_path / "active-hosted"

    assert main(_active_hosted_argv(tmp_path, "active-hosted-preflight")) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "ready"
    assert payload["network_requests"] == 0
    assert payload["provider_configuration_read"] is False
    assert payload["artifacts_created"] is False
    assert payload["outbound_projection"]["excluded"][-1] == "secrets"
    assert not run_root.exists()


def test_active_hosted_config_check_is_offline_and_redacted(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: OpenAICompatibleConfig(
            provider="deepseek",
            base_url="https://api.deepseek.com",
            api_key="top-secret",
            model="deepseek-v4-pro",
            thinking_mode=kwargs["thinking_mode"],
        ),
    )

    argv = _active_hosted_argv(tmp_path, "active-hosted-config-check")
    for flag in (
        "--authorize-hosted",
        "--authorize-observations",
        "--authorize-tool-results",
        "--authorize-revision-source",
        "--authorize-feedback",
    ):
        argv.remove(flag)

    assert main(argv) == 0
    output = capsys.readouterr().out
    payload = json.loads(output)
    assert payload["status"] == "ready"
    assert payload["endpoint_host"] == "api.deepseek.com"
    assert payload["network_requests"] == 0
    assert payload["provider_configuration_read"] is True
    assert payload["authorization_required"] is False
    assert not any(payload["authorization"].values())
    assert "top-secret" not in output


def test_active_hosted_preflight_requires_every_outbound_authorization(
    tmp_path: Path, capsys
) -> None:
    argv = _active_hosted_argv(tmp_path, "active-hosted-preflight")
    argv.remove("--authorize-feedback")

    assert main(argv) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "not_ready"
    assert "feedback" in payload["error"]


def test_run_refuses_held_out_eval_case(tmp_path: Path, capsys) -> None:
    exit_code = main(
        [
            "run",
            "--case-id",
            "cylinder",
            "--run-root",
            str(tmp_path / "run"),
            "--fake-script",
            "tests/fixtures/fixed_cylinder.py",
            "--max-rounds",
            "1",
        ]
    )

    assert exit_code == 2
    assert "runtime case" in json.loads(capsys.readouterr().out)["error"]
    assert not (tmp_path / "run").exists()


def test_environment_doctor_is_read_only_and_redacts_runtime_root(capsys, monkeypatch) -> None:
    monkeypatch.setenv("BREP2CODE_WSL_DISTRO", "Research-Ubuntu")
    monkeypatch.setenv("BREP2CODE_RUNTIME_ROOT", "/private/research/runtime")
    monkeypatch.setattr(cli_module, "secure_backend_status", lambda config: (True, "ready"))

    assert main(["env", "doctor"]) == 0
    output = capsys.readouterr().out
    payload = json.loads(output)
    assert payload["status"] == "ready"
    assert payload["configuration"]["wsl_distro"] == "Research-Ubuntu"
    assert payload["configuration"]["runtime_layout"] == "<runtime-root>/bin/python"
    assert payload["network_requests"] == 0
    assert payload["artifacts_created"] is False
    assert "/private/research/runtime" not in output


@pytest.mark.secure
def test_fake_run_command_repairs_box(tmp_path: Path, capsys) -> None:
    exit_code = main(
        [
            "run",
            "--case-id",
            "box",
            "--run-root",
            str(tmp_path / "run"),
            "--fake-script",
            str(Path("tests/fixtures/broken_box.py")),
            "--fake-script",
            str(Path("tests/fixtures/fixed_box.py")),
            "--max-rounds",
            "2",
        ]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "succeeded"
    assert payload["provider_requests"] == 2


@pytest.mark.secure
def test_fake_run_command_uses_initial_script_without_provider_request(
    tmp_path: Path, capsys
) -> None:
    exit_code = main(
        [
            "run",
            "--case-id",
            "block_with_hole",
            "--run-root",
            str(tmp_path / "run"),
            "--initial-script",
            "tests/fixtures/broken_block_with_hole.py",
            "--fake-script",
            "tests/fixtures/fixed_block_with_hole.py",
            "--max-rounds",
            "2",
        ]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "succeeded"
    assert payload["provider_requests"] == 1


def test_deepseek_refuses_before_reading_configuration(tmp_path: Path, capsys, monkeypatch) -> None:
    def unexpected_configuration_read():
        raise AssertionError("configuration must not be read before authorization")

    monkeypatch.setattr(cli_module, "deepseek_config_from_env", unexpected_configuration_read)
    exit_code = main(
        [
            "run",
            "--provider",
            "deepseek",
            "--case-id",
            "box",
            "--run-root",
            str(tmp_path / "run"),
            "--max-rounds",
            "1",
        ]
    )
    assert exit_code == 2
    assert "authorize-hosted" in json.loads(capsys.readouterr().out)["error"]
    assert not (tmp_path / "run").exists()


def test_deepseek_requires_explicit_disabled_thinking_before_configuration(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    monkeypatch.setattr(
        cli_module,
        "deepseek_config_from_env",
        lambda **kwargs: (_ for _ in ()).throw(
            AssertionError("configuration must not be read before thinking mode validation")
        ),
    )

    exit_code = main(
        [
            "run",
            "--provider",
            "deepseek",
            "--authorize-hosted",
            "--case-id",
            "box",
            "--run-root",
            str(tmp_path / "run"),
            "--max-rounds",
            "1",
        ]
    )

    assert exit_code == 2
    assert "thinking-mode disabled" in json.loads(capsys.readouterr().out)["error"]
    assert not (tmp_path / "run").exists()


def test_hosted_initial_script_rejects_repository_file_before_configuration(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    def unexpected_configuration_read(*args, **kwargs):
        raise AssertionError("configuration must not be read for a rejected seed")

    monkeypatch.setattr(cli_module, "deepseek_config_from_env", unexpected_configuration_read)
    run_root = tmp_path / "run"
    exit_code = main(
        [
            "run",
            "--provider",
            "deepseek",
            "--authorize-hosted",
            "--thinking-mode",
            "disabled",
            "--case-id",
            "box",
            "--run-root",
            str(run_root),
            "--initial-script",
            "tests/fixtures/broken_box.py",
            "--max-rounds",
            "2",
        ]
    )

    assert exit_code == 2
    error = json.loads(capsys.readouterr().out)["error"]
    assert "authorized artifact under the run-root parent" in error
    assert not run_root.exists()


@pytest.mark.secure
def test_authorized_deepseek_route_binds_limits_and_secure_executor(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    class StubHostedProvider:
        def __init__(self, config, limits) -> None:
            self.name = config.provider
            self.model = config.model
            self.limits = limits
            self.requests_issued = 0
            self.total_tokens = 0
            self.cost_usd = 0.0

        def generate(self, provider_request):
            del provider_request
            self.requests_issued += 1
            self.total_tokens += 20
            self.cost_usd += 0.001
            script = Path("tests/fixtures/fixed_box.py").read_text(encoding="utf-8")
            return ProviderResponse(
                provider=self.name,
                model=self.model,
                script=script,
                usage={"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
            )

    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-secret")
    monkeypatch.setenv("DEEPSEEK_MODEL", "test-model")
    monkeypatch.setattr(cli_module, "OpenAICompatibleProvider", StubHostedProvider)
    run_root = tmp_path / "run"
    initial_script = tmp_path / "initial.py"
    initial_script.write_text(
        Path("tests/fixtures/broken_box.py").read_text(encoding="utf-8"), encoding="utf-8"
    )
    exit_code = main(
        [
            "run",
            "--provider",
            "deepseek",
            "--authorize-hosted",
            "--thinking-mode",
            "disabled",
            "--case-id",
            "box",
            "--run-root",
            str(run_root),
            "--initial-script",
            str(initial_script),
            "--max-rounds",
            "2",
            "--max-requests",
            "1",
            "--provider-timeout",
            "120",
            "--max-retries",
            "0",
            "--max-output-tokens",
            "4096",
            "--max-total-tokens",
            "8192",
            "--max-cost-usd",
            "0.10",
            "--input-cost-per-million",
            "1",
            "--output-cost-per-million",
            "2",
        ]
    )
    assert exit_code == 0, capsys.readouterr().out
    result = json.loads((run_root / "result.json").read_text(encoding="utf-8"))
    assert result["provider_limits"]["max_requests"] == 1
    assert result["provider_accounting"] == {
        "http_attempts": 1,
        "total_tokens": 20,
        "cost_usd": 0.001,
    }
    assert [revision["source"] for revision in result["revisions"]] == [
        "initial_script",
        "provider",
    ]
    assert result["revisions"][0]["execution"]["sandbox_backend"] == "wsl-bwrap"
