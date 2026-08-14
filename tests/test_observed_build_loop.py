import json
from pathlib import Path
from types import SimpleNamespace

import brep2code.cli as cli
from brep2code.agent import FakeLLMProvider, ManualHarness
from brep2code.agent.guidance import GuidanceBundle, GuidanceCardBridge
from brep2code.agent.m97_observation import derive_m96_development_context, validate_m97_observation_context
from brep2code.agent.observed_build import ObservationCall, ObservedBuildLoopRunner
from brep2code.agent.provider import DeepSeekProvider, ProviderResponse, fake_guidance_request, fake_replacement_response
from brep2code.agent.repair import ProviderRequestLifecycleError, ProviderRequestTimeoutError
from brep2code.agent.tools import BRepToolBridge
from brep2code.corpus.runner import CorpusCaseResult, _case_dataclass_to_dict
from brep2code.cad import WslBubblewrapExecutor
from brep2code.monitor import setup_monitor
from brep2code.scaffold import DEFAULT_BUILD_SEQUENCE
from brep2code.storage import RecordStore
from brep2code.cli import _provider_interruption, _sanitize_lifecycle_diagnostics, main


BOX_STEP = Path("case-library/self-authored/box/input.step")
CYLINDER_STEP = Path("case-library/self-authored/cylinder/input.step")
CYLINDER_SCRIPT = Path("case-library/self-authored/cylinder/reference_build_sequence.py")
BLOCK_WITH_HOLE_STEP = Path("case-library/self-authored/block_with_hole/input.step")
BLOCK_WITH_HOLE_SCRIPT = Path("case-library/self-authored/block_with_hole/reference_build_sequence.py")
THREE_HOLE_PLATE_STEP = Path("case-library/self-authored/three_hole_plate/input.step")
THREE_HOLE_PLATE_SCRIPT = Path("case-library/self-authored/three_hole_plate/reference_build_sequence.py")
GUIDANCE_INDEX = Path("runtime_resources/experience-cards/index.json")
GUIDANCE_CARD = Path("runtime_resources/experience-cards/cards/vertical-cylinder-construction.json")


def _bridge(tmp_path: Path, *, max_calls: int = 8) -> BRepToolBridge:
    store = RecordStore(tmp_path / "data")
    record = store.ensure_record("box")
    (record.input_dir / "input.step").write_bytes(BOX_STEP.read_bytes())
    return BRepToolBridge(store=store, max_calls=max_calls)


def test_observation_call_budget_is_scoped_to_each_session(tmp_path: Path) -> None:
    bridge = _bridge(tmp_path, max_calls=1)
    trace_dir = tmp_path / "traces"

    first_session = bridge.observe("box", "session-a", "call-1", "probe_summary", trace_dir=trace_dir)
    second_session = bridge.observe("box", "session-b", "call-1", "probe_summary", trace_dir=trace_dir)
    exhausted = bridge.observe("box", "session-a", "call-2", "probe_summary", trace_dir=trace_dir)

    assert first_session["ok"] is True
    assert second_session["ok"] is True
    assert exhausted["error"]["code"] == "tool_call_limit_exceeded"


def test_observed_build_loop_rejects_non_fake_provider(tmp_path: Path) -> None:
    try:
        ObservedBuildLoopRunner(harness=ManualHarness(store=RecordStore(tmp_path / "data")), provider=object())  # type: ignore[arg-type]
    except ValueError as exc:
        assert "allow_hosted" in str(exc)
    else:
        raise AssertionError("expected offline runner to reject a non-fake provider")


def test_fake_provider_observation_build_loop_has_no_input_mount_or_path_egress(tmp_path: Path) -> None:
    store = RecordStore(tmp_path / "data")
    harness = ManualHarness(store=store)
    provider = FakeLLMProvider([fake_replacement_response(DEFAULT_BUILD_SEQUENCE)])
    runner = ObservedBuildLoopRunner(harness=harness, provider=provider)

    result = runner.run(
        "box",
        input_path=BOX_STEP,
        observation_session_id="session-a",
        observation_calls=[ObservationCall(call_id="summary-1", tool="probe_summary")],
    )

    assert result.status == "pass"
    assert result.harness_result is not None
    bundle = result.harness_result.signal_bundle
    assert bundle["observation_build_capability"] == {"input_mount_present": False}
    assert bundle["observation"]["entry_count"] == 1
    request_text = "\n".join(message.content for message in provider.requests[0].messages)
    assert "input.step" not in request_text
    assert str((tmp_path / "data").resolve()) not in request_text
    traces = result.harness_result.revision.traces
    assert (traces / "observation_queries.jsonl").exists()
    assert (traces / "provider_response.json").exists()
    assert "input.step" not in (traces / "llm_messages.jsonl").read_text(encoding="utf-8")


def test_observed_build_rejects_fake_cadquery_script_before_execution(tmp_path: Path) -> None:
    store = RecordStore(tmp_path / "data")
    provider = FakeLLMProvider([fake_replacement_response("import cadquery\n")])
    runner = ObservedBuildLoopRunner(harness=ManualHarness(store=store), provider=provider)

    result = runner.run(
        "box",
        input_path=BOX_STEP,
        observation_session_id="session-cadquery",
        observation_calls=[ObservationCall(call_id="summary-1", tool="probe_summary")],
    )

    assert result.status == "fail"
    assert result.harness_result is not None
    execution = result.harness_result.signal_bundle["execution"]
    assert execution["sandbox_termination_reason"] == "contract_rejected"
    assert execution["build_script_contract"]["violations"][0]["module"] == "cadquery"
    assert "never cadquery" in provider.requests[0].messages[0].content


