# WP-M67-001: Hosted Telemetry Collection and Analysis

- Status: done
- Milestone: M67
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G3

## Goal

Perform a fresh, development-only, pre-registered hosted collection that uses
M65/M66 telemetry to distinguish provider wait, context size, and local phases
without changing prompt policy or reusing any earlier report/budget.

## Scope

- Complete a read-only preflight selecting a small fixed development-only set
  with independent one-case reports, no repair, a fixed model/deadline and
  `wsl-bwrap` execution.
- Verify M67 telemetry is present in both completed and interrupted reports,
  then define the report fields and limited descriptive analysis.
- Request fresh, itemized user authorization only after manifest hashes,
  provider configuration, executor, report-path freshness, exact request cap,
  deadline and durable monitoring method are recorded.
- Add an offline-tested `observed-development --case-id` selector so each
  pre-registered manifest case has an independent terminal report without
  modifying manifest membership or weakening request bounds.

## Compatibility constraints

No provider call, prompt/runtime/manifest change, retry, external data,
credential display, or M54/M63/M64 budget/report/authorization reuse before
fresh preflight and explicit user approval. This workpack does not authorize
held-out evaluation or causal/model-quality claims.

## Acceptance

```powershell
uv run python -m pytest tests\test_agent_m3_repair_loop.py tests\test_observed_build_loop.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Status transition

Record preflight before requesting authorization. After any separately
authorized collection, record terminal reports and descriptive-only findings.
G3 closure requires Liaol independent review.

## Read-only preflight evidence

- [`m67-hosted-telemetry-preflight.md`](../../workflow/m67-hosted-telemetry-preflight.md)
  records the fixed three-case scope, hash, configuration/executor checks,
  fresh reports, bounds and authorization gate.
- 2026-08-09 offline acceptance: focused tests 21 passed; Ruff, governance and
  `git diff --check` passed. No provider request or credential display occurred.

## Closure rationale

The three authorized independent reports provide the intended telemetry: two
requests timed out before a response and one returned in 107.942 seconds then
failed only during sandboxed script execution. This supports request-specific
latency but does not attribute it to network or provider. Liaol approved the
bounded interpretation, request accounting and no-retry disposition.

## Independent review

- Reviewer: Liaol
- Outcome: approved on 2026-08-09
- Verified: three independent budgets/reports, telemetry boundaries, separated
  provider timeout from script failure, no-retry rule and lifecycle alignment.

## Out of scope

Prompt/context rewrite, Articraft adoption, unbounded sampling, retries,
token estimation, held-out claims, or use of earlier nominal request remains.
