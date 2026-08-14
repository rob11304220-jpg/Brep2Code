# WP-M113-001: Prismatic Policy-Design Route

- Status: done
- Milestone: M113
- Owner: Codex
- Reviewer: not required
- Risk tier: G1

## Goal

Replace the non-runnable M97 held-out continuation in route navigation with a
new, offline policy/design-decision trigger that follows M112 `inconclusive`.

## Scope

Update only the prismatic references in the five-family roadmap, four-track
roadmap, case portfolio and deferred trigger index. Add one deferred G2
policy/design workpack; it has no provider, input or execution authority.

## Compatibility constraints

Do not modify M96/M97 or TRG-009 policy, card, prompt, case, split, manifest,
runtime, provider, budget or report path. Offline and credential-free only.

## Acceptance

```powershell
uv run python -m pytest -m fast -q
uv run python tools\check_governance.py
git diff --check
```

## Status transition

Record owner acceptance, then close and archive this route-only workpack.

## Owner acceptance and closure

- Added `WP-TRG-019` as the sole offline prismatic re-entry after M112 and
  removed any route implication that `TRG-009` is selectable.
- Updated only the five-family roadmap, four-track roadmap, case portfolio and
  deferred trigger index. Fast tests (66 passed, 165 deselected), governance
  and `git diff --check` passed.
- Closure rationale: route navigation only; no M97 policy, held-out input,
  provider, preflight, authorization or hosted scope changed.

## Out of scope

Policy implementation, held-out inspection, provider construction, preflight,
authorization, hosted execution or selection of TRG-009.