def test_reference_assisted_loop_requests_card_then_builds_cylinder(tmp_path: Path) -> None:
    provider = FakeLLMProvider([
        fake_guidance_request(),
        fake_replacement_response(CYLINDER_SCRIPT.read_text(encoding="utf-8")),
    ])
    runner = ObservedBuildLoopRunner(harness=ManualHarness(store=RecordStore(tmp_path / "data")), provider=provider)

    result = runner.run(
        "cylinder", input_path=CYLINDER_STEP, observation_session_id="m85",
        observation_calls=[ObservationCall(call_id="summary-1", tool="probe_summary")],
        guidance_bundle=GuidanceBundle.from_paths(GUIDANCE_INDEX, GUIDANCE_CARD), required_guidance_role="final primitive",
    )

    assert result.status == "pass"
    assert result.provider_requests == 2
    assert result.harness_result is not None
    assert result.harness_result.signal_bundle["guidance"]["returned_card_ids"] == ["vertical-cylinder-construction"]
    assert result.harness_result.signal_bundle["guidance"]["selected_role"] == "final primitive"
    assert len(provider.requests) == 2
    assert provider.requests[0].metadata["phase"] == "guidance_request"
    assert provider.requests[1].metadata["phase"] == "script_generation"
    assert "vertical-cylinder-construction" in provider.requests[1].messages[-1].content
    assert "input.step" not in "\n".join(message.content for request in provider.requests for message in request.messages)


