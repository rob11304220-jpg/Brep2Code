# WP-M169-001: Legacy Hosted Provenance Navigation Migration

- Status: done
- Milestone: M169
- Owner: Codex
- Reviewer: not required
- Risk tier: G1

## Goal

Migrate legacy hosted-route navigation away from completed workpacks and verify
that every remaining direct completed/archived-workpack link is an allowed
acceptance, original-evidence, audit or provenance exception.

## Scope

- Replace historical route links in the post-M9 and M69/M9 hosted reviews with
  their stable evidence, decision and current-route authorities.
- Verify retained links in experiment registry, evidence ledger, decision
  records, milestone history, navigation and governance runbook.
- Record the final bounded exception set without modifying execution ledgers.

## Attribution question and sampling intent

Distinguish a historical route entry from a necessary immutable original
evidence reference. Stop if a retained link does not meet the durable citation
contract or lacks a stable authority.

## Code paths

None.

## Docs to update

- `docs/architecture/v1/post-m9-evidence-gated-roadmap.md`
- `docs/architecture/v1/m9-abc-hosted-evaluation-review.md`
- `docs/architecture/v1/m69-project-progress-and-improvement-review.md`
- `docs/workflow/status.md`
- this workpack and active handoff

## Trace/schema changes

None.

## Decision-package impact

- `decision_id`: none; historical navigation/provenance only.
- Q01/Q02/Q03/Q04 effect: none.
- Evidence role: preserve irreplaceable terminal evidence paths.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

Do not delete reports, workpacks or decision evidence. Do not alter current
route, trigger disposition, provider authorization, case scope or runtime.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Migrate all in-scope route links, verify every retained direct link against the
citation contract, pass acceptance, and close the package.

## Permitted stop conditions

Review, frozen-input drift, out-of-scope dependency, or reproducible blocker.

## Evidence reuse / guidance-card disposition

No reusable knowledge.

## Status transition

On closure update status first, move this workpack to `done/`, archive the
handoff, and run the governance audit.

## Durable conclusion and route disposition

The citation contract and stable evidence indexes own the conclusion. This
workpack retains migration acceptance and provenance only.

## Closure rationale

Replaced all in-scope post-M9, M9 and M69 completed-workpack route links with
stable authorities. The final scan found 24 direct completed/archive links
outside workpacks/handoffs, each in an allowed navigation, acceptance, original
terminal-evidence, evidence-ledger, decision-record or audit context. Governance
audit and `git diff --check` passed on 2026-08-13.

## Out of scope

Hosted execution, provider changes, report alteration, route reclassification,
case/runtime changes, code changes or broad archival rewrite.
