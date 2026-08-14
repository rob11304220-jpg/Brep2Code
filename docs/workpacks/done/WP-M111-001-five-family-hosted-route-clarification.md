# WP-M111-001: Five-Family Hosted Route Clarification

- Status: done
- Milestone: M111
- Owner: Codex
- Reviewer: not required
- Risk tier: G1

## Goal

Record M110-001's independently reviewed five-family readiness conclusions in
the existing route documents, without changing a deferred trigger, selecting
a campaign, or widening hosted authority.

## Scope

- Update the five-family delivery roadmap with the M110 disposition and the
  minimum dependency order to a future single-family campaign.
- Update the four-track roadmap and the case-portfolio navigation only where
  they describe that same five-family route.

## Compatibility constraints

Offline and credential-free. Preserve case, split, manifest, card, pack,
runtime, provider, policy, budget, report, monitor and deferred-workpack
boundaries. This work does not satisfy a trigger or authorize preflight or
hosted egress.

## Acceptance

```powershell
uv run python -m pytest -m fast -q
uv run python tools\check_governance.py
git diff --check
```

## Status transition

Record owner acceptance, then close the workpack and archive its handoff.

## Owner acceptance and closure

- Updated only `five-family-hosted-capability-roadmap.md`,
  `four-track-program-roadmap.md`, and the five-family section of
  `case-portfolio.md`.
- The route now makes the order explicit: hosted-stability completion;
  prismatic-only M97 readiness decision when applicable; one user-selected
  family; then fresh G3 preflight and itemized authorization.
- `uv run python -m pytest -m fast -q` passed (66 passed, 165 deselected);
  `uv run python tools\check_governance.py` and `git diff --check` passed.
- Closure rationale: this is route navigation only. It creates no trigger,
  campaign, provider scope, runtime projection or hosted authorization.

## Out of scope

Any provider request, hosted preflight, trigger activation, deferred-workpack
edit, family selection, runtime-card qualification, source/case access, or
implementation change.
