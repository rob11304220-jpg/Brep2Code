# ADR-0029: Govern Only Validated Face-Selected Dependent-Cut Pairs

- **Status**: Accepted
- **Date**: 2026-08-05

## Context

M25 preregistered and deterministically produced exactly six axis-aligned
face-selected dependent-cut cases. The scoped audit established stable output,
the frozen seven-operation selector dependency, geometry, editability,
semantics, split isolation, and negative selector controls.

## Decision

Promote only these six `face-selected-dependent-cut-v1` records to active
self-authored governance cases. They retain their frozen `SelectPlanarFace`
contract, deterministic reference scripts, case metadata, and registry
pointers. The library audit validates this grammar only against the six frozen
records.

## Consequences

The claim remains limited to one unique planar +Z maximum-Z boss-top face. It
does not introduce general topological naming, B-Rep-to-sequence recovery, an
executable manifest, provider input, training input, or runtime behavior.
