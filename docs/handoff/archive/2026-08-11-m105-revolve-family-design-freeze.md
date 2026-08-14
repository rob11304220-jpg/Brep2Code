# Handoff: M105 Revolve Family Design Freeze

- **Date**: 2026-08-11
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M105-001-revolve-family-design-freeze`

## Goal

Freeze one bounded `revolve-v1` axisymmetric grammar, its Q01 facts, split,
oracle, gates and counterexamples before any candidate asset is produced.

## Done

- M104-001 case-card completion was accepted, closed and archived.
- User selected the former `WP-TRG-012`; it was active as M105-001.
- Created `revolve-v1-preregistration.json` and ADR-0063; no candidate asset,
  manifest, provider input or runtime resource was created.
- Owner acceptance passed: generic intake audit, fast tests (66 passed), Ruff,
  governance audit and `git diff --check`.
- Liaol completed independent G2 review and approved closure on 2026-08-11.

## In progress

- None.

## Next

- Await an explicit user selection before activating any next workpack.
  `WP-TRG-013` is the separately selected future controlled-production route
  for the frozen `revolve-v1` rows.

## Decisions

- ADR-0063 fixes the +Z sense as a deterministic API convention, not a Q01
  observable claim, because reversed axes are B-Rep-equivalent at 360 degrees.
- Candidate production remains offline-only and separately selected; no
  provider or hosted authority is granted.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/done/WP-M105-001-revolve-family-design-freeze.md` |
| Freeze | `docs/corpus/sequence-paired/revolve-v1-preregistration.json` |
| ADR | `docs/architecture/adr/0063-revolve-v1-design-freeze.md` |
| Future route | `docs/workpacks/deferred/WP-TRG-013-revolve-family-controlled-production.md` |

## Resume prompt

```
Continue Brep2Code after completed M105-001 revolve-family design freeze.
Read docs/workflow/status.md and this archived handoff for historical context.
First action: await an explicit user-selected bounded workpack; do not produce revolve candidates or call a provider without that selection.
```
