# WP-M33-002: Axis-Relative Nested-Cylinder Audit

- Status: done
- Milestone: M33
- Owner: Codex

## Goal

Implement the preregistered temporary +Y axis-relative measurement audit.

## Scope

- Measure +Y axis location, axial span, transverse XZ shoulder footprint,
  radius order and shared planar adjacency.
- Verify one temporary +Y relation and controls for global +Z logic, +X axis,
  non-coaxiality and missing shoulder.

## Compatibility constraints

Offline temporary geometry only. Do not change M32, public probe, runtime,
assets, manifest, provider, parser, gates, helpers, IR or SDK.

## Acceptance

- Only the +Y temporary relation matches.
- All four controls remain unsupported.
- Focused tests, Ruff and `git diff --check` pass.

## Completion

- Added an independent +Y axis-relative reporter and temporary rotated controls.
- The +Y relation matched only from axis-relative facts; the old +Z-only
  reporter did not promote it. +X, non-coaxial and missing-shoulder controls
  remained unsupported.
- Four focused tests, Ruff and `git diff --check` passed. M32, public probe,
  runtime, case assets, manifests, provider, parser and gates remain unchanged.

## Out of scope

Arbitrary axes, feature labels, history recovery, case asset admission, public
probe expansion, runtime adoption and hosted evaluation.
