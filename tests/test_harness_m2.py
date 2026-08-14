from __future__ import annotations

import json
from pathlib import Path
import shutil
import time

from brep2code.agent import harness as harness_module
from brep2code.agent.harness import ManualHarness, _safe_probe_summary
from brep2code.brep.safe_probe import (
    INPUT_PROBE_TIMEOUT_SECONDS,
    OUTPUT_PROBE_TIMEOUT_SECONDS,
    safe_probe_summary as actual_safe_probe_summary,
)
from brep2code.storage import RecordStore
from brep2code.cad import ExecutionResult


BOX_STEP = Path("case-library/self-authored/box/input.step")


def _slow_probe_worker(_path: str, _trace: str, _result_queue) -> None:
    time.sleep(2)


class _ProvenanceExecutor:
    """Deterministic executor double for provenance classification tests."""

    def __init__(self, *, normal_accesses: list[str] | None = None, coverage: bool = True) -> None:
        self.normal_accesses = normal_accesses or []
        self.coverage = coverage
        self.calls: list[Path | None] = []

    def run(
        self,
        workspace: Path,
        script_name: str = "build_sequence.py",
        *,
        timeout: int,
        input_path: Path | None,
        trace_input_access: bool,
    ):
        self.calls.append(input_path)
        output = workspace / "output" / "model.step"
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(BOX_STEP, output)
        trace_path = workspace / "intermediates" / "provenance-input-access.log"
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        is_normal_run = input_path is not None
        accesses = self.normal_accesses if is_normal_run else []
        if self.coverage:
            trace_path.write_text("coverage=active\n" + "\n".join(accesses), encoding="utf-8")
        return ExecutionResult(
            command=["test-executor", script_name],
            cwd=workspace,
            exit_code=0,
            stdout="",
            stderr="",
            duration_seconds=0.01,
            sandbox_backend="wsl-bwrap",
            sandboxed=True,
            provenance_trace_path=str(trace_path) if self.coverage else None,
            provenance_input_accesses=accesses,
            provenance_coverage=self.coverage,
        )


def test_harness_gates_default_step_output_against_box_input(tmp_path: Path) -> None:
    harness = ManualHarness(store=RecordStore(tmp_path / "data"))

    result = harness.run("box-smoke", input_path=BOX_STEP)

    assert result.status == "pass"
    bundle = json.loads(result.revision.signal_bundle.read_text(encoding="utf-8"))
    gates = {gate["name"]: gate for gate in bundle["gates"]}
    assert bundle["probes"]["input_summary"]["ok"] is True
    assert bundle["probes"]["output_summary"]["ok"] is True
    assert gates["output_model_step_readable"]["status"] == "pass"
    assert gates["bbox_delta"]["status"] == "pass"
    assert gates["volume_delta"]["status"] == "pass"
    assert gates["topology_count_delta"]["status"] == "pass"


def test_harness_reports_unreadable_output_step(tmp_path: Path) -> None:
    script = tmp_path / "bad_step.py"
    script.write_text(
        "from pathlib import Path\n"
        "out = Path('output')\n"
        "out.mkdir(exist_ok=True)\n"
        "(out / 'model.step').write_text('not a real step file', encoding='utf-8')\n",
        encoding="utf-8",
    )
    harness = ManualHarness(store=RecordStore(tmp_path / "data"))

    result = harness.run("bad-output", script=script, input_path=BOX_STEP)

    assert result.status == "fail"
    gates = {gate["name"]: gate for gate in result.signal_bundle["gates"]}
    assert gates["output_model_step_exists"]["status"] == "pass"
    assert gates["output_model_step_readable"]["status"] == "fail"
    assert result.signal_bundle["probes"]["output_summary"]["ok"] is False


def test_harness_rejects_unsupported_cad_import_before_executor_runs(tmp_path: Path) -> None:
    script = tmp_path / "cadquery_build.py"
    script.write_text("import cadquery as cq\nshape = cq.Workplane('XY')\n", encoding="utf-8")
    executor = _ProvenanceExecutor()

    result = ManualHarness(store=RecordStore(tmp_path / "data"), executor=executor).run(
        "unsupported-cad-import", script=script, input_path=BOX_STEP
    )

    contract = result.signal_bundle["execution"]["build_script_contract"]
    gates = {gate["name"]: gate for gate in result.signal_bundle["gates"]}
    assert result.status == "fail"
    assert executor.calls == []
    assert contract["status"] == "fail"
    assert contract["violations"] == [
        {
            "code": "unsupported_cad_import",
            "line": 1,
            "module": "cadquery",
            "message": "cadquery is unavailable; use installed OCP bindings instead",
        }
    ]
    assert result.signal_bundle["execution"]["sandbox_termination_reason"] == "contract_rejected"
    assert gates["script_exit_code"]["metric"] == {"exit_code": 126}
    assert result.signal_bundle["provenance"]["absent_input_control"] == {
        "status": "not_run",
        "reason": "build_script_contract_rejected",
    }
    assert any("OCP" in hint for hint in result.signal_bundle["repair_hints"])


