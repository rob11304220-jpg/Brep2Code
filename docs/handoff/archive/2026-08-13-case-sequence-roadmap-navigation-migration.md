# Handoff: Case and sequence roadmap navigation migration

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M168-001-case-sequence-roadmap-navigation-migration`

## Goal

Replace case/sequence historical workpack timelines with stable navigation.

## Done

- M165--M167 froze citation rules, classified deferred routes, and migrated the
  high-frequency workpack and milestone indexes.

## In progress

- Migrate Fusion, sequence-paired and family-charter historical references.

## Next

- Identify durable authority for each in-scope route conclusion.
- Update navigation, run acceptance, and close M168.

## Decisions

- Completed workpacks remain immutable provenance, not architecture or case
  authorities.

## Blockers

- None.

## Key paths

| Kind | Path |
|------|------|
| Files | `docs/architecture/v1/fusion360-paired-data-roadmap.md` |
| Files | `docs/architecture/v1/sequence-paired-prismatic-hole-roadmap.md` |
| Commands | `uv run python tools/check_governance.py`; `git diff --check` |

## Resume prompt

```
Continue Brep2Code work: complete M168 case and sequence roadmap navigation migration.
Read docs/handoff/active/2026-08-13-case-sequence-roadmap-navigation-migration.md.
First action: map every in-scope historical conclusion to a durable authority.
```
