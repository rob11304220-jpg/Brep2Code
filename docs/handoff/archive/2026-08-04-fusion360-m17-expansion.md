# Handoff: Fusion 360 validated-subset expansion

- **Date**: 2026-08-04
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Select and locally replay a preregistered small Fusion subset that tests both
currently supported profile classes without widening the replay surface.

## Done

- M14 supplied three replay-pass, family-isolated cases.
- M15 approved M16; M16 completed the explicit local-only control manifests.
- M17 fixed a source-order scan bound of 200 entries per official split.
- The selected two development cases passed; the selected held-out Line3D case
  failed all geometry gates because listed curve starts were non-continuous.

## Next

- Do not advance M18. A future loop-ordering diagnostic needs a separately
  scoped workpack and must retain the held-out failure as a control.

## Decisions

- No feature-support expansion: only one transformed profile and one zero-taper
  NewBody distance extrude remain valid.
- No replacement held-out case, scan extension, parser change, corpus run or
  provider request occurred.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/done/WP-M17-001-fusion360-validated-subset-expansion.md` |
| Selection | `docs/corpus/external/fusion360-gallery-r1.0.1-m17-001-selection.json` |
| Report | `data/fusion360-gallery-m17-replay/report.json` |
