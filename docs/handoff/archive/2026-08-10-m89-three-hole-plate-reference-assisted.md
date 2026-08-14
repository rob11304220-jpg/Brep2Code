# Handoff: M89 Three-hole-plate Reference-assisted Hosted Smoke

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M89-001-reference-assisted-p1-three-hole-plate-hosted-smoke`

## Goal

Implement and offline-validate a fixed `three_hole_plate` reference-assisted
two-request CLI path, then complete read-only hosted preflight. Do not invoke
a provider before explicit authorization of the exact M89 bounds.

## Done

- M86 fake-provider admission covers the `repeated boolean-cut tool` role of
  the frozen vertical-cylinder card.
- M88 froze M89 as the next evidence-ready case.

## In progress

- None. M89's one authorized execution is terminal `interrupted` after a
  request-specific provider timeout; Liaol independently approved its
  no-retry closure.

## Next

- Wait for the user to choose a new bounded package. Do not retry or create
  another hosted run from this checkpoint.

## Decisions

- M89 tests only the existing repeated-cut role/card; it cannot broaden
  retrieval or produce a new card.
- A failed or timed-out M89 request is terminal and cannot activate M90.

## Blockers

- M89's hosted budget is exhausted and the terminal report cannot be resumed.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M89-001-reference-assisted-p1-three-hole-plate-hosted-smoke.md` |
| CLI | `brep2code/cli/__init__.py` |
| Test | `tests/test_observed_build_loop.py` |
| Planned report | `data/corpus-runs/m89-three-hole-plate-reference-assisted.json` |
| Planned monitor | `data/monitor-runs/m89-three-hole-plate-reference-assisted.monitor.json` |

## Resume prompt

```
Continue Brep2Code after M89's closed three-hole-plate reference-assisted smoke.
Read docs/handoff/active/2026-08-10-m89-three-hole-plate-reference-assisted.md.
First action: read docs/workflow/status.md and wait for the user to select a
new bounded workpack; do not retry or issue another provider request.
```
