# ADR-0063: Freeze One Full-Revolution Stepped-Radial Family

- **Status**: Accepted
- **Date**: 2026-08-11

## Context

Modeling-sequence coverage has no axisymmetric family release. The next
selected gap must isolate revolve from sweep and loft, while retaining a
deterministic construction and family-isolated split before any candidate is
produced.

## Decision

Freeze `revolve-v1` as one closed six-segment stepped radial profile in the XZ
plane, entirely on the positive radial side of a declared +Z axis, revolved
through exactly 360 degrees. Three centred-axis rows are development-only and
three translated-axis rows are held-out; no substitutions or grammar changes
are allowed after production begins. Wrong-axis, partial-angle, degenerate
profile and split-leak controls are required.

The +Z axis sense is a deterministic Q02 API convention, not a Q01 observable
claim: reversing the axis for a 360-degree revolution has the same final
B-Rep. The family therefore does not claim signed-direction recovery.

## Consequences

The preregistration supports only a separately selected controlled-production
workpack. It adds no case assets, manifest entries, runtime resource, provider
input, hosted scope, guidance card or general B-Rep-to-sequence capability.
