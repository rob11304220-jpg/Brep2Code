# Handoff: M25-002 face-selected dependent-cut production complete

- **Date**: 2026-08-05
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Produce and validate exactly the six preregistered M25 cases without expanding
the face-selector claim.

## Done

- The six frozen candidates are hash-stable across two clean builds.
- The scoped audit passed geometry, exact selector dependency, five mutations,
  semantic invariants, split isolation, and wrong/vertical/ambiguous controls.
- Focused tests (5), Ruff, `audit_case_library.py --replay` (57 records), and
  `git diff --check` passed.

## In progress

- Historical M25 production is complete. Its later review and restricted
  governance promotion were completed under ADR-0029; the six records are now
  active self-authored cases.

## Next

- Superseded by the active M26-001 design workpack. The next family still
  begins with coverage-gap preregistration; no manifest, provider, training,
  or runtime change is authorized by this historical M25 record.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/done/WP-M25-002-face-selected-dependent-cut-controlled-production.md` |
| Preregistration | `docs/corpus/sequence-paired/face-selected-dependent-cut-v1-preregistration.json` |
| Audit / producer | `tools/audit_sequence_paired_face_selected_dependent_cut.py` |

## Resume prompt

```
Read status.md and the active M26 handoff. M25 is fully promoted under
ADR-0029; do not reopen its production or governance work.
```
