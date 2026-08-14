# WP-M81-001: Monitorable Single-Request Checkpoints

- Status: done
- Milestone: M81
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Make the existing `provider-control` and `observed-first-pass` commands
produce atomic, content-free `running` checkpoints before an authorized
provider request, so the unchanged M70 monitor can observe their lifecycle.

## Scope

- Add explicit prepare/execute lifecycle operations for the two single-request
  commands. Only the producer writes its report; M70 remains report-read-only.
- Make execute refuse a missing, malformed, terminal, or non-prepared report;
  write request issuance immediately before the provider call and a parseable
  terminal completed/interrupted report afterward.
- Preserve no prompt/response/credential/STEP retention, one-request bounds,
  existing hosted authorization checks, non-streaming transport, and
  `wsl-bwrap` enforcement.
- Add deterministic offline tests for preparation, monitor attachment,
  terminal transitions, timeout checkpointing and overwrite refusal.

## Out of scope

Provider request, credential inspection, model/endpoint/prompt change,
manifest/case change, M80 report preparation, background launch service,
monitor mutation, retry, or hosted authorization.

## Acceptance

```powershell
uv run python -m pytest tests\test_observed_build_loop.py tests\test_durable_monitor.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Status transition

Liaol selected M81 on 2026-08-10. M81 must be independently reviewed before
re-entering M80. Its closure does not authorize M80 or any provider request.

## Owner acceptance record

- Added producer-owned `prepare`/`execute` phases to `provider-control` and
  `observed-first-pass`. Prepared reports are content-free, monitorable
  `running` checkpoints; execute records issuance immediately before the
  request and terminalizes handled lifecycle failures.
- M70 remains unchanged and report-read-only. Offline regressions cover monitor
  attachment, terminal transition, old-report refusal and timeout accounting.
- 2026-08-10 acceptance passed: `uv run python -m pytest
  tests\test_observed_build_loop.py tests\test_durable_monitor.py -q` — 22
  passed in 42.08s; `uv run python -m ruff check .`,
  `uv run python tools\check_governance.py`, and `git diff --check` passed.
- Pending independent review: Liaol must verify the producer/monitor
  separation, prepared/issued/terminal transitions, timeout accounting, and
  absence of hosted egress.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-10. The review confirms producer-owned reports,
  M70 read-only separation, lifecycle/timeout accounting coverage, and no
  hosted egress.
- Closure rationale: M81 closes the local monitorability gap. It authorizes
  only a fresh M80 preflight, never a provider request or reuse of a report.
