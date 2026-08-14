# Handoff: M155 Runtime-and-Hosted Entry Boundary

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `done` (archived after G2 closure)
- **Related workpack**: `WP-M155-001-runtime-and-hosted-entry-boundary`

## Goal

Freeze the entry boundary that any later runtime-projection or
hypothesis-to-hosted-evaluation route must satisfy before it may be selected.

## Done

- M154 published the implementation-contract coverage layer and was
  independently approved on 2026-08-13.
- The user explicitly selected the route-recommended successor `WP-TRG-038`.

## In progress

- None. M155 is closed.

## Next

- No active workpack. Wait for explicit user selection of a bounded successor.
  `WP-TRG-028` and `WP-TRG-035` remain downstream and may not be
  auto-activated.

## Decisions

- M155 defines entry conditions only; it may not create any runtime artifact,
  provider-facing projection, authorization text, or hosted request.
- Later routes must freeze their own runtime-projection form, egress-safe
  reference projection, campaign scope, and authorization text rather than
  inheriting them by default from M155.
- Liaol approved the independent G2 review on 2026-08-13, so M155 may now be
  archived without selecting a successor.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M155-001-runtime-and-hosted-entry-boundary.md` |
| Trigger | `docs/workpacks/deferred/WP-TRG-038-runtime-and-hosted-entry-boundary.md` |
| Route | `docs/architecture/v1/post-m152-authority-and-contract-hardening-route.md` |
| Status | `docs/workflow/status.md` |

## Resume prompt

M155 is complete. Read `docs/workflow/status.md` and continue only with an
explicitly selected bounded successor. Reuse the M155 entry-boundary document
as a selection gate only.
