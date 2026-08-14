# WP-M167-001: Historical Workpack Navigation Migration

- Status: done
- Milestone: M167
- Owner: Codex
- Reviewer: not required
- Risk tier: G1

## Goal

Move high-frequency historical workpack navigation to stable route, decision,
contract and evidence indexes, retaining completed packages only as explicitly
labeled acceptance or provenance records.

## Scope

- Replace the long chronological execution catalog in `docs/workpacks/README.md`
  with durable entry routing and archive/provenance guidance.
- Make milestone history prioritize durable conclusions and add the M161--M166
  governance history.
- Preserve every completed and archived workpack file and all necessary
  terminal-report provenance links.

## Attribution question and sampling intent

Distinguish a stable navigation responsibility from a need to open a bounded
execution ledger. Stop if migration would remove a unique evidence/report link
or change a historical conclusion.

## Code paths

None.

## Docs to update

- `docs/workpacks/README.md`
- `docs/workflow/milestone-history.md`
- `docs/workflow/status.md`
- this workpack and active handoff

## Trace/schema changes

None.

## Decision-package impact

- `decision_id`: none; documentation navigation only.
- Q01/Q02/Q03/Q04 effect: none.
- Evidence role: preserve acceptance and provenance links.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

Do not delete or edit completed/archived execution ledgers. Keep direct links
where a workpack is the irreplaceable terminal report or acceptance record.
Do not alter deferred trigger disposition, current selection or authorization.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the compact workpack entry page and stable milestone navigation, pass
acceptance, and close the package.

## Permitted stop conditions

Review, frozen-input drift, out-of-scope dependency, or reproducible blocker.

## Evidence reuse / guidance-card disposition

No reusable knowledge.

## Status transition

On closure update status first, move this workpack to `done/`, archive the
handoff, and run the governance audit.

## Durable conclusion and route disposition

`workpack-governance.md`, the route-disposition index and milestone history
own navigation. This package retains scope, acceptance and closure provenance.

## Closure rationale

Replaced the long chronological `docs/workpacks/README.md` execution catalog
with stable entry routing, and migrated milestone history to durable authorities
with only one explicitly labeled acceptance-record exception. Added M161--M167
governance history. `uv run python tools\check_governance.py` and `git diff
--check` passed on 2026-08-13.

## Out of scope

Bulk rewriting every historical architecture document, deleting evidence,
trigger reclassification, code, cases, manifests, Harness, provider or hosted
work.
