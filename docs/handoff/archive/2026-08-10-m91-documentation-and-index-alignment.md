# Handoff: M91 documentation and index alignment

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M91-001-documentation-and-index-alignment`

## Goal

Correct current documentation and knowledge-index drift found after M90 without
changing case assets or any runtime/provider boundary.

## Done

- Read-only audit identified stale 75-case summaries, a stale M23 route link,
  stale active-workpack pointers in three decision records, and an M76
  prerequisite that conflicts with ADR-0051.

## In progress

- G1 documentation and index alignment.

## Next

- Run the G1 acceptance checks, close this workpack, then select the separate
  G2 M90 case-metadata lifecycle alignment workpack.

## Decisions

- Keep M90 outside executable manifests, provider inputs and runtime; this
  workpack corrects descriptions only and does not broaden that boundary.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Status | `docs/workflow/status.md` |
| Workpack | `docs/workpacks/active/WP-M91-001-documentation-and-index-alignment.md` |
| M90 decision | `docs/architecture/adr/0055-repeated-feature-pattern-governance.md` |

## Resume prompt

```
Continue M91 G1 documentation and index alignment.
Read docs/handoff/active/2026-08-10-m91-documentation-and-index-alignment.md
and docs/workflow/status.md. Run the stated acceptance checks before closure.
```
