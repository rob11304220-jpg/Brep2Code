"""Offline, report-driven monitoring for already-authorized hosted runs.

This module observes a corpus report and writes only a separate monitor-state
file. It never constructs a provider, reads credentials, launches a process,
or changes a corpus report.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from uuid import uuid4


SCHEMA_VERSION = 1
RUNNING = "running"
TERMINAL_STATUSES = {"completed", "interrupted"}
VALID_RUN_STATUSES = {RUNNING, *TERMINAL_STATUSES}


class MonitorError(ValueError):
    """A monitor input or state-contract failure with a stable operator code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def setup_monitor(
    report_path: Path | str,
    state_path: Path | str,
    *,
    stale_after_seconds: int,
    now: datetime | None = None,
) -> dict:
    """Create monitor-owned state from one report observation.

    Invalid reports are recorded as an operator handoff rather than retried.
    """
    report = Path(report_path)
    state = Path(state_path)
    _validate_paths(report, state)
    observed_at = _utc_now(now)
    base = _base_state(report, stale_after_seconds, observed_at)
    try:
        return _observe(base, report, observed_at, initial=True, state_path=state)
    except MonitorError as exc:
        return _operator_action(base, observed_at, exc, state)


def observe_monitor(state_path: Path | str, *, now: datetime | None = None) -> dict:
    """Observe once; never wait, retry, launch, or signal a hosted process."""
    state = Path(state_path)
    payload = _read_state(state)
    observed_at = _utc_now(now)
    if payload["monitor_status"] != "monitoring":
        return payload
    report = Path(payload["report_path"])
    try:
        return _observe(payload, report, observed_at, initial=False, state_path=state)
    except MonitorError as exc:
        return _operator_action(payload, observed_at, exc, state)


def teardown_monitor(state_path: Path | str, *, now: datetime | None = None) -> dict:
    """Stop monitor lifecycle locally without changing the observed report."""
    state = Path(state_path)
    payload = _read_state(state)
    if payload["monitor_status"] == "monitoring":
        observed_at = _utc_now(now)
        payload.update(
            {
                "monitor_status": "stopped",
                "terminal_status": "operator_teardown",
                "operator_handoff": {
                    "code": "operator_teardown",
                    "message": "Monitoring was stopped by the operator; inspect the report before any new run.",
                    "observed_at": observed_at,
                },
            }
        )
        _write_state(state, payload)
    return payload


def _base_state(report: Path, stale_after_seconds: int, observed_at: str) -> dict:
    if stale_after_seconds < 0:
        raise MonitorError("invalid_stale_after", "stale-after seconds must be non-negative")
    return {
        "schema_version": SCHEMA_VERSION,
        "report_path": str(report.resolve()),
        "stale_after_seconds": stale_after_seconds,
        "monitor_status": "monitoring",
        "heartbeat": {"count": 0, "observed_at": observed_at},
        "last_lifecycle_phase": None,
        "last_report_mtime_ns": None,
        "last_progress": None,
        "terminal_status": None,
        "operator_handoff": None,
    }


def _observe(payload: dict, report: Path, observed_at: str, *, initial: bool, state_path: Path) -> dict:
    report_payload = _read_report(report)
    lifecycle = report_payload["run_status"]
    report_mtime_ns = report.stat().st_mtime_ns
    if lifecycle == RUNNING:
        age = datetime.fromtimestamp(report.stat().st_mtime, timezone.utc)
        elapsed = datetime.fromisoformat(observed_at) - age
        if elapsed.total_seconds() > payload["stale_after_seconds"]:
            raise MonitorError("stale_report", "report heartbeat is older than the configured stale window")
    previous_mtime = payload["last_report_mtime_ns"]
    payload["heartbeat"] = {"count": payload["heartbeat"]["count"] + 1, "observed_at": observed_at}
    payload["last_lifecycle_phase"] = lifecycle
    payload["last_report_mtime_ns"] = report_mtime_ns
    payload["last_progress"] = "initial" if initial else (
        "no_progress" if previous_mtime == report_mtime_ns else "report_updated"
    )
    if lifecycle in TERMINAL_STATUSES:
        payload["monitor_status"] = "terminal"
        payload["terminal_status"] = lifecycle
        payload["operator_handoff"] = {
            "code": "terminal_report",
            "message": "Terminal report observed; review it before any new authorized run.",
            "observed_at": observed_at,
        }
    _write_state(state_path, payload)
    return payload


def _operator_action(payload: dict, observed_at: str, error: MonitorError, state_path: Path) -> dict:
    payload["monitor_status"] = "operator_action_required"
    payload["terminal_status"] = "operator_action_required"
    payload["operator_handoff"] = {
        "code": error.code,
        "message": str(error),
        "observed_at": observed_at,
    }
    _write_state(state_path, payload)
    return payload


def _read_report(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise MonitorError("missing_report", "report does not exist") from exc
    except json.JSONDecodeError as exc:
        raise MonitorError("malformed_report", "report is not valid JSON") from exc
    if not isinstance(payload, dict) or payload.get("run_status") not in VALID_RUN_STATUSES:
        raise MonitorError("malformed_report", "report must contain a supported run_status")
    return payload


def _read_state(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise MonitorError("missing_state", "monitor state does not exist") from exc
    except json.JSONDecodeError as exc:
        raise MonitorError("malformed_state", "monitor state is not valid JSON") from exc
    required = {"schema_version", "report_path", "stale_after_seconds", "monitor_status", "heartbeat"}
    if not isinstance(payload, dict) or payload.get("schema_version") != SCHEMA_VERSION or not required <= payload.keys():
        raise MonitorError("malformed_state", "monitor state does not match schema version 1")
    if payload["monitor_status"] not in {"monitoring", "terminal", "stopped", "operator_action_required"}:
        raise MonitorError("malformed_state", "monitor state has an unsupported status")
    if not isinstance(payload["heartbeat"], dict) or not isinstance(payload["heartbeat"].get("count"), int):
        raise MonitorError("malformed_state", "monitor state heartbeat is invalid")
    return payload


def _validate_paths(report: Path, state: Path) -> None:
    if report.resolve() == state.resolve():
        raise MonitorError("invalid_state_path", "monitor state path must differ from report path")


def _write_state(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    try:
        temporary.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def _utc_now(now: datetime | None) -> str:
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        raise MonitorError("invalid_time", "monitor time must be timezone-aware")
    return current.astimezone(timezone.utc).isoformat()
