from pathlib import Path
import json

from brep2code.agent.m135_epoch import (
    EXECUTOR,
    MODEL,
    PROVIDER,
    PROVIDER_DEADLINE_SECONDS,
    REQUEST_CAP,
    frozen_conditions,
    frozen_request,
    frozen_transcript,
    mark_issued,
    mark_terminal,
    prepare_checkpoint,
    run_fake_epoch,
    run_fake_serial_epoch,
    static_api_rejection_observation,
    terminal_from_observed,
)
from brep2code.cli import main
from brep2code.agent.observed_build import ObservationCall, ObservedBuildLoopRunner
from brep2code.agent.guidance import GuidanceBundle
from brep2code.agent.provider import FakeLLMProvider, fake_replacement_response
from brep2code.agent.harness import ManualHarness
from brep2code.cad import WslBubblewrapExecutor
from brep2code.storage import RecordStore


def test_m135_frozen_cohort_and_checkpoint_continue_after_condition_terminal(tmp_path: Path) -> None:
    root = Path.cwd()
    conditions = frozen_conditions(root)
    assert len(conditions) == REQUEST_CAP
    assert [item.family for item in conditions[:3]] == ["repeated_feature_pattern"] * 3
    report = tmp_path / "epoch.json"
    prepare_checkpoint(report, provider="fake", model="fake", conditions=conditions)
    mark_issued(report, conditions[0].condition_id)
    terminal = mark_terminal(report, conditions[0].condition_id, "script_api_failure")
    assert terminal["run_status"] == "running"
    assert terminal["conditions"][1]["state"] == "not_issued"
    issued = mark_issued(report, conditions[1].condition_id)
    assert issued["requests_used"] == 2
    assert issued["requests_remaining"] == 16


def test_m135_integrity_fault_stops_unissued_conditions(tmp_path: Path) -> None:
    conditions = frozen_conditions(Path.cwd())
    report = tmp_path / "epoch.json"
    prepare_checkpoint(report, provider="fake", model="fake", conditions=conditions)
    mark_issued(report, conditions[0].condition_id)
    terminal = mark_terminal(report, conditions[0].condition_id, "policy_hash_drift", integrity=True)
    assert terminal["run_status"] == "completed"
    assert terminal["conditions"][1]["state"] == "not_issued_epoch_integrity"


def test_m135_fake_epoch_accounts_all_conditions_without_provider(tmp_path: Path) -> None:
    conditions = frozen_conditions(Path.cwd())
    report = tmp_path / "epoch.json"
    prepare_checkpoint(report, provider="fake", model="fake", conditions=conditions)
    terminal = run_fake_epoch(report, conditions, lambda _condition: "pass")
    assert terminal["run_status"] == "completed"
    assert terminal["requests_used"] == REQUEST_CAP
    assert terminal["requests_remaining"] == 0
    assert {item["state"] for item in terminal["conditions"]} == {"pass"}


def test_m135_transcripts_are_path_free_and_hash_pinned() -> None:
    root = Path.cwd()
    conditions = frozen_conditions(root)
    assert len({item.transcript_sha256 for item in conditions}) == REQUEST_CAP
    for condition in conditions:
        payload = frozen_transcript(root, condition)
        encoded = json.dumps(payload, sort_keys=True)
        assert "path" not in payload
        assert "step" not in encoded.lower()


def test_m135_frozen_requests_have_one_hash_pinned_card_injection_only_for_card() -> None:
    root = Path.cwd()
    for condition in frozen_conditions(root):
        frozen = frozen_request(root, condition)
        assert frozen.request.model == MODEL
        assert frozen.request.messages[0].content
        assert frozen.system_instruction_sha256 == "f22e625ea874a7ecec10a0bc88b37f40ec05cb4086a4f777dcde9d3a5d19d7a1"
        if condition.treatment == "card":
            assert len(frozen.request.messages) == 3
            assert frozen.request.messages[-1].role == "tool"
            assert frozen.request.messages[-1].name == "get_guidance_card"
            assert frozen.card_source_sha256 == "55341683e3e7df3e058a845193e34fba20b0650c0db28a31489ad5d343b60d30"
            assert frozen.card_response_sha256 == "e43c0599d133f86ed3f11ba9e15b907f9a37af4098b8a0645611910c3f0c54de"
        else:
            assert len(frozen.request.messages) == 2
            assert frozen.card_response_sha256 is None
            assert frozen.card_source_sha256 is None




