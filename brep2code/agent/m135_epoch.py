"""Frozen 18-condition epoch identity and durable accounting checkpoint."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import ast
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable

from brep2code.agent.guidance import GuidanceBundle, GuidanceCardBridge, TOOL_NAME
from brep2code.agent.harness import ManualHarness
from brep2code.agent.observed_build import ObservedBuildResult
from brep2code.agent.provider import FakeLLMProvider, LLMMessage, LLMProvider, ProviderRequest
from brep2code.agent.repair import ProviderRequestLifecycleError, ProviderRequestTimeoutError, _complete_provider
from brep2code.corpus.report import write_corpus_report
from tools.m115_prismatic_policy import M115_STATIC_API_CLASSIFIER_VERSION, classify_static_api


POLICY = "m135-existing-family-development-v1"
REQUEST_CAP = 18
PROVIDER = "deepseek"
MODEL = "deepseek-v4-pro"
PROVIDER_DEADLINE_SECONDS = 120
EXECUTOR = "wsl-bwrap"
SYSTEM_INSTRUCTION = (
    "Generate one complete build_sequence.py from the bounded observation transcript. "
    "The build has no input STEP mount; write only output/model.step. "
    "Use only installed OCP modules and symbols; never cadquery, OCC.Core, or invented OCP names."
)
_GUIDANCE_INDEX = "runtime_resources/experience-cards/index.json"
_GUIDANCE_CARD = "runtime_resources/experience-cards/cards/vertical-cylinder-construction.json"
_SOURCES = (
    ("repeated_feature_pattern", "docs/corpus/sequence-paired/repeated-feature-pattern-v1-preregistration.json", ("no_card",)),
    ("axisymmetric_revolve", "docs/corpus/sequence-paired/revolve-v1-preregistration.json", ("no_card",)),
    ("dependent_face_selection", "docs/corpus/sequence-paired/face-selected-dependent-cut-v1-preregistration.json", ("no_card",)),
    ("multi_inner_loop_pocket", "docs/corpus/sequence-paired/multi-inner-loop-pocket-v1-preregistration.json", ("no_card",)),
    ("prismatic_cylindrical_cut", "docs/corpus/sequence-paired/reference-guided-through-hole-variation-v1-preregistration.json", ("card", "no_card")),
)


@dataclass(frozen=True)
class EpochCondition:
    condition_id: str
    family: str
    case_id: str
    treatment: str
    input_sha256: str
    transcript_sha256: str = ""


@dataclass(frozen=True)
class FrozenRequest:
    """Exact local request material for one M135 condition; no provider is built."""

    request: ProviderRequest
    system_instruction_sha256: str
    card_response_sha256: str | None
    card_source_sha256: str | None


def frozen_conditions(root: Path) -> list[EpochCondition]:
    """Load only frozen development rows in the M134 order; fail closed on drift."""
    conditions: list[EpochCondition] = []
    for family, relative, treatments in _SOURCES:
        payload = json.loads((root / relative).read_text(encoding="utf-8"))
        for row in payload["cases"]:
            if row.get("data_split") != "development":
                continue
            case = json.loads((root / row["candidate_directory"] / "case.json").read_text(encoding="utf-8"))
            digest = sha256((root / row["candidate_directory"] / case["input_step"]).read_bytes()).hexdigest()
            if digest != case.get("sha256"):
                raise ValueError(f"input hash drift: {row['case_id']}")
            for treatment in treatments:
                condition_id = f"{family}:{row['case_id']}:{treatment}"
                transcript = _transcript_payload(condition_id, family, row, treatment)
                transcript_digest = sha256(_canonical_json(transcript).encode("utf-8")).hexdigest()
                conditions.append(EpochCondition(condition_id, family, row["case_id"], treatment, digest, transcript_digest))
    if len(conditions) != REQUEST_CAP or len({item.condition_id for item in conditions}) != REQUEST_CAP:
        raise ValueError("M135 frozen cohort must contain exactly 18 unique conditions")
    return conditions


def frozen_transcript(root: Path, condition: EpochCondition) -> dict:
    """Return the path-free, deterministic outbound fact envelope for one row."""
    for family, relative, treatments in _SOURCES:
        if family != condition.family or condition.treatment not in treatments:
            continue
        payload = json.loads((root / relative).read_text(encoding="utf-8"))
        for row in payload["cases"]:
            if row.get("case_id") == condition.case_id and row.get("data_split") == "development":
                result = _transcript_payload(condition.condition_id, family, row, condition.treatment)
                if sha256(_canonical_json(result).encode("utf-8")).hexdigest() != condition.transcript_sha256:
                    raise ValueError("M135 transcript hash drift")
                return result
    raise ValueError("M135 transcript condition drift")


def frozen_request(root: Path, condition: EpochCondition) -> FrozenRequest:
    """Build the hash-pinned single-request envelope without provider state."""
    messages = [
        LLMMessage(role="system", content=SYSTEM_INSTRUCTION),
        LLMMessage(role="user", content=_canonical_json(frozen_transcript(root, condition))),
    ]
    card_response_sha256 = None
    card_source_sha256 = None
    if condition.treatment == "card":
        bundle = GuidanceBundle.from_paths(root / _GUIDANCE_INDEX, root / _GUIDANCE_CARD)
        card = GuidanceCardBridge("m135-frozen", bundle).call(TOOL_NAME, {"role": "single boolean-cut tool"})
        if not card.ok or card.result is None:
            raise ValueError("M135 frozen card unavailable")
        # Match the existing direct-guidance injection serializer exactly.
        card_bytes = json.dumps(card.result, sort_keys=True).encode("utf-8")
        card_response_sha256 = sha256(card_bytes).hexdigest()
        card_source_sha256 = bundle.card_sha256
        messages.append(LLMMessage(role="tool", name=TOOL_NAME, content=card_bytes.decode("utf-8")))
    return FrozenRequest(
        request=ProviderRequest(
            model=MODEL,
            messages=messages,
            max_output_tokens=None,
            metadata={"policy": POLICY, "condition_id": condition.condition_id, "single_request": True},
        ),
        system_instruction_sha256=sha256(SYSTEM_INSTRUCTION.encode("utf-8")).hexdigest(),
        card_response_sha256=card_response_sha256,
        card_source_sha256=card_source_sha256,
    )


def terminal_from_observed(condition: EpochCondition, result: ObservedBuildResult, script: str | None) -> str:
    """Map one completed fake/hosted-compatible route to one frozen terminal class."""
    if result.harness_result is None:
        return "lifecycle_ended_before_script"
    if condition.treatment == "card":
        if script is None or classify_static_api(script).category != "api_admissible":
            return "static_api_inadmissible"
    execution = result.harness_result.signal_bundle["execution"]
    if execution["exit_code"] != 0:
        return "sandbox_execution_failed"
    return "full_success" if result.status == "pass" else "downstream_gate_failed"


def run_fake_serial_epoch(
    path: Path,
    *,
    root: Path,
    provider: FakeLLMProvider,
    harness: ManualHarness,
) -> dict:
    """Run M135's frozen conditions serially through the no-input Harness.

    This deliberately accepts only the local fake provider.  A future hosted
    lifecycle must be separately scoped and authorized rather than widening
    this regression path.
    """
    if not isinstance(provider, FakeLLMProvider):
        raise ValueError("M135 serial lifecycle requires FakeLLMProvider")
    return run_serial_epoch(path, root=root, provider=provider, harness=harness, provider_timeout=None)


def run_serial_epoch(
    path: Path,
    *,
    root: Path,
    provider: LLMProvider,
    harness: ManualHarness,
    provider_timeout: int | None,
) -> dict:
    """Run the frozen serial contract through a provider deadline worker and Harness."""
    conditions = frozen_conditions(root)
    for condition in conditions:
        current = json.loads(path.read_text(encoding="utf-8"))
        if current["run_status"] != "running":
            return current
        mark_issued(path, condition.condition_id)
        try:
            response = _complete_provider(provider, frozen_request(root, condition).request, timeout_seconds=provider_timeout)
        except (ProviderRequestTimeoutError, ProviderRequestLifecycleError):
            mark_terminal(path, condition.condition_id, "lifecycle_ended_before_script")
            continue
        script_update = response.script_update
        if script_update is None or script_update.kind != "replace" or script_update.content is None:
            mark_terminal(path, condition.condition_id, "lifecycle_ended_before_script")
            continue
        script = script_update.content
        classification = classify_static_api(script) if condition.treatment == "card" else None
        if classification is not None and classification.category != "api_admissible":
            mark_terminal(
                path,
                condition.condition_id,
                "static_api_inadmissible",
                static_api_rejection=static_api_rejection_observation(script, classification.reason),
            )
            continue
        case_path = _case_path(root, condition.case_id)
        case = json.loads(case_path.read_text(encoding="utf-8"))
        with NamedTemporaryFile("w", suffix=".py", encoding="utf-8", delete=False) as temporary:
            temporary.write(script)
            script_path = Path(temporary.name)
        try:
            result = harness.run(
                condition.condition_id.replace(":", "-"),
                input_path=case_path.parent / case["input_step"],
                script=script_path,
                build_without_input=True,
            )
        finally:
            script_path.unlink(missing_ok=True)
        execution = result.signal_bundle["execution"]
        terminal = "sandbox_execution_failed" if execution["exit_code"] != 0 else (
            "full_success" if result.status == "pass" else "downstream_gate_failed"
        )
        mark_terminal(path, condition.condition_id, terminal)
    return json.loads(path.read_text(encoding="utf-8"))


def authorize_execution_checkpoint(path: Path, *, monitor_path: Path) -> dict:
    """Make one newly prepared M135 report executable after external authorization."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    contract = payload.get("epoch_contract")
    if (
        payload.get("policy") != POLICY
        or payload.get("run_status") != "running"
        or payload.get("request_state") != "prepared"
        or payload.get("requests_used") != 0
        or payload.get("requests_remaining") != REQUEST_CAP
        or not isinstance(contract, dict)
        or contract.get("monitor_path") != str(monitor_path)
        or contract.get("authorization") != "not_authorized"
        or contract.get("provider_constructed") is not False
    ):
        raise ValueError("M135 execution checkpoint is not a fresh authorized-preflight candidate")
    contract["authorization"] = "authorized_itemized"
    contract["provider_constructed"] = True
    write_corpus_report(path, payload)
    return payload


