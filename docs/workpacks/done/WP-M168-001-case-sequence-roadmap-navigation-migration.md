# WP-M168-001: Case and Sequence Roadmap Navigation Migration

- Status: done
- Milestone: M168
- Owner: Codex
- Reviewer: not required
- Risk tier: G1

## Goal

Move historical Fusion, sequence-paired and family-charter navigation away
from completed workpack timelines to stable case, contract and route indexes.

## Scope

- Migrate the Fusion and sequence-paired historical roadmap link patterns.
- Replace completed-workpack-as-fact references in active family-charter and
  B-Rep module navigation with durable authorities or explicit provenance.
- Preserve every execution ledger and any needed audit/evidence link.

## Attribution question and sampling intent

Distinguish long-lived case/sequence facts from the bounded packages that
produced them. Stop if no stable case, ADR, contract or route authority exists
for a referenced conclusion.

## Code paths

None.

## Docs to update

- `docs/architecture/v1/fusion360-paired-data-roadmap.md`
- `docs/architecture/v1/sequence-paired-prismatic-hole-roadmap.md`
- affected case/module/charter navigation documents
- `docs/workflow/status.md`
- this workpack and active handoff

## Trace/schema changes

None.

## Decision-package impact

- `decision_id`: none; navigation-only work.
- Q01/Q02/Q03/Q04 effect: none.
- Evidence role: historical provenance preservation.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

Do not change case identity, split, lifecycle, implementation contracts,
current route, trigger disposition, runtime behavior or hosted authority.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish stable links for every in-scope historical conclusion, pass acceptance,
and close the package.

## Permitted stop conditions

Review, frozen-input drift, out-of-scope dependency, or reproducible blocker.

## Evidence reuse / guidance-card disposition

No reusable knowledge.

## Status transition

On closure update status first, move this workpack to `done/`, archive the
handoff, and run the governance audit.

## Durable conclusion and route disposition

Case portfolio, case records, contracts and architecture routes own the
navigation. This workpack retains only migration acceptance/provenance.

## Closure rationale

Replaced all in-scope Fusion, sequence-paired, family-charter and B-Rep module
completed-workpack links with review records, ADRs, case/registry records or
current route authorities. Governance audit and `git diff --check` passed on
2026-08-13; direct completed/archive links outside workpacks/handoffs fell
from 57 to 37.

## Out of scope

Case production, split changes, runtime/card changes, trigger activation,
provider/hosted work, broad historical rewrite or code changes.
