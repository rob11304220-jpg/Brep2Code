"""M0 manual harness loop."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
import shutil

from brep2code.brep import discover_input_file
from brep2code.agent.observation import build_observation_context
from brep2code.agent.guidance import GuidanceBundle, GuidanceCardBridge
from brep2code.brep.safe_probe import (
    INPUT_PROBE_TIMEOUT_SECONDS,
    OUTPUT_PROBE_TIMEOUT_SECONDS,
    safe_probe_summary,
)
from brep2code.cad import ExecutionResult, ScriptExecutor
from brep2code.cad.script_contract import BuildScriptContractResult, validate_build_script
from brep2code.scaffold import DEFAULT_BUILD_SEQUENCE
from brep2code.storage import RecordPaths, RecordStore, RevisionPaths
from brep2code.storage.store import write_json


@dataclass(frozen=True)
class HarnessRunResult:
    record: RecordPaths
    revision: RevisionPaths
    status: str
    signal_bundle: dict


class ManualHarness:
    """Creates a revision, prepares build_sequence.py, runs it, and records traces."""

    def __init__(self, store: RecordStore | None = None, executor: ScriptExecutor | None = None) -> None:
        self.store = store or RecordStore()
        self.executor = executor or ScriptExecutor()

    def run(
        self,
        record_id: str,
        script: Path | None = None,
        timeout: int = 60,
        input_path: Path | None = None,
        build_without_input: bool = False,
        observation_envelopes: list[dict] | None = None,
        guidance_bundle: GuidanceBundle | None = None,
        guidance_calls: list[dict] | None = None,
    ) -> HarnessRunResult:
        record = self.store.ensure_record(record_id)
        if input_path is not None:
            self._prepare_input(record, input_path)
        revision = self.store.create_revision(record)
        guidance = _run_guidance_calls(revision, guidance_bundle, guidance_calls)
        script_path = self._prepare_script(revision, script)
        build_script_contract = validate_build_script(script_path)
        observation = _write_observation_context(revision, observation_envelopes)
        record_input = _maybe_discover_input(record)
        execution_input = None if build_without_input else record_input
        execution = (
            self.executor.run(
                revision.workspace,
                script_path.name,
                timeout=timeout,
                input_path=execution_input,
                trace_input_access=True,
            )
            if build_script_contract.valid
            else _contract_rejection_execution(revision.workspace, build_script_contract)
        )

        stdout_path = revision.traces / "stdout.txt"
        stderr_path = revision.traces / "stderr.txt"
        stdout_path.write_text(execution.stdout, encoding="utf-8")
        stderr_path.write_text(execution.stderr, encoding="utf-8")

        model_path = revision.output / "model.step"
        execution_summary = {
            "command": execution.command,
            "cwd": str(execution.cwd),
            "exit_code": execution.exit_code,
            "duration_seconds": round(execution.duration_seconds, 6),
            "timed_out": execution.timed_out,
            "sandbox_backend": execution.sandbox_backend,
            "sandboxed": execution.sandboxed,
            "sandbox_policy_version": execution.sandbox_policy_version,
            "sandbox_capabilities": execution.sandbox_capabilities,
            "sandbox_mounts": execution.sandbox_mounts,
            "sandbox_limits": execution.sandbox_limits,
            "sandbox_termination_reason": execution.sandbox_termination_reason,
            "sandbox_event": execution.sandbox_event,
            "provenance_trace_path": execution.provenance_trace_path,
            "provenance_input_accesses": execution.provenance_input_accesses,
            "provenance_coverage": execution.provenance_coverage,
            "build_script_contract": build_script_contract.as_dict(),
            "build_capability": {"input_mount_present": execution_input is not None},
            "stdout_path": str(stdout_path),
            "stderr_path": str(stderr_path),
        }
        write_json(revision.execution_summary, execution_summary)

        input_probe = (
            safe_probe_summary(record_input, revision.traces, timeout_seconds=INPUT_PROBE_TIMEOUT_SECONDS)
            if record_input
            else None
        )
        output_probe = (
            safe_probe_summary(model_path, revision.traces, timeout_seconds=OUTPUT_PROBE_TIMEOUT_SECONDS)
            if model_path.exists()
            else None
        )
        provenance = (
            self._provenance_control(revision, script_path, timeout, execution)
            if build_script_contract.valid
            else _contract_rejected_provenance()
        )

        gates = [
            {
                "name": "script_exit_code",
                "status": "pass" if execution.exit_code == 0 else "fail",
                "metric": {"exit_code": execution.exit_code},
                "message": "Script exited successfully."
                if execution.exit_code == 0
                else "Script returned a non-zero exit code.",
            },
            {
                "name": "output_model_step_exists",
                "status": "pass" if model_path.exists() else "fail",
                "metric": {"path": str(model_path), "exists": model_path.exists()},
                "message": "Expected output/model.step exists."
                if model_path.exists()
                else "Expected output/model.step was not created.",
            },
            _readable_gate(output_probe),
        ]
        if record_input:
            gates.insert(2, _input_readable_gate(input_probe))
        gates.extend(_comparison_gates(input_probe, output_probe))
        status = "fail" if any(gate["status"] == "fail" for gate in gates) else "pass"
        signal_bundle = {
            "record_id": record.record_id,
            "revision_id": revision.revision_id,
            "status": status,
            "execution": {
                **execution_summary,
                "stdout_preview": _preview(execution.stdout),
                "stderr_preview": _preview(execution.stderr),
            },
            "artifacts": {
                "input_model": {
                    "path": str(record_input) if record_input else None,
                    "exists": record_input.exists() if record_input else False,
                },
                "build_script": {"path": str(script_path), "exists": script_path.exists()},
                "model_step": {"path": str(model_path), "exists": model_path.exists()},
                "intermediates_dir": {
                    "path": str(revision.intermediates),
                    "exists": revision.intermediates.exists(),
                },
            },
            "probes": {
                "input_summary": input_probe,
                "output_summary": output_probe,
            },
            "provenance": provenance,
            "observation_build_capability": {"input_mount_present": execution_input is not None},
            "observation": observation,
            "guidance": guidance,
            "gates": gates,
            "probe_suggestions": [],
            "repair_hints": _repair_hints(
                execution.exit_code,
                model_path.exists(),
                output_probe,
                build_script_contract=build_script_contract,
            ),
        }
        write_json(revision.signal_bundle, signal_bundle)
        return HarnessRunResult(record, revision, status, signal_bundle)

    def _provenance_control(self, revision: RevisionPaths, script_path: Path, timeout: int, normal_execution) -> dict:
        if not normal_execution.provenance_coverage:
            return {
                "version": "reconstruction-provenance-v1",
                "classification": "provenance_unknown",
                "coverage": False,
                "coverage_attestation": {"normal_run": False},
                "normal_trace_path": normal_execution.provenance_trace_path,
                "normal_input_accesses": [],
                "absent_input_control": {"status": "not_run", "reason": "trace_unavailable"},
            }
        if normal_execution.provenance_input_accesses:
            return {
                "version": "reconstruction-provenance-v1",
                "classification": "round_trip",
                "coverage": True,
                "coverage_attestation": {"normal_run": True},
                "normal_trace_path": normal_execution.provenance_trace_path,
                "normal_input_accesses": normal_execution.provenance_input_accesses,
                "absent_input_control": {"status": "not_run", "reason": "normal_input_read"},
            }
        control = revision.root / "provenance-control"
        (control / "output").mkdir(parents=True, exist_ok=True)
        (control / "intermediates").mkdir(exist_ok=True)
        shutil.copy2(script_path, control / "build_sequence.py")
        result = self.executor.run(control, timeout=timeout, input_path=None, trace_input_access=True)
        readable = (control / "output" / "model.step").is_file()
        passed = result.provenance_coverage and not result.provenance_input_accesses and result.exit_code == 0 and readable
        return {
            "version": "reconstruction-provenance-v1",
            "classification": "independent_reconstruction" if passed else "provenance_unknown",
            "coverage": result.provenance_coverage,
            "coverage_attestation": {"normal_run": True, "absent_input_control": result.provenance_coverage},
            "normal_trace_path": normal_execution.provenance_trace_path,
            "normal_input_accesses": [],
            "absent_input_control": {
                "status": "pass" if passed else "fail",
                "exit_code": result.exit_code,
                "output_exists": readable,
                "trace_path": result.provenance_trace_path,
                "input_accesses": result.provenance_input_accesses,
            },
        }

    @staticmethod
    def _prepare_script(revision: RevisionPaths, script: Path | None) -> Path:
        destination = revision.workspace / "build_sequence.py"
        if script is None:
            destination.write_text(DEFAULT_BUILD_SEQUENCE, encoding="utf-8")
        else:
            source = script.resolve()
            if not source.is_file():
                raise FileNotFoundError(f"build script does not exist: {script}")
            shutil.copy2(source, destination)
        return destination

    @staticmethod
    def _prepare_input(record: RecordPaths, input_path: Path) -> Path:
        source = input_path.resolve()
        if not source.is_file():
            raise FileNotFoundError(f"CAD input does not exist: {input_path}")
        destination = record.input_dir / source.name
        if source != destination.resolve():
            shutil.copy2(source, destination)
        return destination


def result_to_dict(result: HarnessRunResult) -> dict:
    payload = asdict(result)
    payload["record"]["root"] = str(result.record.root)
    payload["record"]["input_dir"] = str(result.record.input_dir)
    payload["record"]["revisions_dir"] = str(result.record.revisions_dir)
    payload["record"]["manifest"] = str(result.record.manifest)
    payload["revision"]["root"] = str(result.revision.root)
    payload["revision"]["workspace"] = str(result.revision.workspace)
    payload["revision"]["intermediates"] = str(result.revision.intermediates)
    payload["revision"]["output"] = str(result.revision.output)
    payload["revision"]["traces"] = str(result.revision.traces)
    payload["revision"]["signal_bundle"] = str(result.revision.signal_bundle)
    payload["revision"]["execution_summary"] = str(result.revision.execution_summary)
    return payload


def _preview(text: str, limit: int = 2000) -> str:
    return text if len(text) <= limit else text[:limit] + "\n...[truncated]"


def _write_observation_context(revision: RevisionPaths, envelopes: list[dict] | None) -> dict | None:
    if not envelopes:
        return None
    context = build_observation_context(envelopes)
    payload = json.loads(context)
    session_ids = {entry.get("observation_session_id") for entry in envelopes}
    if len(session_ids) != 1 or None in session_ids:
        raise ValueError("observation_context_requires_one_session")
    path = revision.traces / "observation_context.json"
    path.write_text(context + "\n", encoding="utf-8")
    return {
        "schema_version": payload["schema_version"],
        "session_id": next(iter(session_ids)),
        "transcript_sha256": sha256(context.encode("utf-8")).hexdigest(),
        "context_path": str(path),
        "entry_count": len(envelopes),
    }


def _run_guidance_calls(
    revision: RevisionPaths,
    bundle: GuidanceBundle | None,
    calls: list[dict] | None,
) -> dict | None:
    if bundle is None and not calls:
        return None
    bridge = GuidanceCardBridge(revision.revision_id, bundle)
    results = []
    for call in calls or []:
        result = bridge.call(call.get("tool", ""), call.get("arguments"), trace_dir=revision.traces)
        results.append({"tool": result.tool, "ok": result.ok, "card_id": result.result.get("id") if result.result else None, "error": result.error})
    return {
        "enabled": bundle is not None,
        "index_sha256": bundle.index_sha256 if bundle else None,
        "returned_card_ids": [item["card_id"] for item in results if item["card_id"]],
        "calls": results,
    }


def _maybe_discover_input(record: RecordPaths) -> Path | None:
    try:
        return discover_input_file(record.input_dir)
    except (FileNotFoundError, ValueError):
        return None


def _contract_rejection_execution(workspace: Path, contract: BuildScriptContractResult) -> ExecutionResult:
    message = "; ".join(str(item["message"]) for item in contract.violations)
    return ExecutionResult(
        command=[],
        cwd=workspace,
        exit_code=126,
        stdout="",
        stderr=f"build_script_contract_violation: {message}",
        duration_seconds=0.0,
        sandbox_backend="not_run",
        sandboxed=False,
        sandbox_policy_version="not_run",
        sandbox_capabilities={"filesystem_isolation": False, "network_isolation": False},
        sandbox_termination_reason="contract_rejected",
        sandbox_event={"code": "build_script_contract_violation", "message": message},
    )


def _contract_rejected_provenance() -> dict:
    return {
        "version": "reconstruction-provenance-v1",
        "classification": "provenance_unknown",
        "coverage": False,
        "coverage_attestation": {"normal_run": False},
        "normal_trace_path": None,
        "normal_input_accesses": [],
        "absent_input_control": {"status": "not_run", "reason": "build_script_contract_rejected"},
    }


_safe_probe_summary = safe_probe_summary


def _input_readable_gate(input_probe: dict | None) -> dict:
    readable = bool(input_probe and input_probe.get("ok"))
    return {
        "name": "input_model_step_readable",
        "status": "pass" if readable else "fail",
        "metric": input_probe if input_probe else {"ok": False},
        "message": "Input STEP can be read by the B-Rep probe backend."
        if readable
        else "Input STEP could not be read by the B-Rep probe backend.",
    }


def _readable_gate(output_probe: dict | None) -> dict:
    readable = bool(output_probe and output_probe.get("ok"))
    return {
        "name": "output_model_step_readable",
        "status": "pass" if readable else "fail",
        "metric": output_probe if output_probe else {"ok": False},
        "message": "Output STEP can be read by the B-Rep probe backend."
        if readable
        else "Output STEP could not be read by the B-Rep probe backend.",
    }


def _comparison_gates(input_probe: dict | None, output_probe: dict | None) -> list[dict]:
    if not input_probe or not input_probe.get("ok") or not output_probe or not output_probe.get("ok"):
        return [
            {
                "name": "bbox_delta",
                "status": "skip",
                "metric": {"reason": "input_or_output_probe_unavailable"},
                "message": "Skipped bbox comparison because input or output probe summary is unavailable.",
            },
            {
                "name": "volume_delta",
                "status": "skip",
                "metric": {"reason": "input_or_output_probe_unavailable"},
                "message": "Skipped volume comparison because input or output probe summary is unavailable.",
            },
            {
                "name": "topology_count_delta",
                "status": "skip",
                "metric": {"reason": "input_or_output_probe_unavailable"},
                "message": "Skipped topology comparison because input or output probe summary is unavailable.",
            },
        ]

    bbox_metric = _bbox_delta(input_probe["bbox"], output_probe["bbox"])
    volume_metric = _scalar_delta(input_probe["volume"], output_probe["volume"])
    count_metric = _count_delta(input_probe["counts"], output_probe["counts"])
    return [
        {
            "name": "bbox_delta",
            "status": "pass" if bbox_metric["max_abs_delta"] <= 1e-5 else "fail",
            "metric": bbox_metric,
            "message": "Output bbox matches input bbox within tolerance."
            if bbox_metric["max_abs_delta"] <= 1e-5
            else "Output bbox differs from input bbox.",
        },
        {
            "name": "volume_delta",
            "status": "pass" if volume_metric["relative_delta"] <= 1e-5 else "fail",
            "metric": volume_metric,
            "message": "Output volume matches input volume within tolerance."
            if volume_metric["relative_delta"] <= 1e-5
            else "Output volume differs from input volume.",
        },
        {
            "name": "topology_count_delta",
            "status": "pass" if count_metric["total_abs_delta"] == 0 else "fail",
            "metric": count_metric,
            "message": "Output topology counts match input counts."
            if count_metric["total_abs_delta"] == 0
            else "Output topology counts differ from input counts.",
        },
    ]


def _bbox_delta(input_bbox: dict, output_bbox: dict) -> dict:
    input_values = input_bbox["min"] + input_bbox["max"]
    output_values = output_bbox["min"] + output_bbox["max"]
    deltas = [round(output_value - input_value, 9) for input_value, output_value in zip(input_values, output_values)]
    return {
        "input": input_bbox,
        "output": output_bbox,
        "delta": deltas,
        "max_abs_delta": max(abs(delta) for delta in deltas),
        "tolerance": 1e-5,
    }


def _scalar_delta(input_value: float, output_value: float) -> dict:
    absolute = abs(output_value - input_value)
    denominator = max(abs(input_value), 1e-12)
    return {
        "input": input_value,
        "output": output_value,
        "absolute_delta": absolute,
        "relative_delta": absolute / denominator,
        "tolerance": 1e-5,
    }


def _count_delta(input_counts: dict[str, int], output_counts: dict[str, int]) -> dict:
    keys = sorted(set(input_counts) | set(output_counts))
    delta = {key: output_counts.get(key, 0) - input_counts.get(key, 0) for key in keys}
    return {
        "input": input_counts,
        "output": output_counts,
        "delta": delta,
        "total_abs_delta": sum(abs(value) for value in delta.values()),
    }


def _repair_hints(
    exit_code: int,
    model_exists: bool,
    output_probe: dict | None = None,
    *,
    build_script_contract: BuildScriptContractResult | None = None,
) -> list[str]:
    hints: list[str] = []
    if build_script_contract is not None and not build_script_contract.valid:
        hints.append("Use only installed OCP modules and symbols; cadquery, OCC, and unavailable OCP names are unsupported.")
    if exit_code != 0:
        hints.append("Inspect traces/stderr.txt and fix the Python exception or process failure.")
    if not model_exists:
        hints.append("Ensure build_sequence.py writes the expected CAD artifact at output/model.step.")
    if model_exists and output_probe and not output_probe.get("ok"):
        hints.append("Ensure output/model.step is a valid STEP file readable by the B-Rep backend.")
    return hints
