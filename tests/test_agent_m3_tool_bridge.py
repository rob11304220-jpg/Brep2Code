from __future__ import annotations

import json
from pathlib import Path

from brep2code.agent import build_observation_context
from brep2code.agent.tools import BRepToolBridge
from brep2code.storage import RecordStore


BOX_STEP = Path("case-library/self-authored/box/input.step")


def _store_with_input(tmp_path: Path) -> RecordStore:
    store = RecordStore(tmp_path / "data")
    record = store.ensure_record("box-smoke")
    destination = record.input_dir / BOX_STEP.name
    destination.write_bytes(BOX_STEP.read_bytes())
    return store


def test_tool_registry_lists_probe_tools_and_schemas() -> None:
    bridge = BRepToolBridge()

    specs = {spec.name: spec for spec in bridge.specs()}

    assert set(specs) == {"probe_summary", "probe_topology", "probe_entity", "sample_entity"}
    assert specs["probe_topology"].schema["properties"]["selector"]["enum"] == [
        "all",
        "solid",
        "shell",
        "face",
        "edge",
    ]
    assert specs["sample_entity"].schema["required"] == ["entity_id", "samples"]


def test_tool_bridge_rejects_unknown_tool_and_invalid_arguments(tmp_path: Path) -> None:
    bridge = BRepToolBridge(store=_store_with_input(tmp_path), max_samples=4)

    unknown = bridge.call("box-smoke", "missing_tool", {})
    bad_selector = bridge.call("box-smoke", "probe_topology", {"selector": "vertex"})
    too_many_samples = bridge.call(
        "box-smoke",
        "sample_entity",
        {"entity_id": "face:000001", "samples": 5},
    )

    assert unknown.error["code"] == "unknown_tool"
    assert bad_selector.error["code"] == "invalid_selector"
    assert too_many_samples.error["code"] == "invalid_sample_count"


def test_tool_bridge_dispatches_probe_and_records_trace(tmp_path: Path) -> None:
    store = _store_with_input(tmp_path)
    bridge = BRepToolBridge(store=store, result_limit_bytes=12_000)
    trace_dir = tmp_path / "traces"

    result = bridge.call("box-smoke", "probe_summary", trace_dir=trace_dir)

    assert result.ok is True
    assert result.result["counts"]["face"] == 6
    lines = (trace_dir / "tool_calls.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    trace = json.loads(lines[0])
    assert trace["tool"] == "probe_summary"
    assert trace["ok"] is True
    assert trace["result"]["counts"]["edge"] == 24


def test_tool_bridge_bounds_oversized_results_with_full_trace(tmp_path: Path) -> None:
    store = _store_with_input(tmp_path)
    bridge = BRepToolBridge(store=store, result_limit_bytes=100)
    trace_dir = tmp_path / "traces"

    result = bridge.call(
        "box-smoke",
        "probe_topology",
        {"selector": "all", "max_entities": 80},
        trace_dir=trace_dir,
    )

    assert result.ok is True
    assert result.trace_path is not None
    assert Path(result.trace_path).exists()
    assert result.result["truncated"] is True
    trace = json.loads((trace_dir / "tool_calls.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert trace["trace_path"] == result.trace_path


def test_tool_bridge_enforces_call_count_limit(tmp_path: Path) -> None:
    bridge = BRepToolBridge(store=_store_with_input(tmp_path), max_calls=1)

    first = bridge.call("box-smoke", "probe_summary")
    second = bridge.call("box-smoke", "probe_summary")

    assert first.ok is True
    assert second.ok is False
    assert second.error["code"] == "tool_call_limit_exceeded"


def test_observation_envelope_is_sanitized_and_revision_traceable(tmp_path: Path) -> None:
    store = _store_with_input(tmp_path)
    bridge = BRepToolBridge(store=store)
    trace_dir = tmp_path / "revision" / "traces"

    envelope = bridge.observe("box-smoke", "obs-1", "call-1", "probe_summary", trace_dir=trace_dir)

    assert envelope["ok"] is True
    assert "input" not in envelope["data"]
    assert "trace_path" not in envelope["data"]
    assert len(envelope["response_sha256"]) == 64
    trace = json.loads((trace_dir / "observation_queries.jsonl").read_text(encoding="utf-8"))
    assert trace["observation_session_id"] == "obs-1"
    assert "input.step" not in (trace_dir / "observation_queries.jsonl").read_text(encoding="utf-8")


def test_observation_context_rejects_path_bearing_payloads() -> None:
    safe = [{"schema_version": 1, "observation_session_id": "obs-1", "data": {"counts": {"face": 6}}}]

    assert "observation_transcript" in build_observation_context(safe)
    try:
        build_observation_context([{**safe[0], "data": {"input": "C:/secret.step"}}])
    except ValueError as exc:
        assert str(exc) == "observation_context_contains_forbidden_field"
    else:
        raise AssertionError("expected path-bearing observation to be rejected")
