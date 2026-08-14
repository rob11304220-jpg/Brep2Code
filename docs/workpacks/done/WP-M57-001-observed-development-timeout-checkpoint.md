# WP-M57-001: Observed-Development Timeout Checkpoint Recovery

- Status: done
- Milestone: M57
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Make the explicit multi-case observation-only runner write an atomic
`interrupted` checkpoint when a provider request times out, retaining only
completed-case evidence and accurate issued-request accounting.

## Scope

- Reproduce the timeout with a deterministic fake/loopback provider.
- Catch the bounded provider timeout at the aggregate runner boundary.
- Write an `interrupted` report containing current case ID, non-sensitive error
  class, completed cases, and consumed request count.
- Add focused regression and preserve normal completed checkpoints.

## Compatibility constraints

Offline and credential-free only. No hosted retry, no M54 report reuse, no
provider/model/prompt/manifest change, and no alteration of M48 egress or
no-input execution boundaries.

## Trace/schema changes

Additive interrupted-run fields are allowed only if documented and covered by
focused regression; never store credentials, raw provider output, or paths in
provider-visible content.

## Decision-package impact

- `decision_id`: `q01-q02-observation-build-separation-v1`.
- Q03/Q04 effect: makes timeout disposition fail-closed and resumable without
  reusing request budget.
- Evidence role: offline provider-lifecycle recovery regression.
- Knowledge disposition: no reusable modeling knowledge.

## Acceptance

```powershell
uv run python -m pytest tests\test_observed_build_loop.py tests\test_corpus_m4.py -q
uv run python -m pytest -m sandbox -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Status transition

Record owner acceptance and Liaol independent review before closure. M54 then
requires a new report path, fresh preflight, and fresh itemized authorization.

## Implementation and owner acceptance

- The aggregate `observed-development` boundary writes an atomic `running`
  checkpoint before its first request and after each completed case.
- A first-pass `ProviderRequestTimeoutError` consumes one issued request,
  writes `interrupted` with the current case ID and exception class, retains
  only prior completed cases, and ends the batch without retrying or advancing
  to later cases.
- A deterministic offline fake-provider regression completes the first of two
  cases, times out on the second, and verifies one retained case, two issued
  requests, zero remaining requests, and no retry.
- Owner acceptance (2026-08-08): focused observed suite `9 passed in 37.32s`;
  focused corpus suite `39 passed in 99.92s`; sandbox suite `73 passed, 92
  deselected in 174.17s`; full suite `165 passed in 189.10s`; Ruff,
  governance audit, and `git diff --check` passed.
- Pending: Liaol independent G2 review.

## Independent review and closure

- Liaol independently reviewed the timeout regression, atomic report fields,
  issued-request accounting, no-retry behavior, acceptance output, and
  lifecycle alignment on 2026-08-08.
- Review outcome: approved. M57 is offline provider-lifecycle recovery
  evidence only; it does not authorize a provider request or M54 budget reuse.

## Out of scope

Retrying the timeout, reusing M54's remaining budget, hosted calls, or claims
about model quality.