def test_harness_accepts_ocp_script_contract(tmp_path: Path) -> None:
    script = tmp_path / "ocp_build.py"
    script.write_text("from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox\n", encoding="utf-8")
    executor = _ProvenanceExecutor()

    result = ManualHarness(store=RecordStore(tmp_path / "data"), executor=executor).run(
        "ocp-script", script=script, input_path=BOX_STEP
    )

    assert result.status == "pass"
    assert len(executor.calls) == 2
    assert result.signal_bundle["execution"]["build_script_contract"] == {
        "version": "build-script-api-v1",
        "status": "pass",
        "violations": [],
    }


def test_harness_rejects_unavailable_ocp_symbol_before_executor_runs(tmp_path: Path) -> None:
    script = tmp_path / "unsupported_ocp_symbol.py"
    script.write_text("from OCP.gp import gp_DZ\n", encoding="utf-8")
    executor = _ProvenanceExecutor()

    result = ManualHarness(store=RecordStore(tmp_path / "data"), executor=executor).run(
        "unsupported-ocp-symbol", script=script, input_path=BOX_STEP
    )

    assert result.status == "fail"
    assert executor.calls == []
    assert result.signal_bundle["execution"]["build_script_contract"]["violations"] == [{
        "code": "unsupported_ocp_symbol", "line": 1, "module": "OCP.gp", "symbol": "gp_DZ",
        "message": "gp_DZ is unavailable from OCP.gp; use installed OCP bindings only",
    }]


def test_harness_rejects_m127_stepcontrol_symbol_without_downstream_inference(tmp_path: Path) -> None:
    """Keep M127's static API class separate from executor and gate outcomes."""

    script = tmp_path / "m127_unsupported_stepcontrol_symbol.py"
    script.write_text(
        "from OCP.STEPControl import STEPControl_STEPModelType\n",
        encoding="utf-8",
    )
    executor = _ProvenanceExecutor()

    result = ManualHarness(store=RecordStore(tmp_path / "data"), executor=executor).run(
        "m127-unsupported-stepcontrol-symbol", script=script, input_path=BOX_STEP
    )

    execution = result.signal_bundle["execution"]
    gates = {gate["name"]: gate for gate in result.signal_bundle["gates"]}
    assert result.status == "fail"
    assert executor.calls == []
    assert execution["sandbox_termination_reason"] == "contract_rejected"
    assert execution["build_script_contract"]["violations"] == [{
        "code": "unsupported_ocp_symbol",
        "line": 1,
        "module": "OCP.STEPControl",
        "symbol": "STEPControl_STEPModelType",
        "message": (
            "STEPControl_STEPModelType is unavailable from OCP.STEPControl; "
            "use installed OCP bindings only"
        ),
    }]
    assert result.signal_bundle["provenance"]["absent_input_control"] == {
        "status": "not_run",
        "reason": "build_script_contract_rejected",
    }
    assert result.signal_bundle["repair_hints"][0] == (
        "Use only installed OCP modules and symbols; cadquery, OCC, and unavailable OCP names are unsupported."
    )
    assert gates["bbox_delta"]["status"] == "skip"
    assert gates["volume_delta"]["status"] == "skip"
    assert gates["topology_count_delta"]["status"] == "skip"


def test_probe_summary_timeout_is_structured_and_bounded(tmp_path: Path) -> None:
    result = _safe_probe_summary(
        BOX_STEP,
        tmp_path,
        timeout_seconds=1,
        worker=_slow_probe_worker,
    )

    assert result["ok"] is False
    assert result["error"]["code"] == "probe_timeout"


