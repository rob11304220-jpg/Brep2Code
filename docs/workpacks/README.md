# Workpacks

Workpacks are the minimum distributable development task package. They are
bounded execution ledgers: scope, owner, acceptance, compatibility constraints
and closure provenance for one change. They do not own the enduring route,
architecture decision, contract, case disposition or evidence interpretation.

Use [workpack governance](../workflow/workpack-governance.md) for the durable
information and citation rules. Use [status](../workflow/status.md) for current
selection, [the route-disposition index](../workflow/workpack-route-disposition-index.md)
for whether a trigger remains meaningful, and [milestone history](../workflow/milestone-history.md)
for compact historical navigation.

## Directory meaning

```text
docs/workpacks/
  active/      # selected execution authority; must match status and active handoff
  backlog/     # identified proposal, not selected authority
  deferred/    # semantic trigger and re-entry provenance, not a queue
  done/        # immutable completed execution ledger
  archive/     # consumed, superseded, rejected or evidence-only provenance
```

The directories retain the full historical record. Search `done/` or `archive/`
only for named acceptance, original-report, audit or provenance needs; never
infer current work, authority or authorization from a historical package.

## Numbering

```text
active:   WP-M<new-milestone>-<number>-<slug>.md
deferred: WP-TRG-<number>-<slug>.md
```

M numbers are assigned only when a user selects a new bounded package.
`WP-TRG-*` names a semantic trigger, not a reserved milestone, owner, budget
or authorization. A completed or archived package is never reactivated; a
renewed question receives a new M number and fresh inputs/authority.

## Required workpack structure

```markdown
# WP-M0-001: Title

- Status: active
- Milestone: M0
- Owner: <owner>
- Reviewer: not required (G0/G1) | <independent reviewer>
- Risk tier: G0 | G1 | G2 | G3

## Goal
## Scope
## Attribution question and sampling intent
## Inputs
## Code paths
## Docs to update
## Trace/schema changes
## Decision-package impact
## Compatibility constraints
## Acceptance
## Owner completion boundary
## Permitted stop conditions
## Evidence reuse / guidance-card disposition
## Status transition
## Closure rationale
## Durable conclusion and route disposition
## Out of scope
## Repair hypothesis and evaluation boundary
## Notes
```

Each section is governed by the detailed template requirements in
[workpack governance](../workflow/workpack-governance.md) and
[task lifecycle](../workflow/task-lifecycle.md). G2/G3 packages require the
additional review and authorization gates defined there.

## Stable navigation

| Question | Start with | Open a workpack only when |
|---|---|---|
| What may be selected now? | [status](../workflow/status.md) | It names the active package or selected trigger. |
| Which route remains meaningful? | [Route Decision Map](../architecture/v1/route-decision-map.md) and [route-disposition index](../workflow/workpack-route-disposition-index.md) | The trigger's exact scope or historical re-entry wording is needed. |
| What is the current project route? | [Current Project Route](../architecture/v1/current-project-route.md) | Acceptance/provenance for a stable route artifact is needed. |
| What did a milestone establish? | [milestone history](../workflow/milestone-history.md), ADRs, contracts and evidence indexes | Its bounded acceptance record or original evidence is needed. |
| What did a hosted run show? | [hosted experiment registry](../workflow/hosted-experiment-registry.md) | The frozen terminal report or audit record is needed. |

Completed-workpack direct links are limited by the
[durable citation contract](../workflow/workpack-governance.md#durable-citation-contract).
This README deliberately does not repeat chronological route history: stable
records above carry the continuing conclusions, while each workpack preserves
the execution detail required for audit and reproduction.
