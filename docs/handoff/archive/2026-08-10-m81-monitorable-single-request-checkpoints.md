# Handoff: M81 monitorable single-request checkpoints

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M81-001-monitorable-single-request-checkpoints`

## Goal

Repair the local report lifecycle that blocked M80: single-request producers
must write a monitorable `running` report before any request, while M70 stays
strictly read-only for reports.

## Done

- M80 preflight documented the producer/monitor lifecycle mismatch; no hosted
  request was issued.
- Liaol selected the narrow offline G2 M81 fix.

## In progress

- Add prepare/execute lifecycle transitions and deterministic offline tests
  for `provider-control` and `observed-first-pass`.

## Next

- M81 acceptance is complete: focused lifecycle tests (22 passed), full Ruff,
  governance audit and patch-format check passed. Obtain Liaol's independent
  review, then re-enter M80 with a fresh preflight. Do not make a provider
  request.

## Decisions

- The producer, not M70, creates and transitions corpus reports. M70 only
  reads the report and writes its separate monitor state.

## Blockers

- M80 remains blocked until M81 closes and a fresh M80 preflight passes.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M81-001-monitorable-single-request-checkpoints.md` |
| CLI | `brep2code/cli/__init__.py` |
| Monitor tests | `tests/test_durable_monitor.py` |

## Resume prompt

```
Continue Brep2Code M81 monitorable single-request checkpoints.
Read the M81 active workpack and this handoff. Implement only the offline
prepare/execute report lifecycle and tests; do not contact a provider.
```
