"""Fail-closed local contract for M176's asymmetric hosted campaign.

This module deliberately prepares no provider and reads no credential.  A
future G3 executor must validate the returned prepared checkpoint again before
constructing its provider.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile

from brep2code.agent.guidance import GuidanceBundle
from brep2code.agent.harness import HarnessRunResult, ManualHarness
from brep2code.agent.observed_build import ObservationCall, ObservedBuildLoopRunner
from brep2code.agent.provider import (
    DeepSeekProviderError,
    FakeLLMProvider,
    LLMMessage,
    LLMProvider,
    ProviderRequest,
)
from brep2code.agent.repair import _complete_provider, _write_script_update
from brep2code.agent.repair_policy import classify_terminal_feedback
from brep2code.cad import WslBubblewrapExecutor
from brep2code.corpus.report import write_corpus_report
from brep2code.monitor import setup_monitor
from brep2code.storage import RecordStore


POLICY = "m176-asymmetric-hosted-campaign-v1"
COMPLETION_CAP = 102
PROVIDER_REQUEST_CAP = 69
M179_POLICY = "m179-asymmetric-hosted-campaign-v1"
M179_SPEC = "docs/corpus/knowledge/m179-asymmetric-campaign-refreeze-v1.json"
M182_POLICY = "m182-asymmetric-case-local-continuation-v1"
M182_SPEC = "docs/corpus/knowledge/m182-asymmetric-case-local-continuation-v1.json"


class AsymmetricCampaignError(ValueError):
    """The frozen asymmetric campaign cannot safely be prepared."""


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AsymmetricCampaignError("frozen campaign material is unavailable") from exc
    if not isinstance(value, dict):
        raise AsymmetricCampaignError("frozen campaign material must be an object")
    return value


def _fingerprint(case_ids: list[str], records: dict[str, Path]) -> str:
    rows = []
    for case_id in sorted(case_ids):
        record_path = records[case_id]
        record = _load(record_path)
        input_path = record_path.parent / record.get("input_step", "")
        if not input_path.is_file() or _sha256(input_path) != record.get("sha256"):
            raise AsymmetricCampaignError("M176 registered input hash drift")
        rows.append({"case_id": case_id, "input_sha256": record["sha256"], "case_json_sha256": _sha256(record_path)})
    return sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def frozen_contract(root: Path) -> dict:
    """Validate M175/M176 and return only the immutable execution contract."""
    spec_path = root / "docs/corpus/knowledge/m176-asymmetric-campaign-freeze-v1.json"
    spec = _load(spec_path)
    qualification_path = root / spec.get("qualification", {}).get("path", "")
    if not qualification_path.is_file() or _sha256(qualification_path) != spec["qualification"].get("sha256"):
        raise AsymmetricCampaignError("M176 qualification hash drift")
    qualification = _load(qualification_path)
    main = [case_id for rows in qualification.get("main_cohort", {}).get("groups", {}).values() for case_id in rows]
    annex = qualification.get("feasibility_annex", {}).get("rows", [])
    roles = [row.get("role") for row in annex]
    if len(main) != 30 or len(set(main)) != 30 or len(annex) != 3 or roles != ["final primitive", "single boolean-cut tool", "repeated boolean-cut tool"]:
        raise AsymmetricCampaignError("M175 cohort or annex-role drift")
    registry_path = root / qualification.get("registry", {}).get("path", "")
    if not registry_path.is_file() or _sha256(registry_path) != qualification["registry"].get("sha256"):
        raise AsymmetricCampaignError("M175 registry hash drift")
    registry = _load(registry_path)
    records = {item.get("case_id"): root / item.get("case_record", "") for item in registry.get("cases", [])}
    if any(case_id not in records for case_id in main + [row.get("case_id") for row in annex]):
        raise AsymmetricCampaignError("M175 case registration drift")
    if any(_load(records[case_id]).get("data_split") != "development" for case_id in main):
        raise AsymmetricCampaignError("M176 main cohort permits development cases only")
    if _fingerprint(main, records) != spec["main_cohort"].get("input_fingerprint_sha256") or _fingerprint([row["case_id"] for row in annex], records) != spec["feasibility_annex"].get("input_fingerprint_sha256"):
        raise AsymmetricCampaignError("M176 input fingerprint drift")
    guidance = qualification["feasibility_annex"]["guidance"]
    index = root / guidance["index"]
    card = root / guidance["card"]
    if _sha256(index) != guidance["index_sha256"] or _sha256(card) != guidance["card_sha256"]:
        raise AsymmetricCampaignError("M176 guidance hash drift")
    if spec.get("provider") != {"name": "deepseek", "model": "deepseek-v4-pro", "max_output_tokens": 4096, "provider_timeout_seconds": 120, "serial_only": True, "retry": "forbidden"}:
        raise AsymmetricCampaignError("M176 provider bounds drift")
    if spec.get("executor") != {"name": "wsl-bwrap", "input_mount": "no-input"} or spec.get("execution_order") != ["feasibility_annex", "main_cohort"]:
        raise AsymmetricCampaignError("M176 execution boundary drift")
    identities = spec.get("report_identities")
    if not isinstance(identities, dict) or set(identities) != {"annex_report", "annex_monitor", "main_report", "main_monitor"} or len(set(identities.values())) != 4:
        raise AsymmetricCampaignError("M176 report identity drift")
    if spec.get("completion_cap") != COMPLETION_CAP or spec["main_cohort"].get("completion_cap") != 90 or spec["feasibility_annex"].get("completion_cap") != 12:
        raise AsymmetricCampaignError("M176 completion accounting drift")
    if shutil.which("wsl.exe") is None and shutil.which("wsl") is None:
        raise AsymmetricCampaignError("wsl-bwrap executor is unavailable")
    return {"policy": POLICY, "main_case_ids": main, "annex": annex, "guidance": guidance, "identities": identities, "completion_cap": COMPLETION_CAP, "provider_request_cap": PROVIDER_REQUEST_CAP, "spec_sha256": _sha256(spec_path)}


def prepare(root: Path, *, stale_after_seconds: int = 300) -> dict:
    """Create both fresh local checkpoints and monitors without provider state."""
    return _prepare_contract(root, frozen_contract(root), stale_after_seconds=stale_after_seconds)


def _prepare_contract(root: Path, contract: dict, *, stale_after_seconds: int) -> dict:
    paths = {name: root / relative for name, relative in contract["identities"].items()}
    if any(path.exists() for path in paths.values()):
        raise AsymmetricCampaignError("M176 report or monitor identity is not fresh")
    for product, report_key, monitor_key, completion_cap, request_cap in (
        ("feasibility_annex", "annex_report", "annex_monitor", 12, 9),
        ("main_cohort", "main_report", "main_monitor", 90, 60),
    ):
        payload = {"schema_version": 1, "policy": contract["policy"], "run_status": "running", "request_state": "prepared", "product": product, "campaign_spec_sha256": contract["spec_sha256"], "completion_slots_cap": completion_cap, "completion_slots_used": 0, "provider_request_cap": request_cap, "requests_used": 0, "requests_remaining": request_cap, "authorization": "not_authorized", "provider_constructed": False, "monitor_path": str(paths[monitor_key])}
        write_corpus_report(paths[report_key], payload)
        setup_monitor(paths[report_key], paths[monitor_key], stale_after_seconds=stale_after_seconds)
    return {"status": "prepared_offline", **contract}


def validate_execute_admission(root: Path) -> dict:
    """Confirm that both checkpoints remain fresh G3 authorization candidates."""
    return _validate_execute_admission(root, frozen_contract(root))


def _validate_execute_admission(root: Path, contract: dict) -> dict:
    for product, report_key, monitor_key, request_cap in (("feasibility_annex", "annex_report", "annex_monitor", 9), ("main_cohort", "main_report", "main_monitor", 60)):
        path = root / contract["identities"][report_key]
        payload = _load(path)
        if payload.get("policy") != contract["policy"] or payload.get("product") != product or payload.get("run_status") != "running" or payload.get("request_state") != "prepared" or payload.get("completion_slots_used", 0) != 0 or payload.get("requests_used") != 0 or payload.get("requests_remaining") != request_cap or payload.get("authorization") != "not_authorized" or payload.get("provider_constructed") is not False or payload.get("monitor_path") != str(root / contract["identities"][monitor_key]):
            raise AsymmetricCampaignError("M176 checkpoint is not a fresh execute-admission candidate")
    return contract


def frozen_m179_contract(root: Path) -> dict:
    """Bind M179's fresh identities to the unchanged M176 campaign material."""
    base = frozen_contract(root)
    path = root / M179_SPEC
    spec = _load(path)
    if spec.get("policy") != M179_POLICY or spec.get("m176_spec_sha256") != base["spec_sha256"]:
        raise AsymmetricCampaignError("M179 campaign freeze drift")
    identities = spec.get("report_identities")
    if not isinstance(identities, dict) or set(identities) != {"annex_report", "annex_monitor", "main_report", "main_monitor"} or len(set(identities.values())) != 4:
        raise AsymmetricCampaignError("M179 report identity drift")
    return {**base, "policy": M179_POLICY, "identities": identities, "spec_sha256": _sha256(path)}


