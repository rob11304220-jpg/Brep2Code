# WP-M161-001: Route Decision Map

- Status: done
- Milestone: M161
- Owner: Codex
- Reviewer: not required
- Risk tier: G1

## Goal

Publish a decision-navigation layer that helps humans and Agents decide why a
route concerning interaction/repair policy, case denominator, or experience
projection should be selected, retained, replaced or retired before turning it
into a workpack.

## Scope

- Add a compact route decision map under architecture/v1.
- Add one AGENTS entry that routes route/portfolio decisions to the map.
- Define route dispositions separately from workpack lifecycle states.
- Record the architectural decision and an active handoff.

## Attribution question and sampling intent

Distinguish route-level decision navigation from both per-hypothesis theory
navigation and executable workpack selection.  Stop if the map requires
reclassifying a case, altering a deferred workpack, changing a runtime contract
or granting any provider/hosted authority.

## Inputs

- `docs/architecture/v1/current-project-route.md`
- `docs/architecture/v1/project-theory-map.md`
- `docs/workflow/status.md`

## Code paths

None.

## Docs to update

- `AGENTS.md`
- `docs/architecture/v1/route-decision-map.md`
- `docs/architecture/adr/0080-route-decision-map.md`
- `docs/workflow/status.md`
- active handoff and this workpack

## Trace/schema changes

None.

## Decision-package impact

- `decision_id`: none; this is a navigation layer above individual packages.
- Q01/Q02 effect: none.
- Q03/Q04 effect: none.
- Evidence role: governance/navigation clarification only.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

Default offline behavior, existing case/card/manifest authorities, the frozen
TRG-039 → TRG-040 → TRG-041 ordering and all hosted gates remain unchanged.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the map, ADR, AGENTS route and handoff; pass both acceptance commands;
then update status first and archive the completed workpack/handoff.

## Permitted stop conditions

Review, frozen-input drift, an out-of-scope dependency, or a reproducible
blocker.

## Evidence reuse / guidance-card disposition

No reusable knowledge.

## Status transition

On closure update `status.md` first, move this workpack to `done/`, archive
the handoff, and run the governance audit.

## Closure rationale

Published the map, ADR and AGENTS route entry. `uv run python
tools\check_governance.py` and `git diff --check` passed on 2026-08-13.  The
map deliberately leaves deferred-inventory disposition to a future selected
review.

## Out of scope

Auditing, merging, retiring or reactivating deferred workpacks; case changes;
card extraction or retrieval; SDK/IR changes; Harness/manifest/provider
changes; and hosted work.
