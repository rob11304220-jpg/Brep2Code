import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from brep2code.cli import main
from brep2code.monitor import MonitorError, observe_monitor, setup_monitor, teardown_monitor


NOW = datetime(2026, 8, 9, 12, 0, tzinfo=timezone.utc)


def _report(path: Path, status: str) -> None:
    path.write_text(json.dumps({"run_status": status}), encoding="utf-8")


def test_setup_and_no_progress_observation_leave_report_unchanged(tmp_path: Path) -> None:
    report = tmp_path / "report.json"
    state = tmp_path / "monitor.json"
    _report(report, "running")
    before = report.read_text(encoding="utf-8")

    setup = setup_monitor(report, state, stale_after_seconds=60, now=NOW)
    observed = observe_monitor(state, now=NOW + timedelta(seconds=1))

    assert setup["heartbeat"]["count"] == 1
    assert observed["heartbeat"]["count"] == 2
    assert observed["last_lifecycle_phase"] == "running"
    assert observed["last_progress"] == "no_progress"
    assert report.read_text(encoding="utf-8") == before


def test_terminal_reports_write_operator_handoff_and_stop_monitoring(tmp_path: Path) -> None:
    for status in ("completed", "interrupted"):
        report = tmp_path / f"{status}.json"
        state = tmp_path / f"{status}-monitor.json"
        _report(report, status)

        payload = setup_monitor(report, state, stale_after_seconds=60, now=NOW)
        again = observe_monitor(state, now=NOW + timedelta(seconds=1))

        assert payload["monitor_status"] == "terminal"
        assert payload["terminal_status"] == status
        assert payload["operator_handoff"]["code"] == "terminal_report"
        assert again == payload


def test_missing_malformed_and_stale_reports_require_operator_action(tmp_path: Path) -> None:
    missing_state = tmp_path / "missing-monitor.json"
    missing = setup_monitor(tmp_path / "missing.json", missing_state, stale_after_seconds=60, now=NOW)
    assert missing["operator_handoff"]["code"] == "missing_report"

    malformed_report = tmp_path / "malformed.json"
    malformed_report.write_text("not-json", encoding="utf-8")
    malformed = setup_monitor(malformed_report, tmp_path / "malformed-monitor.json", stale_after_seconds=60, now=NOW)
    assert malformed["operator_handoff"]["code"] == "malformed_report"

    stale_report = tmp_path / "stale.json"
    _report(stale_report, "running")
    stale_time = (NOW - timedelta(seconds=61)).timestamp()
    import os
    os.utime(stale_report, (stale_time, stale_time))
    stale = setup_monitor(stale_report, tmp_path / "stale-monitor.json", stale_after_seconds=60, now=NOW)
    assert stale["operator_handoff"]["code"] == "stale_report"


def test_teardown_and_cli_never_need_provider_configuration(tmp_path: Path, capsys) -> None:
    report = tmp_path / "report.json"
    state = tmp_path / "monitor.json"
    _report(report, "running")

    assert main(["monitor", "setup", "--report", str(report), "--state", str(state)]) == 0
    assert main(["monitor", "teardown", "--state", str(state)]) == 0
    payload = teardown_monitor(state, now=NOW)

    assert payload["terminal_status"] == "operator_teardown"
    assert '"monitor_status": "stopped"' in capsys.readouterr().out


def test_setup_refuses_to_use_the_report_as_monitor_state(tmp_path: Path) -> None:
    report = tmp_path / "report.json"
    _report(report, "running")

    try:
        setup_monitor(report, report, stale_after_seconds=60, now=NOW)
    except MonitorError as exc:
        assert exc.code == "invalid_state_path"
    else:
        raise AssertionError("expected report/state path separation")
