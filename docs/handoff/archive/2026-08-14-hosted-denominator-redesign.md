# Handoff: hosted denominator redesign

- **Date**: 2026-08-14
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M174-001-hosted-milestone-denominator-redesign`

## Goal

Replace M172's infeasible equal-card-strata plan with a no-card 30-case main
cohort and three-case card feasibility annex before M173 qualifies any row.

## Done

- M173 found the current three-role card boundary cannot support 20 distinct
  card rows; it is deferred.
- User selected the asymmetric redesign; ADR-0084 records its boundary.

## In progress

- M174 charter and metadata reconciliation are complete pending validation.

## Next

- Run M174 governance/diff validation, close the charter, then create a fresh
  active M173 qualification ledger under the asymmetric denominator.

## Decisions

- The two evidence products are unpooled and not a card-effect comparison.
- The annex retains one explicit hash-bound card and the existing closed-loop
  boundary only for its three direct roles. See ADR-0084.

## Blockers

- None currently. Stop if validation finds a scope drift, or if any selection,
  held-out access, runtime, provider, repair, or hosted change is required.

## Key paths

| Kind | Path |
|---|---|
| Files | `docs/workpacks/active/WP-M174-001-hosted-milestone-denominator-redesign.md` |
| Route | `docs/architecture/v1/current-project-route.md` |
| Commands | `uv run python tools/check_governance.py` |

## Resume prompt

```
Continue Brep2Code work: complete M174's asymmetric denominator redesign.
Read this handoff and active workpack. First reconcile the authoritative
registry versus M145 count using metadata only.
```
