# Handoff: Legacy trigger route disposition

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M166-001-legacy-trigger-route-disposition`

## Goal

Classify every remaining legacy deferred hosted/family trigger against a stable
authority without activating it.

## Done

- M165 closed the durable completed-workpack citation contract.

## In progress

- Assess TRG-005--010, TRG-016 and TRG-018 against current routes and terminal
  evidence.

## Next

- Read each trigger and its current route/evidence authority.
- Update the route-disposition index, then run acceptance.

## Decisions

- `deferred` is lifecycle location; route disposition is separate planning
  metadata and never authorization.

## Blockers

- None.

## Key paths

| Kind | Path |
|------|------|
| Files | `docs/workflow/workpack-route-disposition-index.md` |
| Files | `docs/workpacks/deferred/WP-TRG-005-*.md` through `WP-TRG-018-*.md` |
| Commands | `uv run python tools/check_governance.py`; `git diff --check` |

## Resume prompt

```
Continue Brep2Code work: complete M166 legacy trigger route disposition.
Read docs/handoff/active/2026-08-13-legacy-trigger-route-disposition.md.
First action: classify the eight in-scope triggers from their stable authorities.
```
