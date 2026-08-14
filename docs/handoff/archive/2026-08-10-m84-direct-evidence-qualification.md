# Handoff: M84 reference-pack direct-evidence qualification

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M84-001-reference-pack-direct-evidence-qualification`

## Goal

Determine whether the preregistered `vertical-cylinder-construction-v1`
candidate has three independent, direct, source-linked development cases that
satisfy ADR-0016's entry threshold for a later M19-002 selection.

## Done

- M83 froze the seven candidate packs and their source-boundary audit.
- User selected M84. Its fixed cases are `cylinder`, `block_with_hole`, and
  `three_hole_plate`; they respectively use the action as a final primitive,
  single cut tool, and repeated cut tool.
- Added the fixed qualification record and local source-action audit. All
  three scripts directly invoke `OCP.BRepPrimAPI.BRepPrimAPI_MakeCylinder`.
- Added the bounded source-linked experimental card; it remains unmounted.
- Owner checks passed: M83 audit, M84 qualification audit, runtime-guidance
  audit, 4 focused tests, full Ruff, governance audit, and diff check.

## In progress

- None.

## Next

- M84 is closed after Liaol's independent approval. M19-002 is eligible for
  separate user selection but is not active and its card is not runtime-visible.

## Decisions

- This qualification is intentionally narrow: it excludes arbitrary axes,
  blind/angled/non-circular tools, and all unobserved geometry roles.
- A pass makes M19-002 eligible for separate user selection only; it does not
  activate retrieval or alter runtime behavior.

## Blockers

- None for M84. M19-002 remains inactive pending separate user selection.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M84-001-reference-pack-direct-evidence-qualification.md` |
| Candidate contract | `docs/corpus/reference-packs/reference-pack-contract-v1.json` |
| Boundary | `docs/architecture/adr/0016-evidence-bounded-runtime-guidance-cards.md` |

## Resume prompt

```
Continue Brep2Code M84 direct-evidence qualification.
Read docs/handoff/active/2026-08-10-m84-direct-evidence-qualification.md.
M84 is complete. Before any successor, read docs/workflow/status.md; M19-002
must be separately selected and remains an offline development-only evaluation.
Do not mount, inject, or retrieve the experimental card, change runtime,
provider, prompt, or manifest, or make any hosted request.
```
