from __future__ import annotations

import json
from pathlib import Path
from queue import Empty

from brep2code.agent.provider import DeepSeekProvider, FakeLLMProvider, LLMMessage, ProviderRequest, ProviderResponse, fake_replacement_response
from brep2code.agent.repair import (
    ProviderRequestLifecycleError,
    ProviderRequestTimeoutError,
    RepairLoopRunner,
    _complete_provider,
    repair_result_to_dict,
)
from brep2code.cli import main
from brep2code.storage import RecordStore


BOX_STEP = Path("case-library/self-authored/box/input.step")


PASSING_SCRIPT = (
    "from pathlib import Path\n"
    "from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox\n"
    "from OCP.IFSelect import IFSelect_RetDone\n"
    "from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer\n"
    "shape = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()\n"
    "Path('output').mkdir(exist_ok=True)\n"
    "writer = STEPControl_Writer()\n"
    "writer.Transfer(shape, STEPControl_AsIs)\n"
    "status = writer.Write('output/model.step')\n"
    "if status != IFSelect_RetDone:\n"
    "    raise RuntimeError('failed to write STEP')\n"
)


def test_repair_loop_repairs_failing_script_with_fake_provider(tmp_path: Path) -> None:
    initial = tmp_path / "broken_build.py"
    initial.write_text("raise RuntimeError('boom')\n", encoding="utf-8")
    provider = FakeLLMProvider([fake_replacement_response(PASSING_SCRIPT)])
    runner = RepairLoopRunner(
        harness=None,
        provider=provider,
    )
    runner.harness.store = RecordStore(tmp_path / "data")

    result = runner.run("box-smoke", initial, input_path=BOX_STEP, max_rounds=1)

    assert result.status == "pass"
    assert result.stop_reason == "pass"
    assert result.provider_requests == 1
    assert [attempt.status for attempt in result.attempts] == ["fail", "pass"]
    assert len({attempt.revision_id for attempt in result.attempts}) == 2
    first_revision = Path(result.attempts[0].signal_bundle_path).parent
    second_revision = Path(result.attempts[1].signal_bundle_path).parent
    assert (first_revision / "workspace" / "build_sequence.py").read_text(encoding="utf-8") == (
        "raise RuntimeError('boom')\n"
    )
    assert PASSING_SCRIPT in (second_revision / "workspace" / "build_sequence.py").read_text(encoding="utf-8")
    assert (first_revision / "traces" / "llm_messages.jsonl").exists()
    assert (first_revision / "traces" / "provider_response.json").exists()
    assert (first_revision / "traces" / "script_update.json").exists()
    request_text = provider.requests[0].messages[1].content
    assert "RuntimeError" in request_text
    assert "script_exit_code" in request_text
    assert "repair_hints" in request_text
    assert '"input_summary"' in request_text
    assert '"max": [' in request_text


def test_repair_loop_stops_on_max_rounds(tmp_path: Path) -> None:
    initial = tmp_path / "broken_build.py"
    initial.write_text("raise RuntimeError('boom')\n", encoding="utf-8")
    runner = RepairLoopRunner(
        provider=FakeLLMProvider([fake_replacement_response("raise RuntimeError('still broken')\n")])
    )
    runner.harness.store = RecordStore(tmp_path / "data")

    result = runner.run("box-smoke", initial, max_rounds=1)

    assert result.status == "fail"
    assert result.stop_reason == "max_rounds"
    assert result.provider_requests == 1
    assert [attempt.status for attempt in result.attempts] == ["fail", "fail"]


def test_repair_loop_reports_missing_provider_script_update(tmp_path: Path) -> None:
    initial = tmp_path / "broken_build.py"
    initial.write_text("raise RuntimeError('boom')\n", encoding="utf-8")
    runner = RepairLoopRunner(
        provider=FakeLLMProvider([ProviderResponse(provider="fake", model="fake-repair", output_text="no edit")])
    )
    runner.harness.store = RecordStore(tmp_path / "data")

    result = runner.run("box-smoke", initial, max_rounds=1)

    assert result.status == "provider_error"
    assert result.stop_reason == "missing_script_update"
    assert result.provider_requests == 1
    assert result.error["code"] == "missing_script_update"
    payload = repair_result_to_dict(result)
    assert payload["attempts"][0]["status"] == "fail"
    trace = json.loads(
        (Path(result.attempts[0].signal_bundle_path).parent / "traces" / "provider_response.json").read_text(
            encoding="utf-8"
        )
    )
    assert trace["response"]["output_text"] == "no edit"


