---
type: review
related-project: Brep2Code
status: completed
---

# M17-008 Review: Independent Default Line3D Regression

M17-008 inspected only train positions 401--600 and test positions 201--400,
excluding every family used by M14 through M17-006. It selected development
orders 406 (`85638_2ab1040c_0003`) and 446 (`91457_c0320701_0003`), plus
held-out order 211 (`139674_8774f1a3_0060`).

The unchanged M17-007 default replay passed existing bbox, volume and topology
gates for all three rows. No selector rejection, write failure or gate failure
occurred, so no stopping condition was triggered. The cumulative bounded
evidence is seven development and three held-out gate passes.

No mapping, gate, syntax, Harness, corpus, provider, hosted or runtime-guidance
behavior changed. This is parser-local regression evidence, so no experience
card was created. Any further scope expansion remains a separately selected
workpack; M18 remains unselected.
