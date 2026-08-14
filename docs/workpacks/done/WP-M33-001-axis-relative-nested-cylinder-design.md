# WP-M33-001: Axis-Relative Nested-Cylinder Design

- Status: done
- Milestone: M33
- Owner: Codex

## Goal

Freeze one +Y rotated control for the nested-cylinder/shoulder relation so
that a future audit can test axis-relative measurement rather than global +Z
or XY assumptions.

## Scope

- Use temporary deterministic geometry only; create no case asset.
- Require +Y coaxiality, radius order, shared shoulder, axial projection and
  transverse-plane footprint facts.
- Freeze global-XY, non-+Y, non-coaxial and missing-shoulder controls.

## Decision-package impact

- `decision_id`: `q01-axis-relative-nested-cylinder-v1`.
- Evidence is design only. M32 remains a separate reviewed +Z observable unit.

## Compatibility constraints

Offline-only. No public probe, runtime, manifest, provider, parser, helper,
IR, SDK, gate or case-library change.

## Acceptance

- Preregistration fixes the +Y scope, axis-relative facts, controls and stop
  rule before implementation.
- It does not reuse M27 direction evidence as cylinder evidence.
- JSON parsing and `git diff --check` pass.

## Completion

- Added the M33 decision package and design-only preregistration.
- M33-002 is the only permitted follow-up and remains offline/temporary.

## Out of scope

Arbitrary orientations, generic feature recognition, asset admission, public
probe expansion, runtime adoption and hosted evaluation.
