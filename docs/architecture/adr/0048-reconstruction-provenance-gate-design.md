# ADR-0048: Require Provenance Evidence for Reconstruction Claims

- **Status**: Accepted
- **Date**: 2026-08-08

## Context

M44 passed all existing executable, readability, bbox, volume, and topology
gates by reading `/input/model.step` and re-exporting it through OCP.  These
gates measure artifact health and output geometry, not the origin of the
output geometry.  A path-string ban alone would not be sufficient because
input access can be indirect through helpers, subprocesses, or native calls;
nor should it prevent separately logged Q01 B-Rep observation.

## Decision

For future Q03 reconstruction evaluation, classify results by executed input
provenance: `round_trip`, `independent_reconstruction`, or
`provenance_unknown`.  Any verified direct or indirect executed read of the
mounted original STEP is `round_trip`; unresolved access is
`provenance_unknown` and fails closed for reconstruction claims.  Only a
verified no-read execution trace plus a successful absent-input-mount control,
in addition to existing health gates, can supply
`independent_reconstruction` provenance evidence.

Q01 observations, if needed, must remain separately bounded and logged; they
do not grant the executed build script access to the original STEP for an
independent-reconstruction claim.

## Consequences

Existing gates remain useful for Harness health and continue to report their
own results.  Historical M44-like passes remain round-trip evidence, not
failures.  Implementing provenance tracing, the control run, result fields, or
sandbox capability separation requires a separately selected G2 workpack with
independent review.  This decision authorizes no provider call, prompt change,
runtime modification, or reconstruction-quality claim.
