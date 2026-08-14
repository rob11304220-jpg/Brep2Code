# Handoff: M21-004 complete and M22 coverage route

- **Date**: 2026-08-05
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Complete the selected M22-000 development-side modeling knowledge foundation
before any multi-contour, dependency, or external sequence-supervised work.

## Done

- M21-004 completed offline. ADR-0023 scopes the six-record `rounded-slot-v1`
  metadata contract and promotes the three `offset_rounded_slot` assets to
  active self-authored cases, without manifest/provider/runtime admission.
- Focused tests (7), the 45-record replay audit, the six-record family audit,
  Ruff, and `git diff --check` passed.
- ADR-0021/0022 record the order: governance closure, modeling-knowledge
  foundation, self-authored multi-contour pocket evidence, dependency evidence,
  then constrained external routes.
- The user selected M22-000 on 2026-08-05. It is complete; M22-001 remains
  unselected and is now eligible for separate user selection.
- M22-000 completed offline: the six-cell coverage matrix is source-linked,
  and three bounded knowledge units preserve the self-authored-family and
  Fusion/ABC evidence boundaries without creating a runtime projection.

## In progress

- No active workpack. M22-001 is the next eligible, separately selected route.

## Next

1. Await explicit selection of M22-001.
2. If selected, use the coverage matrix to state the outer-plus-inner-loop
   hypothesis, counterexample, and stopping rule before candidate production.

## Decisions

- ADR-0023 is accepted; it does not authorize executable-manifest, hosted, or
  runtime use for `rounded-slot-v1`.
- ADR-0021 is accepted; it does not authorize external download, hosted use,
  or runtime changes.
- ADR-0022 establishes development-side modeling knowledge; it does not expose
  broad documents or unreviewed claims to runtime LLMs.
- M21-004 remains limited to family-specific case-library governance.

## Blockers

- M22-001 requires separate user selection; it must not produce assets during
  design.

## Key paths

| Kind | Path |
|---|---|
| Completed M21 workpack | `docs/workpacks/done/WP-M21-004-rounded-slot-governance-promotion.md` |
| Coverage route | `docs/architecture/adr/0021-evidence-sequenced-case-coverage-expansion.md` |
| Completed knowledge foundation | `docs/workpacks/done/WP-M22-000-modeling-knowledge-system-foundation.md` |
| M22 planning | `docs/workpacks/backlog/WP-M22-001-multi-contour-pocket-design.md` |
| Status | `docs/workflow/status.md` |

## Resume prompt

```
Await explicit selection of M22-001. Read this handoff, the M22-000 completed
workpack, ADR-0022, and docs/corpus/knowledge/coverage-matrix.json. If
selected, design only; do not create assets, change manifests, or start
M22-002.
```
