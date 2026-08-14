---
type: review
related-project: Brep2Code
status: completed
---

# M17-007 Review: Restricted Fusion Line3D Default Mapping

## Decision

M17-005's fixed four-case matrix and M17-006's independent 2 development/1
held-out matrix provide five development and two held-out gate passes for the
same frozen selector.  The policy therefore adopts it as the default only for
the exact supported Line3D native-history subset, as recorded in ADR-0017.

## Boundary and regression evidence

`replay()` now requires the input STEP bbox for Line3D and delegates to the
endpoint-ordering selector.  It rejects when the axis is not unique or the
subset is not met.  `replay_strict()` is retained solely for historical
comparison reports.  Circle3D keeps the prior strict replay path.

The local M14 replay, M17 replay, M17-005 fixed comparison matrix and M17-006
independent comparison matrix all completed with their required gate outcomes.
Focused tests passed 5/5 and Ruff passed for changed paths.

## Non-promotion

This is not a general Fusion parser claim and does not alter Harness, CLI,
manifests, corpus/provider behavior, geometry gates, runtime guidance or M18.
The result is parser-local implementation evidence rather than an experience
card: no runtime guidance card was created.
