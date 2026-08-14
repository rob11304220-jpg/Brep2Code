# Handoff: Legacy Evidence and Decision Reconciliation

- **Date**: 2026-08-06
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Complete M28-001's documentation-only migration of legacy evidence into the
Harness-oriented Q01--Q04 decision base.

## Done

- ADR-0036, the evidence-disposition index, the M10 fixed-script execution
  boundary, and missing Q01/Q03/Q04 decision packages have been added.

## In progress

- None.

## Next

- If selected, create a design-only workpack for the planned multi-candidate
  selector control. It is not yet authorized to produce assets.

## Decisions

- ADR-0036 requires each legacy evidence family to have one explicit
  development-side disposition.
- `q03-local-geometry-feedback-v1` is deferred: its package cannot override
  WP-M10-002's unmet trigger.

## Blockers

- None. New case production remains a separately selected task.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M28-001-legacy-evidence-decision-reconciliation.md` |
| Disposition index | `docs/corpus/knowledge/evidence-disposition.json` |
| Decision index | `docs/corpus/knowledge/decisions/index.json` |
| ADR | `docs/architecture/adr/0036-legacy-evidence-disposition-and-decision-index.md` |

## Resume prompt

```
Continue M28-001 legacy-evidence reconciliation. Read ADR-0036, the active
workpack, evidence-disposition.json, and status.md. First action: validate
JSON and document links; do not select or produce a new case family.
```
