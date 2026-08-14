# Handoff: M23-001 additive-boss-dependent-cut design

- **Date**: 2026-08-05
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Record the completed six-row `additive-boss-dependent-cut-v1` design before
any candidate production.

## Done

- The user selected M23-001.
- ADR-0025 accepted the bounded offline design route.
- The design document, preregistration, and M23-002 backlog workpack exist.

## In progress

- No active workpack.

## Next

1. Await separate user selection of M23-002 before producing assets.
2. Do not infer a producer, new rows, manifest, provider, or runtime task.

## Decisions

- ADR-0025 limits the family to a joined boss and blind cut, without face/edge
  references or runtime implications.

## Blockers

- M23-002 requires separate user selection; no runtime blocker exists.

## Key paths

| Kind | Path |
|------|------|
| ADR | `docs/architecture/adr/0025-additive-boss-dependent-cut-design.md` |
| Design | `docs/architecture/v1/additive-boss-dependent-cut-sequence-pair-design.md` |
| Preregistration | `docs/corpus/sequence-paired/additive-boss-dependent-cut-v1-preregistration.json` |
| Successor | `docs/workpacks/backlog/WP-M23-002-additive-boss-dependent-cut-controlled-production.md` |

## Resume prompt

```
M23-001 is complete. Read workflow status before selecting M23-002. Do not
create assets or infer a manifest, provider, or runtime task.
```
