# Handoff: Fusion independent Line3D selector validation

- **Date**: 2026-08-04
- **Subproject**: `brep2code`
- **Status**: completed

## Goal

Test the unchanged M17-005 selector against a small independent, locally
cached Fusion Line3D population without altering strict replay.

## Done

- M17-005 passed its fixed four-case matrix but remained candidate-only.
- M17-006 preregistered independent source-family selection, split boundary,
  frozen mapping and stopping conditions.
- The selected 2 development/1 held-out families all passed the frozen
  selector; one development strict baseline failed volume and topology gates.

## In progress

- The independent matrix is complete; strict replay remains the default.

## Next

- Await an explicitly selected mapping-policy review before changing any
  default path or opening another validation workpack.

## Decisions

- The selector and geometry gates are frozen from M17-005.
- The selector now has 5 development/2 held-out gate passes across the two
  workpacks, but this is still not a generic mapping-policy decision.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Completed workpack | `docs/workpacks/done/WP-M17-006-independent-line3d-selector-validation.md` |
| Prior review | `docs/architecture/v1/fusion360-m17-selector-promotion-validation-review.md` |
| Selection record | `docs/corpus/external/fusion360-gallery-r1.0.1-m17-006-selection.json` |
| Review | `docs/architecture/v1/fusion360-m17-independent-line3d-selector-validation-review.md` |

## Resume prompt

```
M17-006 is complete. The frozen selector passed an independent 2 development/
1 held-out matrix, including one strict-baseline failure. Strict replay remains
the default; do not change it, extend the scan, run corpus/provider/hosted work
or start M18 without a newly selected workpack.
```
