---
type: roadmap
related-project: Brep2Code
status: active
---

# Evidence-Gated Case-Family Expansion Priorities

## Purpose

This route converts the M20--M24 development experience into a ranked list of
case-family hypotheses. It is a planning aid for development workpacks, not an
authorization to select all rows, create assets, promote candidates, alter an
executable manifest, or use a provider.

## Operating rule

Choose exactly one item at a time. Its design workpack must use the M24 intake
contract to freeze its grammar, rows, family-isolated split, semantic
invariants, mutations, negative controls, and stopping rule before candidate
production. Production, review, and lifecycle promotion remain separate user-
selected steps under ADR-0020 and ADR-0026.

## Ordered route

| Order | Candidate work | Gap and bounded hypothesis | Required evidence / stopping rule |
|---|---|---|---|
| 0 | M23 evidence review | Close the governance interpretation of the six additive-boss-dependent-cut experimental candidates. | Compare frozen evidence with prior families; propose at most one disposition. It must not itself promote assets. |
| 1 | `face-selected-dependent-cut-v1` design | Test an explicit, observable selector for a downstream boss top face before a blind cut; it must not be a coordinate-only support label. | Face-selection identity, exact sequence, mutations, target/wrong-face negative controls, and held-out family isolation. Stop if no stable selector can be stated without broad parser/IR work. |
| 2 | `multi-inner-loop-pocket-v1` design | Extend the nested-pocket evidence from one inner island to a fixed outer loop plus two inner islands. | Loop roles, strict containment, blind removed-volume invariant, single-solid invariant, and single-loop/split-leak controls. |
| 3 | `oriented-rounded-slot-v1` design | Separate orientation ambiguity from arbitrary curves by rotating the existing fixed arc-based slot grammar. | Plane/frame declaration, orientation-sensitive geometry and mutation checks, and axis-aligned/incorrect-frame controls. Do not add splines. |
| 4 | `repeated-feature-pattern-v1` design | Test a bounded repeated-feature cardinality and placement dependency. | Exact instance count and positions, spacing mutation, omitted/extra-instance controls, and one frozen pattern form. |
| 5 | `revolve-v1` design | Add one axisymmetric construction family without conflating it with sweep or loft. | Axis, profile, angle, direction, volume/topology invariants, and wrong-axis/partial-angle controls. |
| 6 | `shell-v1` *or* `rib-v1` design | Add one bounded complex-topology hypothesis, not both. | For shell: thickness/opening semantics; for rib: attachment/thickness semantics. Retain a single-solid contract and stop on multi-solid ambiguity. |
| 7 | robustness micro-family | Test exactly one declared stress source: thin-wall, near-tangent, boundary-adjacent, scale/unit, or orientation. | Frozen stress interval, non-degenerate control, failure taxonomy, and a stopping condition; it cannot claim general robustness. |
| 8 | external native-history admission | Validate an operation-diverse external source only after self-authored dependency evidence is reviewed. | Source/license/representation audit, deterministic small split, local replay evidence, and no hosted use by default. |

## Explicit non-routes

- Do not combine face/edge selection, patterns, fillets, and arbitrary curves
  in one family.
- Treat revolve, sweep, and loft as separate families.
- Do not replace a rejected row or use parameter-count growth as evidence of a
  new capability.
- Neither this route nor a passing family authorizes runtime retrieval, an IR,
  a parser/helper/SDK change, external download, manifest admission, training,
  or hosted evaluation.

## Current selection

Orders 0--3 are complete: M23, M25, M26, and M27 are governed as active
family-specific evidence sets. M27 promoted exactly six frozen
`oriented-rounded-slot-v1` records after offline production, review, and
governance promotion; it did not create executable-manifest, provider, training,
or runtime behavior.

Order 4 completed as M90: exactly six `repeated-feature-pattern-v1` records
are governed as active, family-scoped evidence for one four-instance
rectangular-grid cylindrical through-cut grammar. They remain absent from
executable manifests, provider inputs and runtime resources. Order 5 completed
as M105--M108: exactly six `revolve-v1` records are active, family-scoped
governance evidence under ADR-0064 and remain absent from executable manifests,
provider inputs and runtime resources. Orders 6--8 remain unselected and must
be taken one at a time.
