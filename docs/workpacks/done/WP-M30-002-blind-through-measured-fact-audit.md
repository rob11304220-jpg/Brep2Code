# WP-M30-002: Blind/Through Measured-Fact Audit

- Status: done
- Milestone: M30
- Owner: Codex

## Goal

Implement an offline-only reporter for the M30 frozen +Z single-cylinder
prismatic family, then audit its measurements against fixed oracle labels only
after classification.

## Scope

- Measure cylindrical-face count, axis, radius, face-edge-face adjacency and
  adjacent planar-face footprints.
- Classify `blind`, `through`, or `unsupported` from those measurements.
- Verify frozen through/blind nominal examples and reject the counterbore
  non-matching control as `unsupported`.

## Compatibility constraints

The reporter is a development tool only. It must not modify the public probe
contract, runtime tools, manifests, registry, provider, parser or gates.

## Acceptance

- Reference labels are absent from report inputs.
- Frozen nominal blind/through records classify from measured facts.
- Counterbore does not collapse to either class.
- Focused tests, Ruff and `git diff --check` pass.

## Completion

- Added `tools/audit_blind_through_observability.py`, an offline-only reporter
  that measures adjacency and planar footprints before classifying extent.
- The three frozen through development records classified `through`; the three
  blind held-out records classified `blind`; all counterbore controls remained
  `unsupported` because they have two cylindrical faces.
- Eight focused tests, Ruff, and `git diff --check` passed. The public probe
  contract, runtime, manifest, registry, provider, parser and gates remain
  unchanged.

## Out of scope

Generic feature recognition, arbitrary cylinder axes, multi-cylinder cuts,
history recovery, runtime adoption, public probe expansion and hosted work.
