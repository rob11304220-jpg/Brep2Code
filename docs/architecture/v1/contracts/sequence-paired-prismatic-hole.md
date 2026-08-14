---
type: contract
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - M20
  - sequence-paired
  - prismatic-hole
---

# Contract: Sequence-Paired Prismatic-Hole Pilot

This contract applies only to M20's development-side prismatic-hole pilot.  It neither
changes the Harness script contract nor creates a general modeling IR.

## Canonical grammar v1

Each sequence is normalized to exactly these ordered operations:

```text
SketchRect(id, plane=XY, length_x, length_y)
ExtrudeBase(id, profile=SketchRect, direction=+Z, distance)
CutCylinder(id, target=ExtrudeBase, variant, axis=+Z, center_xy, ...)
```

`variant` is one of:

- `through`: `radius`; the cutter extends across the base;
- `blind`: `radius`, `depth`; the cutter starts at the top face and terminates
  inside the base; or
- `counterbore`: `through_radius`, `bore_radius`, `bore_depth`; it represents
  one semantic feature but replays as a through cylinder followed by a larger
  top-side blind cylinder.

All lengths use mm.  The profile is axis-aligned in the XY plane, the base
occupies `z=[0, distance]`, and the cylindrical axis is `+Z`.  Unsupported
planes, rotated axes, multiple profiles, multiple features, taper, additive
features, non-circular cuts, or ambiguous fields reject without fallback.

## Oracle provenance

The M20 seed cases are `self_authored_deterministic_reference` oracles.  Their
canonical JSON is a reviewed normalization of the committed OCP reference
script, not native design history and not inferred ground truth.  Future native
history sources must use a different provenance value.  A sequence comparison
is valid only when candidate and oracle have the same grammar version and the
same normalization frame.

## Seed selection and split

The preregistered seed record is
`docs/corpus/sequence-paired/prismatic-hole-v1-seed.json`.  It contains exactly
two development families (`centered_through_hole`, `counterbored_plate`) and
one held-out family (`blind_hole_block`).  A seed result cannot be improved by
replacing a case, moving a family, or widening this grammar.

M20-002's separately preregistered controlled expansion is
`docs/corpus/sequence-paired/prismatic-hole-v1-expansion.json`.  It fixes
three through-hole development variants, three counterbore development
candidate variants, and three blind-hole held-out variants.  The three
template families remain split-isolated.  Counterbore candidate records may
also declare `candidate_sequence`; when present, it must name a local
candidate JSON with this grammar version and exactly agree with the declared
oracle after normalization.  Candidate assets remain experimental and require
the same audit; neither their directory nor their producer admits them to a
manifest, corpus, provider, training, or runtime path.

## Three evidence layers

1. **Geometry**: deterministic OCP replay writes a readable STEP whose bbox,
   volume, and topology counts pass the existing Harness comparison gates
   against the selected input STEP.
2. **Sequence**: the normalizer validates the exact ordered operation IDs,
   kinds, references, parameters, and dependencies.  Candidate comparison is
   exact JSON agreement after this documented normalization; it is not a claim
   that every geometrically equivalent history is identical.
3. **Editability**: each case declares mutations.  A base-length mutation must
   change the matching bbox extent and increase volume; a radius/depth mutation
   must preserve the bbox and decrease volume.  The replay must remain valid.

The first layer alone is insufficient to call a sequence correct.

## Pilot metadata boundary

Pilot JSON and its audit report are development-side evidence.  They are not a
CorpusRunner manifest, provider payload, runtime resource, or training input.
No automatic producer or admission rule is created by this contract.
