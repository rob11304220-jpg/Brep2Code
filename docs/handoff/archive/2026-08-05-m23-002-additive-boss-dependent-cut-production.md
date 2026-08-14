# Handoff: M23-002 additive-boss dependent-cut production complete

- **Date**: 2026-08-05
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Preserve the six `additive-boss-dependent-cut-v1` experimental candidates and
their offline evidence pending a separately selected successor.

## Done

- Generated exactly three centered development and three offset held-out rows.
- Verified clean-directory normalized STEP hash stability for all six.
- Passed geometry, exact dependency sequence, four editability mutations,
  semantic invariants, split isolation, 5 focused tests, and family audit 6/6.
- Kept all candidates experimental and outside registry, manifests, provider,
  training, and runtime paths.

## In progress

- No active workpack.

## Next

Await user selection of a bounded M23 successor. Do not promote candidates or
alter any runtime path without a separate review and decision.

## Decisions

- M23-002 proves only a self-authored deterministic oracle for the frozen
  base-to-boss-to-blind-cut grammar; see [ADR-0025](../../architecture/adr/0025-additive-boss-dependent-cut-design.md).

## Blockers

- Any successor requires separate user selection.

## Key paths

| Kind | Path |
|---|---|
| Completed workpack | `docs/workpacks/done/WP-M23-002-additive-boss-dependent-cut-controlled-production.md` |
| Review | `docs/architecture/v1/m23-additive-boss-dependent-cut-controlled-production-review.md` |
| Producer | `tools/build_m23_additive_boss_dependent_cut_candidates.py` |
| Audit | `tools/audit_sequence_paired_additive_boss_dependent_cut.py` |

## Resume prompt

```
Read this handoff, ADR-0025, the frozen preregistration, and the M23-002
review. Do not promote the experimental candidates, change manifests, or
start a successor without explicit user selection.
```
