from __future__ import annotations

import json
from pathlib import Path

from brep2code.agent.harness import ManualHarness
from brep2code.brep import (
    ProbeError,
    discover_input_file,
    load_model,
    probe_entity,
    probe_summary,
    probe_topology,
    sample_entity,
)
from brep2code.brep.serialize import bounded_result
from brep2code.cli import main
from brep2code.storage import RecordStore


BOX_STEP = Path("case-library/self-authored/box/input.step")


def test_probe_summary_reads_step_fixture() -> None:
    model = load_model(BOX_STEP)

    summary = probe_summary(model)

    assert summary["ok"] is True
    assert summary["format"] == "step"
    assert summary["counts"]["face"] == 6
    assert summary["counts"]["edge"] == 24
    assert summary["bbox"]["min"] == [0.0, 0.0, 0.0]
    assert summary["bbox"]["max"] == [10.0, 20.0, 30.0]


def test_topology_entity_and_sampling_are_available() -> None:
    model = load_model(BOX_STEP)

    topology = probe_topology(model, selector="face", max_entities=2)
    entity = probe_entity(model, "face:000001")
    samples = sample_entity(model, "face:000001", 3)
    edge_samples = sample_entity(model, "edge:000001", 2)

    assert topology["ok"] is True
    assert topology["returned"] == 2
    assert topology["truncated"] is True
    assert entity["ok"] is True
    assert entity["entity_type"] == "face"
    assert "area" in entity
    assert samples["ok"] is True
    assert samples["returned"] == 3
    assert len(samples["samples"]) == 3
    assert edge_samples["ok"] is True
    assert edge_samples["entity_type"] == "edge"
    assert edge_samples["returned"] == 2


def test_probe_reports_invalid_entity_as_structured_error() -> None:
    model = load_model(BOX_STEP)

    try:
        probe_entity(model, "face:999999")
    except ProbeError as exc:
        payload = exc.to_result()
    else:
        raise AssertionError("expected ProbeError")

    assert payload == {
        "ok": False,
        "error": {"code": "entity_not_found", "message": "unknown entity id: face:999999"},
    }


def test_missing_input_is_structured_error() -> None:
    try:
        load_model(BOX_STEP.parent / "missing.step")
    except ProbeError as exc:
        payload = exc.to_result()
    else:
        raise AssertionError("expected ProbeError")

    assert payload["ok"] is False
    assert payload["error"]["code"] == "input_not_found"


def test_result_size_limit_can_write_trace(tmp_path: Path) -> None:
    model = load_model(BOX_STEP)
    trace_dir = tmp_path / "traces"

    result = probe_topology(model, max_entities=1000, trace_dir=trace_dir, limit_bytes=100)

    assert result["ok"] is True
    assert result["truncated"] is True
    trace_path = Path(result["trace_path"])
    assert trace_path.exists()
    full_payload = json.loads(trace_path.read_text(encoding="utf-8"))
    assert full_payload["ok"] is True
    assert full_payload["counts"]["face"] == 6


def test_bounded_result_without_trace_returns_structured_overflow() -> None:
    result = bounded_result({"ok": True, "payload": "x" * 1000}, limit_bytes=100)

    assert result["ok"] is False
    assert result["error"]["code"] == "result_too_large"


def test_record_input_discovery_and_run_input_copy(tmp_path: Path) -> None:
    store = RecordStore(tmp_path / "data")
    harness = ManualHarness(store=store)

    result = harness.run("box-smoke", input_path=BOX_STEP)
    discovered = discover_input_file(result.record.input_dir)

    assert discovered.name == "input.step"
    assert discovered.exists()


def test_probe_cli_with_explicit_input(capsys) -> None:
    exit_code = main(["probe", "--input", str(BOX_STEP)])

    output = capsys.readouterr().out
    payload = json.loads(output)
    assert exit_code == 0
    assert payload["ok"] is True
    assert payload["counts"]["face"] == 6


def test_probe_cli_with_record_input(tmp_path: Path, capsys) -> None:
    harness = ManualHarness(store=RecordStore(tmp_path / "data"))
    harness.run("box-smoke", input_path=BOX_STEP)

    exit_code = main(["probe", "--record", "box-smoke", "--data-root", str(tmp_path / "data")])

    output = capsys.readouterr().out
    payload = json.loads(output)
    assert exit_code == 0
    assert payload["ok"] is True
    assert payload["file_name"] == "input.step"
