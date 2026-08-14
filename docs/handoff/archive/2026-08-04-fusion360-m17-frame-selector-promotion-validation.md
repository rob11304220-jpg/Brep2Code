# Handoff: Fusion Line3D frame selector promotion validation

- **Date**: 2026-08-04
- **Subproject**: `brep2code`
- **Status**: completed

## Goal

Validate, only within the four fixed hash-linked Fusion Line3D cases, whether
the M17-004 explicit frame selector can repair the held-out case without
regressing any development control.

## Done

- M17-004 nominated the profile-normal / STEP-projection / extent-boundary
  selector without changing replay behavior.
- M17-005 has preregistered its fixed cases, matrix, gates and stopping rules.
- The focused selector contract passed 3/3 tests, and the ignored local matrix
  reproduced the strict baseline then passed all four selector-treatment rows.

## In progress

- The four-case fixed-subset validation is complete; strict replay remains the
  default and the selector path is candidate-only.

## Next

- Await an explicit review/workpack before any further promotion. Do not infer
  generic parser support or start M18.

## Decisions

- The candidate has no fallback axis and no authority outside the one Sketch /
  one zero-taper NewBody extrude / Line3D outer-loop subset.
- The strict baseline was preserved and all selector-treatment rows passed;
  this validates only the hash-locked subset, not a general mapping policy.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Completed workpack | `docs/workpacks/done/WP-M17-005-frame-selector-promotion-validation.md` |
| Evidence review | `docs/architecture/v1/fusion360-m17-frame-evidence-audit-review.md` |
| Evidence tool | `tools/audit_fusion360_m17_frame.py` |
| Strict replay | `tools/replay_fusion360_m14.py` |
| Validation report | `docs/architecture/v1/fusion360-m17-selector-promotion-validation-review.md` |

## Resume prompt

```
M17-005 is complete. Read its review before proposing any new work. The
selector result is limited to four fixed hash-linked cases; strict replay is
still the default. Do not run corpus/provider/hosted work or start M18 without
an explicit newly selected workpack.
```
