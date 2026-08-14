# Handoff: Prismatic-hole controlled expansion

- **Date**: 2026-08-04
- **Subproject**: `brep2code`
- **Status**: done

## Goal

M20-002 is complete: its frozen `prismatic-hole-v1` grammar passed the exactly
nine paired self-authored cases (6 development / 3 held-out), including the
audited counterbore candidate producer, without changing runtime behavior or
global case-library governance.

## Done

- M20-001 completed and its review permitted a separate controlled expansion,
  but explicitly rejected global governance promotion.
- All nine M20-002 cases passed geometry, exact sequence, and declared
  editability checks.  The focused suite passed 8 tests; a second counterbore
  production matched the checked-in SHA-256 values.
- Completion review permits only a future independent governance-promotion
  proposal; it records no reusable experience card.

## In progress

- No M20 task is in progress.

## Next

1. Await an explicit user choice before creating any future governance-promotion
   workpack.

## Decisions

- Freeze `SketchRect -> ExtrudeBase -> CutCylinder`; no grammar expansion or
  source-history claim.  See [ADR-0018](../../architecture/adr/0018-sequence-paired-prismatic-hole-pilot.md).
- Candidate generation is not case admission.  Explicit audit passed, but no
  registry, manifest, provider, training, or runtime route changed.

## Blockers

- None.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/done/WP-M20-002-prismatic-hole-controlled-expansion.md` |
| Contract | `docs/architecture/v1/contracts/sequence-paired-prismatic-hole.md` |
| Review | `docs/architecture/v1/m20-prismatic-hole-controlled-expansion-review.md` |
| Audit | `tools/audit_sequence_paired_prismatic_hole.py` |

## Resume prompt

```
Continue Brep2Code after M20-002. Read the completion review and workflow
status. First action: wait for an explicit user decision before proposing a
separate governance-promotion workpack.
```
