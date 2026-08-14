# Handoff: Prismatic Card-Effect Policy Design

- **Date**: 2026-08-11
- **Subproject**: `brep2code`
- **Status**: `completed`
- **Related workpack**: `WP-M114-001-prismatic-card-effect-policy-design`

## Goal

Complete the selected offline G2 design decision that follows M112
`inconclusive`, without creating a new execution policy or hosted scope.

## Done

- M113 aligned routes and created deferred TRG-019.
- Liaol independently approved M114's finite end-to-end policy design.

## In progress

- None. M114-001 is closed.

## Next

- Await a user-selected G2 development-only policy freeze; it must implement
  ADR-0065's design without reusing M97 or accessing held-out inputs.

## Decisions

- The design must be finite and end-to-end, with API admissibility classified
  before sandbox/geometry gates; it cannot reinterpret M97.
- [ADR-0065](../../architecture/adr/0065-prismatic-end-to-end-card-effect-policy-design.md)
  records this decision.

## Blockers

- Hosted stability is unmet; no provider action is in scope.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M114-001-prismatic-card-effect-policy-design.md` |
| Trigger | `docs/workpacks/archive/WP-TRG-019-prismatic-card-effect-policy-design.md` |
| M112 decision | `docs/workflow/m112-parameter-variation-held-out-readiness-review.md` |

## Resume prompt

```
M114-001 is closed. Await a user-selected G2 development-only policy freeze;
do not reuse M97 or access held-out/provider resources.
```
