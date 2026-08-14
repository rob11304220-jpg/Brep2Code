# Handoff: asymmetric cohort and annex qualification

- **Date**: 2026-08-14
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M175-001-asymmetric-cohort-and-annex-qualification`

## Goal

Qualify M174's 30-row no-card development cohort and three-role card-assisted
feasibility annex without producing a manifest or issuing a provider request.

## Done

- M174 reconciled the registry and replaced the infeasible equal-card design.
- User confirmed M175 re-entry.

## In progress

- M175 independently approved and closed.

## Next

- If selected, create a new bounded campaign-input freeze workpack; do not
  initiate hosted work.

## Decisions

- The main cohort and annex remain unpooled; main rows are all no-card.
- The annex retains only M170's three direct card roles and one-edit repair
  boundary. See ADR-0084 and M174 charter.

## Blockers

- None. No campaign-input freeze is selected.

## Key paths

| Kind | Path |
|---|---|
| Files | `docs/workpacks/active/WP-M175-001-asymmetric-cohort-and-annex-qualification.md` |
| Charter | `docs/workflow/m174-asymmetric-hosted-denominator-charter.md` |
| Commands | `uv run python tools/check_governance.py` |

## Resume prompt

```
Continue Brep2Code work: complete M175's asymmetric cohort and annex
qualification. Read this handoff and active workpack. First define a metadata-
only dossier schema for the 36 declared development candidates.
```
