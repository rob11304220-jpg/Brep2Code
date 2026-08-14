# WP-M162-001: Workpack Governance and Route Index

- Status: done
- Milestone: M162
- Owner: Codex
- Reviewer: not required
- Risk tier: G1

## Goal

Make workpacks bounded execution ledgers, promote durable navigation to stable
authorities, and publish a first route-disposition index for the current
closed-loop trigger cluster.

## Scope

- Publish workpack lifecycle, archive and durable-reference rules.
- Publish current-cluster dispositions for TRG-035 and TRG-038 through TRG-041.
- Update the Agent and workpack entry documents with the new routing rule.
- Archive consumed TRG-038 after recording its durable authority.

## Attribution question and sampling intent

Distinguish a workpack's execution provenance from a durable route conclusion.
Stop if applying the rule requires a bulk historical reclassification, changes
a deferred trigger's substantive re-entry condition, or alters case/runtime/
provider authority.

## Code paths

None.

## Docs to update

- `AGENTS.md`
- `docs/workflow/workpack-governance.md`
- `docs/workflow/workpack-route-disposition-index.md`
- `docs/workflow/status.md`
- `docs/workpacks/README.md` and `docs/workpacks/deferred/README.md`
- ADR, active workpack and handoff

## Trace/schema changes

None.

## Decision-package impact

- `decision_id`: none; governance navigation only.
- Q01/Q02 effect: none.
- Q03/Q04 effect: none.
- Evidence role: documentation/provenance governance only.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

Existing current-route order, deferred trigger content, case/card authorities,
offline default and hosted authorization gates remain unchanged.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the governance rule, route index, ADR and entry links; archive only
the already-consumed TRG-038 trigger; pass acceptance; then close the package.

## Permitted stop conditions

Review, frozen-input drift, out-of-scope dependency, or reproducible blocker.

## Evidence reuse / guidance-card disposition

No reusable knowledge.

## Status transition

On closure update status first, move this workpack to `done/`, archive the
handoff, and run governance audit.

## Closure rationale

Published the durable-reference and archive rules, current-cluster disposition
index and ADR-0081.  TRG-038 was moved to archive after confirming M155 owns
its lasting boundary.  `uv run python tools\check_governance.py` and `git diff
--check` passed on 2026-08-13.

## Out of scope

Bulk workpack-reference rewrites, disposition of all historical deferred
records, deletion of evidence, case/card/runtime/provider changes, and hosted
work.
