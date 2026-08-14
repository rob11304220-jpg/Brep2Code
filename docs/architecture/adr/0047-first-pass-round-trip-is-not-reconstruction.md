# ADR-0047: Do Not Count Input STEP Round-Trip as Reconstruction

- **Status**: Accepted
- **Date**: 2026-08-08

## Context

Under the M42 runtime contract, M44's held-out generated script read the
mounted `/input/model.step` and wrote that geometry to `output/model.step`.
It passed the existing executable, readability, bbox, volume, and topology
gates, despite creating no independent CAD construction or editability evidence.

## Decision

Classify direct input STEP read-and-re-export results as execution or
round-trip compatibility evidence, never as B-Rep-to-CAD reconstruction
success.  Preserve the current gates for Harness health, but require a later,
separately selected Q03 reconstruction-provenance gate before an evaluation can
claim reconstruction success.

## Consequences

M43/M44 cannot supply a model-quality success rate or justify a helper/runtime
promotion.  The next eligible work is bounded provenance-gate design; it must
state which input reads are forbidden or classified and how valid independent
construction remains evaluable.
