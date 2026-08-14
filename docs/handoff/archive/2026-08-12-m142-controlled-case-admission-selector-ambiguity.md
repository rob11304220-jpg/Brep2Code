# Handoff: M142 Controlled Case Admission — Selector-Ambiguity Pilot

- **Date**: 2026-08-12
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M142-001-controlled-case-admission-selector-ambiguity`

## Goal

Define and locally audit an immutable admission record using the existing
planar-face selector unique-versus-ambiguous evidence set, without creating a
runtime projection, expanding the case library or executing held-out input.

## Done

- M141 is complete and independently reviewed.
- User selected the selector-ambiguity pilot for TRG-027: existing unique
  `face-selected-dependent-cut-v1` oracle, twin-boss development discriminating
  evidence and its reviewed held-out counterpart, plus fixed negative controls.
- Published admission-record v1 contract, schema, selector pilot record and
  offline auditor. The audit binds five source hashes, validates two
  development-side case roles, and reports `held_out_access=not_performed`.
- Focused admission tests (2), split-safe full test selection (264), Ruff,
  governance audit, and `git diff --check` passed. The complete suite excludes
  only `test_m29_selector_ambiguity.py`, because it reconstructs the frozen
  held-out candidate and is prohibited in M142.

## In progress

- Obtain Liaol's independent G2 review of the immutable admission record,
  source hashes, held-out isolation, and validation evidence. Keep the record
  as evidence source only.

## Next

- Independent reviewer: audit the published contract, pilot record and source
  hashes; confirm held-out access was not performed; then accept or reject M142.

## Decisions

- The twin-boss held-out row is not to be newly inspected or executed. Its prior
  reviewed, hash-pinned audit evidence may be linked as split-isolation proof.
- A selector ambiguity is a terminal stop under M141, not a source-repair or
  implicit sequence/IR route.
- After this admission record receives independent review, the user may select
  `WP-TRG-029` to classify the existing development-side evidence into
  admission profiles. Only after that profile crosswalk receives independent
  review may the user select `WP-TRG-028` to derive one card, pack, SDK/IR
  fragment, or retrieval projection.
- ADR-0071 records the added stratification gate. It changes neither M142's
  frozen pilot nor any runtime, provider, manifest, or held-out boundary.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M142-001-controlled-case-admission-selector-ambiguity.md` |
| Decision | `docs/corpus/knowledge/decisions/q01-selector-ambiguity-v1/decision.json` |
| Preregistration | `docs/corpus/sequence-paired/selector-ambiguity-v1-preregistration.json` |
| Production review | `docs/architecture/v1/m29-selector-ambiguity-controlled-production-review.md` |
| M141 policy | `docs/architecture/v1/contracts/classified-repair-policy.md` |
| Admission contract | `docs/architecture/v1/contracts/admission-record-v1.md` |
| Pilot record | `docs/corpus/knowledge/admissions/selector-ambiguity-v1.json` |
| Auditor | `tools/audit_admission_record.py` |
| ADR | `docs/architecture/adr/0072-immutable-admission-record-evidence-boundary.md` |
| Added route decision | `docs/architecture/adr/0071-admission-profile-stratification-before-projection.md` |
| Deferred stratification workpack | `docs/workpacks/deferred/WP-TRG-029-case-library-stratification-and-admission-profiles.md` |

## Resume prompt

```
Continue Brep2Code work: independently review M142's selector-ambiguity
admission record.
Read docs/handoff/active/2026-08-12-m142-controlled-case-admission-selector-ambiguity.md.
First action: run `uv run python tools/audit_admission_record.py`, inspect the
hash-bound documentary evidence, and verify that held-out access remains
`not_performed` without reading or running the held-out candidate anew.
```
