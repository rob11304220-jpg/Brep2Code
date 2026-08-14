# Handoff: M143 Case-Library Stratification and Admission Profiles

- **Date**: 2026-08-12
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M143-001-case-library-stratification-and-admission-profiles`

## Goal

Create a development-side `admission-profile-v1` from existing tracked case
metadata and reviewed evidence. It must make mechanism-specific evidence and
fail-closed requirements auditable without admitting cases or creating runtime
knowledge.

## Done

- M142 was independently reviewed and closed; its selector-ambiguity admission
  record is hash-bound and records held-out access as not performed.
- User selected TRG-029 and activated M143 with Liaol as independent reviewer.
- Published a draft `admission-profile-v1`, metadata-only inventory/audit, and
  focused tests. Inventory reads no STEP or reference script.
- The inventory found a reproducible lifecycle conflict: three active-registry
  `param_offset_rounded_slot_*` held-out rows have authoritative `case.json`
  status `experimental`; see `docs/architecture/v1/m143-case-library-inventory-conflict.md`.

## In progress

- Await a separately selected bounded metadata-reconciliation workpack. M143
  must not alter case metadata or inspect the held-out fixtures to resolve the
  conflict.

## Next

- After reconciliation, rerun `uv run python tools/audit_admission_profile.py`
  and finish the profile classification/review without fixture access.

## Decisions

- Classification is not a subjective difficulty rank and cannot change a case
  lifecycle, admission status, or runtime eligibility.
- Held-out evidence remains documentary/hash-pinned only; do not inspect or
  execute a held-out fixture.
- M143 may recommend at most three future decision gaps but cannot select one.

## Blockers

- Authoritative lifecycle metadata conflict documented above; no in-scope fix.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M143-001-case-library-stratification-and-admission-profiles.md` |
| M142 record | `docs/corpus/knowledge/admissions/selector-ambiguity-v1.json` |
| Library index | `docs/corpus/library/catalog.json` |
| Coverage matrix | `docs/corpus/knowledge/coverage-matrix.json` |
| Route ADR | `docs/architecture/adr/0071-admission-profile-stratification-before-projection.md` |
| Conflict report | `docs/architecture/v1/m143-case-library-inventory-conflict.md` |
| Inventory/audit | `tools/audit_admission_profile.py` |

## Resume prompt

```
Continue Brep2Code M143 only after a separately selected bounded reconciliation
has resolved the documented registry/case.json lifecycle conflict. Then rerun
the metadata-only admission-profile audit; do not read or execute held-out
fixtures, create cases, change a manifest, or create runtime knowledge.
```
