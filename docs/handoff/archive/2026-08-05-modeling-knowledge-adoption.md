# Handoff: Modeling Knowledge Adoption Documentation

- **Date**: 2026-08-05
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Move reusable M25--M27 case-family design evidence out of archived workpack-only
discovery into the development-side modeling knowledge system, without changing
runtime scope.

## Done

- Added reviewed, bounded knowledge units for face-selected dependent cuts,
  multi-inner-loop pockets, and oriented rounded slots.
- Updated the coverage matrix, library README, and library catalog to the
  completed M27 / 75-active-case state.
- Updated the ranked case-family route so M27 is completed and no successor is
  implicitly selected.
- Added ADR-0034 and the design page that separates development-side reference
  use from future runtime-card, analysis, Harness helper, IR, DSL, SDK, manifest,
  provider, training, and runtime adoption gates.
- Validated all changed JSON with `ConvertFrom-Json` and ran `git diff --check`.
- Archived the completed M27 handoff.

## In progress

- None.

## Next

- Select a new bounded coverage gap only through the coverage matrix and a
  separate workpack.

## Decisions

- Archived workpacks remain acceptance evidence, while reviewed projections in
  `docs/corpus/knowledge/` are the long-term development-side reference.
- [ADR-0034](../../architecture/adr/0034-modeling-knowledge-adoption-boundaries.md)
  preserves separate authorization and evidence gates for every runtime or
  Harness adoption.

## Blockers

- None. No runtime or hosted authorization is implied by this documentation work.

## Key paths

| Kind | Path |
|------|------|
| Design | `docs/architecture/v1/modeling-knowledge-adoption.md` |
| ADR | `docs/architecture/adr/0034-modeling-knowledge-adoption-boundaries.md` |
| Knowledge | `docs/corpus/knowledge/operations/` |
| Planning | `docs/corpus/knowledge/coverage-matrix.json` |
| Commands | `Get-Content -Raw <json> | ConvertFrom-Json`; `git diff --check` |

## Resume prompt

```
Resume Brep2Code after completed modeling-knowledge adoption documentation.
Read docs/handoff/active/2026-08-05-modeling-knowledge-adoption.md.
First action: select a new bounded coverage gap through the knowledge matrix.
```
