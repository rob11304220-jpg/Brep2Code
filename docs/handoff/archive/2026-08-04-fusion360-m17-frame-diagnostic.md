# Handoff: Fusion 360 sketch-frame extrude-direction diagnostic

- **Date**: 2026-08-04
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Complete a finite ordering/direction treatment matrix for the fixed M17
held-out Line3D mismatch.

## Done

- M17-002 rejected endpoint ordering alone and restored the strict baseline.
- M17-003 ran every preregistered held-out row. Only `ordered_y` passed all
  held-out gates; the other four rows failed at least one gate.
- Applying `ordered_y` to the three M14/M17 Line3D controls made all three
  degenerate (volume relative delta 1.0). Both Circle3D controls retained
  their strict-baseline pass outcome.

## In progress

- No further work is selected. Await a separately scoped, evidence-gated
  workpack; M18 remains backlog.

## Next

- Do not reopen M17 without a separately scoped workpack. No M18 transition
  is implied by the result.

## Decisions

- `ordered_y` is case-local evidence, not a safe parser rule. Strict replay is
  unchanged; no manifest, corpus, provider or M18 transition follows.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Completed workpack | `docs/workpacks/done/WP-M17-003-sketch-frame-extrude-direction-diagnostic.md` |
| Status authority | `docs/workflow/status.md` |
| Review | `docs/architecture/v1/fusion360-m17-frame-diagnostic-review.md` |
| Diagnostic tool | `tools/diagnose_fusion360_m17_frame.py` |

## Resume prompt

```
Continue Brep2Code from the completed M17-003 record. Read
docs/workflow/status.md and this handoff. First action: wait for a separately
selected evidence-gated workpack; do not reopen M17, modify parser behavior,
or start M18 without explicit scope.
```
