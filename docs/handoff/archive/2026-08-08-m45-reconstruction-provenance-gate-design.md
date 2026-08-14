# Handoff: M45 reconstruction-provenance gate design

- **Date**: 2026-08-08
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M45-001-reconstruction-provenance-gate-design`

## Goal

Design an offline Q03 classification/control boundary so that M44-style STEP
round trips cannot be reported as B-Rep-to-CAD reconstruction.

## Done

- User selected the bounded M45 design work after reviewing M44.
- Defined `round_trip`, `independent_reconstruction`, and
  `provenance_unknown`, with verified input reads taking precedence over
  geometry success.
- Defined the future absent-input execution control and separated Q01
  observation capability from executed-script input access.
- Added ADR-0048 and the reviewed decision package; no runtime changed.

## In progress

- None.

## Next

- If selected, create a separate G2 offline implementation workpack with an
  independent reviewer; it must trace indirect input access and add the
  absent-input control without provider use.

## Decisions

- Preserve existing geometry gates as Harness-health gates; they are not
  provenance evidence.  See ADR-0048.

## Blockers

- None.

## Key paths

| Kind | Path |
|------|------|
| Branch | `main` |
| Files | `docs/workpacks/done/WP-M45-001-reconstruction-provenance-gate-design.md`; `docs/architecture/adr/0048-reconstruction-provenance-gate-design.md` |
| Evidence | `data/records/corpus-abc_v00_00000031/revisions/20260808T022759497760Z/workspace/build_sequence.py` |

## Resume prompt

```
Continue Brep2Code work: decide whether to select M45's G2 offline provenance-gate implementation.
Read docs/handoff/archive/2026-08-08-m45-reconstruction-provenance-gate-design.md.
First action: read ADR-0048 and create a workpack only if the implementation scope is selected.
```
