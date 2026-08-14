# WP-M60-001: Observed-Development Lifecycle-Diagnostic Checkpoint

- Status: done
- Milestone: M60
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Atomically project M58's existing sanitized provider-worker lifecycle
diagnostics into an `observed-development` interruption checkpoint, so a
future separately authorized batch retains phase evidence when a request
terminates.

## Scope

- Preserve only `last_phase`, phase events with monotonic elapsed milliseconds,
  and sanitized `error_class` beneath a checkpoint interruption.
- Handle M58 timeout and lifecycle-error exits as terminal, issued-request
  interruptions without retrying or advancing to a later case.
- Reject malformed diagnostic fields rather than serializing them.
- Update the observed-build contract and add deterministic local checkpoint
  regressions for startup-unobserved, in-flight HTTP wait, and returned-worker
  error diagnostics.

## Compatibility constraints

Offline and credential-free only. No provider construction/call, manifest or
prompt change, M54 retry, report-path reuse, request-budget reuse, executor
policy change, or external data. Default execution remains network-free. A
timeout remains fail-closed and terminates its worker.

## Trace/schema boundary

The additive checkpoint `diagnostics` object must contain no request content,
credentials, URLs, local paths, raw provider output, environment values, or
timeout configuration. Existing interruption code, case ID, exception class,
request issuance accounting, and atomic checkpoint behavior remain unchanged.

## Acceptance

```powershell
uv run python -m pytest tests\test_observed_build_loop.py -q
uv run python -m pytest tests\test_agent_m3_repair_loop.py tests\test_observed_build_loop.py -q
uv run python -m pytest -m sandbox -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Status transition

Record owner acceptance and Liaol independent review before closure. Update
`status.md` first, then this workpack and handoff; archive the handoff on
closure. M54 remains blocked.

## Owner acceptance

- `observed-development` now maps both M58 timeout and lifecycle-error exits to
  one terminal interruption checkpoint. The request count is decremented once,
  no subsequent case is run, and the existing timeout code/case/exception
  fields remain present.
- The checkpoint rebuilds diagnostics only when the exact M58 schema passes its
  phase, monotonic timing, and error-class checks; malformed or extra fields
  are omitted.
- Added deterministic local coverage for startup-unobserved, HTTP-wait, and
  returned-worker-error diagnostics, plus malformed-field rejection.
- Offline acceptance passed on 2026-08-08:
  - `uv run python -m pytest tests\test_agent_m3_repair_loop.py tests\test_observed_build_loop.py -q` — 18 passed
  - `uv run python -m pytest -m sandbox -q` — 77 passed, 92 deselected
  - `uv run python -m pytest` — 169 passed
  - `uv run python -m ruff check .` — passed
  - `uv run python tools\check_governance.py` — passed
  - `git diff --check` — passed

## Closure rationale

Liaol independently approved M60 on 2026-08-09 after reviewing checkpoint
behavior, the strict diagnostic schema boundary, offline test evidence, and
M54 non-retry compliance. M54 remains blocked; this work issued no provider
request and did not reuse its interrupted-batch budget.

## Independent review

- Reviewer: Liaol
- Outcome: approved on 2026-08-09
- Verified: G2 scope, atomic interruption semantics, diagnostic whitelist,
  request accounting, offline test evidence, and governance alignment.

## Out of scope

Hosted preflight or connectivity tests, provider retries, credential access,
new hosted samples, causal/model-quality claims, or diagnostic-driven budget
reuse.