def test_m97_fixed_development_calibration_uses_nine_fake_requests(tmp_path: Path, capsys) -> None:
    report = tmp_path / "m97.json"
    assert main([
        "reference-guided-through-hole-development-calibration",
        "--provider", "fake",
        "--request-budget", "9",
        "--data-root", str(tmp_path / "data"),
        "--report", str(report),
    ]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["requests_used"] == 9
    assert [(case["condition"], case["provider_requests"]) for case in payload["cases"]] == [
        ("card", 2), ("baseline", 1), ("card", 2),
        ("baseline", 1), ("card", 2), ("baseline", 1),
    ]
    assert all(case["status"] == "pass" for case in payload["cases"])


def test_m97_low_row_outbound_context_is_measured_facts_only(tmp_path: Path) -> None:
    root = Path.cwd()
    record = json.loads((root / "docs/corpus/sequence-paired/reference-guided-through-hole-variation-v1-preregistration.json").read_text(encoding="utf-8"))
    entry = next(item for item in record["cases"] if item["case_id"].endswith("development_low"))
    context = derive_m96_development_context(entry, root=root)
    validate_m97_observation_context(context)
    directory = root / entry["candidate_directory"]
    provider = FakeLLMProvider([fake_replacement_response((directory / "reference_build_sequence.py").read_text(encoding="utf-8"))])
    result = ObservedBuildLoopRunner(harness=ManualHarness(store=RecordStore(tmp_path / "data")), provider=provider).run(
        "m97-low", input_path=directory / "input.step", observation_session_id="ignored",
        observation_calls=[], observation_context=context,
    )
    assert result.status == "pass"
    system_instruction = provider.requests[0].messages[0].content
    assert "installed OCP modules and symbols" in system_instruction
    assert "invented OCP names" in system_instruction
    outbound = provider.requests[0].messages[-1].content
    payload = json.loads(outbound)
    cut = payload["observation_transcript"][0]["data"]["cylindrical_cut"]
    assert cut == {"radius": 2.0, "axis": "+Z", "center_xy": [9.0, 10.0], "extent": "through"}
    assert set(payload["observation_transcript"][0]["data"]) == {"kind", "base_bbox", "cylindrical_cut"}
    assert "input.step" not in outbound and "reference_build_sequence.py" not in outbound


def test_m97_rejects_non_frozen_request_budget(tmp_path: Path, capsys) -> None:
    assert main([
        "reference-guided-through-hole-development-calibration",
        "--provider", "fake", "--request-budget", "8", "--data-root", str(tmp_path / "data"),
    ]) == 2
    assert "nine requests" in json.loads(capsys.readouterr().out)["error"]


def test_m97_hosted_requires_explicit_authorization(tmp_path: Path, capsys) -> None:
    assert main([
        "reference-guided-through-hole-development-calibration",
        "--provider", "deepseek", "--request-budget", "9", "--data-root", str(tmp_path / "data"),
    ]) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "authorization_required"


def test_m97_hosted_prepare_writes_fresh_nine_request_checkpoint(tmp_path: Path, capsys, monkeypatch) -> None:
    monkeypatch.setattr(
        DeepSeekProvider,
        "from_env_file",
        lambda _path: SimpleNamespace(name="deepseek", model="deepseek-v4-pro"),
    )
    report = tmp_path / "m97-hosted.json"
    assert main([
        "reference-guided-through-hole-development-calibration",
        "--provider", "deepseek", "--authorize-hosted", "--phase", "prepare",
        "--request-budget", "9", "--data-root", str(tmp_path / "data"), "--report", str(report),
    ]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["run_status"] == "running"
    assert payload["request_state"] == "prepared"
    assert payload["requests_used"] == 0
    assert payload["requests_remaining"] == 9


def test_m97_hosted_execute_accounts_for_all_nine_requests(tmp_path: Path, capsys, monkeypatch) -> None:
    monkeypatch.setattr(
        DeepSeekProvider,
        "from_env_file",
        lambda _path: SimpleNamespace(name="deepseek", model="deepseek-v4-pro"),
    )

    class StubRunner:
        def __init__(self, **_kwargs) -> None:
            pass

        def run(self, _record_id: str, **kwargs):
            calls = 2 if kwargs["guidance_bundle"] is not None else 1
            for _ in range(calls):
                kwargs["before_provider_request"]()
            return SimpleNamespace(status="pass", provider_requests=calls)

    monkeypatch.setattr(cli, "ObservedBuildLoopRunner", StubRunner)
    report = tmp_path / "m97-hosted.json"
    prepare = [
        "reference-guided-through-hole-development-calibration",
        "--provider", "deepseek", "--authorize-hosted", "--request-budget", "9",
        "--data-root", str(tmp_path / "data"), "--report", str(report),
    ]
    assert main([*prepare, "--phase", "prepare"]) == 0
    capsys.readouterr()
    assert main([*prepare, "--phase", "execute"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["run_status"] == "completed"
    assert payload["requests_used"] == 9
    assert payload["requests_remaining"] == 0
    assert [(case["condition"], case["provider_requests"]) for case in payload["cases"]] == [
        ("card", 2), ("baseline", 1), ("card", 2),
        ("baseline", 1), ("card", 2), ("baseline", 1),
    ]


def test_m97_development_inputs_pass_no_input_wsl_bwrap_preflight(tmp_path: Path) -> None:
    development = ("low", "nominal", "high")
    for variant in development:
        directory = Path(f"case-library/self-authored/param_reference_guided_through_hole_development_{variant}")
        provider = FakeLLMProvider([fake_replacement_response((directory / "reference_build_sequence.py").read_text(encoding="utf-8"))])
        result = ObservedBuildLoopRunner(
            harness=ManualHarness(store=RecordStore(tmp_path / variant), executor=WslBubblewrapExecutor()),
            provider=provider,
        ).run(
            f"m97-no-input-{variant}",
            input_path=directory / "input.step",
            observation_session_id=f"m97-no-input-{variant}",
            observation_calls=[ObservationCall(call_id="summary-1", tool="probe_summary")],
        )
        assert result.status == "pass"
        assert result.harness_result is not None
        assert result.harness_result.signal_bundle["observation_build_capability"] == {"input_mount_present": False}


def test_observed_build_projects_sanitized_first_response_byte_timing(tmp_path: Path) -> None:
    replacement = fake_replacement_response(CYLINDER_SCRIPT.read_text(encoding="utf-8"))
    provider = FakeLLMProvider([
        fake_guidance_request(),
        ProviderResponse(
            provider=replacement.provider,
            model=replacement.model,
            output_text=replacement.output_text,
            script_update=replacement.script_update,
            raw_summary={"first_response_byte_elapsed_ms": 3},
        ),
    ])
    result = ObservedBuildLoopRunner(harness=ManualHarness(store=RecordStore(tmp_path / "data")), provider=provider).run(
        "cylinder",
        input_path=CYLINDER_STEP,
        observation_session_id="m89-first-byte",
        observation_calls=[ObservationCall(call_id="summary-1", tool="probe_summary")],
        guidance_bundle=GuidanceBundle.from_paths(GUIDANCE_INDEX, GUIDANCE_CARD),
        required_guidance_role="final primitive",
    )

    assert result.status == "pass"
    assert result.telemetry["request_timing"]["first_byte_offset_ms"] is not None
    assert result.telemetry["request_timing"]["first_byte_offset_ms"] >= 3


def test_reference_assisted_loop_propagates_positive_token_cap_to_both_requests(tmp_path: Path) -> None:
    provider = FakeLLMProvider([
        fake_guidance_request(),
        fake_replacement_response(CYLINDER_SCRIPT.read_text(encoding="utf-8")),
    ])
    result = ObservedBuildLoopRunner(harness=ManualHarness(store=RecordStore(tmp_path / "data")), provider=provider).run(
        "cylinder", input_path=CYLINDER_STEP, observation_session_id="m89-003-token-cap",
        observation_calls=[ObservationCall(call_id="summary-1", tool="probe_summary")],
        guidance_bundle=GuidanceBundle.from_paths(GUIDANCE_INDEX, GUIDANCE_CARD),
        required_guidance_role="final primitive", max_output_tokens=4096,
    )

    assert result.status == "pass"
    assert [request.max_output_tokens for request in provider.requests] == [4096, 4096]


def test_direct_guidance_keeps_one_request_per_condition(tmp_path: Path) -> None:
    bundle = GuidanceBundle.from_paths(GUIDANCE_INDEX, GUIDANCE_CARD)
    direct = GuidanceCardBridge("test", bundle).call("get_guidance_card", {"role": "single boolean-cut tool"})
    assert direct.ok and direct.result is not None
    provider = FakeLLMProvider([fake_replacement_response(BLOCK_WITH_HOLE_SCRIPT.read_text(encoding="utf-8"))])
    result = ObservedBuildLoopRunner(harness=ManualHarness(store=RecordStore(tmp_path / "data")), provider=provider).run(
        "direct-guidance",
        input_path=BLOCK_WITH_HOLE_STEP,
        observation_session_id="m135-direct-guidance",
        observation_calls=[ObservationCall(call_id="summary-1", tool="probe_summary")],
        guidance_bundle=bundle,
        required_guidance_role="single boolean-cut tool",
        direct_guidance=direct.result,
    )

    assert result.status == "pass"
    assert result.provider_requests == 1
    assert len(provider.requests) == 1
    assert provider.requests[0].metadata["guidance_mode"] == "direct"
    assert provider.requests[0].messages[-1].name == "get_guidance_card"


def test_observed_build_rejects_non_positive_token_cap(tmp_path: Path) -> None:
    runner = ObservedBuildLoopRunner(
        harness=ManualHarness(store=RecordStore(tmp_path / "data")), provider=FakeLLMProvider([])
    )
    try:
        runner.run(
            "box", input_path=BOX_STEP, observation_session_id="bad-token-cap",
            observation_calls=[ObservationCall(call_id="summary-1", tool="probe_summary")], max_output_tokens=0,
        )
    except ValueError as exc:
        assert str(exc) == "max_output_tokens must be a positive integer"
    else:
        raise AssertionError("expected a positive token cap validation error")


def test_reference_assisted_loop_admits_each_preregistered_cylinder_role_offline(tmp_path: Path) -> None:
    cases = [
        ("cylinder", CYLINDER_STEP, CYLINDER_SCRIPT, "final primitive"),
        ("block-with-hole", BLOCK_WITH_HOLE_STEP, BLOCK_WITH_HOLE_SCRIPT, "single boolean-cut tool"),
        ("three-hole-plate", THREE_HOLE_PLATE_STEP, THREE_HOLE_PLATE_SCRIPT, "repeated boolean-cut tool"),
    ]

    for record_id, input_path, script_path, role in cases:
        provider = FakeLLMProvider([
            fake_guidance_request(role=role),
            fake_replacement_response(script_path.read_text(encoding="utf-8")),
        ])
        runner = ObservedBuildLoopRunner(
            harness=ManualHarness(store=RecordStore(tmp_path / record_id / "data")), provider=provider
        )

        result = runner.run(
            record_id, input_path=input_path, observation_session_id=f"m86-{record_id}",
            observation_calls=[ObservationCall(call_id="summary-1", tool="probe_summary")],
            guidance_bundle=GuidanceBundle.from_paths(GUIDANCE_INDEX, GUIDANCE_CARD), required_guidance_role=role,
        )

        assert result.status == "pass"
        assert result.provider_requests == 2
        assert provider.requests[0].metadata["required_guidance_role"] == role
        assert result.harness_result is not None
        assert result.harness_result.signal_bundle["guidance"] == {
            "enabled": True,
            "index_sha256": GuidanceBundle.from_paths(GUIDANCE_INDEX, GUIDANCE_CARD).index_sha256,
            "selected_role": role,
            "returned_card_ids": ["vertical-cylinder-construction"],
            "calls": [{"tool": "get_guidance_card", "ok": True, "card_id": "vertical-cylinder-construction", "error": None}],
        }


def test_reference_assisted_loop_rejects_non_fixed_tool_call(tmp_path: Path) -> None:
    provider = FakeLLMProvider([ProviderResponse(provider="fake", model="fake", output_text="bad")])
    result = ObservedBuildLoopRunner(harness=ManualHarness(store=RecordStore(tmp_path / "data")), provider=provider).run(
        "cylinder", input_path=CYLINDER_STEP, observation_session_id="m85-bad",
        observation_calls=[ObservationCall(call_id="summary-1", tool="probe_summary")],
        guidance_bundle=GuidanceBundle.from_paths(GUIDANCE_INDEX, GUIDANCE_CARD), required_guidance_role="final primitive",
    )

    assert result.status == "provider_error"
    assert result.provider_requests == 1
    assert result.error["code"] == "invalid_guidance_tool_call"


def test_reference_assisted_cli_prepare_then_execute_checkpoints_each_request(tmp_path: Path) -> None:
    report = tmp_path / "m85.json"
    base = [
        "reference-assisted-smoke", "--record", "cylinder", "--input", str(CYLINDER_STEP),
        "--data-root", str(tmp_path / "data"), "--request-budget", "2",
        "--fake-replacement-script", str(CYLINDER_SCRIPT), "--report", str(report),
    ]
    assert main([*base, "--phase", "prepare"]) == 0
    assert json.loads(report.read_text(encoding="utf-8"))["requests_used"] == 0
    assert main([*base, "--phase", "execute"]) == 0
    terminal = json.loads(report.read_text(encoding="utf-8"))
    assert terminal["run_status"] == "completed"
    assert terminal["requests_used"] == 2
    assert terminal["requests_remaining"] == 0
    assert terminal["result"]["status"] == "pass"


def test_reference_assisted_block_with_hole_cli_is_fixed_and_checkpoints_two_requests(tmp_path: Path, capsys) -> None:
    report = tmp_path / "m87.json"
    base = [
        "reference-assisted-block-with-hole-smoke", "--record", "block-with-hole", "--input", str(BLOCK_WITH_HOLE_STEP),
        "--data-root", str(tmp_path / "data"), "--request-budget", "2",
        "--fake-replacement-script", str(BLOCK_WITH_HOLE_SCRIPT), "--report", str(report),
    ]

    assert main([*base, "--phase", "prepare"]) == 0
    assert main([*base, "--phase", "execute"]) == 0
    terminal = json.loads(report.read_text(encoding="utf-8"))
    assert terminal["policy"] == "m87-reference-assisted-block-with-hole-v1"
    assert terminal["run_status"] == "completed"
    assert terminal["requests_used"] == 2
    assert terminal["result"]["status"] == "pass"

    assert main([*base, "--case-id", "cylinder"]) == 2
    assert "M87 is fixed to block_with_hole / single boolean-cut tool" in capsys.readouterr().out


def test_reference_assisted_three_hole_plate_cli_is_fixed_and_checkpoints_two_requests(tmp_path: Path, capsys) -> None:
    report = tmp_path / "m89.json"
    base = [
        "reference-assisted-three-hole-plate-smoke", "--record", "three-hole-plate", "--input", str(THREE_HOLE_PLATE_STEP),
        "--data-root", str(tmp_path / "data"), "--request-budget", "2",
        "--fake-replacement-script", str(THREE_HOLE_PLATE_SCRIPT), "--report", str(report),
    ]

    assert main([*base, "--phase", "prepare"]) == 0
    assert main([*base, "--phase", "execute"]) == 0
    terminal = json.loads(report.read_text(encoding="utf-8"))
    assert terminal["policy"] == "m89-reference-assisted-three-hole-plate-v1"
    assert terminal["run_status"] == "completed"
    assert terminal["requests_used"] == 2
    assert terminal["requests_remaining"] == 0
    assert terminal["result"]["status"] == "pass"

    assert main([*base, "--guidance-role", "single boolean-cut tool"]) == 2
    assert "M89 is fixed to three_hole_plate / repeated boolean-cut tool" in capsys.readouterr().out


def test_m89_003_bounded_output_cli_is_fixed_and_records_token_cap(tmp_path: Path, capsys) -> None:
    report = tmp_path / "m89-003.json"
    base = [
        "reference-assisted-three-hole-plate-bounded-output-smoke", "--record", "three-hole-plate",
        "--input", str(THREE_HOLE_PLATE_STEP), "--data-root", str(tmp_path / "data"),
        "--request-budget", "2", "--fake-replacement-script", str(THREE_HOLE_PLATE_SCRIPT),
        "--report", str(report),
    ]
    assert main([*base, "--phase", "prepare"]) == 0
    prepared = json.loads(report.read_text(encoding="utf-8"))
    assert prepared["policy"] == "m89-003-three-hole-plate-bounded-output-v1"
    assert prepared["max_output_tokens"] == 4096
    assert main([*base, "--phase", "execute"]) == 0
    terminal = json.loads(report.read_text(encoding="utf-8"))
    assert terminal["requests_used"] == 2
    assert terminal["result"]["status"] == "pass"

    assert main([*base, "--max-output-tokens", "4095"]) == 2
    assert "M89-003 requires --max-output-tokens 4096" in capsys.readouterr().out


def test_m118_stability_cli_uses_a_fresh_policy_and_checkpoint(tmp_path: Path, capsys) -> None:
    report = tmp_path / "m118.json"
    base = [
        "reference-assisted-three-hole-plate-stability-smoke", "--record", "three-hole-plate",
        "--input", str(THREE_HOLE_PLATE_STEP), "--data-root", str(tmp_path / "data"),
        "--request-budget", "2", "--fake-replacement-script", str(THREE_HOLE_PLATE_SCRIPT),
        "--report", str(report),
    ]
    assert main([*base, "--phase", "prepare"]) == 0
    prepared = json.loads(report.read_text(encoding="utf-8"))
    assert prepared["policy"] == "m118-three-hole-plate-stability-v1"
    assert prepared["max_output_tokens"] == 4096
    assert main([*base, "--phase", "execute"]) == 0
    terminal = json.loads(report.read_text(encoding="utf-8"))
    assert terminal["policy"] == "m118-three-hole-plate-stability-v1"
    assert terminal["requests_used"] == 2
    assert terminal["result"]["status"] == "pass"

    assert main([*base, "--request-budget", "1"]) == 2


def test_m127_stability_reentry_cli_uses_a_fresh_policy_and_checkpoint(tmp_path: Path, capsys) -> None:
    report = tmp_path / "m127.json"
    base = [
        "reference-assisted-three-hole-plate-stability-reentry-smoke", "--record", "three-hole-plate",
        "--input", str(THREE_HOLE_PLATE_STEP), "--data-root", str(tmp_path / "data"),
        "--request-budget", "2", "--fake-replacement-script", str(THREE_HOLE_PLATE_SCRIPT),
        "--report", str(report),
    ]
    assert main([*base, "--phase", "prepare"]) == 0
    prepared = json.loads(report.read_text(encoding="utf-8"))
    assert prepared["policy"] == "m127-three-hole-plate-stability-reentry-v1"
    assert prepared["max_output_tokens"] == 4096
    assert main([*base, "--phase", "execute"]) == 0
    terminal = json.loads(report.read_text(encoding="utf-8"))
    assert terminal["policy"] == "m127-three-hole-plate-stability-reentry-v1"
    assert terminal["requests_used"] == 2
    assert terminal["result"]["status"] == "pass"

    assert main([*base, "--request-budget", "1"]) == 2
    assert "M127 requires exactly two requests and zero repair rounds" in capsys.readouterr().out
    assert main([*base, "--max-output-tokens", "4095"]) == 2
    assert "M127 requires --max-output-tokens 4096" in capsys.readouterr().out


def test_observation_only_repair_keeps_input_unmounted_and_filters_paths(tmp_path: Path) -> None:
    store = RecordStore(tmp_path / "data")
    harness = ManualHarness(store=store)
    provider = FakeLLMProvider(
        [
            fake_replacement_response("raise RuntimeError('intentional failure')\n"),
            fake_replacement_response(DEFAULT_BUILD_SEQUENCE),
        ]
    )
    runner = ObservedBuildLoopRunner(harness=harness, provider=provider)

    result = runner.run(
        "box",
        input_path=BOX_STEP,
        observation_session_id="session-repair",
        observation_calls=[ObservationCall(call_id="summary-1", tool="probe_summary")],
        max_repair_rounds=1,
    )

    assert result.status == "pass"
    assert result.repair is not None
    assert result.repair.status == "pass"
    assert result.provider_requests == 2
    messages = "\n".join(path.read_text(encoding="utf-8") for path in (tmp_path / "data").rglob("llm_messages.jsonl"))
    assert "input.step" not in messages
    assert str((tmp_path / "data").resolve()) not in messages
    for bundle_path in (tmp_path / "data").rglob("signal_bundle.json"):
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        assert bundle["observation_build_capability"] == {"input_mount_present": False}


def test_corpus_projects_provenance_eligibility_separately_from_health() -> None:
    case = CorpusCaseResult(
        case_id="geometry-only",
        tier="development",
        record_id="record",
        revision_id="revision",
        status="pass",
        gate_statuses={"bbox_delta": "pass"},
        failure_type=None,
        signal_bundle_path="signal_bundle.json",
        probes={},
        provenance={"classification": "provenance_unknown"},
    )

    payload = _case_dataclass_to_dict(case)

    assert payload["status"] == "pass"
    assert payload["provenance"]["classification"] == "provenance_unknown"
    assert payload["reconstruction_eligible"] is False


def test_observed_first_pass_cli_runs_fake_without_input_mount(tmp_path: Path, capsys) -> None:
    script = tmp_path / "replacement.py"
    script.write_text(DEFAULT_BUILD_SEQUENCE, encoding="utf-8")

    exit_code = main([
        "observed-first-pass", "--record", "box", "--input", str(BOX_STEP),
        "--data-root", str(tmp_path / "data"), "--fake-replacement-script", str(script),
    ])

    assert exit_code == 0
    assert '"input_mount_present": false' in capsys.readouterr().out


def test_observed_first_pass_cli_rejects_hosted_before_provider_construction(tmp_path: Path, capsys) -> None:
    exit_code = main([
        "observed-first-pass", "--record", "box", "--input", str(BOX_STEP),
        "--data-root", str(tmp_path / "data"), "--provider", "deepseek",
    ])

    assert exit_code == 2
    assert "authorization_required" in capsys.readouterr().out


def test_provider_control_fake_writes_redacted_completed_report(tmp_path: Path, capsys) -> None:
    report = tmp_path / "control.json"

    exit_code = main(["provider-control", "--report", str(report)])

    assert exit_code == 0
    assert '"run_status": "completed"' in capsys.readouterr().out
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload == {
        "schema_version": 1,
        "policy": "provider-control-v1",
        "run_status": "completed",
        "provider": "fake",
        "model": "fake-control",
        "requests_used": 1,
        "requests_remaining": 0,
    }
    assert "Return exactly OK." not in report.read_text(encoding="utf-8")


def test_provider_control_rejects_hosted_before_provider_construction(tmp_path: Path, capsys) -> None:
    exit_code = main(["provider-control", "--report", str(tmp_path / "control.json"), "--provider", "deepseek"])

    assert exit_code == 2
    assert "authorization_required" in capsys.readouterr().out


def test_provider_control_prepare_is_monitorable_then_execute_is_terminal(tmp_path: Path) -> None:
    report = tmp_path / "control.json"
    monitor = tmp_path / "control.monitor.json"

    assert main(["provider-control", "--report", str(report), "--phase", "prepare"]) == 0
    prepared = json.loads(report.read_text(encoding="utf-8"))
    assert prepared["run_status"] == "running"
    assert prepared["request_state"] == "prepared"
    assert setup_monitor(report, monitor, stale_after_seconds=60)["monitor_status"] == "monitoring"
    assert main(["provider-control", "--report", str(report), "--phase", "execute"]) == 0

    terminal = json.loads(report.read_text(encoding="utf-8"))
    assert terminal["run_status"] == "completed"
    assert terminal["request_state"] == "issued"
    assert terminal["requests_used"] == 1
    assert "Return exactly OK." not in report.read_text(encoding="utf-8")


def test_single_request_prepare_refuses_an_existing_report(tmp_path: Path, capsys) -> None:
    report = tmp_path / "control.json"
    assert main(["provider-control", "--report", str(report), "--phase", "prepare"]) == 0

    assert main(["provider-control", "--report", str(report), "--phase", "prepare"]) == 2
    assert "fresh" in capsys.readouterr().out


def test_observed_first_pass_prepare_is_monitorable_then_execute_is_terminal(tmp_path: Path) -> None:
    script = tmp_path / "replacement.py"
    script.write_text(DEFAULT_BUILD_SEQUENCE, encoding="utf-8")
    report = tmp_path / "observed.json"
    monitor = tmp_path / "observed.monitor.json"
    base = [
        "observed-first-pass", "--record", "box", "--input", str(BOX_STEP), "--data-root", str(tmp_path / "data"),
        "--report", str(report), "--fake-replacement-script", str(script),
    ]

    assert main([*base, "--phase", "prepare"]) == 0
    assert setup_monitor(report, monitor, stale_after_seconds=60)["monitor_status"] == "monitoring"
    assert main([*base, "--phase", "execute"]) == 0

    terminal = json.loads(report.read_text(encoding="utf-8"))
    assert terminal["run_status"] == "completed"
    assert terminal["requests_used"] == 1
    assert terminal["result"]["status"] == "pass"


def test_observed_first_pass_execute_checkpoints_timeout_after_issuance(tmp_path: Path, monkeypatch) -> None:
    script = tmp_path / "replacement.py"
    script.write_text(DEFAULT_BUILD_SEQUENCE, encoding="utf-8")
    report = tmp_path / "observed-timeout.json"
    base = [
        "observed-first-pass", "--record", "box", "--input", str(BOX_STEP), "--data-root", str(tmp_path / "data"),
        "--report", str(report), "--fake-replacement-script", str(script),
    ]
    assert main([*base, "--phase", "prepare"]) == 0

    def timeout_after_issuance(_self, *_args, before_provider_request=None, **_kwargs):
        assert before_provider_request is not None
        before_provider_request()
        raise ProviderRequestTimeoutError("simulated timeout")

    monkeypatch.setattr("brep2code.cli.ObservedBuildLoopRunner.run", timeout_after_issuance)
    assert main([*base, "--phase", "execute"]) == 1

    terminal = json.loads(report.read_text(encoding="utf-8"))
    assert terminal["run_status"] == "interrupted"
    assert terminal["request_state"] == "issued"
    assert terminal["requests_used"] == 1
    assert terminal["interruption"]["code"] == "provider_request_timeout"


def test_observed_development_cli_runs_multiple_cases_without_path_egress(tmp_path: Path, capsys) -> None:
    manifest = tmp_path / "development.json"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "cases": [
                    {"case_id": "box-a", "tier": "P0", "input_step": str(BOX_STEP).replace("\\", "/")},
                    {"case_id": "box-b", "tier": "P0", "input_step": str(BOX_STEP).replace("\\", "/")},
                ],
            }
        ),
        encoding="utf-8",
    )
    script = tmp_path / "replacement.py"
    script.write_text(DEFAULT_BUILD_SEQUENCE, encoding="utf-8")
    data_root = tmp_path / "data"
    report = tmp_path / "report.json"

    exit_code = main(
        [
            "observed-development", "--manifest", str(manifest), "--data-root", str(data_root), "--report", str(report),
            "--max-cases", "2", "--max-rounds", "0", "--executor", "wsl-bwrap", "--fake-replacement-script", str(script),
        ]
    )

    assert exit_code == 0
    assert '"run_status": "completed"' in capsys.readouterr().out
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert [case["status"] for case in payload["cases"]] == ["pass", "pass"]
    telemetry = payload["cases"][0]["telemetry"]
    assert telemetry["schema_version"] == 1
    assert telemetry["request_timing"]["send_offset_ms"] is not None
    assert telemetry["request_timing"]["done_offset_ms"] is not None
    assert telemetry["request_timing"]["first_byte_offset_ms"] is None
    assert telemetry["request_timing"]["token_usage"] is None
    assert telemetry["context_ledger"]["message_count"] == 2
    assert telemetry["context_ledger"]["sections"]["system_instruction"]["chars"] > 0
    assert telemetry["context_ledger"]["sections"]["observation_transcript"]["utf8_bytes"] > 0
    assert telemetry["phase_elapsed_ms"]["provider_wait"] is not None
    assert telemetry["phase_elapsed_ms"]["harness"] is not None
    assert "Generate one complete" not in json.dumps(telemetry)
    assert "input.step" not in json.dumps(telemetry)
    messages = "\n".join(path.read_text(encoding="utf-8") for path in data_root.rglob("llm_messages.jsonl"))
    assert "input.step" not in messages
    assert str(data_root.resolve()) not in messages
    for bundle_path in data_root.rglob("signal_bundle.json"):
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        assert bundle["observation_build_capability"] == {"input_mount_present": False}


def test_observed_development_cli_selects_one_named_case(tmp_path: Path, capsys) -> None:
    manifest = tmp_path / "development.json"
    manifest.write_text(
        json.dumps(
            {"schema_version": 1, "cases": [
                {"case_id": "box-a", "tier": "P0", "input_step": str(BOX_STEP).replace("\\", "/")},
                {"case_id": "box-b", "tier": "P0", "input_step": str(BOX_STEP).replace("\\", "/")},
            ]}
        ),
        encoding="utf-8",
    )
    script = tmp_path / "replacement.py"
    script.write_text(DEFAULT_BUILD_SEQUENCE, encoding="utf-8")
    report = tmp_path / "selected.json"

    exit_code = main([
        "observed-development", "--manifest", str(manifest), "--case-id", "box-b",
        "--data-root", str(tmp_path / "data"), "--report", str(report), "--max-cases", "1",
        "--max-rounds", "0", "--executor", "wsl-bwrap", "--fake-replacement-script", str(script),
    ])

    assert exit_code == 0
    assert '"run_status": "completed"' in capsys.readouterr().out
    assert [case["case_id"] for case in json.loads(report.read_text(encoding="utf-8"))["cases"]] == ["box-b"]


def test_observed_development_checkpoints_timeout_without_retry(tmp_path: Path, capsys, monkeypatch) -> None:
    manifest = tmp_path / "development.json"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "cases": [
                    {"case_id": "box-a", "tier": "P0", "input_step": str(BOX_STEP).replace("\\", "/")},
                    {"case_id": "box-b", "tier": "P0", "input_step": str(BOX_STEP).replace("\\", "/")},
                ],
            }
        ),
        encoding="utf-8",
    )
    script = tmp_path / "replacement.py"
    script.write_text(DEFAULT_BUILD_SEQUENCE, encoding="utf-8")
    report = tmp_path / "timeout-report.json"

    class TimeoutAfterFirstFakeProvider(FakeLLMProvider):
        instance: "TimeoutAfterFirstFakeProvider | None" = None

        def __init__(self, responses) -> None:
            super().__init__(responses)
            type(self).instance = self

        def complete(self, request):
            response = super().complete(request)
            if len(self.requests) == 2:
                raise ProviderRequestTimeoutError(
                    "simulated provider deadline",
                    diagnostics={
                        "last_phase": "http_started",
                        "events": [
                            {"phase": "worker_started", "elapsed_ms": 0},
                            {"phase": "http_started", "elapsed_ms": 1},
                        ],
                        "error_class": "ProviderRequestTimeoutError",
                    },
                )
            return response

    monkeypatch.setattr("brep2code.cli.FakeLLMProvider", TimeoutAfterFirstFakeProvider)

    exit_code = main(
        [
            "observed-development", "--manifest", str(manifest), "--data-root", str(tmp_path / "data"),
            "--report", str(report), "--max-cases", "2", "--max-rounds", "0",
            "--executor", "wsl-bwrap", "--fake-replacement-script", str(script),
        ]
    )

    assert exit_code == 1
    assert TimeoutAfterFirstFakeProvider.instance is not None
    assert len(TimeoutAfterFirstFakeProvider.instance.requests) == 2
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["run_status"] == "interrupted"
    interruption = payload["interruption"]
    assert interruption["code"] == "provider_request_timeout"
    assert interruption["case_id"] == "box-b"
    assert interruption["exception_type"] == "ProviderRequestTimeoutError"
    assert interruption["diagnostics"] == {
        "last_phase": "http_started",
        "events": [{"phase": "worker_started", "elapsed_ms": 0}, {"phase": "http_started", "elapsed_ms": 1}],
        "error_class": "ProviderRequestTimeoutError",
    }
    telemetry = interruption["telemetry"]
    assert telemetry["request_timing"]["send_offset_ms"] is not None
    assert telemetry["request_timing"]["done_offset_ms"] is None
    assert telemetry["request_timing"]["first_byte_offset_ms"] is None
    assert telemetry["request_timing"]["token_usage"] is None
    assert telemetry["phase_elapsed_ms"]["provider_wait"] is not None
    assert "input.step" not in json.dumps(telemetry)
    assert [case["case_id"] for case in payload["cases"]] == ["box-a"]
    assert payload["requests_used"] == 2
    assert payload["requests_remaining"] == 0


