---
type: design
related-project: Brep2Code
status: preregistered
---

# Multi-Contour Pocket Sequence-Pair Design (`multi-contour-pocket-v1`)

## Decision

`multi-contour-pocket-v1` is the third bounded self-authored sequence-paired
family. It tests a blind pocket defined by an outer and a contained inner
closed loop. The two loops deliberately remove only their annular region:
the output must retain both an outer rim and an inner island.

The M22 shorthand `Sketch(outer + inner loop) -> ExtrudeBase -> CutPocket`
describes the target capability. The executable deterministic-oracle sequence
is necessarily four operations, because a solid base is needed before the
multi-contour pocket sketch can target it:

```text
SketchRect(base) -> ExtrudeBase(base) -> SketchPocketLoops(outer, inner) -> CutPocket(base, blind)
```

This is local deterministic-oracle evidence only. It is not native-history
evidence, generic loop recognition, or B-Rep-to-sequence recovery.

## Target coverage cells and hypothesis

| Matrix cell | Existing gap | Hypothesis | Counterexample / stopping rule |
|---|---|---|---|
| `sketch_topology` | no outer-plus-inner loops | Two closed, coplanar, nested rectangular loops can retain their containment and opposite role in a frozen deterministic sequence. | Stop if either loop is lost, intersecting, non-contained, or replaced by a single-loop profile. |
| `feature_semantics` | no inner-profile pocket | A blind cut of the annular profile preserves a rim, an inner island, and a pocket floor. | Stop if the cut is through, removes the island, removes the rim, or collapses to a single rectangular cut. |
| `sequence_dependency` | only base-to-cut / profile-to-cut evidence | The pocket sketch has an explicit dependency on the base and both loops are required inputs to the cut. | Stop if the canonical prefix/dependencies cannot be retained, or if a different sequence is needed for a passing result. |

## Frozen operation-contract draft

This draft describes the evidence M22-002 must seek; it is not a confirmed
knowledge unit and does not claim an OpenCascade API signature.

| Field | Frozen contract |
|---|---|
| Function family | `SketchRect`, `ExtrudeBase`, `SketchPocketLoops`, blind `CutPocket` |
| Base parameters | `base_length_x`, `base_length_y`, `base_height`; each positive |
| Loop parameters | outer/inner center, length and width; both closed, coplanar, axis-aligned rectangles |
| Preconditions | inner loop strictly contained in outer loop; outer loop strictly contained in the top face; all clearances positive; `0 < pocket_depth < base_height` |
| Expected B-Rep delta | one solid retains an outer rim and central island while a blind annular recess adds outer/inner pocket walls and a floor |
| Topology invariants | both loop roles survive; no through cut; no loop intersection; no disconnected solids; canonical cut consumes the base and both-loop sketch |
| Numeric boundary | all dimensions are explicit millimetre values in the preregistration; no general tolerance claim is made |
| Unverified properties | arcs/splines, multiple inner loops, non-axis-aligned loops, face/edge references, alternate sequences, general B-Rep inference |

## Capability comparison

| Dimension | `prismatic-hole-v1` | `rounded-slot-v1` | `multi-contour-pocket-v1` |
|---|---|---|---|
| Cut profile | circular primitive | composite single closed loop | two nested closed loops |
| Base dependency | base to cylinder cut | base plus second profile | base plus two-loop profile |
| Required semantic preservation | cut variant/depth | rounded-slot caps and throughness | outer rim, inner island, and blind annular floor |
| Held-out distinction | blind-hole family | offset rounded-slot family | offset nested-loop placement family |
| Information gain | single-cut variants | composite-profile dependency | multi-contour topology and inner-profile pocket |

## Frozen selection and split

The exact six rows are recorded in
[`multi-contour-pocket-v1-preregistration.json`](../../corpus/sequence-paired/multi-contour-pocket-v1-preregistration.json).

- Development: three `multi_contour_pocket_centered` low/nominal/high rows.
- Held-out: three `multi_contour_pocket_offset` low/nominal/high rows.

No case asset exists at design time. M22-002 may produce only these rows; no
row may be substituted, moved, or added after the producer/audit results are
known.

## Rejection and stability contract

Every M22-002 rejection retains its preregistration ID, producer revision,
first failing layer, and one stable class: `catalog_violation`,
`parameter_invalid`, `loop_containment_violation`,
`producer_execution_failure`, `hash_nondeterminism`,
`geometry_replay_mismatch`, `sequence_mismatch`,
`topology_invariant_failure`, `semantic_degeneration`,
`editability_mutation_failure`, or `split_family_leak`.

The producer must generate every candidate twice into clean directories and
require byte-identical committed STEP hashes. M22-002 must exercise a
single-loop degeneration control, a through-cut control, an inner-island-loss
control, and a split-leak control. A failure is evidence for review; it does
not authorize grammar expansion or replacement cases.

## Boundaries

This preregistration changes no asset, manifest, runtime resource, prompt,
Harness behavior, provider route, external-data boundary, training input,
parser, helper, SDK, or IR.
