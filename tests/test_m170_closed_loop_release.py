from pathlib import Path

from brep2code.agent import ClosedLoopReleaseRunner, FakeLLMProvider, GuidanceBundle, ManualHarness
from brep2code.agent.provider import ProviderResponse, ScriptUpdate, ToolCall, fake_replacement_response
from brep2code.storage import RecordStore


ROOT = Path(__file__).resolve().parents[1]
CARD_INDEX = ROOT / "runtime_resources/experience-cards/index.json"
CARD = ROOT / "runtime_resources/experience-cards/cards/vertical-cylinder-construction.json"
IDENTITY = {"campaign_id": "m170-offline", "campaign_spec_sha256": "b" * 64}


def _tool(name: str, arguments: dict) -> ProviderResponse:
    return ProviderResponse(provider="fake", model="fake", output_text=f"Call {name}", tool_call=ToolCall(name, arguments))


def _runner(tmp_path: Path, responses: list[ProviderResponse]) -> ClosedLoopReleaseRunner:
    return ClosedLoopReleaseRunner(
        harness=ManualHarness(store=RecordStore(tmp_path / "data")),
        provider=FakeLLMProvider(responses),
    )


def test_m170_composes_declared_probe_card_generation_and_pass(tmp_path: Path) -> None:
    script = (ROOT / "case-library/self-authored/cylinder/reference_build_sequence.py").read_text(encoding="utf-8")
    result = _runner(tmp_path, [
        _tool("probe_summary", {}),
        _tool("get_guidance_card", {"role": "final primitive"}),
        fake_replacement_response(script),
    ]).run(
        "cylinder",
        input_path=ROOT / "case-library/self-authored/cylinder/input.step",
        campaign_identity=IDENTITY,
        observation_session_id="m170-cylinder",
        guidance_bundle=GuidanceBundle.from_paths(CARD_INDEX, CARD),
        selected_guidance_role="final primitive",
    )

    assert result.status == "pass"
    assert result.stop_reason == "stop_pass"
    assert result.provider_completions == 3
    assert result.initial.tool_calls == 2
    assert (result.initial.harness_result.revision.traces / "closed_loop_release.json").is_file()


def test_m170_allows_one_source_edit_after_local_execution_failure(tmp_path: Path) -> None:
    repaired = (ROOT / "case-library/self-authored/cylinder/reference_build_sequence.py").read_text(encoding="utf-8")
    result = _runner(tmp_path, [
        _tool("probe_summary", {}),
        _tool("get_guidance_card", {"role": "final primitive"}),
        fake_replacement_response("raise RuntimeError('broken generation')\n"),
        ProviderResponse(provider="fake", model="fake", output_text="edit", script_update=ScriptUpdate(kind="edit", content=repaired)),
    ]).run(
        "cylinder",
        input_path=ROOT / "case-library/self-authored/cylinder/input.step",
        campaign_identity=IDENTITY,
        observation_session_id="m170-cylinder-repair",
        guidance_bundle=GuidanceBundle.from_paths(CARD_INDEX, CARD),
        selected_guidance_role="final primitive",
    )

    assert result.status == "pass"
    assert result.stop_reason == "pass"
    assert result.provider_completions == 4
    assert result.repair is not None
    assert result.repair.decision.classification == "output_artifact"
