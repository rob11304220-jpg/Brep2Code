# WP-M49-001: Post-M48 Closed-Loop Roadmap and Contract Alignment

- Status: done
- Milestone: M49
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Record the user-selected, evidence-gated order from M48's observation/build
boundary to a real LLM closed loop, controlled reference-model variants, and
only then external-data evaluation. Correct documentation that still presents
the implemented M48 contract as planned.

## Scope

- Add a durable post-M48 roadmap with task tiers, dependencies, and hosted
  authorization boundaries.
- Mark the Q01/Q02 capability contract as active and state its exact M48
  implementation status.
- Update architecture and workflow navigation to make the roadmap discoverable.

## Inputs

- User direction recorded on 2026-08-08.
- M48 closure evidence and ADR-0049.
- Existing task-lifecycle and hosted-provider authorization rules.

## Code paths

None. Documentation and lifecycle records only.

## Docs to update

- `docs/architecture/v1/post-m48-closed-loop-roadmap.md`
- `docs/architecture/v1/contracts/q01-observation-build-separation.md`
- `docs/architecture/overview.md`
- `docs/workflow/status.md`
- this workpack and its active handoff

## Trace/schema changes

None. The roadmap identifies future schema work but changes no runtime
behavior, trace, report, manifest, or CLI contract.

## Decision-package impact

- `decision_id`: none; this is implementation routing, not a new runtime decision.
- Q01/Q02 effect: records the required observation-to-provider integration order.
- Q03/Q04 effect: preserves geometry gates and provenance as separate evidence.
- Evidence role: process and scope control only.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

Default operation remains offline and credential-free. This workpack does not
authorize a provider request, external data intake, a prompt change, a
manifest change, IR/SDK work, or runtime behavior change.

## Acceptance

```powershell
uv run python tools\check_governance.py
uv run python -m pytest tests\test_governance_audit.py -q
uv run python -m ruff check .
git diff --check
```

## Evidence reuse / guidance-card disposition

No reusable evidence; this workpack creates only a development-routing record.

## Status transition

On closure, update `docs/workflow/status.md` first, move this workpack to
`done/`, archive the active handoff, and run the governance audit. The next
G2 or G3 step requires a separately selected bounded workpack; G2/G3 also
require an independent reviewer.

## Closure rationale

The user-selected closed-loop-first route, its G2/G3 dependencies, and the
reference-model non-egress boundary are recorded in the durable roadmap. The
Q01/Q02 contract now accurately states M48's implemented capability while
preserving the separate provider-integration boundary. Closure verification is
recorded in this workpack after lifecycle archival.

## Out of scope

Any code change, provider call, external-data use, executable manifest change,
or evaluation claim.
