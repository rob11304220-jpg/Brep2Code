"""Fail-closed classification and source-only repair for M141.

The policy consumes terminal Harness feedback only.  It does not inspect an
input B-Rep, select an entity, or construct a hosted provider.  Routes that
need sequence/IR locators deliberately stop until such a contract exists.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from brep2code.agent.harness import HarnessRunResult, ManualHarness
from brep2code.agent.provider import FakeLLMProvider, LLMMessage, LLMProvider, ProviderRequest
from brep2code.storage.store import write_json


@dataclass(frozen=True)
class RepairDecision:
    classification: str
    route: str
    allowed: bool
    max_requests: int
    stop_reason: str | None = None


@dataclass(frozen=True)
class ClassifiedRepairResult:
    status: str
    stop_reason: str
    decision: RepairDecision
    provider_requests: int
    result: HarnessRunResult | None = None


def classify_terminal_feedback(bundle: dict[str, Any]) -> RepairDecision:
    """Map one sanitized terminal bundle to exactly one repair decision."""

    if bundle.get("status") == "pass":
        return _stop("pass", "stop_pass")

    execution = _mapping(bundle.get("execution"))
    provenance = _mapping(bundle.get("provenance"))
    if execution.get("sandboxed") or execution.get("sandbox_termination_reason") not in {None, "completed", "contract_rejected"}:
        return _stop("sandbox_or_provenance", "stop_policy_rejected")
    if provenance.get("classification") == "round_trip":
        return _stop("sandbox_or_provenance", "stop_policy_rejected")

    declared = bundle.get("repair_classification")
    if declared in {"selector_ambiguous", "geometry_semantic", "editability"}:
        return _stop(str(declared), "stop_unsupported")
    if declared in {"provider_or_protocol", "unknown_or_mixed"}:
        return _stop(str(declared), "stop_ambiguous")

    contract = _mapping(execution.get("build_script_contract"))
    if contract.get("status") == "fail":
        return _source("static_api_contract")
    gates = {item.get("name"): item for item in bundle.get("gates", []) if isinstance(item, dict)}
    if any(gates.get(name, {}).get("status") == "fail" for name in ("output_model_step_exists", "output_model_step_readable")):
        return _source("output_artifact")
    if execution.get("timed_out"):
        return _stop("execution_timeout", "stop_unsupported")
    if execution.get("exit_code") not in (None, 0):
        return _source("execution_local")
    return _stop("unknown_or_mixed", "stop_ambiguous")


class ClassifiedRepairRunner:
    """Apply the sole admitted M141 route with a local fake provider.

    ``source_only`` accepts one explicit ``edit`` response containing the new
    source.  A replacement response, sequence route, or any unclassified
    terminal feedback stops before a provider call.
    """

    def __init__(self, *, harness: ManualHarness, provider: LLMProvider) -> None:
        if not isinstance(provider, FakeLLMProvider):
            raise ValueError("ClassifiedRepairRunner is offline and requires FakeLLMProvider")
        self.harness = harness
        self.provider = provider

    def run(self, failed: HarnessRunResult, *, timeout: int = 60) -> ClassifiedRepairResult:
        decision = classify_terminal_feedback(failed.signal_bundle)
        if not decision.allowed:
            self._write_evidence(failed, decision, provider_requests=0, stop_reason=decision.stop_reason or "stop_ambiguous")
            return ClassifiedRepairResult("fail", decision.stop_reason or "stop_ambiguous", decision, 0)

        request = ProviderRequest(
            model=getattr(self.provider, "model", "fake-classified-repair"),
            messages=[
                LLMMessage(role="system", content="Apply one source-only edit to build_sequence.py. Do not regenerate a sequence or access files/tools."),
                LLMMessage(role="user", content=_source_context(failed, decision)),
            ],
            metadata={"policy": "classified-repair-v1", "route": decision.route, "max_requests": decision.max_requests},
        )
        response = self.provider.complete(request)
        update = response.script_update
        if update is None or update.kind != "edit" or update.path != "build_sequence.py" or not update.content:
            self._write_evidence(failed, decision, provider_requests=1, stop_reason="invalid_source_edit")
            return ClassifiedRepairResult("provider_error", "invalid_source_edit", decision, 1)

        with NamedTemporaryFile("w", encoding="utf-8", suffix=".py", delete=False) as replacement:
            replacement.write(update.content)
            replacement_path = Path(replacement.name)
        try:
            repaired = self.harness.run(failed.record.record_id, script=replacement_path, timeout=timeout)
        finally:
            replacement_path.unlink(missing_ok=True)
        signature_before = _signature(failed.signal_bundle, decision.classification)
        signature_after = _signature(repaired.signal_bundle, classify_terminal_feedback(repaired.signal_bundle).classification)
        stop_reason = "pass" if repaired.status == "pass" else "stop_plateau" if signature_before == signature_after else "source_patch_not_converged"
        self._write_evidence(failed, decision, provider_requests=1, stop_reason=stop_reason)
        self._write_evidence(repaired, classify_terminal_feedback(repaired.signal_bundle), provider_requests=1, stop_reason=stop_reason)
        return ClassifiedRepairResult(repaired.status, stop_reason, decision, 1, repaired)

    @staticmethod
    def _write_evidence(result: HarnessRunResult, decision: RepairDecision, *, provider_requests: int, stop_reason: str) -> None:
        write_json(result.revision.traces / "classified_repair.json", {"schema_version": 1, "decision": asdict(decision), "provider_requests": provider_requests, "stop_reason": stop_reason})


def _source(classification: str) -> RepairDecision:
    return RepairDecision(classification, "source_only", True, 1)


def _stop(classification: str, reason: str) -> RepairDecision:
    return RepairDecision(classification, "stop", False, 0, reason)


def _mapping(value: object) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _source_context(result: HarnessRunResult, decision: RepairDecision) -> str:
    bundle = result.signal_bundle
    context = {
        "classification": decision.classification,
        "route": decision.route,
        "execution": {key: bundle.get("execution", {}).get(key) for key in ("exit_code", "timed_out", "sandboxed", "sandbox_termination_reason")},
        "gates": [{key: item.get(key) for key in ("name", "status", "message")} for item in bundle.get("gates", []) if isinstance(item, dict)],
        "repair_hints": bundle.get("repair_hints", []),
        "build_sequence": (result.revision.workspace / "build_sequence.py").read_text(encoding="utf-8"),
    }
    return json.dumps(context, ensure_ascii=False, sort_keys=True)


def _signature(bundle: dict[str, Any], classification: str) -> str:
    execution = _mapping(bundle.get("execution"))
    failed_gates = sorted(item.get("name") for item in bundle.get("gates", []) if isinstance(item, dict) and item.get("status") == "fail")
    return json.dumps({"classification": classification, "exit_code": execution.get("exit_code"), "termination": execution.get("sandbox_termination_reason"), "failed_gates": failed_gates}, sort_keys=True)
