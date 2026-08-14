# Handoff: Trigger-Driven Workpack Reindex

- **Date**: 2026-08-11
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M103-001-trigger-driven-workpack-reindex`

## Goal

Reindex unstarted, trigger-driven workpacks as semantic `WP-TRG-*` records;
reserve new M numbers for newly activated execution workpacks.

## Done

- Current status and the unarchived workpack inventory were reviewed.
- M103-001 was opened as the bounded governance change.

## In progress

- None.

## Next

- Await explicit selection of a new bounded package.

## Decisions

- Completed workpacks retain historical M labels; only future, unstarted
  packages lose them. The resulting convention is recorded in ADR-0061.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Files | `docs/workpacks/`, `docs/workflow/status.md` |
| Commands | `uv run python tools/check_governance.py` |

## Resume prompt

```
Continue Brep2Code work: finish M103-001 trigger-driven workpack reindex.
Read docs/handoff/active/2026-08-11-trigger-driven-workpack-reindex.md.
First action: inspect migrated deferred package references and run governance checks.
```