def frozen_m182_contract(root: Path) -> dict:
    """Bind M182's fresh identities to M179 and its continuation policy."""
    base = frozen_m179_contract(root)
    path = root / M182_SPEC
    spec = _load(path)
    if spec.get("policy") != M182_POLICY or spec.get("m179_spec_sha256") != base["spec_sha256"]:
        raise AsymmetricCampaignError("M182 campaign freeze drift")
    identities = spec.get("report_identities")
    if not isinstance(identities, dict) or set(identities) != {"annex_report", "annex_monitor", "main_report", "main_monitor"} or len(set(identities.values())) != 4:
        raise AsymmetricCampaignError("M182 report identity drift")
    return {**base, "policy": M182_POLICY, "identities": identities, "spec_sha256": _sha256(path)}


def prepare_m179(root: Path, *, stale_after_seconds: int = 300) -> dict:
    """Create M179's fresh local checkpoints without provider state."""
    return _prepare_contract(root, frozen_m179_contract(root), stale_after_seconds=stale_after_seconds)


def validate_m179_execute_admission(root: Path) -> dict:
    """Validate M179's fresh identities before the later G3 boundary."""
    return _validate_execute_admission(root, frozen_m179_contract(root))


def authorize_m179_execution(root: Path) -> dict:
    """Atomically record the external authorization after fresh admission.

    Provider construction remains false here: it is set only by the per-request
    checkpoint immediately before a provider call.
    """
    contract = validate_m179_execute_admission(root)
    for report_key in ("annex_report", "main_report"):
        path = root / contract["identities"][report_key]
        payload = _load(path)
        payload.setdefault("completion_slots_used", 0)
        payload["authorization"] = "authorized_itemized"
        write_corpus_report(path, payload)
    return contract


