# WP-M165-001: Durable Workpack Citation Contract

- Status: done
- Milestone: M165
- Owner: Codex
- Reviewer: not required
- Risk tier: G1

## Goal

Freeze an auditable rule for when stable documentation may directly cite a
completed or archived workpack, while keeping execution ledgers as provenance
rather than project-route or fact authorities.

## Scope

- Define permitted direct-reference classes and required stable authorities.
- Define the limited audit, original-report and historical-provenance
  exceptions.
- Add a checkable navigation rule without reclassifying any deferred trigger or
  rewriting historical route records.

## Attribution question and sampling intent

Distinguish a necessary link to acceptance/original evidence from a link that
makes a completed workpack the sole statement of a still-valid conclusion.
Stop if the proposed contract would change a route disposition or an evidence
interpretation.

## Code paths

None.

## Docs to update

- `docs/workflow/workpack-governance.md`
- `docs/workflow/navigation.md`
- `docs/workflow/status.md`
- this workpack and active handoff

## Trace/schema changes

None.

## Decision-package impact

- `decision_id`: none; documentation-governance convention only.
- Q01/Q02/Q03/Q04 effect: none.
- Evidence role: provenance routing only.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

Completed workpacks remain immutable. Existing ADR, contract, evidence-ledger,
milestone-history and terminal-report links remain valid. This package does not
activate, reclassify, archive or delete any trigger.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the citation contract in stable governance/navigation records, pass
acceptance, and close the package.

## Permitted stop conditions

Review, frozen-input drift, out-of-scope dependency, or reproducible blocker.

## Evidence reuse / guidance-card disposition

No reusable knowledge.

## Status transition

On closure update status first, move this workpack to `done/`, archive the
handoff, and run the governance audit.

## Durable conclusion and route disposition

The enduring rule belongs in `workpack-governance.md` and `navigation.md`.
This package retains scope, acceptance and closure provenance only. No trigger
disposition changes in this package.

## Closure rationale

Published the normative durable citation contract in
`docs/workflow/workpack-governance.md` and its low-context routing summary in
`docs/workflow/navigation.md`. `uv run python tools\check_governance.py` and
`git diff --check` passed on 2026-08-13. No trigger disposition changed.

## Out of scope

Changing current routes, deferred trigger disposition, milestone history,
workpack archival locations, code, cases, manifests, Harness, provider or
hosted behavior.
