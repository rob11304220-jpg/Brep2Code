# WP-M26-001: Multi-Inner-Loop Pocket Design and Preregistration

- Status: done
- Milestone: M26
- Owner: Codex

## Goal

Freeze one bounded self-authored blind-pocket family with an outer rectangular
loop and two inner rectangular islands before any candidate production.

## Scope

- Preregister exactly six family-isolated rows and a four-operation oracle.
- Freeze loop roles, strict containment/non-overlap, semantic invariants,
  directional mutations, negative controls, rejection taxonomy, and
  hash-stability checks.
- Define a candidate-only successor production boundary.

## Compatibility constraints

Offline-only. No assets, producer, registry, manifest, provider, training,
runtime, parser/helper/SDK, IR, or generic multi-contour recognition changes.

## Acceptance

- The M24 intake audit passes the frozen record.
- The record proves all rows retain one outer loop and exactly two non-overlapping
  inner islands; single-inner-loop, overlap, containment, through-cut, and
  split-leak controls are declared for later family audit.
- `git diff --check` passes.

## Evidence reuse / guidance-card disposition

No runtime experience card: this is planning evidence only.

## Next

M26-002 has completed separately scoped production; the six candidates remain
experimental pending a distinct evidence review.

## Result

Completed offline on 2026-08-05. The M24 intake audit passed for all six frozen
rows; no scope or row changed during production.

## Out of scope

Candidate production, generic loop inference, rotated/curved profiles,
face/edge references, promotion, external data, hosted evaluation, and runtime
changes.
