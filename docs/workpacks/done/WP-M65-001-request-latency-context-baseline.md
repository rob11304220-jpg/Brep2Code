# WP-M65-001: Request Latency and Context Baseline

- Status: done
- Milestone: M65
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Implement a privacy-preserving, offline-testable request-level latency and
context baseline for observed first-pass generation. The goal is to separate
provider wait, local observation/Harness time, and context composition before
any future hosted diagnosis.

## Scope

- Record a versioned telemetry object with request start/done timing,
  provider-wait duration, null first-byte timing when the adapter cannot expose
  it, and the existing sanitized lifecycle phases on hosted-worker paths.
- Record per-section character and UTF-8-byte counts for system instruction and
  bounded observation transcript, plus total message counts; never serialize
  message content, raw provider responses, paths, credentials, or environment
  values.
- Record local input-prepare, observation, Harness, and end-to-end durations
  for successful observed-build runs.
- Project telemetry into observed-development case reports and add deterministic
  fake-provider/worker-boundary tests.
- Update the module and contract docs with explicit limitations: character
  counts are not token counts; token/first-byte/reasoning fields remain null or
  missing unless the provider exposes them.

## Compatibility constraints

Offline and credential-free only. Do not alter the runtime prompt, manifest,
provider selection, executor policy, report reuse rules, or request budgets.
No provider construction/call, external data, raw prompt retention, or hosted
retry is permitted.

## Acceptance

```powershell
uv run python -m pytest tests\test_agent_m3_repair_loop.py tests\test_observed_build_loop.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Status transition

Record owner acceptance and Liaol independent review before closure. Update
`status.md` first, then workpack and handoff; archive the handoff on closure.

## Owner acceptance

- Observed-build telemetry now projects a content-free, versioned ledger into
  first-pass and observed-development results: system/observation character and
  UTF-8-byte counts, message count, null unavailable first-byte/token fields,
  and local input-prepare/observation/provider-wait/Harness/end-to-end timing.
- No runtime prompt text, raw observation transcript, provider response,
  credential, environment value, local path, provider call, manifest, or
  executor policy was added to telemetry.
- Offline acceptance passed on 2026-08-09:
  - `uv run python -m pytest tests\test_agent_m3_repair_loop.py tests\test_observed_build_loop.py -q` — 20 passed
  - `uv run python -m ruff check .` — passed
  - `uv run python tools\check_governance.py` — passed
  - `git diff --check` — passed

## Pending independent review

- Reviewer: Liaol
- Required checks: schema contains counts/timing only; unavailable token/TTFT
  fields remain null rather than estimates; reports project telemetry; no
  hosted/prompt-policy expansion; stated offline acceptance and lifecycle
  records agree.

## Closure rationale

M65 adds only offline, content-free telemetry and preserves all existing
provider/prompt/executor boundaries. Liaol independently approved the privacy
schema, null-field semantics, report projection and 20-test acceptance on
2026-08-09. No provider request was issued.

## Independent review

- Reviewer: Liaol
- Outcome: approved on 2026-08-09
- Verified: telemetry has only counts/timing, unavailable fields are null,
  no prompt/provider-policy expansion occurred, report projection is covered,
  and acceptance/lifecycle records agree.

## Out of scope

Prompt rewrite, context compaction, model/provider change, streaming API,
token estimation, Articraft-source adoption, hosted calls, or causal claims
from M63/M64 beyond their recorded boundary.
