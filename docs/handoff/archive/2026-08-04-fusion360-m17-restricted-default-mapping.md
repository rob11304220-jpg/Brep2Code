# Handoff: Restricted Fusion Line3D default mapping

- **Date**: 2026-08-04
- **Subproject**: `brep2code`
- **Status**: completed

## Goal

Resolve the M17 mapping-policy review without expanding Fusion support.

## Done

- Adopted the frozen selector as the default only for the evidence-bounded
  Line3D subset in ADR-0017.
- M14, M17, M17-005 and M17-006 local matrices retained their required gates.
- Added fail-closed input-bbox coverage and the workpack evidence-card
  disposition requirement.

## In progress

- None.

## Next

- Keep the restricted mapping unchanged. Any Fusion scope expansion or
  Harness integration requires a newly selected workpack and independent
  evidence. M18 remains unselected.

## Decisions

- The historical strict Line3D path is comparison-only; it is not a fallback.
- The selector result is parser-local, not runtime guidance.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| ADR | `docs/architecture/adr/0017-restricted-fusion-line3d-default-mapping.md` |
| Workpack | `docs/workpacks/done/WP-M17-007-restricted-line3d-default-mapping-policy.md` |
| Review | `docs/architecture/v1/fusion360-m17-restricted-default-mapping-review.md` |

## Resume prompt

```
M17-007 is complete. The fail-closed selector is default only for the bounded
Fusion Line3D subset. Do not extend it, integrate it with Harness, or start
M18 without a new evidence-scoped workpack.
```
