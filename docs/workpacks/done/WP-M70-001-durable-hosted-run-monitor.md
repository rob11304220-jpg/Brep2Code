# WP-M70-001: Durable Hosted-Run Monitor

- Status: done
- Milestone: M70
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

Implement report-driven heartbeat setup/teardown and terminal handoff records.
The monitor is read-only except for its own automation lifecycle; it never
retries, spends budget, changes prompts, or issues provider calls.

## Goal

Make long-running, already-authorized hosted processes observable beyond an
interactive command window without giving the monitor authority over provider
work.

## Scope

- Define a versioned, report-driven monitor state: report path, heartbeat,
  last observed lifecycle phase, terminal status and operator handoff record.
- Add deterministic local tests for setup, no-progress observation, terminal
  completion/interruption and teardown.
- Document the durable launch and handoff procedure, including the fact that a
  monitor may wake a task but cannot resume an interrupted run.

## Dependencies and stopping rule

M69 is complete. This workpack is offline and may proceed only after a user
selects it. Stop at a missing, malformed or stale report: record the condition
and request operator action; do not infer process health or launch a retry.

## Compatibility constraints

Default execution remains network-free. Do not construct a provider, read
credentials, alter report schemas outside monitor-owned records, mutate a
corpus report, reuse a budget, change prompt/executor policy, or add an
unbounded background service.

## Acceptance

```powershell
uv run python -m pytest tests -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

The selected focused tests may replace the full suite only when the validation
plan records their independent coverage and duration boundary.

## Status transition

Before activation, assign one owner and retain an independent reviewer. Update
`docs/workflow/status.md` first, then this workpack and an active handoff.
Record monitor-owned files, acceptance output and review before closure.

## Collaboration plan

- Owner: Codex; exclusive paths are `brep2code/monitor.py`, the monitor CLI,
  monitor tests and this workpack's lifecycle records.
- Independent reviewer: Liaol; review the report/state separation, fail-closed
  outcomes, acceptance output and lifecycle alignment before closure.
- Closure condition: all acceptance gates have terminal passing output and the
  independent review records no scope or evidence-boundary issue.

## Implementation evidence

- Added `brep2code.monitor`: versioned, atomically written monitor-owned
  state with report path, heartbeat, lifecycle phase, progress state, terminal
  outcome and operator handoff.
- Added `brep2code monitor setup|observe|teardown`. It only reads the report;
  setup/observe never construct a provider or access provider configuration.
- Missing, malformed and stale `running` reports stop with an
  `operator_action_required` handoff. Terminal reports stop monitoring;
  teardown only records `operator_teardown` in monitor state.
- Added the durable launch/handoff runbook and ADR-0050.

## Validation record

- `uv run python -m pytest tests\\test_durable_monitor.py -q` — pass: 5
  passed in 0.15s.
- `uv run python -m ruff check brep2code\\monitor.py brep2code\\cli\\__init__.py tests\\test_durable_monitor.py` — pass.
- `uv run python tools\\check_governance.py` — pass.
- `git diff --check` — pass.
- `uv run python -m pytest -m fast -q` — blocked by one pre-existing failure:
  `test_deepseek_provider_loads_ignored_env_file_and_parses_script_replacement`
  uses a response fixture without `headers`, while the current provider reads
  request-id headers. Result: 57 passed, 1 failed, 118 deselected.
- `uv run python -m pytest -q` — same independent provider-fixture failure;
  175 passed, 1 failed in 190.44s. No M70 file appears in that traceback.

## Review status

- Liaol independently approved closure on 2026-08-09. The review confirmed
  report/state separation, fail-closed outcomes and the recorded evidence
  boundary. The provider-fixture mismatch is moved to a new bounded workpack;
  it does not invalidate M70's monitor evidence.

## Closure rationale

- The monitor implementation and every M70-specific acceptance check pass.
- The only suite failure is an unrelated response-double mismatch; the user
  explicitly approved M70 closure and selected a separate small workpack to
  align that fixture without changing provider behavior.

## Out of scope

Provider retries, scheduled hosted launches, credential handling, prompt or
model changes, endpoint probes, CAD correctness changes and causal claims
about M69.
