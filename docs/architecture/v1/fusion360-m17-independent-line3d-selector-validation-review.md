---
type: review
related-project: Brep2Code
status: completed
---

# M17-006 Review: Independent Fusion Line3D Selector Validation

## Selection and scope

M17-006 used only the already cached Fusion r1.0.1 release. It inspected the
pre-registered train positions 201--400 and test positions 1--200, excluded
every M14--M17-005 source family, and selected the first two eligible train
families plus the first eligible test family. The tracked selection record
contains source order, split, paths and SHA-256 for `141323_f85efdd4_0000`,
`136900_4fe212e6_0010`, and `143017_21d96cc2_0005`.

No selector, gate, syntax, manifest, corpus, provider or hosted setting
changed. The M17-005 selector remained frozen.

## Matrix result

| Case | Split | Strict replay | Frozen selector |
|---|---|---|---|
| `141323_f85efdd4_0000` | development | pass | pass |
| `136900_4fe212e6_0010` | development | volume/topology fail | pass |
| `143017_21d96cc2_0005` | held-out | pass | pass |

All selector rows passed the existing bbox, volume and topology gates. Along
with M17-005, this yields five development and two held-out hash-linked
Line3D selector passes. It is independent evidence because the three new
families were not selected or used by prior M14--M17-005 work.

## Decision boundary

The new result strengthens the bounded selector hypothesis but does not change
the strict default replay policy. A subsequent mapping-policy review must
explicitly decide whether the accumulated seven-row evidence is sufficient for
any restricted default-path promotion; it must not claim generic Fusion parser
support or silently expand operation/curve scope. M18 remains unselected.
