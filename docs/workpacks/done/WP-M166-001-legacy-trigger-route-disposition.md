# WP-M166-001: Legacy Trigger Route Disposition

- Status: done
- Milestone: M166
- Owner: Codex
- Reviewer: not required
- Risk tier: G1

## Goal

Classify the remaining legacy hosted and family-campaign deferred triggers
against their current stable route authorities, so `deferred/` no longer
implies an unranked execution queue.

## Scope

- Classify TRG-005--010, TRG-016 and TRG-018 as future option, superseded,
  rejected or archive-only.
- Link each disposition to its durable route, evidence or experiment authority.
- Preserve trigger files and exact original re-entry provenance.

## Attribution question and sampling intent

Distinguish still-relevant future questions from routes answered, reframed or
retained only as historical evidence. Stop if a stable authority cannot support
a disposition without revising an experiment's evidence interpretation.

## Code paths

None.

## Docs to update

- `docs/workflow/workpack-route-disposition-index.md`
- `docs/workflow/status.md`
- this workpack and active handoff

## Trace/schema changes

None.

## Decision-package impact

- `decision_id`: none; route-navigation classification only.
- Q01/Q02/Q03/Q04 effect: none.
- Evidence role: historical trigger and re-entry provenance.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

All triggers remain immutable deferred records unless their existing semantic
trigger has already been consumed. This package changes no activation
condition, provider authorization, report budget, case scope or runtime path.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish one disposition and durable authority for every in-scope trigger, pass
acceptance, and close the package.

## Permitted stop conditions

Review, frozen-input drift, out-of-scope dependency, or reproducible blocker.

## Evidence reuse / guidance-card disposition

No reusable knowledge.

## Status transition

On closure update status first, move this workpack to `done/`, archive the
handoff, and run the governance audit.

## Durable conclusion and route disposition

The maintained route-disposition index owns the classifications. This package
retains scope, source checks, acceptance and closure provenance.

## Closure rationale

Classified TRG-005--010, TRG-016 and TRG-018 in the maintained
route-disposition index: six legacy routes are `superseded`, while the two
family-campaign questions are constrained `future option`s. `uv run python
tools\check_governance.py` and `git diff --check` passed on 2026-08-13.

## Out of scope

Trigger activation, moving unconsumed triggers, new case/family work, held-out
access, provider/hosted activity, code or runtime changes.
