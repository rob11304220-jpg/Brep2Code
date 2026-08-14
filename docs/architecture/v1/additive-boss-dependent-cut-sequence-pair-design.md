---
type: design
related-project: Brep2Code
status: preregistered
---

# Additive-Boss-Dependent-Cut Sequence-Pair Design (`additive-boss-dependent-cut-v1`)

## Decision

This fourth bounded self-authored sequence-paired family tests an explicit
additive boss followed by a blind cylindrical cut whose sketch is supported by
the boss top face. Its sole deterministic-oracle sequence is:

```text
SketchRect(base) → ExtrudeBase → SketchRect(boss) → ExtrudeBoss(join)
→ SketchCircle(cut on boss.top_face) → CutCylinder(boss, blind)
```

It is local deterministic-oracle evidence only. It is not native history,
face/edge-reference support, generic feature recognition, or B-Rep-to-sequence
recovery.

## Target coverage cells and hypothesis

| Matrix cell | Existing gap | Hypothesis | Counterexample / stopping rule |
|---|---|---|---|
| `feature_semantics` | no additive feature followed by a dependent cut | A rectangular boss can join the base before a blind cylindrical cut removes only material from that boss. | Stop if the boss is absent/disconnected, the cut removes base material, or the cut becomes through. |
| `sequence_dependency` | no multi-feature prefix ending in a downstream feature target | The cut sketch can explicitly depend on `boss.top_face`, and the cut can target the joined boss prefix. | Stop if a passing result needs a different prefix/dependency or the cut can be applied directly to the base. |
| `parameter_robustness` | no independent boss-and-dependent-cut mutations | Base, boss, cut radius, and cut depth mutations change their declared observables without changing the grammar. | Stop if a mutation invalidates the prefix, crosses the boss/base boundary, or yields an ambiguous semantic result. |

## Frozen operation-contract draft

| Field | Frozen contract |
|---|---|
| Function family | `SketchRect`, `ExtrudeBase`, `SketchRect`, `ExtrudeBoss(join)`, `SketchCircle`, blind `CutCylinder` |
| Base parameters | positive `base_length_x`, `base_length_y`, `base_height` |
| Boss parameters | axis-aligned rectangular profile strictly inside the base top face; positive `boss_length_x`, `boss_length_y`, `boss_height` |
| Cut parameters | circular center strictly inside the boss top face; `0 < cut_depth < boss_height` and positive radius with positive wall clearance |
| Expected B-Rep delta | one solid base plus raised boss, with a blind cylindrical recess that begins on the boss top and preserves base material below the boss |
| Topology invariants | one connected solid; boss remains joined; cut is blind; cut floor lies above the base top; outer base extents remain; no face/edge reference |
| Unverified properties | fillets/chamfers, rotated profiles, multiple bosses/cuts, face/edge references, alternate sequences, generic B-Rep inference |

## Frozen selection and split

The exact six rows are in
[`additive-boss-dependent-cut-v1-preregistration.json`](../../corpus/sequence-paired/additive-boss-dependent-cut-v1-preregistration.json).

- Development: three centered `additive_boss_dependent_cut_centered` low/nominal/high rows.
- Held-out: three offset `additive_boss_dependent_cut_offset` low/nominal/high rows.

M23-001 creates no assets. M23-002 may produce only these rows; no row may be
substituted, moved, or added after production or audit begins.

## Rejection and stability contract

Every M23-002 rejection retains its preregistration ID, producer revision,
first failing layer, and one stable class: `catalog_violation`,
`parameter_invalid`, `boss_containment_violation`, `cut_containment_violation`,
`producer_execution_failure`, `hash_nondeterminism`,
`geometry_replay_mismatch`, `sequence_mismatch`, `topology_invariant_failure`,
`semantic_degeneration`, `editability_mutation_failure`, or
`split_family_leak`.

The future producer must generate every candidate twice into clean directories
and require byte-identical normalized STEP hashes. Its audit must include a
no-boss control, a disconnected-boss control, a through-cut control, a
base-cut control, and a split-leak control. Failure is retained evidence; it
does not authorize grammar expansion or case substitution.

## Boundaries

This preregistration changes no asset, manifest, runtime resource, prompt,
Harness behavior, provider route, external-data boundary, training input,
parser, helper, SDK, or IR.