def prepare_m182(root: Path, *, stale_after_seconds: int = 300) -> dict:
    """Create M182's fresh local checkpoints without provider state."""
    return _prepare_contract(root, frozen_m182_contract(root), stale_after_seconds=stale_after_seconds)


def validate_m182_execute_admission(root: Path) -> dict:
    """Validate M182's fresh identities before a separate G3 boundary."""
    return _validate_execute_admission(root, frozen_m182_contract(root))


def authorize_m182_execution(root: Path) -> dict:
    """Atomically record a later itemized authorization for M182 only."""
    contract = validate_m182_execute_admission(root)
    for report_key in ("annex_report", "main_report"):
        path = root / contract["identities"][report_key]
        payload = _load(path)
        payload.setdefault("completion_slots_used", 0)
        payload["authorization"] = "authorized_itemized"
        write_corpus_report(path, payload)
    return contract


def run_fake_m179(root: Path, provider: FakeLLMProvider) -> dict:
    """Exercise serial provider-request accounting with a local fake only.

    This is deliberately not a hosted executor: a non-fake provider is rejected
    before any request material is prepared.
    """
    return run_m179_serial(root, provider, allow_hosted=False)


def run_fake_m182(root: Path, provider: FakeLLMProvider) -> dict:
    """Exercise M182 continuation semantics with a local fake only."""
    return run_m182_serial(root, provider, allow_hosted=False)


def run_m179_serial(root: Path, provider: LLMProvider, *, allow_hosted: bool) -> dict:
    """Run fixed per-case Q01/card/generation/repair state machines serially."""
    if not isinstance(provider, FakeLLMProvider) and not allow_hosted:
        raise AsymmetricCampaignError("M179 execution adapter requires explicit hosted authorization")
    contract = _authorized_m179_contract(root) if allow_hosted else validate_m179_execute_admission(root)
    return _run_serial_contract(root, provider, allow_hosted=allow_hosted, contract=contract, continue_case_local=False)


def run_m182_serial(root: Path, provider: LLMProvider, *, allow_hosted: bool) -> dict:
    """Run M182 serially, retaining eligible provider failures per case."""
    if not isinstance(provider, FakeLLMProvider) and not allow_hosted:
        raise AsymmetricCampaignError("M182 execution adapter requires explicit hosted authorization")
    contract = _authorized_m182_contract(root) if allow_hosted else validate_m182_execute_admission(root)
    return _run_serial_contract(root, provider, allow_hosted=allow_hosted, contract=contract, continue_case_local=True)