def test_observed_development_checkpoint_projects_only_valid_lifecycle_diagnostics() -> None:
    startup = ProviderRequestLifecycleError(
        "worker could not start",
        diagnostics={"last_phase": "worker_phase_unobserved", "events": [], "error_class": "RuntimeError"},
    )
    http_wait = ProviderRequestTimeoutError(
        "provider deadline",
        diagnostics={
            "last_phase": "http_first_response_byte",
            "events": [
                {"phase": "worker_started", "elapsed_ms": 0},
                {"phase": "http_started", "elapsed_ms": 3},
                {"phase": "http_first_response_byte", "elapsed_ms": 4},
            ],
            "error_class": "ProviderRequestTimeoutError",
        },
    )
    worker_error = ProviderRequestLifecycleError(
        "worker returned error",
        diagnostics={
            "last_phase": "http_failed",
            "events": [
                {"phase": "worker_started", "elapsed_ms": 0},
                {"phase": "http_started", "elapsed_ms": 1},
                {"phase": "http_failed", "elapsed_ms": 2},
            ],
            "error_class": "DeepSeekProviderError",
        },
    )

    startup_checkpoint = _provider_interruption("case-startup", startup)
    http_checkpoint = _provider_interruption("case-http", http_wait)
    error_checkpoint = _provider_interruption("case-error", worker_error)

    assert startup_checkpoint["code"] == "provider_request_failed"
    assert startup_checkpoint["diagnostics"] == startup.diagnostics
    assert http_checkpoint["code"] == "provider_request_timeout"
    assert http_checkpoint["diagnostics"] == http_wait.diagnostics
    assert error_checkpoint["code"] == "provider_request_failed"
    assert error_checkpoint["diagnostics"] == worker_error.diagnostics

    malformed = {
        "last_phase": "http_started",
        "events": [{"phase": "http_started", "elapsed_ms": 1, "url": "https://example.invalid"}],
        "error_class": "ProviderRequestTimeoutError",
    }
    assert _sanitize_lifecycle_diagnostics(malformed) is None
