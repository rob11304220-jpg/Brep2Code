# Handoff: Fusion Line3D frame-evidence audit

- **Date**: 2026-08-04
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Audit the fixed four Fusion Line3D cases for existing transform, profile and
extent evidence that could distinguish their replay-direction mappings.

## Done

- M17-003 rejected `ordered_y` as a general rule: it passes the fixed held-out
  but degenerates all three Line3D controls.
- M17-004 is scoped and selected; no code or replay treatment has run.

## In progress

- Built and validated the local-only, source-linked evidence table for all four
  fixed cases.

## Next

- Wait for a user decision on whether to create a separate selector-promotion
  workpack. Do not change replay behavior or start M18 automatically.

## Decisions

- The fixed evidence nominates a profile-normal / STEP-projection /
  extent-boundary selector only for separate promotion evaluation; it is not a
  parser policy change.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Completed workpack | `docs/workpacks/done/WP-M17-004-fusion-line3d-frame-evidence-audit.md` |
| Status authority | `docs/workflow/status.md` |
| Previous review | `docs/architecture/v1/fusion360-m17-frame-diagnostic-review.md` |
| M17-004 review | `docs/architecture/v1/fusion360-m17-frame-evidence-audit-review.md` |
| Audit tool | `tools/audit_fusion360_m17_frame.py` |
| Local evidence | `data/fusion360-gallery-m17-frame-evidence/{report.json,report.md}` |

## Resume prompt

```
Continue Brep2Code after the completed M17-004 frame-evidence audit. Read
docs/workflow/status.md and
docs/architecture/v1/fusion360-m17-frame-evidence-audit-review.md. First
action: wait for the user to choose a separately scoped selector-promotion
workpack; do not alter replay behavior, select cases, or start M18 implicitly.
```
