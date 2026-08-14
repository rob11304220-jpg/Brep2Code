# WP-M32-001: Nested-Cylinder Shoulder Observability Design

- Status: done
- Milestone: M32
- Owner: Codex

## Goal

Freeze a Q01 observable-only design for a bounded nested-cylinder and planar
shoulder relation, using M30's multi-cylinder counterbore controls without
turning their reference labels into inputs.

## Scope

- Reuse only the three existing +Z counterbore records as fixed oracle rows.
- Require exactly two cylinders, coaxiality, ordered radii and one shared
  adjacent planar shoulder.
- Freeze single-cylinder, non-coaxial, missing-shoulder and label-leakage
  negative controls.

## Decision-package impact

- `decision_id`: `q01-nested-cylindrical-shoulder-v1`.
- Q01/Q02 effect: report a geometric relation only when all measured facts
  agree; otherwise stop as `unsupported`.
- Knowledge disposition: design only; no observable unit is reviewed.

## Compatibility constraints

Offline-only. No asset production, public probe, runtime, classifier, helper,
IR, SDK, manifest, provider, parser or gate change.

## Acceptance

- The preregistration records facts, controls and stopping rule before code.
- M30's counterbore role remains a negative control for the single-cylinder
  unit and is not retroactively relabeled.
- JSON parsing and `git diff --check` pass.

## Completion

- Added the M32 decision package and frozen observable-only preregistration.
- M32-002 is the only allowed implementation follow-up, and must remain an
  offline measured-fact reporter.

## Out of scope

Generic counterbore recognition, history recovery, candidate production,
public probe expansion, runtime adoption and hosted evaluation.
