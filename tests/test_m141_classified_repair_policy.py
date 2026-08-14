from pathlib import Path

from brep2code.agent.harness import ManualHarness
from brep2code.agent.provider import FakeLLMProvider, ProviderResponse, ScriptUpdate
from brep2code.agent.repair_policy import ClassifiedRepairRunner, classify_terminal_feedback
from brep2code.storage import RecordStore


def test_classification_is_fail_closed_for_unlocated_sequence_feedback() -> None:
    decision = classify_terminal_feedback({"status": "fail", "repair_classification": "selector_ambiguous"})

    assert decision.route == "stop"
    assert decision.allowed is False
    assert decision.stop_reason == "stop_unsupported"


def test_classification_admits_only_local_execution_failure() -> None:
    decision = classify_terminal_feedback({"status": "fail", "execution": {"exit_code": 1, "timed_out": False}})

    assert decision.classification == "execution_local"
    assert decision.route == "source_only"
    assert decision.max_requests == 1


def test_classification_allows_uncovered_provenance_but_rejects_round_trip() -> None:
    uncovered = classify_terminal_feedback({"status": "fail", "execution": {"exit_code": 1}, "provenance": {"classification": "provenance_unknown", "coverage": False}})
    round_trip = classify_terminal_feedback({"status": "fail", "execution": {"exit_code": 1}, "provenance": {"classification": "round_trip", "coverage": True}})

    assert uncovered.route == "source_only"
    assert round_trip.stop_reason == "stop_policy_rejected"


def test_classified_runner_repairs_admitted_local_failure_with_fake_provider(tmp_path: Path) -> None:
    harness = ManualHarness(store=RecordStore(tmp_path / "data"))
    initial = tmp_path / "broken.py"
    initial.write_text("raise RuntimeError('boom')\n", encoding="utf-8")
    failed = harness.run("m141-source", script=initial)
    provider = FakeLLMProvider([ProviderResponse(provider="fake", model="fake", output_text="edit", script_update=ScriptUpdate(kind="edit", content="from pathlib import Path\nPath('output').mkdir(exist_ok=True)\nPath('output/model.step').write_text('not a step')\n"))])

    result = ClassifiedRepairRunner(harness=harness, provider=provider).run(failed)

    assert result.provider_requests == 1
    assert result.stop_reason == "source_patch_not_converged"
    assert result.result is not None
    assert (failed.revision.traces / "classified_repair.json").exists()
    assert provider.requests[0].metadata == {"policy": "classified-repair-v1", "route": "source_only", "max_requests": 1}


def test_classified_runner_never_calls_provider_for_sandbox_feedback(tmp_path: Path) -> None:
    harness = ManualHarness(store=RecordStore(tmp_path / "data"))
    initial = tmp_path / "broken.py"
    initial.write_text("raise RuntimeError('boom')\n", encoding="utf-8")
    failed = harness.run("m141-sandbox", script=initial)
    failed.signal_bundle["execution"]["sandboxed"] = True
    provider = FakeLLMProvider()

    result = ClassifiedRepairRunner(harness=harness, provider=provider).run(failed)

    assert result.stop_reason == "stop_policy_rejected"
    assert provider.requests == []
