# ADR-0030: Preregister a Bounded Multi-Inner-Loop Pocket Family

- **Status**: Accepted
- **Date**: 2026-08-05

## Context

The governed `multi-contour-pocket-v1` evidence establishes exactly one outer
rectangular loop plus one inner rectangular island in a blind annular pocket.
The coverage matrix identifies multiple inner loops as the next bounded sketch
topology gap. M25's face-selection result is complete and must not be
generalized while addressing this separate gap.

## Decision

Create M26-001 as an offline design-and-preregistration workpack for exactly
six `multi-inner-loop-pocket-v1` rows. Its canonical oracle is a rectangular
base followed by one outer rectangular loop and two strictly contained,
non-overlapping rectangular inner islands, then one blind pocket cut. The
record freezes three centered development rows, three offset held-out rows,
loop-role invariants, directional mutations, negative controls, and a
candidate-only production boundary.

## Consequences

- A later, separately selected production workpack can test the exact frozen
  three-loop grammar without substituting rows or broadening loop semantics.
- The result cannot establish arbitrary loop geometry, curved or rotated
  profiles, generic multi-contour recognition, face/edge references, or
  B-Rep-to-sequence recovery.
- M26-001 creates no assets, producer, active registry entry, executable
  manifest, provider input, training input, or runtime behavior.
