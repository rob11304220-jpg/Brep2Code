# WP-M32-002: Nested-Cylinder Measured-Fact Audit

- Status: done
- Milestone: M32
- Owner: Codex

## Goal

Implement the preregistered offline reporter for two coaxial cylinders and a
shared planar shoulder.

## Scope

- Measure cylinder cardinality, axes, radii and adjacent faces.
- Require exactly one shared planar shoulder before reporting the relation.
- Verify frozen counterbore rows plus temporary non-coaxial and
  missing-shoulder controls.

## Compatibility constraints

Offline development tool only. Do not change public probe/runtime behavior,
case assets, manifests, provider, parser, gates, helpers, IR or SDK.

## Acceptance

- Three frozen rows match only from measured facts.
- Both temporary controls are `unsupported` with their recorded reason.
- Focused tests, Ruff and `git diff --check` pass.

## Completion

- Added `tools/audit_nested_cylindrical_shoulder.py`; it measures two-cylinder
  cardinality, axes, radii, face adjacency and shared planar shoulders.
- All three frozen rows matched the relation. Temporary non-coaxial and
  missing-shoulder controls returned their respective `unsupported` reasons.
- Five focused tests, Ruff and `git diff --check` passed. No case asset,
  public probe, runtime, manifest, provider, parser or gate changed.

## Out of scope

Feature labels, counterbore recognition, history recovery, public probe
expansion, runtime behavior, hosted evaluation or asset admission.
