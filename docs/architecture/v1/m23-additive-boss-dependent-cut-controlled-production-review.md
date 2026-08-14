---
type: review
related-project: Brep2Code
status: completed
---

# M23-002 Review: Additive-Boss-Dependent-Cut Controlled Production

## Scope and result

M23-002 produced exactly the six rows frozen by M23-001: three centered
development candidates and three offset held-out candidates. Each was built
twice in clean directories, with byte-identical normalized STEP hashes.

All six experimental candidates passed existing geometry replay gates, the
exact six-operation oracle `SketchRect -> ExtrudeBase -> SketchRect ->
ExtrudeBoss(join) -> SketchCircle(boss.top_face) -> CutCylinder(blind)`, four
preregistered editability mutations, and one-solid/base-extent/boss-height/
blind-cut-volume invariants. Focused controls reject a base-targeted cut, a
through-cut, and a split leak. The five focused tests, family audit, and Ruff passed.

## Interpretation

This is reproducible self-authored deterministic-oracle evidence for one
axis-aligned rectangular boss with a dependent blind circular cut. It does not
demonstrate generic feature recovery, arbitrary dependent features, native
history, face/edge references, or B-Rep-to-sequence inference.

## Governance disposition

The six candidates remain `experimental`, unregistered, and absent from all
executable manifests, provider, training, and runtime paths. Any future review
or governance decision requires separate user selection.
