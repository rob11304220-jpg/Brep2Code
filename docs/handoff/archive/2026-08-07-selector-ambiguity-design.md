# Handoff: Selector-Ambiguity Pair Design

- **Date**: 2026-08-07
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Complete M29-001's design-only preregistration of a Q01 predicate-selector
ambiguity pair.

## Done

- ADR-0037 and the selector-ambiguity-v1 preregistration freeze the unchanged
  predicate, two planned twin-boss rows, and fail-closed negative controls.
- The generic intake audit passed.

## In progress

- None.

## Next

- M29-002 may be selected separately for controlled production; it remains
  backlog and must not be inferred from the completed design.

## Decisions

- The selector predicate remains planar +Z at maximum output Z; only candidate
  cardinality changes between the fixed unique oracle and twin-boss controls.
- Cardinality two stops before any dependent sketch or cut. Coordinate and
  enumeration tie-breakers are negative controls, not alternatives.

## Blockers

- None. Production is intentionally not selected.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M29-001-selector-ambiguity-design.md` |
| Preregistration | `docs/corpus/sequence-paired/selector-ambiguity-v1-preregistration.json` |
| Decision | `docs/corpus/knowledge/decisions/q01-selector-ambiguity-v1/decision.json` |
| ADR | `docs/architecture/adr/0037-selector-ambiguity-pair-preregistration.md` |

## Resume prompt

```
Continue M29-001 selector-ambiguity design. Read ADR-0037, the active
workpack, and the preregistration. First action: validate its intake contract
and JSON; do not produce candidate assets or modify runtime behavior.
```
