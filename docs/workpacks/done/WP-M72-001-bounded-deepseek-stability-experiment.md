# WP-M72-001: Bounded DeepSeek Stability Experiment

- Status: done
- Milestone: M72
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G3

After M71, preflight and separately authorize a fresh sequential development
experiment that measures response stability only. Each mode/case has new
reports, deadlines and budget; no old authorization or request remainder is
reused.

## Goal

Collect the minimum new, pre-registered engineering evidence needed to decide
whether provider lifecycle is stable enough to investigate CAD output and
repair correctness separately.

## Preconditions

- M70's durable monitor and M71's offline compatibility matrix are accepted.
- A new read-only G3 preflight records the selected compatible mode, fixed
  development-only cases, SHA-256/manifest scope, outbound summary boundary,
  `wsl-bwrap` availability, deadline, per-report one-request accounting,
  request/cost cap and fresh report paths.
- The user separately and explicitly authorizes destination, provider/model,
  egress content, cases, mode, rounds, deadline and budget after that
  preflight. No prior authorization or remaining request count applies.

## Experiment boundary

Run sequentially with no repair and one new report per pre-registered request.
Compare lifecycle completion and timing only; retain content-free telemetry
and existing safe response metadata. The experiment must not change prompt,
manifest, executor, model, endpoint or selected mode after the first result.

The stability gate for considering M73 is:

1. every pre-registered request has one parseable terminal report;
2. no issued request ends as `provider_request_timeout` or lifecycle error;
3. all reports meet their authorized deadline and record the same selected
   compatibility mode; and
4. the independent reviewer confirms no scope/budget/report-path violation.

Any failure stops the experiment. It is evidence for a new offline diagnosis,
not a reason to add cases, retry, relax a deadline or start M73.

## Compatibility constraints

All generated execution remains `wsl-bwrap`; default operation remains
network-free. Use only the user-confirmed fixed development cases; do not
expand to held-out cases, reuse reports/budgets, retain raw
prompt/response/credential data, run concurrently, or claim model quality,
network root cause or CAD correctness.

## Acceptance

Before authorization, run the preflight's independently bounded local checks,
including governance audit and `git diff --check`. After any authorized run,
record every report path and terminal result, then run the relevant offline
report/contract checks, Ruff and governance audit. G3 closure requires Liaol's
independent review.

## Status transition

Do not activate until M70/M71 are done and the user chooses this bounded
workpack. Update `docs/workflow/status.md` first, then this workpack and an
active handoff. A completed stability experiment either records the four-part
gate result or a no-retry failure disposition.

## Activation record

- Activated by Liaol on 2026-08-10 after M70 and M71 closure.
- Preflight is read-only and in progress. The workpack's conflicting case-scope
  wording was resolved by Liaol on 2026-08-10: use the three fixed development
  cases, never held-out cases.

## Read-only preflight

- [`m72-hosted-stability-preflight.md`](../../workflow/m72-hosted-stability-preflight.md)
  records the exact mode, fixed development cases, hashes, no-egress controls,
  non-secret configuration check, report-path freshness, one-request budget
  rule, deadline, and authorization gate.
- Fresh local `wsl-bwrap` controls passed for all three cases using only their
  checked-in reference scripts. Focused lifecycle tests passed (21) and Ruff
  passed. No provider request was issued.

## Authorized execution record

- Liaol explicitly authorized the preflight's complete itemized scope on
  2026-08-10. The first sequential request used only
  `param_additive_boss_low`, its dedicated report, non-streaming JSON mode,
  zero repair rounds, `wsl-bwrap`, one-request budget and a 300-second
  provider deadline.
- `data/corpus-runs/m72-param-additive-boss-low.json` is parseable and reached
  terminal `interrupted`: `provider_request_timeout`, `requests_used: 1`,
  `requests_remaining: 0`. Its lifecycle telemetry retained only
  `worker_started` and `http_started`; no first byte, response content or
  generated-script result was observed.
- The M70 monitor state at
  `data/monitor-runs/m72-param-additive-boss-low.monitor.json` reached its
  terminal report handoff. The request's `provider_wait` was 300.029 seconds
  (300.853 seconds end-to-end).
- This is a no-retry terminal disposition. The remaining pre-registered cases
  were not started; their fresh report paths remain unused. M72 does not meet
  its stability gate and cannot start M73.

## Review status

- Owner: Codex — recorded the preflight, authorization, terminal report and
  mandatory no-retry stop on 2026-08-10.
- Independent reviewer: Liaol — approved closure on 2026-08-10 after reviewing
  the request accounting, timeout-only interpretation, unused remaining cases,
  report paths and lifecycle alignment.

## Closure rationale

- Liaol independently approved closure on 2026-08-10. The review confirmed
  the report is terminal and parseable, the one-request budget was accounted,
  the timeout-only interpretation is bounded, the remaining cases/reports were
  unused, and no retry or M73 progression occurred.
- M72's four-part stability gate fails at condition 2 because its issued
  request ended as `provider_request_timeout`. It is closed as a controlled
  no-retry failure disposition, not as evidence about model quality, network
  root cause, CAD correctness, or provider-wide availability.

## Out of scope

Repair effectiveness, output schema changes, OCP API changes, geometry-gate
changes, prompt/context optimization, held-out expansion, external data,
provider/model comparison and unbounded availability measurement.
