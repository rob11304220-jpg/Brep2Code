# Handoff: Selector-Ambiguity Controlled Production

- **Date**: 2026-08-07
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Complete M29-002's offline production and audit of the two frozen
selector-ambiguity candidate rows.

## Done

- M29-001 froze the pair and its negative controls.
- A candidate-only producer, family-specific auditor, and focused tests have
  been added; candidate assets have not yet been produced.

## In progress

- None.

## Next

- Select a new decision gap only through the updated decision index. The two
  M29 candidates remain experimental and cannot be promoted implicitly.

## Decisions

- A twin-boss cardinality of two is an expected `ambiguous` stop, not a
  geometry failure or a target to repair.
- The M29 review created `planar-face-selector-cardinality-v1` as a bounded
  development-side observable unit; it does not authorize runtime use.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M29-002-selector-ambiguity-controlled-production.md` |
| Producer | `tools/build_m29_selector_ambiguity_candidates.py` |
| Audit | `tools/audit_sequence_paired_selector_ambiguity.py` |
| Preregistration | `docs/corpus/sequence-paired/selector-ambiguity-v1-preregistration.json` |

## Resume prompt

```
Continue M29-002 selector-ambiguity controlled production. Read the active
workpack and preregistration. First action: run the focused tests and the
candidate producer; do not alter registry, manifest, provider, or runtime.
```
