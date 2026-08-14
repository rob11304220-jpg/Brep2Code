from pathlib import Path

from brep2code.agent import FakeLLMProvider, ManualHarness
from brep2code.agent.guidance import GuidanceBundle
from brep2code.agent.provider import ProviderResponse, ToolCall, fake_replacement_response
from brep2code.agent.tool_turn import (
    ToolTurnLimits,
    ToolTurnLoopRunner,
    campaign_identity_from_prepared_checkpoint,
)
from brep2code.scaffold import DEFAULT_BUILD_SEQUENCE
from brep2code.storage import RecordStore


BOX_STEP = Path("case-library/self-authored/box/input.step")
CYLINDER_STEP = Path("case-library/self-authored/cylinder/input.step")
CYLINDER_SCRIPT = Path("case-library/self-authored/cylinder/reference_build_sequence.py")
GUIDANCE_INDEX = Path("runtime_resources/experience-cards/index.json")
GUIDANCE_CARD = Path("runtime_resources/experience-cards/cards/vertical-cylinder-construction.json")
IDENTITY = {"campaign_id": "offline-m140", "campaign_spec_sha256": "a" * 64}


def _tool(name: str, arguments: dict) -> ProviderResponse:
    return ProviderResponse(provider="fake", model="fake", output_text=f"Call {name}", tool_call=ToolCall(name, arguments))


def test_tool_turn_loop_continues_after_probe_then_records_execution_feedback(tmp_path: Path) -> None:
    provider = FakeLLMProvider([_tool("probe_summary", {}), fake_replacement_response(DEFAULT_BUILD_SEQUENCE)])
    runner = ToolTurnLoopRunner(harness=ManualHarness(store=RecordStore(tmp_path / "data")), provider=provider)

    result = runner.run("box", input_path=BOX_STEP, campaign_identity=IDENTITY, observation_session_id="m140-box")

    assert result.status == "pass"
    assert result.provider_requests == 2
    assert result.tool_calls == 1
    assert result.stop_reason == "execution_feedback"
    assert result.harness_result is not None
    assert result.trace[-1]["kind"] == "execution_feedback"
    request = provider.requests[1]
    assert request.messages[-1].role == "tool"
    assert request.messages[-1].name == "probe_summary"
    assert "input.step" not in request.messages[-1].content
    assert (result.harness_result.revision.traces / "tool_turn_trace.json").is_file()


def test_tool_turn_loop_rejects_unselected_or_wrong_card_without_egress(tmp_path: Path) -> None:
    provider = FakeLLMProvider([
        _tool("get_guidance_card", {"role": "single boolean-cut tool"}),
        fake_replacement_response(DEFAULT_BUILD_SEQUENCE),
    ])
    runner = ToolTurnLoopRunner(harness=ManualHarness(store=RecordStore(tmp_path / "data")), provider=provider)

    result = runner.run("box", input_path=BOX_STEP, campaign_identity=IDENTITY, observation_session_id="m140-card")

    assert result.status == "pass"
    assert result.trace[0]["kind"] == "tool"
    assert provider.requests[1].messages[-1].content == '{"error":{"code":"guidance_not_selected","message":"requested card is not selected for this campaign"},"ok":false,"tool":"get_guidance_card"}'


def test_tool_turn_loop_allows_only_the_frozen_card_role(tmp_path: Path) -> None:
    provider = FakeLLMProvider([
        _tool("get_guidance_card", {"role": "final primitive"}),
        fake_replacement_response(CYLINDER_SCRIPT.read_text(encoding="utf-8")),
    ])
    runner = ToolTurnLoopRunner(harness=ManualHarness(store=RecordStore(tmp_path / "data")), provider=provider)

    result = runner.run(
        "cylinder",
        input_path=CYLINDER_STEP,
        campaign_identity=IDENTITY,
        observation_session_id="m140-cylinder",
        guidance_bundle=GuidanceBundle.from_paths(GUIDANCE_INDEX, GUIDANCE_CARD),
        selected_guidance_role="final primitive",
    )

    assert result.status == "pass"
    assert result.tool_calls == 1
    assert "vertical-cylinder-construction" in provider.requests[1].messages[-1].content


def test_tool_turn_loop_stops_at_global_tool_budget(tmp_path: Path) -> None:
    provider = FakeLLMProvider([_tool("probe_summary", {}), _tool("probe_summary", {})])
    runner = ToolTurnLoopRunner(
        harness=ManualHarness(store=RecordStore(tmp_path / "data")),
        provider=provider,
        limits=ToolTurnLimits(max_turns=3, max_tool_calls=1, max_tool_result_bytes=12_000),
    )

    result = runner.run("box", input_path=BOX_STEP, campaign_identity=IDENTITY, observation_session_id="m140-budget")

    assert result.status == "provider_error"
    assert result.stop_reason == "tool_call_limit_exceeded"
    assert result.provider_requests == 1
    assert result.tool_calls == 1


def test_tool_turn_loop_returns_a_sanitized_malformed_tool_error_then_continues(tmp_path: Path) -> None:
    provider = FakeLLMProvider([
        _tool("probe_topology", {"selector": "vertex"}),
        fake_replacement_response(DEFAULT_BUILD_SEQUENCE),
    ])
    runner = ToolTurnLoopRunner(harness=ManualHarness(store=RecordStore(tmp_path / "data")), provider=provider)

    result = runner.run("box", input_path=BOX_STEP, campaign_identity=IDENTITY, observation_session_id="m140-malformed")

    assert result.status == "pass"
    assert '"code":"invalid_selector"' in provider.requests[1].messages[-1].content


def test_campaign_identity_accepts_only_a_fresh_m139_checkpoint() -> None:
    checkpoint = {
        "campaign_id": "offline-m140",
        "campaign_spec_sha256": "a" * 64,
        "request_state": "prepared",
        "requests_used": 0,
    }

    assert campaign_identity_from_prepared_checkpoint(checkpoint) == IDENTITY
    checkpoint["requests_used"] = 1
    try:
        campaign_identity_from_prepared_checkpoint(checkpoint)
    except ValueError as exc:
        assert "fresh prepared" in str(exc)
    else:
        raise AssertionError("expected used checkpoint rejection")