def _case_path(root: Path, case_id: str) -> Path:
    matches = list(root.glob(f"case-library/self-authored/{case_id}/case.json"))
    if len(matches) != 1:
        raise ValueError(f"M135 case identity drift: {case_id}")
    return matches[0]


def static_api_rejection_observation(script: str, reason: str | None) -> dict:
    """Return content-free diagnostics for a rejected M115 static API script."""
    try:
        tree = ast.parse(script)
    except SyntaxError:
        imports: list[str] = []
        calls: list[str] = []
        parse_status = "syntax_error"
    else:
        imports = sorted({node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module})
        calls = sorted({node.func.id for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)})
        parse_status = "parsed"
    return {
        "schema_version": 1,
        "classifier_version": M115_STATIC_API_CLASSIFIER_VERSION,
        "reason": reason,
        "script_sha256": sha256(script.encode("utf-8")).hexdigest(),
        "utf8_bytes": len(script.encode("utf-8")),
        "parse_status": parse_status,
        "import_modules": imports,
        "call_names": calls,
    }


def _transcript_payload(condition_id: str, family: str, row: dict, treatment: str) -> dict:
    """Whitelist only preregistered development facts; no paths, STEP or scripts."""
    parameters = row.get("parameters")
    if not isinstance(parameters, dict):
        raise ValueError("M135 transcript parameters missing")
    payload = {
        "schema_version": 1,
        "policy": POLICY,
        "condition_id": condition_id,
        "family": family,
        "data_split": "development",
        "facts": parameters,
    }
    if treatment == "card":
        payload["guidance"] = {"card_policy": "reference-guided-through-hole-variation-v1-m96", "role": "single boolean-cut tool"}
    return payload


