# WP-M63-001: M54 Fresh Hosted Preflight and Decision Gate

- Status: done
- Milestone: M63
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G3

## Goal

Complete a fresh, read-only preflight for a possible new M54 development-split
hosted evaluation, incorporating M60 lifecycle checkpoint diagnostics and
M62's durable validation-window guidance. No provider request is authorized by
this workpack alone.

## Preflight scope

- Destination: `https://api.deepseek.com`; provider/model: DeepSeek
  `deepseek-v4-pro`.
- Egress, if separately authorized: only M48 path-free bounded observation
  transcripts; no raw STEP, paths, filenames, reference scripts, docs, traces,
  credentials, or environment values.
- Fixed input: all 12 rows of
  `case-library/manifests/self-authored/parametric-development.json`.
- Bound: one first pass plus at most one repair per case, at most 24 requests,
  with a 120-second per-request deadline and `wsl-bwrap` no-input execution.
- Proposed new report: `data/corpus-runs/m63-parametric-development-deepseek-observation.json`.

## Required checks

- Recompute manifest and selected-input SHA-256 values; verify scope and the
  corresponding local `wsl-bwrap` preflight.
- Verify non-secret provider configuration presence, model selection, secure
  executor availability, actual CLI request bounds, and M60 diagnostic
  projection without displaying credential values.
- Confirm the proposed report path has no `running` or `interrupted`
  checkpoint, and state durable-monitoring/outer-time risks.

## Compatibility constraints

Do not call a provider, inspect credential values, reuse M54's prior report or
23 nominal remaining requests, alter manifest/prompt/runtime policy, or treat
prior timeouts as model-quality evidence. A fresh hosted run requires a new
itemized user authorization after this preflight and Liaol independent review.

## Acceptance

```powershell
uv run python -m pytest tests\test_observed_build_loop.py -q
uv run python tools\check_governance.py
git diff --check
```

## Read-only preflight evidence

- [`m63-hosted-preflight.md`](../../workflow/m63-hosted-preflight.md) records
  the fixed split, destination/egress boundary, matching manifest/input hashes,
  non-sensitive configuration, `wsl-bwrap`, CLI request bound, fresh report
  path, and durable-monitoring risk.
- `uv run python -m pytest tests\test_observed_build_loop.py -q` — 10 passed
  in 41.45s; it remains local fake-provider coverage only.
- `uv run python tools\check_governance.py` and `git diff --check` passed.
- No provider request, credential value, or budget reuse occurred. The next
  action was an explicit itemized user authorization, not an automatic launch.
- On 2026-08-09, the user explicitly authorized the bounded M63 batch. The
  first case (`param_additive_boss_low`) issued one request, which reached the
  120-second provider deadline. The new report atomically records
  `interrupted`, `requests_used=1`, `requests_remaining=23`, and only the
  non-sensitive lifecycle diagnostics `worker_started` and `http_started`.
  No cases completed; do not attribute this timeout to model or geometry
  quality, and do not reuse the nominal 23 remaining requests.

## Status transition

The read-only preflight and itemized authorization were recorded before launch.
After the authorized batch interrupted at the first request, actual accounting
and report status were recorded. G3 closure now requires Liaol independent
review and an explicit no-retry disposition or a new bounded workpack with
fresh preflight and authorization.

## Out of scope

Provider connectivity probes, trial requests, adaptive sampling, budget reuse,
held-out evaluation, or claims about model quality/cause from a timeout.

## Closure rationale

The authorized fresh batch wrote a fail-closed interruption checkpoint after
its first 120-second provider deadline. The checkpoint preserved only bounded
lifecycle diagnostics and consumed one request; no M54/M63 nominal remainder
is reusable. Liaol independently approved this outcome on 2026-08-09 after
reviewing the scope, request accounting, diagnostic boundary, and no-retry
disposition. Follow-on cause discrimination is separately scoped as M64.

## Independent review

- Reviewer: Liaol
- Outcome: approved on 2026-08-09
- Verified: itemized authorization scope, M63 report interruption and one
  issued-request accounting, sanitized lifecycle diagnostics, no-retry/budget
  non-reuse, and lifecycle alignment.
