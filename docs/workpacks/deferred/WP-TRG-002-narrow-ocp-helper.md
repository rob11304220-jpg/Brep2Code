# WP-TRG-002: Narrow OCP Operation Helper

- Status: deferred
- Owner: unassigned

## Goal

Introduce one minimal runtime helper only when completed external evidence proves a repeated, attributable OCP operation problem that existing script repair cannot address reliably.

## Trigger condition

At least three completed external cases share the same directly attributable OCP/API, parameter, or dependency-sequencing failure.

## Scope

- Define one constrained helper input/output contract for the demonstrated failure family.
- Preserve the underlying script, gate statuses, and failure evidence rather than converting failures into opaque helper outcomes.
- Add a smallest regression set covering each observed external pattern and a non-match case.

## Inputs

- Completed evidence review with the three or more attributable examples.
- [Post-M9 roadmap](../../architecture/v1/post-m9-evidence-gated-roadmap.md)
- [Runtime boundaries](../../architecture/v1/runtime-boundaries.md)

## Code paths

Determined by the selected operation family; do not choose a code path before the evidence review.

## Docs to update

Update runtime materials, the relevant contract/module documentation, tests, status, handoff, and a new ADR describing the lasting helper boundary.

## Trace/schema changes

Any new structured helper signal must be versioned and retain the original gate-level evidence. No full provider response, credential, or environment data may be added.

## Compatibility constraints

Default offline behavior, `wsl-bwrap` execution for provider-generated scripts, and existing gates remain unchanged. The helper is not a generic CAD SDK, IR, CAD workplace, or new provider tool surface.

## Acceptance

- Regression cases reproduce the original failure family before the helper and pass after it without hiding gate evidence.
- Non-matching corpus cases preserve previous behavior.
- The helper's contract is bounded enough to exclude unrelated modeling operations.

## Status transition

When done, update status, handoff, contracts, runtime material, and ADR before moving this workpack to `done/`. Reassess IR eligibility only after two helpers are independently validated.

## Out of scope

Generic feature APIs, project CAD SDK, IR, external corpus expansion, hosted reruns, FEA, VLM judging, and multi-agent orchestration.
