# Handoff: M80 revalidation preflight

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M80-001-minimal-p0-end-to-end-revalidation`

## Goal

Complete a fresh G3 preflight using M81's monitorable checkpoint lifecycle;
then wait for a new itemized authorization before any provider request.

## Done

- M81 is closed after Liaol's independent review. It supplies producer-owned
  prepare/execute checkpoints while preserving M70 report-read-only behavior.
- M80 is reactivated for a new local preflight; no prior report, budget or
  authorization is eligible for reuse.

## In progress

- M80-v2 completed under Liaol's explicit authorization. Control passed. Box
  received a response but its generated script imported unavailable `cadquery`,
  so `wsl-bwrap` execution and output gates failed. Both capacities are used.

## Next

- Run the remaining offline closure checks and obtain Liaol's independent G3
  review. Do not retry, repair, change the profile, or start M73.

## Decisions

- Use new M80-v2 report and monitor paths. Control prepare/monitor/execute must
  complete before box prepare/monitor/execute can begin.

## Blockers

- M80 is terminally stopped by the generated-script execution failure. Liaol
  must independently review its bounded no-retry disposition before closure.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M80-001-minimal-p0-end-to-end-revalidation.md` |
| M81 | `docs/workpacks/done/WP-M81-001-monitorable-single-request-checkpoints.md` |
| Profile | `docs/workflow/m79-historical-contract-drift-diagnosis.md` |

## Resume prompt

```
Continue Brep2Code M80 revalidation preflight. Read this handoff, the active
M80 workpack and M79 profile. Complete only local checks; do not contact a
provider without a new itemized user authorization.
```
