# ADR-0054: Preregister a Bounded Repeated-Feature Pattern Family

- **Status**: Accepted
- **Date**: 2026-08-10

## Context

The governed self-authored library contains individual and repeated cylindrical
cuts, including the fixed `three_hole_plate` hosted case, but no family-scoped
evidence for a declared pattern operation with exact cardinality and placement
invariants. This is the next ranked isolated feature-semantic gap.

## Decision

Create M90-001 as an offline design-and-preregistration workpack for exactly
six `repeated-feature-pattern-v1` candidates: a rectangular base followed by
one four-instance, axis-aligned 2x2 grid of cylindrical through cuts. Three
centred rows are development and three offset rows are held out.

## Consequences

- M90-002 may produce only these six frozen rows, retaining them as
  experimental pending separate evidence review and promotion.
- The result cannot establish polar, nested, variable-count or generic pattern
  recognition, and does not generalize the existing hosted result.
- M90-001 creates no manifest entry, provider input, runtime card, training
  input, or hosted request.
