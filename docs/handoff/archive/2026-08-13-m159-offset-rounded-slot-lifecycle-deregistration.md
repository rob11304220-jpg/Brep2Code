# Handoff: M159 offset rounded-slot lifecycle deregistration

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `done` (archived after G2 closure)
- **Related workpack**: `WP-M159-001-offset-rounded-slot-lifecycle-deregistration`

## Goal

Align the active registry to the authoritative experimental lifecycle state of
three offset-rounded-slot case metadata records without accessing assets.

## Done

- User selected the lifecycle-reconciliation workpack required by M158.
- The three dirty `case.json` inputs were read only; they explicitly downgrade
  the rows to experimental and remove reference-script availability.

## In progress

- None. M159 is closed.

## Next

- M158 may resume its full-suite validation now that admission-profile
  consistency is restored. Do not resume M157 until M158 is independently
  approved.

## Decisions

- `case.json` is the lifecycle authority. M159 preserves the user's downgraded
  metadata and deregisters the registry pointers rather than restoring active
  status or reference-script declarations.
- No fixture or script may be opened; M159 operates only on registry and JSON
  metadata.
- Owner validation passed: 4 focused tests, both metadata-only audits, focused
  Ruff, governance audit, and `git diff --check` (only LF/CRLF warnings).
- Liaol approved the independent G2 review on 2026-08-13, allowing M159 to
  close and M158 to resume without lifecycle re-promotion.

## Blockers

- None. Stop if completing this alignment requires changing the frozen case
  metadata or any non-lifecycle surface.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M159-001-offset-rounded-slot-lifecycle-deregistration.md` |
| Registry | `docs/corpus/registry/self-authored.json` |
| Profile | `docs/corpus/knowledge/admissions/case-library-admission-profile-v1.json` |
| Blocked chain | `docs/workpacks/archive/WP-M158-001-guidance-bundle-explicit-selection-blocked.md` |

## Resume prompt

```
Continue Brep2Code M159: deregister only the three offset-rounded-slot rows
whose case metadata is experimental. Preserve the user changes; do not read
fixtures/scripts or change runtime/provider/hosted surfaces.
```
