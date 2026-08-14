# Handoff: M148 Project Theory Map and Document Navigation

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `done` (archived after G1 closure)
- **Related workpack**: `WP-M148-001-project-theory-map-and-document-navigation`

## Goal

Create one compact theory-map entry that routes development-side theory,
runtime/system architecture, evidence-asset records, and current workflow
status without changing their authorities.

## Done

- M146 delivered the reviewed source-linked crosswalk and M147 aligned the
  successor route.
- User selected TRG-031; M148 is active.

## In progress

- None. M148 is closed.

## Next

- Wait for explicit user selection of a deferred successor. Do not activate
  TRG-032 through TRG-035 or TRG-028 automatically.

## Decisions

- Theory navigation is the M146 crosswalk; the Q01--Q04 pipeline is the
  system/runtime view; case and governance records are evidence-asset views;
  `status.md` remains the only execution authority.
- The theory map is a compact link layer, not a new registry or source of
  runtime/hosted authority.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M148-001-project-theory-map-and-document-navigation.md` |
| Crosswalk | `docs/corpus/knowledge/development-evidence-crosswalk-v1.md` |
| Target map | `docs/architecture/v1/project-theory-map.md` |

## Resume prompt

M148 is complete. Read `docs/workflow/status.md` and wait for explicit user
selection of a bounded successor. Do not infer authority from the theory map.
