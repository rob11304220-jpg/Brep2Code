# Handoff: M88 Reference-assisted Case Ladder

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M88-001-reference-assisted-case-ladder-plan`

## Goal

Freeze the staged workpack allocation for reference-assisted development cases
without changing runtime behavior or invoking a provider.

## Done

- M85 (`cylinder`) and M87 (`block_with_hole`) each have one terminal,
  two-request hosted pass using the frozen vertical-cylinder card.
- M86 established deterministic offline role selection for `cylinder`,
  `block_with_hole`, and `three_hole_plate`.

## In progress

- None. M88 has frozen the evidence-readiness ladder and the required G2/G3
  package boundaries for the seven existing P0/P1 reference packs.

## Next

- Wait for the user to select M89 or another bounded package. M89 is the sole
  next recommended execution package: `three_hole_plate` with the existing
  repeated-cut role/card.

## Decisions

- Order by incremental evidence readiness: run the admitted repeated-cut role
  before qualifying a new `box` card, even though `box` is geometrically
  simpler.
- Every new mechanism is split into offline G2 card qualification and a
  separate, explicitly authorized G3 hosted smoke.

## Blockers

- No hosted authorization exists for M89 or later packages.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M88-001-reference-assisted-case-ladder-plan.md` |
| Status | `docs/workflow/status.md` |
| Reference-pack contract | `docs/corpus/reference-packs/reference-pack-contract-v1.json` |
| Evidence reports | `data/corpus-runs/m85-cylinder-reference-assisted.json`; `data/corpus-runs/m87-block-with-hole-reference-assisted.json` |

## Resume prompt

```
Continue Brep2Code M88 reference-assisted case-ladder planning.
Read docs/handoff/active/2026-08-10-reference-assisted-case-ladder.md.
First action: run the M88 documentation/governance acceptance commands and
record their terminal results before closing or selecting M89.
```