def _run_serial_contract(root: Path, provider: LLMProvider, *, allow_hosted: bool, contract: dict, continue_case_local: bool) -> dict:
    """Run one frozen contract; only M182 contains provider-local exceptions."""
    outcomes: list[dict] = []
    for product, report_key, rows in (
        ("feasibility_annex", "annex_report", contract["annex"]),
        ("main_cohort", "main_report", [{"case_id": case_id, "role": None} for case_id in contract["main_case_ids"]]),
    ):
        path = root / contract["identities"][report_key]
        payload = _load(path)
        payload["cases"] = []
        for row in rows:
            case_id = row["case_id"]
            requests_before = payload["requests_used"]
            try:
                result = _run_case(
                    root, contract, provider, product=product, case_id=case_id,
                    guidance_role=row.get("role"), payload=payload, report_path=path,
                    allow_hosted=allow_hosted,
                )
            except DeepSeekProviderError as exc:
                if continue_case_local:
                    issued = payload["requests_used"] - requests_before
                    result = {"case_id": case_id, "status": "provider_error", "stop_reason": type(exc).__name__, "provider_requests": issued, "completion_slots_used": 1 + issued}
                else:
                    payload["run_status"] = "interrupted"
                    payload["interruption"] = {"code": "runner_exception", "case_id": case_id, "exception_type": type(exc).__name__}
                    write_corpus_report(path, payload)
                    raise
            except Exception as exc:
                payload["run_status"] = "interrupted"
                payload["interruption"] = {"code": "runner_exception", "case_id": case_id, "exception_type": type(exc).__name__}
                write_corpus_report(path, payload)
                raise
            payload["cases"].append(result)
            payload["completion_slots_used"] += result["completion_slots_used"]
            if payload["completion_slots_used"] > payload["completion_slots_cap"]:
                raise AsymmetricCampaignError("M180 completion-slot cap exceeded")
            write_corpus_report(path, payload)
        payload["request_state"] = "completed_offline_fake" if isinstance(provider, FakeLLMProvider) else "completed"
        payload["run_status"] = "completed"
        write_corpus_report(path, payload)
        outcomes.extend(payload["cases"])
    return {
        "status": "completed_offline_fake" if isinstance(provider, FakeLLMProvider) else "completed",
        "requests_used": sum(_load(root / contract["identities"][key])["requests_used"] for key in ("annex_report", "main_report")),
        "completion_cap": contract["completion_cap"],
        "cases": outcomes,
    }


def _authorized_m179_contract(root: Path) -> dict:
    contract = frozen_m179_contract(root)
    for report_key in ("annex_report", "main_report"):
        payload = _load(root / contract["identities"][report_key])
        if payload.get("authorization") != "authorized_itemized" or payload.get("run_status") != "running" or payload.get("requests_used") != 0:
            raise AsymmetricCampaignError("M180 checkpoint is not an authorized fresh execution")
    return contract


def _authorized_m182_contract(root: Path) -> dict:
    contract = frozen_m182_contract(root)
    for report_key in ("annex_report", "main_report"):
        payload = _load(root / contract["identities"][report_key])
        if payload.get("authorization") != "authorized_itemized" or payload.get("run_status") != "running" or payload.get("requests_used") != 0:
            raise AsymmetricCampaignError("M182 checkpoint is not an authorized fresh execution")
    return contract


def _m180_harness(root: Path) -> ManualHarness:
    return ManualHarness(store=RecordStore(root / "data"), executor=WslBubblewrapExecutor())


def _case_input(root: Path, case_id: str) -> Path:
    registry = _load(root / "docs/corpus/registry/self-authored.json")
    entries = {item.get("case_id"): item.get("case_record") for item in registry.get("cases", [])}
    record_path = root / str(entries.get(case_id, ""))
    record = _load(record_path)
    input_path = record_path.parent / str(record.get("input_step", ""))
    if not input_path.is_file():
        raise AsymmetricCampaignError("M180 registered input is unavailable")
    return input_path


def _mark_request(payload: dict, report_path: Path, *, allow_hosted: bool) -> None:
    if payload["requests_used"] >= payload["provider_request_cap"]:
        raise AsymmetricCampaignError("M180 provider request cap exceeded")
    payload["request_state"] = "issued"
    payload["provider_constructed"] = allow_hosted
    payload["requests_used"] += 1
    payload["requests_remaining"] -= 1
    write_corpus_report(report_path, payload)


