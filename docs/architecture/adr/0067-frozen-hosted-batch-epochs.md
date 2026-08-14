# ADR-0067: Use Frozen Hosted Batch Epochs for Comparable Family Evidence

- **Status**: Accepted
- **Date**: 2026-08-12
- **Context**: Existing hosted routes treated a shared stability failure as a
  practical gate for all later families. That is appropriate for an invalid
  execution boundary, but not for a script/API, geometry, or timeout terminal
  result on one otherwise independently frozen condition. Repairing prompts,
  API instructions, policies, or execution code while collecting results also
  destroys within-batch comparability.

## Decision

Use a frozen hosted batch epoch for the existing five-family development
cohort. One epoch fixes its provider/model, bounded egress, installed-OCP
instruction, executor, case/split order, card/no-card condition, gates,
deadline, output bound, report/monitor identities and zero-repair policy
before authorization.

Serial issuance is retained for accounting and monitoring, with at most one
request in flight, but it is not a causal gate between families. A terminal
result for one condition is an observation and the remaining frozen conditions
continue without modification. Only an epoch-integrity fault—policy/hash/split
drift, unauthorized egress, accounting/report identity failure, executor/
provenance boundary failure, invalid provider configuration, or a predeclared
systemic-availability stop—may pause the epoch. A repair or policy change
belongs to a later epoch.

## Rationale

The five family questions are bounded independently, while the batch provides
a comparable operating context. Preserving fixed conditions yields useful
per-family evidence without turning mixed terminal outcomes into a global
capability score or allowing adaptive changes to contaminate the denominator.

## Consequences

- **Positive**: One script/API or geometry failure does not erase independent
  observations from other frozen conditions; results are comparable within an
  epoch.
- **Negative**: A fixed epoch can retain known failures instead of immediately
  trying a repair, and needs a larger preflight/authorization budget.
- **Mitigation**: Pre-register integrity stop rules, preserve unissued
  conditions explicitly, and move all remediation to a separately selected
  later epoch after independent terminal review.

## Alternatives Considered

| Option | Rejected because |
|---|---|
| Stop every family after the first terminal failure | Conflates a condition observation with a global blocker and discards independent evidence. |
| Repair prompts or code inside the batch | Changes the treatment and makes the batch denominator non-comparable. |
| Run all families concurrently | Weakens request accounting, durable monitoring and controlled budget attribution without improving the fixed cohort's inference. |
