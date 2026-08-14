# WP-M117-001: Hosted-Stability Re-entry Evidence Review

- Status: done
- Milestone: M117
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Review only retained, local evidence to decide whether a fresh hosted-stability
experiment may be proposed for later G3 preflight. This package neither
constructs a provider nor sends a request.

## Scope

- Compare M69, M72, M80-v2, M82 and M89-003 terminal records against one
  explicit re-entry predicate: all observations in a proposed fresh stability
  set must have parseable terminal reports, no provider timeout or lifecycle
  error, and a locally admissible generated-script path where a script exists.
- Preserve M69/M72/M80/M89 accounting, reports, monitors, budgets and
  authorizations as terminal and non-reusable.
- Record whether M82's local static API gate and M89-003's bounded-output
  telemetry are prerequisites only, rather than evidence of stable provider
  lifecycle.
- If the predicate is not supported, close as blocked-by-hosted-stability with
  a precise re-entry requirement. If it is supported, propose—but do not
  activate—a separately selected G3 stability-preflight package.

## Compatibility constraints

Offline and credential-free. Read only existing local policy, preflight,
terminal-report and review records. Do not read held-out inputs; modify or
reuse an existing report/monitor/budget/authorization; construct a provider;
run preflight; request authorization; issue a request; change a card, prompt,
model, endpoint, manifest, case/split, sandbox or Harness gate; or claim
provider, model or general CAD quality.

## Acceptance

```powershell
uv run python -m pytest tests\test_agent_m3_provider_trace.py tests\test_harness_m2.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Status transition

Record owner review evidence and conclusion, then obtain Liaol's independent
review before closure. Update `status.md` first, then this workpack and the
handoff; archive the handoff after closure.

## Owner evidence review and acceptance (2026-08-11)

- The predicate and retained-evidence assessment are recorded in
  [`m117-hosted-stability-reentry-evidence-review.md`](../../architecture/v1/m117-hosted-stability-reentry-evidence-review.md).
- M72 fails the predicate with its terminal `provider_request_timeout`; M80-v2
  fails it because the returned script was not API-admissible. M82 is a local
  prevention control, while M89-003 is one bounded success that cannot create
  a fresh stability set or erase terminal failures.
- The outcome is therefore **no direct M115 calibration**. It may only support
  a future, separately selected stability-only G3 preflight with fresh policy,
  accounting and paths.
- Acceptance passed: focused provider/Harness tests (22 passed in 28.63
  seconds), Ruff, governance audit and `git diff --check`. Liaol's independent
  G2 review is required before closure.

## Independent G2 review and closure (2026-08-11)

Liaol independently approved closure. The review accepted the explicit
predicate, the classifications of M69/M72/M80/M82/M89-003, and the conclusion
that no retained record can authorize direct calibration. It permits only the
user-selected creation of a new, stability-only G3 preflight package; it grants
no provider construction, preflight result, request, budget reuse or hosted
authorization.

## Out of scope

Any hosted experiment or authorization; development calibration; M97 reuse;
held-out activity; retry/repair; dependency installation; runtime promotion;
or a conclusion from one successful request.