def test_repair_cli_runs_local_fake_provider_loop(tmp_path: Path, capsys) -> None:
    initial = tmp_path / "broken_build.py"
    initial.write_text("raise RuntimeError('boom')\n", encoding="utf-8")
    replacement = tmp_path / "replacement_build.py"
    replacement.write_text(PASSING_SCRIPT, encoding="utf-8")

    exit_code = main(
        [
            "repair",
            "--record",
            "box-smoke",
            "--script",
            str(initial),
            "--fake-replacement-script",
            str(replacement),
            "--input",
            str(BOX_STEP),
            "--data-root",
            str(tmp_path / "data"),
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["status"] == "pass"
    assert [attempt["status"] for attempt in payload["attempts"]] == ["fail", "pass"]


def test_repair_cli_reports_missing_deepseek_configuration(tmp_path: Path, capsys, monkeypatch) -> None:
    initial = tmp_path / "broken_build.py"
    initial.write_text("raise RuntimeError('boom')\n", encoding="utf-8")
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    exit_code = main(
        [
            "repair",
            "--provider",
            "deepseek",
            "--record",
            "deepseek-smoke",
            "--script",
            str(initial),
            "--env-file",
            str(tmp_path / "missing.env"),
            "--data-root",
            str(tmp_path / "data"),
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 2
    assert payload["status"] == "configuration_error"
    assert "DEEPSEEK_API_KEY" in payload["error"]


def test_provider_worker_start_failure_has_sanitized_lifecycle_diagnostics(monkeypatch) -> None:
    monkeypatch.setattr("brep2code.agent.repair.mp.get_context", lambda _method: _WorkerContext(_StartFailureProcess()))

    try:
        _complete_provider(_deepseek_provider(), _provider_request(), timeout_seconds=7)
    except ProviderRequestLifecycleError as exc:
        assert exc.diagnostics == {
            "last_phase": "worker_phase_unobserved",
            "events": [],
            "error_class": "RuntimeError",
        }
    else:
        raise AssertionError("expected startup failure")


def test_provider_http_wait_timeout_preserves_worker_phases(monkeypatch) -> None:
    process = _WorkerProcess(alive=True)
    monkeypatch.setattr("brep2code.agent.repair.mp.get_context", lambda _method: _WorkerContext(process))
    monkeypatch.setattr("brep2code.agent.repair._deepseek_complete_worker", _http_wait_worker)

    try:
        _complete_provider(_deepseek_provider(), _provider_request(), timeout_seconds=7)
    except ProviderRequestTimeoutError as exc:
        assert exc.diagnostics == {
            "last_phase": "http_first_response_byte",
            "events": [
                {"phase": "worker_started", "elapsed_ms": 0},
                {"phase": "http_started", "elapsed_ms": 1},
                {"phase": "http_first_response_byte", "elapsed_ms": 2},
            ],
            "error_class": "ProviderRequestTimeoutError",
        }
    else:
        raise AssertionError("expected provider timeout")
    assert process.terminated is True


def test_provider_worker_error_preserves_phase_and_error_class(monkeypatch) -> None:
    monkeypatch.setattr("brep2code.agent.repair.mp.get_context", lambda _method: _WorkerContext(_WorkerProcess()))
    monkeypatch.setattr("brep2code.agent.repair._deepseek_complete_worker", _error_worker)

    try:
        _complete_provider(_deepseek_provider(), _provider_request(), timeout_seconds=7)
    except ProviderRequestLifecycleError as exc:
        assert exc.diagnostics == {
            "last_phase": "http_failed",
            "events": [
                {"phase": "worker_started", "elapsed_ms": 0},
                {"phase": "http_started", "elapsed_ms": 1},
                {"phase": "http_failed", "elapsed_ms": 2},
            ],
            "error_class": "DeepSeekProviderError",
        }
    else:
        raise AssertionError("expected worker error")


def _deepseek_provider() -> DeepSeekProvider:
    return DeepSeekProvider(api_key="test-key")


def _provider_request() -> ProviderRequest:
    return ProviderRequest(model="deepseek-v4-pro", messages=[LLMMessage(role="user", content="offline simulation")])


class _WorkerQueue:
    def __init__(self) -> None:
        self.items: list[tuple[str, object]] = []

    def put(self, item: tuple[str, object]) -> None:
        self.items.append(item)

    def get(self, timeout: int | None = None):
        if not self.items:
            raise Empty
        return self.items.pop(0)

    def get_nowait(self):
        return self.get()


class _WorkerProcess:
    def __init__(self, *, alive: bool = False) -> None:
        self.alive = alive
        self.terminated = False

    def configure(self, target, args) -> None:
        self.target = target
        self.args = args

    def start(self) -> None:
        self.target(*self.args)

    def join(self, timeout=None) -> None:
        pass

    def is_alive(self) -> bool:
        return self.alive and not self.terminated

    def terminate(self) -> None:
        self.terminated = True


class _StartFailureProcess:
    def configure(self, target, args) -> None:
        pass

    def start(self) -> None:
        raise RuntimeError("offline startup failure")


class _WorkerContext:
    def __init__(self, process) -> None:
        self.queue = _WorkerQueue()
        self.process = process

    def Queue(self):
        return self.queue

    def Process(self, *, target, args):
        self.process.configure(target, args)
        return self.process


def _http_wait_worker(_provider, _request, result_queue) -> None:
    result_queue.put(("phase", {"phase": "worker_started", "elapsed_ms": 0}))
    result_queue.put(("phase", {"phase": "http_started", "elapsed_ms": 1}))
    result_queue.put(("phase", {"phase": "http_first_response_byte", "elapsed_ms": 2}))


def _error_worker(_provider, _request, result_queue) -> None:
    result_queue.put(("phase", {"phase": "worker_started", "elapsed_ms": 0}))
    result_queue.put(("phase", {"phase": "http_started", "elapsed_ms": 1}))
    result_queue.put(("phase", {"phase": "http_failed", "elapsed_ms": 2}))
    result_queue.put(("error", {"error_class": "DeepSeekProviderError", "message": "request failed"}))
