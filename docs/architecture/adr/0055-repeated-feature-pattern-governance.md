# ADR-0055: Govern Only Validated Repeated-Feature Pattern Sequence Pairs

- **Status**: Accepted
- **Date**: 2026-08-10

## Context

M90 preregistered, produced and audited six `repeated-feature-pattern-v1`
records: three centred development and three offset held-out cases. Every row
uses a rectangular base and exactly four equal-radius cylindrical through cuts
at a declared 2x2 rectangular grid. All passed hash stability, replay,
sequence, editability, semantic and split controls.

## Decision

Promote only these six records to active self-authored governance cases. They
retain their frozen contract, deterministic reference scripts, metadata,
candidate sequences and registry pointers. They remain absent from executable
manifests and runtime resources.

## Consequences

The evidence is limited to one four-instance, axis-aligned rectangular-grid
through-cut grammar. It does not support polar, nested, variable-count,
variable-radius, rotated or generic patterns; it also does not authorize a
provider request, runtime card, training input or B-Rep-to-sequence claim.