def _canonical_json(payload: dict) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def prepare_checkpoint(path: Path, *, provider: str, model: str, conditions: list[EpochCondition]) -> dict:
    if path.exists():
        raise ValueError("M135 report path must be fresh")
    if len(conditions) != REQUEST_CAP:
        raise ValueError("M135 requires 18 conditions")
    payload = {"schema_version": 1, "policy": POLICY, "run_status": "running", "request_state": "prepared", "provider": provider, "model": model, "requests_used": 0, "requests_remaining": REQUEST_CAP, "conditions": [{"condition_id": item.condition_id, "input_sha256": item.input_sha256, "transcript_sha256": item.transcript_sha256, "state": "not_issued"} for item in conditions]}
    write_corpus_report(path, payload)
    return payload


def prepare_preflight_checkpoint(path: Path, monitor_path: Path, *, root: Path) -> dict:
    """Prepare the fixed local M135 contract without constructing a provider."""
    if monitor_path.exists():
        raise ValueError("M135 monitor path must be fresh")
    if path.resolve() == monitor_path.resolve():
        raise ValueError("M135 report and monitor paths must differ")
    payload = prepare_checkpoint(path, provider=PROVIDER, model=MODEL, conditions=frozen_conditions(root))
    payload["epoch_contract"] = {
        "executor": EXECUTOR,
        "provider_deadline_seconds": PROVIDER_DEADLINE_SECONDS,
        "max_output_tokens": None,
        "max_repair_rounds": 0,
        "max_retry_count": 0,
        "max_requests": REQUEST_CAP,
        "monitor_path": str(monitor_path),
        "authorization": "not_authorized",
        "provider_constructed": False,
    }
    write_corpus_report(path, payload)
    return payload


