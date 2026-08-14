# Handoff: M64 hosted timeout-cause discrimination

- **Date**: 2026-08-09
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M64-001-hosted-timeout-cause-discrimination`

## Goal

Prepare a new, bounded diagnostic package to distinguish M63's transport or
provider-response timeout from a possible task-latency contribution, without
reusing any earlier batch, report, budget, or authorization.

## Done

- Liaol independently approved M63. Its first request timed out at the
  120-second deadline after `worker_started` and `http_started`, with zero
  completed cases; its nominal remaining 23 requests are invalid.

## In progress

- Fresh read-only preflight is complete in
  [`m64-hosted-timeout-diagnostic-preflight.md`](../../workflow/m64-hosted-timeout-diagnostic-preflight.md).
  M64 added and offline-tested `provider-control`, which enforces an explicit
  hosted flag, one-request budget and durable redacted report. The two proposed
  calls are a 120-second fixed control and a 300-second single fixed-case
  comparison, each with a new report path and one request. Both were
  separately authorized: the control completed at its 120-second bound, while
  the fixed-case request reached its 300-second deadline and wrote an
  `interrupted` report with `worker_started`/`http_started` only.

## Next

- Obtain Liaol's independent review of the two reports and the limited result:
  this excludes a blanket endpoint/authentication failure but does not prove
  task complexity caused the fixed-case timeout.

## Decisions

- A timely control plus a timely extended fixed-case response can only make
  task latency plausible; it cannot establish causality from one sample.
- Any new hosted request needs its own explicit authorization. M54/M63 nominal
  remaining budgets cannot be reused.

## Blockers

- Both M64 one-request budgets are consumed. Awaiting Liaol independent review;
  no retry or further provider request is authorized.

## Closure

Liaol independently approved M64 on 2026-08-09. The workpack is closed with
the bounded conclusion that the fixed request exhibited request-specific
latency/handling beyond both deadlines, not a proven task-complexity cause.
No retry is authorized.

## Resume prompt

```
Continue M64 with read-only preflight only. Do not issue a control or fixed-case
provider request, inspect credential values, or reuse M54/M63 reports/budgets
until the user explicitly authorizes the exact M64 parameters.
```
