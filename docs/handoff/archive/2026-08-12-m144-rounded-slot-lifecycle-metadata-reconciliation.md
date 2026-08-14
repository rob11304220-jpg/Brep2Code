# Handoff: M144 Rounded-Slot Lifecycle Metadata Reconciliation

- **Date**: 2026-08-12
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M144-001-rounded-slot-lifecycle-metadata-reconciliation`

## Goal

Reconcile only the case metadata lifecycle of the three ADR-0023-promoted
offset-rounded-slot cases, without inspecting or executing their fixtures.

## Done

- M143 metadata-only inventory found the active-registry versus `case.json`
  lifecycle conflict and recorded its exact scope.
- User selected M144 to resolve that metadata-only dependency before M143
  resumes.

## In progress

- Verify the ADR-0023 promotion evidence and align only the three case records'
  lifecycle/reference-script declarations with it.

## Next

- Add a deterministic metadata audit, run split-safe checks, and obtain Liaol's
  independent G2 review; then restore M143 from blocked to active.

## Decisions

- Do not read, hash, replay, or execute the held-out STEP fixtures.
- Do not change any split, geometry, parameters, baselines, sequences,
  reference-script contents, registry row, card, manifest, or runtime/provider
  boundary.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M144-001-rounded-slot-lifecycle-metadata-reconciliation.md` |
| Promotion authority | `docs/architecture/adr/0023-rounded-slot-sequence-pair-governance.md` |
| Conflict report | `docs/architecture/v1/m143-case-library-inventory-conflict.md` |
| M143 blocked workpack | `docs/workpacks/archive/WP-M143-001-case-library-stratification-and-admission-profiles.md` |

## Resume prompt

```
Continue M144: reconcile only lifecycle/reference-script metadata of the three
ADR-0023-promoted offset-rounded-slot case records. Do not open STEP fixtures
or change any split, baseline, sequence, manifest, or runtime/provider path.
```