def _run_case(
    root: Path, contract: dict, provider: LLMProvider, *, product: str, case_id: str,
    guidance_role: str | None, payload: dict, report_path: Path, allow_hosted: bool,
) -> dict:
    harness = _m180_harness(root)
    bundle = None
    if guidance_role is not None:
        bundle = GuidanceBundle.from_paths(root / contract["guidance"]["index"], root / contract["guidance"]["card"])

    def mark_issued() -> None:
        _mark_request(payload, report_path, allow_hosted=allow_hosted)

    requests_before = payload["requests_used"]
    try:
        initial = ObservedBuildLoopRunner(harness=harness, provider=provider, allow_hosted=allow_hosted).run(
            f"m179-{product}-{case_id}", input_path=_case_input(root, case_id),
            observation_session_id=f"m179-{product}-{case_id}",
            observation_calls=[ObservationCall(call_id="summary-1", tool="probe_summary")],
            timeout=120, provider_timeout=120, max_output_tokens=4096,
            max_repair_rounds=0, guidance_bundle=bundle, required_guidance_role=guidance_role,
            before_provider_request=mark_issued,
        )
    except DeepSeekProviderError as exc:
        issued = payload["requests_used"] - requests_before
        return {"case_id": case_id, "status": "provider_error", "stop_reason": type(exc).__name__, "provider_requests": issued, "completion_slots_used": 1 + issued}
    issued = payload["requests_used"] - requests_before
    result = {"case_id": case_id, "status": initial.status, "stop_reason": "initial_terminal", "provider_requests": issued, "completion_slots_used": 1 + issued}
    if initial.harness_result is None or initial.harness_result.status == "pass":
        return result
    decision = classify_terminal_feedback(initial.harness_result.signal_bundle)
    if not decision.allowed:
        result["stop_reason"] = decision.stop_reason or "ineligible_repair"
        result["repair_classification"] = decision.classification
        return result
    repair = _run_source_only_repair(harness, provider, initial.harness_result, mark_issued, allow_hosted=allow_hosted)
    result.update(repair)
    result["provider_requests"] = payload["requests_used"] - requests_before
    result["completion_slots_used"] = 1 + result["provider_requests"]
    return result


def _run_source_only_repair(
    harness: ManualHarness, provider: LLMProvider, failed: HarnessRunResult, mark_issued, *, allow_hosted: bool,
) -> dict:
    decision = classify_terminal_feedback(failed.signal_bundle)
    request = ProviderRequest(
        model=getattr(provider, "model", "fake-m180"),
        messages=[
            LLMMessage(role="system", content="Apply one source-only edit to build_sequence.py. Do not regenerate a sequence or access files/tools."),
            LLMMessage(role="user", content=json.dumps({"classification": decision.classification, "route": decision.route})),
        ], metadata={"policy": "m180-classified-source-only", "route": "source_only", "max_requests": 1},
    )
    mark_issued()
    response = _complete_provider(provider, request, timeout_seconds=120 if allow_hosted else None)
    update = response.script_update
    if update is None or update.kind != "edit" or update.path != "build_sequence.py" or not update.content:
        return {"status": "provider_error", "stop_reason": "invalid_source_edit", "repair_provider_requests": 1}
    with NamedTemporaryFile("w", encoding="utf-8", suffix=".py", delete=False) as replacement:
        replacement.write(update.content)
        replacement_path = Path(replacement.name)
    try:
        repaired = harness.run(failed.record.record_id, script=replacement_path, timeout=120, build_without_input=True)
    finally:
        replacement_path.unlink(missing_ok=True)
    _write_script_update(repaired.revision.traces, update)
    return {"status": repaired.status, "stop_reason": "repair_pass" if repaired.status == "pass" else "source_patch_not_converged", "repair_provider_requests": 1}


def run_authorized_m179(root: Path, provider: LLMProvider) -> dict:
    """Hosted-only boundary for an already-constructed fixed DeepSeek provider."""
    if getattr(provider, "name", None) != "deepseek" or getattr(provider, "model", None) != "deepseek-v4-pro":
        raise AsymmetricCampaignError("M180 requires deepseek-v4-pro")
    return run_m179_serial(root, provider, allow_hosted=True)


def run_authorized_m182(root: Path, provider: LLMProvider) -> dict:
    """Hosted-only M182 boundary with case-local provider containment."""
    if getattr(provider, "name", None) != "deepseek" or getattr(provider, "model", None) != "deepseek-v4-pro":
        raise AsymmetricCampaignError("M182 requires deepseek-v4-pro")
    return run_m182_serial(root, provider, allow_hosted=True)
