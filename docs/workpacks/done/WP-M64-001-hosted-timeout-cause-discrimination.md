# WP-M64-001: Hosted Timeout-Cause Discrimination

- Status: done
- Milestone: M64
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G3

## Goal

Create a fresh, bounded diagnostic decision package that can distinguish a
transport/provider-response failure from a task-latency contribution to M63's
first-request timeout. The initial phase is read-only. No M54 or M63 budget,
report, request, or authorization is reusable.

## Scope

- Inspect the local request-construction and worker-lifecycle boundaries for
  M63's fixed `param_additive_boss_low` case without exposing request content,
  credentials, or environment values.
- Preflight two separately authorized, one-request experiments against the
  same DeepSeek endpoint and `deepseek-v4-pro` model:
  1. a minimal fixed control prompt, `Return exactly OK.`, to establish a
     credentialed endpoint/model response baseline; and
  2. one fresh replay of the fixed M63 observation transcript with a longer,
     explicitly authorized provider deadline.
- Use different new report paths and a request budget of one for each
  experiment. Preserve only sanitized lifecycle diagnostics and request
  accounting.
- Record a bounded interpretation: a timely control plus a timely extended
  fixed-case response makes task latency a plausible contributor, not proof;
  a control timeout/failure points to transport/provider responsiveness; any
  mixed or repeated timeout is inconclusive without further separately
  authorized samples.
- Add an offline-testable `provider-control` CLI command for the fixed control
  prompt. It must enforce hosted authorization, a one-request budget, a
  positive provider deadline, durable reporting, and the existing terminable
  provider-worker boundary without serializing prompt or response content.

## Compatibility constraints

No provider request, connectivity probe, credential inspection, manifest or
prompt-policy change, runtime/Harness change, M54/M63 retry, or budget/report
reuse occurs before fresh preflight and itemized user authorization. The
control prompt is the only new outbound content proposed; it contains no local
data. The fixed-case request may send only the already approved M48 path-free
bounded observation transcript. All generated execution remains `wsl-bwrap`.

## Required preflight evidence

- Verify the two experiments can use the same provider endpoint/model and
  isolated request accounting, without writing raw provider content.
- Verify each new report path has no `running` or `interrupted` checkpoint.
- Verify actual CLI timeout/budget behavior and available secure execution
  boundary; do not display credential values.
- State both experiment deadlines, data-egress content, one-request budgets,
  durable-monitoring method, and limits of the interpretation before asking
  for authorization.

## Acceptance

```powershell
uv run python -m pytest tests\test_agent_m3_repair_loop.py tests\test_observed_build_loop.py -q
uv run python tools\check_governance.py
git diff --check
```

## Status transition

M63 was independently reviewed and closed on 2026-08-09. Complete the fresh
read-only preflight, then request separate itemized user authorization for each
remote experiment. Record every terminal result and report path. G3 closure
requires Liaol independent review of evidence boundaries, request accounting,
and the limited causal interpretation.

## Read-only preflight evidence

- [`m64-hosted-timeout-diagnostic-preflight.md`](../../workflow/m64-hosted-timeout-diagnostic-preflight.md)
  records fresh manifest/configuration/executor/report-path checks and the two
  separately itemized authorization candidates.
- `uv run python -m pytest tests\test_agent_m3_repair_loop.py tests\test_observed_build_loop.py -q`
  — 20 passed on 2026-08-09.
- `uv run python -m ruff check .`, `uv run python tools\check_governance.py`,
  and `git diff --check` passed.
- No provider request, credential value, report reuse, or request-budget reuse
  occurred before authorization. The next action was itemized authorization,
  not an automatic launch.

## Authorized diagnostic evidence

- The user separately authorized both M64 experiments on 2026-08-09.
- `data/corpus-runs/m64-deepseek-control.json` reached `completed` after its
  one request within the authorized 120-second deadline. It stores no prompt
  or provider-response content.
- `data/corpus-runs/m64-param-additive-boss-low-deepseek-extended.json` reached
  `interrupted` after its one request reached the authorized 300-second
  deadline. It contains zero completed cases and only `worker_started` then
  `http_started` diagnostics.
- The comparison excludes a simple blanket endpoint/authentication failure,
  but cannot distinguish task complexity from other request-content-specific
  provider/transport behavior. Both M64 request budgets are consumed; no retry
  or further provider request is authorized.

## Out of scope

Unbounded retries, cost or latency claims from one sample, endpoint changes,
raw response retention, held-out evaluation, model-quality claims, or treating
a control prompt as equivalent to the CAD task.

## Closure rationale

The separately authorized control completed while the fixed M63 request timed
out at the longer 300-second deadline. This rejects a simple blanket
endpoint/authentication failure but does not prove task complexity caused the
timeout. Both one-request budgets are consumed. Liaol independently approved
this evidence boundary and no-retry disposition on 2026-08-09.

## Independent review

- Reviewer: Liaol
- Outcome: approved on 2026-08-09
- Verified: separate authorizations, one-request accounting for both reports,
  redacted control-report boundary, limited request-specific-latency inference,
  no-retry disposition, and lifecycle alignment.
