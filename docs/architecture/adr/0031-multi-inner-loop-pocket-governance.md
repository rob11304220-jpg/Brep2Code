# ADR-0031: Govern Only Validated Multi-Inner-Loop Pocket Sequence Pairs

- **Status**: Accepted
- **Date**: 2026-08-05

## Context

M26 preregistered, deterministically produced, audited, and independently
reviewed exactly six `multi-inner-loop-pocket-v1` records: three centered
development and three offset held-out cases. Their frozen grammar is a
rectangular base extrusion followed by one rectangular outer loop enclosing two
strictly contained, non-overlapping rectangular inner islands, then one blind
pocket cut. All six passed hash stability, geometry, exact sequence,
editability, semantic, and split controls.

The candidates remain experimental. Existing sequence-pair ADRs govern other
families and cannot extend the two-inner-loop boundary.

## Decision

Promote only the six records named by
`multi-inner-loop-pocket-v1-m26-001` to active self-authored governance cases.
They retain their frozen three-loop sequence contract, deterministic reference
scripts, case metadata, case cards, and registry pointers. The library audit
validates this grammar only against these six records; executable manifests
remain unchanged.

## Consequences

The claim remains limited to one axis-aligned rectangular outer loop, exactly
two axis-aligned rectangular inner islands, a blind cut, and one connected
solid. It does not introduce generic loop-count handling, curved or rotated
profiles, generic multi-contour recognition, face/edge references,
B-Rep-to-sequence recovery, provider input, training input, or runtime
behavior.
