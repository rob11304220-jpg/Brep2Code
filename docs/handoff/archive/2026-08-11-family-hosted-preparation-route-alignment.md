# Handoff: Family Hosted Preparation Route Alignment

- **Date**: 2026-08-11
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M122-001-family-hosted-preparation-route-alignment`

## Goal

Align the project wording and deferred route so default next work prepares the
family/mechanism campaigns intended for later hosted use, instead of
continuing blocked hosted-stability triggers by default.

## Done

- Updated `status.md`, the hosted batch candidate plan, the five-family
  roadmap, the four-track roadmap, and the deferred workpack index.
- Added `WP-TRG-020` through `WP-TRG-023` as the family-specific charter-draft
  queue for the four no-card five-family candidates.
- Recorded the adaptive slack rule: switch later only among already prepared
  families, without reopening frozen family scope.

## In progress

- None.

## Next

- Await a user-selected bounded package. The default recommended entries are
  now `WP-TRG-020` through `WP-TRG-023`; hosted-stability re-entry remains a
  separate later decision.

## Decisions

- The project's default offline preparation queue should mirror the families it
  wants to run later with hosted evaluation.
- Shared hosted-stability triggers remain valid blockers, but they are not the
  default next-package queue while still unmet.

## Blockers

- Shared hosted-stability re-entry remains unmet for actual execution.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/done/WP-M122-001-family-hosted-preparation-route-alignment.md` |
| Files | `docs/architecture/v1/current-hosted-batch-candidate-plan.md` |
| Files | `docs/workpacks/deferred/README.md` |
| Commands | `python tools\check_governance.py` |

## Resume prompt

```
M122-001 is closed. Read docs/workflow/status.md and wait for a user-selected
bounded package. Prefer WP-TRG-020 through WP-TRG-023 as the default next
family-hosted preparation queue.
```
