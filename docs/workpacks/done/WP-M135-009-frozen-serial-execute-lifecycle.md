# WP-M135-009: Frozen Serial Execute Lifecycle

- Status: done
- Milestone: M135
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Implement and validate the offline-only 18-condition serial lifecycle that
uses M135-008's frozen request contract, one fake response and one no-input
Harness execution per condition, with durable checkpoint accounting.

## Scope

- Add a runner that accepts only `FakeLLMProvider`, issues conditions in frozen
  order, records `issued` before completion and records one terminal state
  before moving to the next condition.
- Execute each returned replacement script through `ManualHarness` with
  `WslBubblewrapExecutor` and `build_without_input=True`; retain zero repair
  and retry behavior.
- Prove all 18 fixed reference-script responses complete serially, and prove a
  condition-level lifecycle failure continues without bypassing accounting.
- Update focused tests, lifecycle record, status and handoff.

## Compatibility constraints

The fixed cohort, request/card hashes, provider/model, executor, deadline,
18-request cap and zero repair/retry boundary remain unchanged. Default
operation remains offline and credential-free. Do not construct a non-fake
provider, access credentials, issue hosted requests, send data, modify cards,
cases or manifests, or reuse hosted report/monitor paths.

## Acceptance

```powershell
uv run python -m pytest tests\test_m135_epoch.py -q
uv run python -m pytest -m fast -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish all-condition fake-provider serial evidence and failure-accounting
regressions, pass all acceptance commands, then obtain Liaol's independent G3
review. A separate user-selected hosted-preflight workpack remains required
before any itemized hosted authorization request.

## Permitted stop conditions

Independent review; explicit hosted authorization; frozen-input drift;
out-of-scope dependency; or reproducible offline validation blocker.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff. Keep the workpack active while awaiting independent review because
the governance audit requires active-directory workpacks to say `Status:
active`.

## Out of scope

Hosted execution or authorization; non-fake provider construction; credential
access; retry or repair; cohort/prompt/card/model/provider changes; held-out
evaluation; card promotion; and M137 terminal review.

## Owner completion evidence (2026-08-12)

`run_fake_serial_epoch()` accepts only `FakeLLMProvider`, durably marks each
of the 18 frozen conditions issued before exactly one frozen request, and runs
each returned script through no-input `WslBubblewrapExecutor` Harness
execution. The full regression completes at 18 used / 0 remaining with all
`full_success`; a separate regression shows downstream-gate,
sandbox-execution and lifecycle-before-script condition terminals continue
the fixed serial accounting. Details are recorded in
[`m135-009-frozen-serial-execute-lifecycle.md`](../../workflow/m135-009-frozen-serial-execute-lifecycle.md).

Owner-side acceptance passed: focused M135 `12 passed in 204.27s`; fast `66
passed`; full suite `250 passed in 558.51s`; Ruff, governance audit and diff
check passed. Await Liaol's independent G3 review. No non-fake provider was
constructed and no hosted authorization is granted.

## Independent review and closure (2026-08-12)

Liaol approved the independent G3 review. The review accepted the fake-only
scope, 18-condition serial accounting, no-input Harness evidence and all
recorded owner-side validation. It grants no hosted authorization. A fresh
preflight remains separately scoped in M135-010.
