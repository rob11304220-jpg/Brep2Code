# Handoff: M36 Status and Evidence Ledger

- **Date**: 2026-08-07
- **Subproject**: `brep2code`
- **Status**: `done`

## Goal

Turn the workflow status page into a compact current-state dashboard and retain
historical and deferred-decision context through dedicated indexes.

## Done

- M35 established a local/CI governance audit baseline.

## In progress

- M36 is relocating duplicated historical status text and adding a structured
  evidence ledger without changing research decisions.

## Next

- Validate links and lifecycle invariants, then archive this handoff and
  complete the workpack.

## Decisions

- Pending ADR-0040: use `status.md` for current state only and a JSON ledger
  for machine-checkable deferred-decision evidence.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M36-001-status-and-evidence-ledger.md` |
| Status | `docs/workflow/status.md` |
| Ledger | `docs/workflow/evidence-ledger.json` |

## Resume prompt

```
Continue Brep2Code M36-001 status and evidence ledger work.
Read docs/handoff/active/2026-08-07-m36-status-and-evidence-ledger.md.
First action: validate the compact status page and JSON ledger with the governance audit.
```
