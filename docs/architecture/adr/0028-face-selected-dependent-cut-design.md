# ADR-0028: Preregister Observable Face Selection Before a Dependent Cut

- **Status**: Accepted
- **Date**: 2026-08-05

## Context

M23 established an explicit deterministic-oracle dependency from a joined boss
to a blind cut, but its declared `boss.top_face` support was not a B-Rep face
identity selector. The highest-value next gap is therefore a narrow,
observable face-selection contract rather than another coordinate-only boss
variant.

## Decision

Create M25-001 as an offline design-and-preregistration workpack for exactly
six `face-selected-dependent-cut-v1` rows. The sole grammar adds one bounded
`SelectPlanarFace` step after the joined boss: select the unique planar face
on the boss body with +Z normal at the maximum output Z extent. The subsequent
circle and blind cut must consume that selected face.

The record freezes three centered development and three offset held-out rows,
selector observables, mutations, semantic invariants, rejection taxonomy, and
producer-stability requirements. It does not define a generic topological
naming scheme, a CAD-kernel API, or runtime face selection. A separately
selected M25-002 is required before candidate production.

## Consequences

- Production can distinguish correct target selection from a coordinate-only
  support declaration with wrong-face, vertical-face, and ambiguity controls.
- The claim remains limited to a unique, axis-aligned boss top face.
- No asset, manifest, provider, training, runtime, parser/helper/SDK, or IR
  path changes in this design workpack.
