# Handoff: M157 selector-ambiguity runtime projection

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M157-001-selector-ambiguity-runtime-projection`

## Goal

Derive and offline-evaluate the smallest safe runtime projection from the M142
selector-ambiguity admission record.

## Done

- User selected `WP-TRG-028` after M156 closure.
- M157 froze an experimental counterexample experience card as the candidate;
  reference pack, SDK, IR, retrieval, provider, and hosted paths are excluded.
- Added the selected `selector-cardinality-stop` experimental card, its index
  entry, and the hash-bound projection comparison record.
- Ran the fixed local ablation: no reference was rejected as
  `guidance_not_enabled`; a wrong explicit card returned
  `vertical-cylinder-construction`; the selected explicit card returned
  `selector-cardinality-stop`. No case asset was read; held-out access is
  `not_performed` and provider requests are zero.
- Passed focused pytest (14), Ruff, runtime-guidance audit, admission-record
  audit, admission-profile audit, governance audit, and diff check.

## In progress

- None. Liaol independently approved M157 on 2026-08-13.

## Next

- M157 is closed and archived. A future case-testing dossier or `WP-TRG-035`
  requires a separate explicit user selection.

## Decisions

- The candidate may state only `cardinality != 1 -> do not bind; stop` for the
  declared selector observation. It is experimental, absent by default, and
  does not change Harness or repair behavior.
- The fixed ablation has three deterministic local calls: no reference, wrong
  reference, and explicit reference. It uses only M142 development identities;
  held-out material remains documentary only and is not read or executed.
- M158 replaced the hard-coded selection with explicit hash-bound one-card
  bundles and bundle-local roles; the explicit-reference arm is now available.

## Blockers

- None. M158 independently closed the guidance-selection blocker.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M157-001-selector-ambiguity-runtime-projection.md` |
| Entry boundary | `docs/architecture/v1/runtime-and-hosted-entry-boundary-v1.md` |
| Admission record | `docs/corpus/knowledge/admissions/selector-ambiguity-v1.json` |
| Projection record | `docs/corpus/knowledge/runtime-projections/selector-cardinality-stop-v1.json` |
| Runtime cards | `runtime_resources/experience-cards/` |

## Resume prompt

```
M157 is closed. If a new workpack is explicitly selected, first read
`docs/workflow/status.md`; do not infer a case-testing, hosted, retrieval,
manifest, Harness, SDK, or IR authorization from M157.
```
