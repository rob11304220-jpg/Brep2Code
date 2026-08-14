# Handoff: Historical workpack navigation migration

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M167-001-historical-workpack-navigation-migration`

## Goal

Replace high-frequency chronological workpack navigation with stable indexes
while retaining acceptance and provenance evidence.

## Done

- M165 froze the durable citation contract.
- M166 classified all deferred triggers in the maintained disposition index.

## In progress

- Compact the workpack entry page and repair milestone-history routing.

## Next

- Update the two high-frequency navigation records.
- Run governance audit and close this final governance-series package.

## Decisions

- Historical execution ledgers remain immutable; only their navigation role is
  reduced.

## Blockers

- None.

## Key paths

| Kind | Path |
|------|------|
| Files | `docs/workpacks/README.md`, `docs/workflow/milestone-history.md` |
| Commands | `uv run python tools/check_governance.py`; `git diff --check` |

## Resume prompt

```
Continue Brep2Code work: complete M167 historical workpack navigation migration.
Read docs/handoff/active/2026-08-13-historical-workpack-navigation-migration.md.
First action: replace the long workpack history catalog with stable navigation.
```