def mark_issued(path: Path, condition_id: str) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("policy") != POLICY or payload.get("run_status") != "running":
        raise ValueError("M135 checkpoint identity drift")
    conditions = payload.get("conditions")
    target = next((item for item in conditions if item["condition_id"] == condition_id), None)
    if target is None or target["state"] != "not_issued" or payload["requests_used"] >= REQUEST_CAP:
        raise ValueError("M135 checkpoint accounting drift")
    target["state"] = "issued"
    payload["request_state"] = "issued"
    payload["requests_used"] += 1
    payload["requests_remaining"] = REQUEST_CAP - payload["requests_used"]
    write_corpus_report(path, payload)
    return payload


def mark_terminal(
    path: Path,
    condition_id: str,
    terminal: str,
    *,
    integrity: bool = False,
    static_api_rejection: dict | None = None,
) -> dict:
    """Close one issued condition, or freeze all remaining rows on integrity loss."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("policy") != POLICY or payload.get("run_status") != "running":
        raise ValueError("M135 checkpoint identity drift")
    target = next((item for item in payload["conditions"] if item["condition_id"] == condition_id), None)
    if target is None or target["state"] != "issued":
        raise ValueError("M135 terminal state drift")
    target["state"] = terminal
    if static_api_rejection is not None:
        if terminal != "static_api_inadmissible":
            raise ValueError("M135 static API diagnostics require static_api_inadmissible")
        target["static_api_rejection"] = static_api_rejection
    if integrity:
        for item in payload["conditions"]:
            if item["state"] == "not_issued":
                item["state"] = "not_issued_epoch_integrity"
        payload["run_status"] = "completed"
        payload["epoch_integrity"] = terminal
    elif payload["requests_used"] == REQUEST_CAP:
        payload["run_status"] = "completed"
    write_corpus_report(path, payload)
    return payload


def run_fake_epoch(path: Path, conditions: list[EpochCondition], outcome: Callable[[EpochCondition], str]) -> dict:
    """Exercise frozen issuance semantics without constructing a hosted provider."""
    for condition in conditions:
        current = json.loads(path.read_text(encoding="utf-8"))
        if current["run_status"] != "running":
            return current
        mark_issued(path, condition.condition_id)
        terminal = outcome(condition)
        integrity = terminal.startswith("epoch_integrity:")
        mark_terminal(path, condition.condition_id, terminal.removeprefix("epoch_integrity:"), integrity=integrity)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload["run_status"] == "running":
        payload["run_status"] = "completed"
        write_corpus_report(path, payload)
    return payload