def test_harness_fails_when_input_probe_is_unavailable_and_keeps_output_deadline(tmp_path: Path, monkeypatch) -> None:
    timeouts: list[int] = []

    def unavailable_input(path: Path, trace_dir: Path, *, timeout_seconds: int) -> dict:
        timeouts.append(timeout_seconds)
        if path.name == "input.step":
            return {"ok": False, "input": str(path), "error": {"code": "probe_timeout", "message": "timeout"}}
        return actual_safe_probe_summary(path, trace_dir, timeout_seconds=timeout_seconds)

    monkeypatch.setattr(harness_module, "safe_probe_summary", unavailable_input)
    harness = ManualHarness(store=RecordStore(tmp_path / "data"))

    result = harness.run("input-probe-timeout", input_path=BOX_STEP)
    gates = {gate["name"]: gate for gate in result.signal_bundle["gates"]}

    assert result.status == "fail"
    assert timeouts == [INPUT_PROBE_TIMEOUT_SECONDS, OUTPUT_PROBE_TIMEOUT_SECONDS]
    assert gates["input_model_step_readable"]["status"] == "fail"
    assert gates["bbox_delta"]["status"] == "skip"
    assert gates["volume_delta"]["status"] == "skip"
    assert gates["topology_count_delta"]["status"] == "skip"


def test_harness_classifies_observed_child_input_read_as_round_trip(tmp_path: Path) -> None:
    executor = _ProvenanceExecutor(normal_accesses=["pid=42 path=/input/model.step"])
    result = ManualHarness(store=RecordStore(tmp_path / "data"), executor=executor).run("child-read", input_path=BOX_STEP)

    provenance = result.signal_bundle["provenance"]
    assert result.status == "pass"
    assert provenance["version"] == "reconstruction-provenance-v1"
    assert provenance["classification"] == "round_trip"
    assert provenance["normal_input_accesses"] == ["pid=42 path=/input/model.step"]
    assert provenance["absent_input_control"] == {"status": "not_run", "reason": "normal_input_read"}
    assert len(executor.calls) == 1


def test_harness_classifies_attested_no_read_control_as_independent(tmp_path: Path) -> None:
    executor = _ProvenanceExecutor()
    result = ManualHarness(store=RecordStore(tmp_path / "data"), executor=executor).run("independent", input_path=BOX_STEP)

    provenance = result.signal_bundle["provenance"]
    assert result.status == "pass"
    assert provenance["classification"] == "independent_reconstruction"
    assert provenance["coverage_attestation"] == {"normal_run": True, "absent_input_control": True}
    assert provenance["absent_input_control"]["status"] == "pass"
    assert executor.calls[1] is None


def test_harness_fails_closed_when_trace_coverage_is_unavailable(tmp_path: Path) -> None:
    executor = _ProvenanceExecutor(coverage=False)
    result = ManualHarness(store=RecordStore(tmp_path / "data"), executor=executor).run("coverage-failure", input_path=BOX_STEP)

    provenance = result.signal_bundle["provenance"]
    assert result.status == "pass"
    assert provenance["classification"] == "provenance_unknown"
    assert provenance["coverage_attestation"] == {"normal_run": False}
    assert provenance["absent_input_control"] == {"status": "not_run", "reason": "trace_unavailable"}
    assert len(executor.calls) == 1


def test_tool_assisted_build_mode_never_mounts_original_input(tmp_path: Path) -> None:
    executor = _ProvenanceExecutor()
    result = ManualHarness(store=RecordStore(tmp_path / "data"), executor=executor).run(
        "no-input-build", input_path=BOX_STEP, build_without_input=True
    )

    assert result.status == "pass"
    assert executor.calls[0] is None
    assert result.signal_bundle["observation_build_capability"] == {"input_mount_present": False}
    assert result.signal_bundle["provenance"]["classification"] == "independent_reconstruction"


def test_harness_records_sanitized_observation_context(tmp_path: Path) -> None:
    executor = _ProvenanceExecutor()
    envelopes = [{"schema_version": 1, "observation_session_id": "obs-1", "call_id": "call-1", "data": {"counts": {"face": 6}}}]
    result = ManualHarness(store=RecordStore(tmp_path / "data"), executor=executor).run(
        "observed-build", input_path=BOX_STEP, build_without_input=True, observation_envelopes=envelopes
    )

    observation = result.signal_bundle["observation"]
    assert observation["session_id"] == "obs-1"
    context = Path(observation["context_path"]).read_text(encoding="utf-8")
    assert "input.step" not in context
    assert "observation_transcript" in context
