# Handoff: M22-001 multi-contour pocket design complete

- **Date**: 2026-08-05
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Preserve the frozen, evidence-seeking `multi-contour-pocket-v1` design as the
only possible input to a separately selected M22-002 production workpack.

## Done

- M22-001 completed offline. Six rows are preregistered: three centered
  development variants and three offset held-out variants, with family-isolated
  splits.
- The canonical deterministic-oracle sequence is `SketchRect -> ExtrudeBase
  -> SketchPocketLoops(outer, inner) -> CutPocket(blind)`.
- The design freezes parameter preconditions, editability mutations, semantic
  invariants (outer rim, inner island, blind annular floor), negative controls,
  rejection taxonomy, and two-clean-output producer stability requirement.
- The knowledge-unit template and existing two operation units now carry an
  evidence-bounded `operation_contract`; it does not assert an unverified
  kernel/API signature or tolerance.
- JSON structure and split-isolation validation passed. No asset, producer,
  manifest, provider, runtime, parser, helper, SDK, or IR changed.

## In progress

- No active workpack.

## Next

1. Await explicit selection of M22-002.
2. If selected, generate only the frozen six rows, audit the listed contract
   invariants, and retain every rejection without replacement or grammar change.

## Decisions

- M22-001 resolves the capability shorthand into a four-operation executable
  sequence so the multi-loop pocket follows a concrete base-solid prefix.
- The design is evidence-seeking only; it does not create a reviewed knowledge
  unit or runtime experience card. See [ADR-0020](../../architecture/adr/0020-two-phase-cross-family-sequence-pair-expansion.md) and [ADR-0022](../../architecture/adr/0022-modeling-knowledge-system.md).

## Blockers

- M22-002 requires separate user selection.

## Key paths

| Kind | Path |
|---|---|
| Completed workpack | `docs/workpacks/done/WP-M22-001-multi-contour-pocket-design.md` |
| Design | `docs/architecture/v1/multi-contour-pocket-sequence-pair-design.md` |
| Frozen rows | `docs/corpus/sequence-paired/multi-contour-pocket-v1-preregistration.json` |
| Next workpack | `docs/workpacks/backlog/WP-M22-002-multi-contour-pocket-controlled-production.md` |

## Resume prompt

```
Await explicit selection of M22-002. Read this handoff, the completed M22-001
workpack, the multi-contour design, and its preregistration JSON. Generate no
row outside the frozen record and do not alter manifest/provider/runtime paths.
```
