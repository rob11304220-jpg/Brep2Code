# Handoff: Rounded-slot sequence-pair route

- **Date**: 2026-08-04
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Execute the frozen, offline `rounded-slot-v1` controlled-expansion workpack
without changing its selection, split, grammar boundary, or runtime scope.

## Done

- Added ADR-0020, requiring design/preregistration to precede controlled
  production for every future sequence-paired family.
- Completed M21-001: selected `rounded-slot-v1`, recorded its capability
  matrix, semantic anti-degeneration requirements, rejection taxonomy, and
  six-row preregistration.
- Completed M21-002: produced only the three preregistered
  `offset_rounded_slot` held-out assets, confirmed their hash stability, and
  audited all six rows. The new assets remain experimental and outside every
  registry, manifest, provider, training, and runtime path.

## In progress

- None. There is no active workpack.

## Next

1. Only if the user selects it, propose a separate M20/M21 cross-family
   governance review; do not promote assets by default.

## Decisions

- [ADR-0020](../../architecture/adr/0020-two-phase-cross-family-sequence-pair-expansion.md)
  establishes two-phase cross-family expansion discipline.
- `rounded-slot-v1` is a deterministic-oracle test of a second-profile,
  composite through-cut dependency; it is not native history or a general IR.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Design | `docs/architecture/v1/rounded-slot-sequence-pair-design.md` |
| Preregistration | `docs/corpus/sequence-paired/rounded-slot-v1-expansion.json` |
| Completed workpack | `docs/workpacks/done/WP-M21-002-rounded-slot-controlled-expansion.md` |
| Review | `docs/architecture/v1/m21-rounded-slot-controlled-expansion-review.md` |
| Governance | `docs/architecture/adr/0020-two-phase-cross-family-sequence-pair-expansion.md` |

## Resume prompt

```
Resume after completed M21-002. Read its review and workflow status before
proposing any next step. Do not promote the experimental rounded-slot assets
or alter manifests, provider, training, or runtime without a separately
selected governance review.
```
