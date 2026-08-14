# Handoff: M23-004 additive-boss dependent-cut promotion

- **Date**: 2026-08-05
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Promote only the six audited M23 candidates into restricted active case-library
governance under ADR-0027.

## Done

- M23-003 confirmed the family is supported but not face-selection evidence.
- User selected the separate M23-004 promotion.
- ADR-0027, active metadata, reference scripts, case cards, registry pointers,
  and family-scoped replay coverage are complete.

## In progress

- No active workpack.

## Next

- Await user selection of the `face-selected-dependent-cut-v1` design or
  another priority-route item; do not select it automatically.

## Decisions

- Promotion is governed only by [ADR-0027](../../architecture/adr/0027-additive-boss-dependent-cut-governance.md).

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M23-004-additive-boss-dependent-cut-governance-promotion.md` |
| ADR | `docs/architecture/adr/0027-additive-boss-dependent-cut-governance.md` |
| Family audit | `tools/audit_sequence_paired_additive_boss_dependent_cut.py` |

## Resume prompt

```
Complete M23-004 only. Promote and audit the frozen six M23 records without
starting the face-selected successor or changing runtime paths.
```
