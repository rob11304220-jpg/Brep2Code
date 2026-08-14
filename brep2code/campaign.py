"""Offline preparation contract for one frozen hosted campaign."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import shutil

from brep2code.corpus.report import write_corpus_report
from brep2code.monitor import setup_monitor


SCHEMA_VERSION = 1
_CARD_PATHS = {
    "vertical-cylinder-construction": "runtime_resources/experience-cards/cards/vertical-cylinder-construction.json",
}
_FORBIDDEN_TRANSCRIPT_KEYS = {"input_step", "raw_step", "reference_script", "path", "filename"}


class CampaignError(ValueError):
    """A fail-closed campaign-spec or preparation error."""


def canonical_json(payload: object) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def prepare_campaign(
    spec_path: Path,
    report_path: Path,
    monitor_path: Path,
    *,
    root: Path,
    stale_after_seconds: int = 300,
) -> dict:
    """Validate one campaign locally and create its fresh prepared checkpoint.

    This function neither reads provider credentials nor constructs a provider.
    """

    if report_path.exists() or monitor_path.exists():
        raise CampaignError("campaign report and monitor paths must be fresh")
    if report_path.resolve() == monitor_path.resolve():
        raise CampaignError("campaign report and monitor paths must differ")
    spec = _load_spec(spec_path)
    _validate_spec(spec, root)
    input_sha256 = _validate_registered_case(spec["case"], root)
    transcript = spec["q01"]["transcript"]
    transcript_sha256 = sha256(canonical_json(transcript).encode("utf-8")).hexdigest()
    card = _validate_card(spec["reference"], root)
    execution = spec["execution"]
    if shutil.which("wsl.exe") is None and shutil.which("wsl") is None:
        raise CampaignError("wsl-bwrap executor is unavailable")
    spec_sha256 = sha256(canonical_json(spec).encode("utf-8")).hexdigest()
    payload = {
        "schema_version": SCHEMA_VERSION,
        "policy": "frozen-hosted-campaign-launcher-v1",
        "run_status": "running",
        "request_state": "prepared",
        "campaign_id": spec["campaign_id"],
        "campaign_spec_sha256": spec_sha256,
        "provider": execution["provider"],
        "model": execution["model"],
        "requests_used": 0,
        "requests_remaining": execution["max_requests"],
        "campaign_contract": {
            "case_id": spec["case"]["case_id"],
            "input_sha256": input_sha256,
            "split_authority_sha256": spec["case"]["split_authority_sha256"],
            "transcript_sha256": transcript_sha256,
            "reference": card,
            "executor": execution["executor"],
            "provider_deadline_seconds": execution["provider_deadline_seconds"],
            "max_output_tokens": execution["max_output_tokens"],
            "max_repair_rounds": spec["generation"]["max_repair_rounds"],
            "max_requests": execution["max_requests"],
            "monitor_path": str(monitor_path),
            "authorization": "not_authorized",
            "provider_constructed": False,
        },
    }
    write_corpus_report(report_path, payload)
    setup_monitor(report_path, monitor_path, stale_after_seconds=stale_after_seconds)
    return payload


def validate_execute_admission(payload: dict, spec_path: Path, monitor_path: Path, *, root: Path) -> None:
    """Validate only the immutable future-execute admission boundary.

    Authorization/provider construction intentionally belong to a future G3
    executor and are not performed here.
    """

    spec = _load_spec(spec_path)
    _validate_spec(spec, root)
    input_sha256 = _validate_registered_case(spec["case"], root)
    transcript_sha256 = sha256(canonical_json(spec["q01"]["transcript"]).encode("utf-8")).hexdigest()
    reference = _validate_card(spec["reference"], root)
    execution = spec["execution"]
    contract = payload.get("campaign_contract")
    if (
        payload.get("run_status") != "running"
        or payload.get("request_state") != "prepared"
        or payload.get("requests_used") != 0
        or not isinstance(contract, dict)
        or contract.get("authorization") != "not_authorized"
        or contract.get("provider_constructed") is not False
        or contract.get("monitor_path") != str(monitor_path)
        or payload.get("campaign_spec_sha256") != sha256(canonical_json(spec).encode("utf-8")).hexdigest()
        or contract.get("case_id") != spec["case"]["case_id"]
        or contract.get("input_sha256") != input_sha256
        or contract.get("split_authority_sha256") != spec["case"]["split_authority_sha256"]
        or contract.get("transcript_sha256") != transcript_sha256
        or contract.get("reference") != reference
        or contract.get("executor") != execution["executor"]
        or contract.get("provider_deadline_seconds") != execution["provider_deadline_seconds"]
        or contract.get("max_output_tokens") != execution["max_output_tokens"]
        or contract.get("max_repair_rounds") != 0
        or contract.get("max_requests") != execution["max_requests"]
    ):
        raise CampaignError("campaign checkpoint is not a fresh execute-admission candidate")


def _load_spec(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CampaignError("campaign spec is unavailable") from exc
    except json.JSONDecodeError as exc:
        raise CampaignError("campaign spec is invalid JSON") from exc
    if not isinstance(payload, dict):
        raise CampaignError("campaign spec must be an object")
    return payload


def _validate_spec(spec: dict, root: Path) -> None:
    required = {"schema_version", "campaign_id", "case", "q01", "reference", "generation", "execution"}
    if set(spec) != required or spec.get("schema_version") != SCHEMA_VERSION:
        raise CampaignError("campaign spec schema mismatch")
    if not isinstance(spec["campaign_id"], str) or not spec["campaign_id"]:
        raise CampaignError("campaign_id must be non-empty")
    case = spec["case"]
    if not isinstance(case, dict) or set(case) != {"case_id", "input_sha256", "data_split", "split_authority", "split_authority_sha256"}:
        raise CampaignError("campaign case boundary is invalid")
    if case["data_split"] != "development":
        raise CampaignError("M139 permits development inputs only")
    if not all(isinstance(case[key], str) and case[key] for key in case):
        raise CampaignError("campaign case values must be non-empty strings")
    split_path = _repo_file(root, case["split_authority"], "split authority")
    if _sha256(split_path) != case["split_authority_sha256"] or not _split_contains(split_path, case["case_id"], case["data_split"]):
        raise CampaignError("campaign split authority drift")
    q01 = spec["q01"]
    if not isinstance(q01, dict) or set(q01) != {"transcript"} or not isinstance(q01["transcript"], dict):
        raise CampaignError("campaign Q01 transcript is invalid")
    transcript = q01["transcript"]
    if transcript.get("data_split") != "development" or _has_forbidden_transcript_key(transcript):
        raise CampaignError("campaign Q01 transcript violates egress boundary")
    reference = spec["reference"]
    if not isinstance(reference, dict) or reference.get("mode") not in {"none", "explicit_card"}:
        raise CampaignError("campaign reference mode is invalid")
    if reference["mode"] == "none" and set(reference) != {"mode"}:
        raise CampaignError("no-card reference must not carry material")
    if reference["mode"] == "explicit_card" and set(reference) != {"mode", "card_id", "index_sha256", "card_sha256", "role"}:
        raise CampaignError("explicit card reference is invalid")
    generation = spec["generation"]
    if generation != {"first_pass": True, "repair_policy": "none", "max_repair_rounds": 0}:
        raise CampaignError("M139 permits first pass and zero repair only")
    execution = spec["execution"]
    required_execution = {"provider", "model", "executor", "provider_deadline_seconds", "max_output_tokens", "max_requests"}
    if not isinstance(execution, dict) or set(execution) != required_execution:
        raise CampaignError("campaign execution boundary is invalid")
    if execution["provider"] != "deepseek" or execution["model"] != "deepseek-v4-pro" or execution["executor"] != "wsl-bwrap":
        raise CampaignError("M139 execution selection is unsupported")
    if not isinstance(execution["provider_deadline_seconds"], int) or execution["provider_deadline_seconds"] < 1:
        raise CampaignError("campaign provider deadline is invalid")
    if not isinstance(execution["max_output_tokens"], int) or execution["max_output_tokens"] < 1:
        raise CampaignError("campaign output token cap is invalid")
    if execution["max_requests"] != 1:
        raise CampaignError("M139 zero-repair campaign requires one request")


def _validate_registered_case(case: dict, root: Path) -> str:
    record_path = root / "case-library" / "self-authored" / case["case_id"] / "case.json"
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
        input_path = record_path.parent / record["input_step"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as exc:
        raise CampaignError("registered case is unavailable") from exc
    digest = _sha256(input_path)
    if record.get("case_id") != case["case_id"] or digest != record.get("sha256") or digest != case["input_sha256"]:
        raise CampaignError("registered case input hash drift")
    return digest


def _validate_card(reference: dict, root: Path) -> dict | None:
    if reference["mode"] == "none":
        return None
    card_id = reference["card_id"]
    relative = _CARD_PATHS.get(card_id)
    if relative is None:
        raise CampaignError("campaign card is not registered")
    index_path = root / "runtime_resources" / "experience-cards" / "index.json"
    card_path = root / relative
    if _sha256(index_path) != reference["index_sha256"] or _sha256(card_path) != reference["card_sha256"]:
        raise CampaignError("campaign card hash drift")
    card = json.loads(card_path.read_text(encoding="utf-8"))
    if card.get("id") != card_id or f"cards/{card_path.name}" not in json.loads(index_path.read_text(encoding="utf-8")).get("cards", []):
        raise CampaignError("campaign card index drift")
    return {"card_id": card_id, "index_sha256": reference["index_sha256"], "card_sha256": reference["card_sha256"], "role": reference["role"]}


def _repo_file(root: Path, value: str, label: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise CampaignError(f"{label} path must be repository-relative")
    resolved = root / path
    if not resolved.is_file():
        raise CampaignError(f"{label} is unavailable")
    return resolved


def _split_contains(path: Path, case_id: str, data_split: str) -> bool:
    def walk(value: object) -> bool:
        if isinstance(value, dict):
            if value.get("case_id") == case_id and value.get("data_split") == data_split:
                return True
            return any(walk(item) for item in value.values())
        if isinstance(value, list):
            return any(walk(item) for item in value)
        return False
    return walk(json.loads(path.read_text(encoding="utf-8")))


def _has_forbidden_transcript_key(value: object) -> bool:
    if isinstance(value, dict):
        return any(key in _FORBIDDEN_TRANSCRIPT_KEYS or _has_forbidden_transcript_key(item) for key, item in value.items())
    if isinstance(value, list):
        return any(_has_forbidden_transcript_key(item) for item in value)
    return False


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()
