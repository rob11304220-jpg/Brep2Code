# WP-M163-001: Consumed-Trigger Archive and Closure Rule

- Status: done
- Milestone: M163
- Owner: Codex
- Reviewer: not required
- Risk tier: G1

## Goal

Apply the permanent workpack closure rule to the verified consumed authority-and-contract trigger cluster and make durable-conclusion promotion a required template field.

## Scope

- Add the durable conclusion and route-disposition field to the workpack template.
- Record `archive-only` dispositions for TRG-028, 031--034 and 037.
- Move those consumed trigger records from `deferred/` to `archive/`.

## Attribution question and sampling intent

Distinguish a trigger whose stated deliverable has a completed durable successor from an unconsumed historical technical or campaign route. Stop if a record lacks a verified completed successor or its durable authority cannot be identified.

## Code paths

None.

## Docs to update

- `docs/workpacks/README.md`
- `docs/workflow/workpack-route-disposition-index.md`
- `docs/workflow/status.md`
- this workpack and active handoff

## Trace/schema changes

None.

## Decision-package impact

- `decision_id`: none; documentation provenance governance only.
- Q01/Q02 effect: none.
- Q03/Q04 effect: none.
- Evidence role: archive/disposition audit only.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

All existing trigger content, durable authorities, case/card/runtime/provider boundaries, current route and hosted authorization requirements remain unchanged.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the template and index updates, archive only the six verified consumed records, pass acceptance, then close the package.

## Permitted stop conditions

Review, frozen-input drift, out-of-scope dependency, or reproducible blocker.

## Evidence reuse / guidance-card disposition

No reusable knowledge.

## Status transition

On closure update status first, move this workpack to `done/`, archive the handoff, and run governance audit.

## Closure rationale

Added the durable-conclusion/disposition template field, recorded six consumed
trigger dispositions, and archived the corresponding records. `uv run python
tools\check_governance.py` and `git diff --check` passed on 2026-08-13.

## Out of scope

Technical disposition of unconsumed historical triggers; case, card, runtime, provider or hosted changes; deletion of execution evidence; and bulk reference rewrites.
