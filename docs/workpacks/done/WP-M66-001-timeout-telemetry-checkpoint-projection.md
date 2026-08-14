# WP-M66-001: Timeout Telemetry Checkpoint Projection

- Status: done
- Milestone: M66
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Preserve M65's content-free latency/context telemetry when an observed
development provider request times out or has a lifecycle error, so the cases
most relevant to latency diagnosis retain safe terminal evidence.

## Scope

- Attach M65 telemetry to a provider timeout/lifecycle exception after local
  observation and provider-wait timing are known.
- Project only a strict whitelist into the atomic `interruption` checkpoint:
  request timing offsets/nulls, count-only context ledger, and local phase
  elapsed milliseconds.
- Keep `done_offset_ms`, first-byte and token fields null when no response is
  available; retain existing lifecycle diagnostics and request accounting.
- Add deterministic fake timeout tests and document the additive schema.

## Compatibility constraints

Offline and credential-free only. No provider call, prompt/runtime/manifest
change, report/budget reuse, retry-policy change, raw prompt/response, path,
credential, environment or token estimation is allowed.

## Acceptance

```powershell
uv run python -m pytest tests\test_agent_m3_repair_loop.py tests\test_observed_build_loop.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Status transition

Record owner acceptance and Liaol independent review before closure. Update
status, workpack and handoff in lifecycle order.

## Owner acceptance

- Observed-build attaches M65 telemetry before re-raising an issued provider
  timeout/lifecycle error. The observed-development interruption projects it
  only through a strict schema whitelist.
- Timeout telemetry retains content counts and elapsed timing only; response
  dependent `done_offset_ms`, first-byte and token fields are null. Existing
  lifecycle diagnostics, terminal behavior and request accounting are
  unchanged.
- Offline acceptance passed on 2026-08-09:
  - `uv run python -m pytest tests\test_agent_m3_repair_loop.py tests\test_observed_build_loop.py -q` — 20 passed
  - `uv run python -m ruff check .` — passed
  - `uv run python tools\check_governance.py` — passed
  - `git diff --check` — passed

## Pending independent review

- Reviewer: Liaol
- Required checks: interruption telemetry is whitelist-only; null fields are
  not estimates; no request/prompt/executor policy changed; timeout accounting
  and lifecycle diagnostics remain compatible.

## Closure rationale

M66 preserves only M65's strict count/timing schema for terminal provider
checkpoints. Liaol independently approved the whitelist, null-field semantics,
compatibility and 20-test acceptance on 2026-08-09. No provider request was
issued.

## Independent review

- Reviewer: Liaol
- Outcome: approved on 2026-08-09
- Verified: strict checkpoint whitelist, null unavailable fields, compatible
  lifecycle/request accounting, no prompt/provider-policy expansion, and
  acceptance/lifecycle alignment.

## Out of scope

Hosted telemetry collection, prompt change, token estimation, streaming,
Articraft adoption, additional retries, or causal claims.
