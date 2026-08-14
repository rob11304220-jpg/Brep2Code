# ADR-0082: Staged Hosted Capability Milestone Route

- **Status**: Accepted
- **Date**: 2026-08-14

## Context

ADR-0078's three-case release proves that M139/M140/M141 compose, but cannot
support a stage-level, stratified hosted capability report.

## Decision

Use TRG-039 as an offline three-case release gate, followed by a user-selected
continuous route of five new bounded workpacks: claim/denominator charter,
case/card qualification, campaign freeze, one 30-case hosted execution, and
terminal review. The planned denominator is three strata of ten: Q01-only/no
card/no repair; Q01 plus one card/no repair; and the full bounded loop. A later
workpack receives a new M-number only when its predecessor passes acceptance.

The user's route selection authorizes automatic claiming of the five named
successor workpacks only. It does not authorize a scope deviation, an inserted
workpack, or provider egress. Unexpected feedback therefore requires a newly
scoped workpack and an explicit user selection before the route can resume. The
G3 execution workpack must stop after preflight and independent review until
fresh itemized authorization covers the provider/model, frozen hashes, outbound
schema, completion/cost budget, deadline, executor, and report paths.

## Consequences

The milestone reports overall/stratum terminal-gate and first-pass rates,
repair eligibility/conversion/plateau, tool/card compliance, completion use,
duration, failure classes, and Wilson intervals. It remains development-only
engineering evidence, not causal card evidence, generic CAD capability,
held-out readiness, or broader repair authority. A selected inserted workpack
must return to the next unmet gate; an unresolved reproducible blocker marks
the route blocked.
