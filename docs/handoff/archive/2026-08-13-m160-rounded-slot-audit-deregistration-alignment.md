# Handoff: M160 rounded-slot audit deregistration alignment

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `done` (archived after G2 closure)
- **Related workpack**: `WP-M160-001-rounded-slot-audit-deregistration-alignment`

## Goal

Make the M21 metadata audit respect M159's lifecycle authority without
changing any case or registry data.

## Done

- M158 resumed full suite reached 282 passing tests; the only failure is the
  M21 audit requiring deregistered experimental rows to remain active.

## In progress

- None. M160 is closed.

## Next

- M158 may resume independent review using M160's full-suite evidence. Do not
  resume M157 until M158 is independently approved.

## Decisions

- The exact three M159 rows are valid historical experimental expansion
  evidence, not active registry members. Other M21 expansion drift remains
  fail closed.
- M160 must not read fixtures or scripts or change data/manifest/runtime scope.
- Owner validation passed: 10 focused tests, both metadata-only audits, focused
  Ruff, governance audit, and the full suite (`284 passed in 502.06s`).
- Liaol approved the independent G2 review on 2026-08-13, allowing M160 to
  close without any data or authority widening.

## Blockers

- None. Stop if a solution requires changing case metadata, registry, or any
  non-audit surface.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M160-001-rounded-slot-audit-deregistration-alignment.md` |
| Audit | `tools/audit_case_library.py` |
| Focused test | `tests/test_case_library_m12.py` |
| Lifecycle authority | `docs/architecture/adr/0076-offset-rounded-slot-lifecycle-deregistration.md` |

## Resume prompt

```
Continue Brep2Code M160: align the M21 metadata audit with M159's three-row
deregistration only. Do not change cases, registry, assets, manifests, runtime,
provider, or hosted behavior.
```
