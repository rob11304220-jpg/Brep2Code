---
type: design
related-project: Brep2Code
status: preregistered
---

# Rounded-Slot Sequence-Pair Design (`rounded-slot-v1`)

## Decision

`rounded-slot-v1` is the next bounded sequence-paired family.  It differs
structurally from `prismatic-hole-v1`: its subtractive feature depends on a
second, composite planar profile rather than on a single cylindrical cutter.
It is a local deterministic-oracle experiment, not native-history evidence or
a B-Rep-to-sequence benchmark.

## Capability matrix

| Dimension | `prismatic-hole-v1` (completed) | `rounded-slot-v1` (planned) |
|---|---|---|
| Feature profile | circular cutter | rectangle plus two circular caps |
| Dependency | base extrusion -> cylinder cut | base extrusion -> second profile -> through cut |
| Semantic risk | through/blind/bore depth lost | rounded slot replaced by rectangular cut or non-through pocket |
| Editable parameters | base, radius, depth | base, slot width, straight length, centre position |
| Held-out distinction | hole semantic family | offset profile placement family |
| Information gain | one subtractive primitive | profile dependency and composite-feature semantics |

## Frozen grammar and evidence

```text
SketchRect(base) -> ExtrudeBase(base) -> SketchRoundedSlot(base) -> CutThrough(base, slot)
```

Each case must pass all layers below:

1. deterministic replay against the committed bbox, volume, and topology
   baseline;
2. exact canonical operation, parameter, and dependency agreement with the
   deterministic-oracle sequence; and
3. preregistered editability mutations.

The semantic audit must additionally reject a non-through cut, a rectangular
replacement for the rounded slot, a cap radius other than half the declared
slot width, or a candidate that drops the second-profile dependency.  These
are feature-preservation predicates, not replacement geometry gates.

## Preregistered split

The exact six rows are recorded in
[`rounded-slot-v1-expansion.json`](../../corpus/sequence-paired/rounded-slot-v1-expansion.json)
before candidate production.

- Development: the existing `rounded_slot` low/nominal/high family.
- Held-out: three new `offset_rounded_slot` low/nominal/high candidates.

The held-out rows vary the profile placement as well as the dimensions, but
the two family IDs remain split-isolated.  No row may be replaced, moved, or
added after producer/audit results are known.

## Rejection and stability contract

Every rejected candidate must retain its preregistration ID, producer revision,
first failing layer, and one stable class: `catalog_violation`,
`parameter_invalid`, `producer_execution_failure`, `hash_nondeterminism`,
`geometry_replay_mismatch`, `sequence_mismatch`, `semantic_degeneration`,
`editability_mutation_failure`, or `split_family_leak`.

The production workpack must generate every new candidate twice in clean
output directories and require byte-identical committed STEP hashes.  It must
also exercise at least one negative semantic-degeneration fixture and one
split-leak fixture.  A failure is evidence for review; it does not authorize a
grammar change, a replacement case, or a relaxed predicate.

## Boundaries

Default execution remains offline and credential-free.  This design changes no
Harness behavior, CLI, gate, manifest, provider policy, runtime resource,
prompt, SDK, general IR, external dataset, or training input.

## Source rationale

The two-phase catalog/producer/gate separation is adapted from the local paper
vault note `Projects/Brep2Code-research/cases/q02/ataeiZerotoCADAgenticSynthesis2026-案例.md`.
Only the development-side audit discipline is adopted; its open-ended agentic
repair, automatic acceptance, scale, and training pipeline are excluded.
