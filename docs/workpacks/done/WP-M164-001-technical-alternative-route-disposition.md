# WP-M164-001: Technical-Alternative Route Disposition

- Status: done
- Milestone: M164
- Owner: Codex
- Reviewer: not required
- Risk tier: G1

## Goal

Classify the unconsumed geometry-diagnostic, helper, IR and DeepCAD triggers
against the current closed-loop route, preserving their exact evidence gates.

## Scope

- Add the TRG-001--004 `future option` dispositions and re-entry evidence to
  the maintained index.
- Link M34 as the durable gate authority where applicable.

## Attribution question and sampling intent

Distinguish routes that remain meaningful conditional technical options from
current prerequisites or consumed records. Stop if any trigger's durable
evidence gate is unclear or the classification would alter its scope.

## Code paths

None.

## Docs to update

- `docs/workflow/workpack-route-disposition-index.md`
- `docs/workflow/status.md`
- this workpack and active handoff

## Trace/schema changes

None.

## Decision-package impact

- `decision_id`: none; route navigation only.
- Q01/Q02/Q03/Q04 effect: none.
- Evidence role: historical trigger disposition only.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

TRG-001--004 remain unconsumed and unchanged. Current release, case, card,
runtime, provider and hosted boundaries remain unchanged.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the disposition index update, pass acceptance, then close the package.

## Permitted stop conditions

Review, frozen-input drift, out-of-scope dependency, or reproducible blocker.

## Evidence reuse / guidance-card disposition

No reusable knowledge.

## Status transition

On closure update status first, move this workpack to `done/`, archive the
handoff, and run governance audit.

## Closure rationale

Recorded TRG-001--004 as `future option`s with their existing exact triggers.
`uv run python tools\check_governance.py` and `git diff --check` passed on
2026-08-13.

## Out of scope

Implementation, trigger activation, archive movement, case expansion, helper,
IR, DeepCAD, provider or hosted work.