def test_m135_no_card_inputs_pass_no_input_wsl_bwrap(tmp_path: Path) -> None:
    root = Path.cwd()
    for condition in frozen_conditions(root):
        if condition.treatment != "no_card":
            continue
        case_path = next(root.glob(f"case-library/self-authored/{condition.case_id}/case.json"))
        case = json.loads(case_path.read_text(encoding="utf-8"))
        directory = case_path.parent
        runner = ObservedBuildLoopRunner(
            harness=ManualHarness(store=RecordStore(tmp_path / condition.case_id), executor=WslBubblewrapExecutor()),
            provider=FakeLLMProvider([fake_replacement_response((directory / case["reference_script"]).read_text(encoding="utf-8"))]),
        )
        result = runner.run(condition.condition_id.replace(":", "-"), input_path=directory / case["input_step"], observation_session_id="m135-preflight", observation_calls=[ObservationCall(call_id="summary", tool="probe_summary")])
        assert result.status == "pass", condition.condition_id


def test_m135_no_card_reference_scripts_do_not_import_repository_helpers() -> None:
    root = Path.cwd()
    for condition in frozen_conditions(root):
        if condition.treatment != "no_card":
            continue
        case_path = next(root.glob(f"case-library/self-authored/{condition.case_id}/case.json"))
        case = json.loads(case_path.read_text(encoding="utf-8"))
        script = (case_path.parent / case["reference_script"]).read_text(encoding="utf-8")
        assert "from tools." not in script, condition.condition_id


def test_m135_card_fake_script_uses_no_input_harness_and_terminal_mapping(tmp_path: Path) -> None:
    root = Path.cwd()
    condition = next(item for item in frozen_conditions(root) if item.treatment == "card")
    case_path = next(root.glob(f"case-library/self-authored/{condition.case_id}/case.json"))
    case = json.loads(case_path.read_text(encoding="utf-8"))
    directory = case_path.parent
    script = (directory / case["reference_script"]).read_text(encoding="utf-8")
    bundle = GuidanceBundle.from_paths(
        root / "runtime_resources/experience-cards/index.json", root / "runtime_resources/experience-cards/cards/vertical-cylinder-construction.json"
    )
    request = frozen_request(root, condition)
    runner = ObservedBuildLoopRunner(
        harness=ManualHarness(store=RecordStore(tmp_path / condition.case_id), executor=WslBubblewrapExecutor()),
        provider=FakeLLMProvider([fake_replacement_response(script)]),
    )
    result = runner.run(
        condition.condition_id.replace(":", "-"),
        input_path=directory / case["input_step"],
        observation_session_id="m135-runner-contract",
        observation_calls=[ObservationCall(call_id="summary", tool="probe_summary")],
        guidance_bundle=bundle,
        required_guidance_role="single boolean-cut tool",
        direct_guidance=json.loads(request.request.messages[2].content),
    )
    assert result.status == "pass"
    assert runner.provider.requests[0].messages[-1].content == request.request.messages[-1].content
    assert terminal_from_observed(condition, result, script) == "full_success"


def test_m138_static_api_rejection_observation_is_content_free_and_deterministic() -> None:
    script = "from bad.module import Bad\nBad()\n"
    observation = static_api_rejection_observation(script, "forbidden_import")
    assert observation["reason"] == "forbidden_import"
    assert observation["script_sha256"] == __import__("hashlib").sha256(script.encode("utf-8")).hexdigest()
    assert observation["import_modules"] == ["bad.module"]
    assert observation["call_names"] == ["Bad"]
    assert script not in str(observation)


