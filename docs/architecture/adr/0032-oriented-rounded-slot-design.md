# ADR-0032: Preregister a Bounded Oriented Rounded-Slot Family

- **Status**: Accepted
- **Date**: 2026-08-05

## Context

The governed `rounded-slot-v1` evidence fixes its composite slot profile along
the global X direction. M26 closes the multiple-inner-loop topology gap, while
the coverage route still identifies profile orientation ambiguity as a separate
gap. This gap must not be merged with arbitrary curves, general frame recovery,
or runtime geometry inference.

## Decision

Create M27-001 as an offline design-and-preregistration workpack for exactly
six `oriented-rounded-slot-v1` rows. Its deterministic oracle is a rectangular
XY base followed by a through rounded-slot cut whose declared in-plane local
axis is either +X or +Y. Three +X rows are development and three +Y rows are
held out; the two frame families are isolated. The record freezes dimensions,
centres, orientation, directional mutations, negative controls, and a
candidate-only production boundary.

## Consequences

- A later, separately selected workpack may test only the six frozen rows and
  their two explicit axis-aligned frames.
- The family cannot establish arbitrary angles, curved or spline profiles,
  general sketch-frame inference, B-Rep-to-sequence recovery, or generic
  profile recognition.
- M27-001 creates no assets, producer output, registry entry, executable
  manifest, provider input, training input, or runtime behavior.
