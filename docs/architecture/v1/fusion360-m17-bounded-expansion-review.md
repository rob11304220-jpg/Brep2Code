---
type: review
related-project: Brep2Code
status: completed
---

# M17 Review: Fusion 360 Bounded Validated-Subset Expansion

## Selection and replay outcome

The preregistered source-order scan inspected 200 official `train` identifiers
(20 accepted by the strict parser) and 2 `test` identifiers (1 accepted). It
selected three new, source-family-isolated cases outside all M14 families.

| Split | Case | Profile | Result |
|---|---|---|---|
| Development | `145540_a4f54d5f_0010` | Line3D polygon | replay and bbox/volume/topology gates pass |
| Development | `21646_a2dd0d00_0058` | Circle3D | replay and bbox/volume/topology gates pass |
| Held-out | `41026_295d1dc8_0003` | Line3D polygon | STEP written, then bbox/volume/topology gates fail |

## Held-out failure classification

The held-out JSON remains inside the nominal one-Sketch/one zero-taper NewBody
extrude feature class, but its `Line3D` curve starts are listed in a
non-continuous order. The strict replay parser accepts the class and constructs
its polygon from listed starts; this formed a degenerate face. The resulting
evidence is bbox max delta 1016 mm, volume relative delta 1.0 and topology
total absolute delta 13.

This is direct, local replay-mapping evidence. It is not a provider outcome,
not a reason to substitute a different held-out case, and not a demonstration
that Fusion lacks paired B-Rep/native-history material.

## Decision

Stop M17 at its preregistered bound. Do not expand the control manifests and do
not select M18: DeepCAD cannot resolve this current parser/mapping question.
Any future repair exploration must be a separately scoped offline workpack that
retains `41026_295d1dc8_0003` as a failing held-out control and does not widen
the operation surface implicitly.
