# Handoff: M90 repeated-feature pattern design

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M90-002-repeated-feature-pattern-controlled-production`

## Goal

Complete the M90 offline repeated-feature-pattern family.

## Done

- User selected the offline case-coverage route; no hosted authority was used.
- M90-001 was activated, ADR-0054 froze its scope, and M90-002--004 were
  registered as non-active successors.
- The six-row preregistration record was created for intake audit.
- The intake audit and governance audit passed; `git diff --check` passed.
- Liaol independently approved M90-001; no hosted authority was used.

## In progress

- None; M90-001--004 are closed.

## Next

- Select a new bounded package only on user direction.

## Decisions

- The first family is `repeated-feature-pattern-v1`, not a mixed pattern,
  revolve or shell package, because it is the next isolated coverage gap; see
  [ADR-0054](../../architecture/adr/0054-repeated-feature-pattern-preregistration.md).

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M90-002-repeated-feature-pattern-controlled-production.md` |
| Preregistration | `docs/corpus/sequence-paired/repeated-feature-pattern-v1-preregistration.json` |
| ADR | `docs/architecture/adr/0054-repeated-feature-pattern-preregistration.md` |

## Resume prompt

```
Continue Brep2Code after M90's offline repeated-feature-pattern completion.
Read docs/handoff/active/2026-08-10-m90-repeated-feature-pattern-design.md,
docs/workflow/status.md, and the completed M90 workpacks.
First action: wait for the user to select a new bounded package; do not contact
a provider or add M90 cases to a manifest.
```
