# Handoff: M70 durable hosted-run monitor

- **Date**: 2026-08-09
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M70-001-durable-hosted-run-monitor`

## Goal

Implement and offline-verify a report-driven, durable monitor for an already-authorized hosted run. The monitor must be read-only with respect to provider work, corpus reports, credentials, prompts and budget.

## Done

- User selected and activated M70; Codex is the owner and Liaol is the independent G2 reviewer.
- Implemented isolated monitor state, `monitor setup|observe|teardown`, deterministic tests, ADR-0050 and the durable-monitor runbook.
- Targeted monitor test, focused Ruff, governance audit and patch-format check pass.

## In progress

- M70 is closed with Liaol's independent G2 approval; the unrelated provider-fixture mismatch has a separately selected follow-up.

## Next

- Activate and complete the separately selected provider-response fixture-alignment workpack.

## Decisions

- Monitor state is separate from, and never mutates, corpus reports. Missing, malformed or stale reports must stop monitoring and request operator action.

## Blockers

- None for M70.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/active/WP-M70-001-durable-hosted-run-monitor.md` |
| Reports | `brep2code/corpus/report.py` |
| Monitor | `brep2code/monitor.py`; `docs/runbooks/durable-hosted-run-monitor.md` |
| Commands | `uv run python -m pytest tests/test_durable_monitor.py -q`; `uv run python tools/check_governance.py` |

## Resume prompt

```
Continue M70 durable hosted-run monitor.
Read docs/handoff/active/2026-08-09-m70-durable-hosted-run-monitor.md and the active M70 workpack.
First action: obtain Liaol's independent review and resolve or separately scope the provider-fixture full-suite blocker.
```
