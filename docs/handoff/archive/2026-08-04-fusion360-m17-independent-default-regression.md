# Handoff: Independent Fusion default Line3D regression

- **Date**: 2026-08-04
- **Subproject**: `brep2code`
- **Status**: completed

## Goal

Confirm the M17-007 restricted default mapping on new, preregistered families.

## Done

- Selected train orders 406/446 and test order 211 outside all prior M17
  families.
- The unchanged default selector passed bbox, volume and topology gates for
  all three rows; cumulative evidence is 7 development/3 held-out passes.

## In progress

- None.

## Next

- Retain the restricted mapping. A new workpack is required for broader
  Fusion support, Harness integration or M18.

## Decisions

- No new experience card: this is parser-local regression evidence.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/done/WP-M17-008-independent-default-line3d-regression.md` |
| Selection | `docs/corpus/external/fusion360-gallery-r1.0.1-m17-008-selection.json` |
| Review | `docs/architecture/v1/fusion360-m17-independent-default-regression-review.md` |

## Resume prompt

```
M17-008 is complete. The bounded default selector now has 7 development and 3
held-out gate passes. Do not expand Fusion support, integrate Harness, or start
M18 without a new evidence-scoped workpack.
```
