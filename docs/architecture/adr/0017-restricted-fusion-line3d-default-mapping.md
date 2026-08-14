# ADR-0017: Use a Fail-Closed Selector for Restricted Fusion Line3D Replay

- **Status**: Accepted
- **Date**: 2026-08-04

## Context

The listed-order / `z_axis` Line3D replay failed one fixed held-out case and
one independently selected development case.  The frozen selector passed
existing bbox, volume and topology gates on five development and two held-out
hash-linked cases.  Its evidence is still limited to one native-history
subset and must not imply generic Fusion support.

## Decision

For only a transformed single Sketch with a profile-plane start, one
zero-taper one-sided NewBody distance extrude, and one Line3D outer loop,
default offline replay endpoint-orders the loop and selects the unique signed
sketch axis from profile normal, input-STEP projection and extent boundary.
The input bbox is mandatory.  Ambiguous, non-boundary, non-closing or
otherwise unsupported Line3D input rejects; no fallback axis or healing is
allowed.  Circle3D continues to use the prior strict path.

## Consequences

- M14 and M17 replay callers must provide the bounded input bbox before a
  Line3D shape is created.
- The historical listed-order / `z_axis` path remains available only for
  comparison reports, not as a fallback.
- This changes neither Harness, CLI, corpus manifests, provider policy, gates,
  runtime guidance retrieval nor supported Fusion operations/curve types.
- Any scope expansion needs a new workpack, independent evidence and review.