def test_m135_fake_serial_lifecycle_runs_all_conditions_through_no_input_harness(tmp_path: Path) -> None:
    root = Path.cwd()
    conditions = frozen_conditions(root)
    scripts = []
    for condition in conditions:
        case_path = next(root.glob(f"case-library/self-authored/{condition.case_id}/case.json"))
        case = json.loads(case_path.read_text(encoding="utf-8"))
        scripts.append(fake_replacement_response((case_path.parent / case["reference_script"]).read_text(encoding="utf-8")))
    report = tmp_path / "epoch.json"
    prepare_checkpoint(report, provider="fake", model="fake", conditions=conditions)
    provider = FakeLLMProvider(scripts)
    result = run_fake_serial_epoch(
        report,
        root=root,
        provider=provider,
        harness=ManualHarness(store=RecordStore(tmp_path / "records"), executor=WslBubblewrapExecutor()),
    )
    assert result["run_status"] == "completed"
    assert result["requests_used"] == REQUEST_CAP
    assert result["requests_remaining"] == 0
    assert {item["state"] for item in result["conditions"]} == {"full_success"}
    assert len(provider.requests) == REQUEST_CAP


def test_m135_fake_serial_lifecycle_continues_after_condition_failures(tmp_path: Path) -> None:
    root = Path.cwd()
    conditions = frozen_conditions(root)
    report = tmp_path / "epoch.json"
    prepare_checkpoint(report, provider="fake", model="fake", conditions=conditions)
    provider = FakeLLMProvider([fake_replacement_response(""), fake_replacement_response("raise RuntimeError('not reached')")])
    result = run_fake_serial_epoch(
        report,
        root=root,
        provider=provider,
        harness=ManualHarness(store=RecordStore(tmp_path / "records"), executor=WslBubblewrapExecutor()),
    )
    assert result["conditions"][0]["state"] == "downstream_gate_failed"
    assert result["conditions"][1]["state"] == "sandbox_execution_failed"
    assert result["conditions"][2]["state"] == "lifecycle_ended_before_script"
    assert result["requests_used"] == REQUEST_CAP


def test_m135_preflight_cli_prepares_fixed_contract_and_monitor(tmp_path: Path, capsys) -> None:
    report = tmp_path / "epoch.json"
    monitor = tmp_path / "monitor.json"

    assert main(["m135-epoch-preflight", "--report", str(report), "--monitor-state", str(monitor)]) == 0

    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["provider"] == PROVIDER
    assert payload["model"] == MODEL
    assert payload["requests_used"] == 0
    assert payload["requests_remaining"] == REQUEST_CAP
    assert payload["epoch_contract"] == {
        "executor": EXECUTOR,
        "provider_deadline_seconds": PROVIDER_DEADLINE_SECONDS,
        "max_output_tokens": None,
        "max_repair_rounds": 0,
        "max_retry_count": 0,
        "max_requests": REQUEST_CAP,
        "monitor_path": str(monitor),
        "authorization": "not_authorized",
        "provider_constructed": False,
    }
    monitor_payload = json.loads(monitor.read_text(encoding="utf-8"))
    assert monitor_payload["monitor_status"] == "monitoring"
    assert '"status": "prepared_offline"' in capsys.readouterr().out


def test_m135_preflight_rejects_reused_or_colliding_paths(tmp_path: Path, capsys) -> None:
    report = tmp_path / "epoch.json"
    monitor = tmp_path / "monitor.json"
    assert main(["m135-epoch-preflight", "--report", str(report), "--monitor-state", str(monitor)]) == 0

    assert main(["m135-epoch-preflight", "--report", str(report), "--monitor-state", str(tmp_path / "other.json")]) == 2
    assert "report path must be fresh" in capsys.readouterr().out
    assert main(["m135-epoch-preflight", "--report", str(tmp_path / "next.json"), "--monitor-state", str(monitor)]) == 2
    assert "monitor path must be fresh" in capsys.readouterr().out
    assert main(["m135-epoch-preflight", "--report", str(tmp_path / "same.json"), "--monitor-state", str(tmp_path / "same.json")]) == 2
    assert "report and monitor paths must differ" in capsys.readouterr().out
