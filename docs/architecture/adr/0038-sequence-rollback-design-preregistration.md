# ADR-0038: Preregister a Verified-Prefix Rollback Experiment

- **Status**: Accepted
- **Date**: 2026-08-07

## Context

The Harness records a final output and an `intermediates/` directory, but it
does not require step-indexed CAD artifacts or retain evidence that a sequence
prefix was correct. Existing repair and sandbox-path results consequently do
not establish whether a localized failure can be recovered without rewriting a
correct prefix.

## Decision

Freeze an offline design using the six-step, deterministic
`additive-boss-dependent-cut-v1` sequence. A later M31-002 experiment may
retain `after-base.step`, `after-boss.step` and `after-cut.step`; inject one
suffix-only invalid-cut-depth defect after the verified boss prefix; and then
regenerate only that suffix. A defect occurring before the boss artifact is a
required non-matching control and cannot be rolled back.

## Consequences

- Prefix identity is an artifact hash plus its existing family-specific checks;
  final success still uses existing Harness gates.
- The experiment is development-side, offline and fixed-script only.
- It does not change default Harness behavior, provider repair, public schemas,
  manifests, helpers, IR/SDK, or claim original-history recovery.
