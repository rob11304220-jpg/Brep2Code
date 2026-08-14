# ADR-0088: Continue the Fixed Campaign after Case-Local Failures

- **Status**: Accepted
- **Date**: 2026-08-14

## Context

The fixed M180 runner re-raises an exception from one case, marking its
product report `interrupted` and preventing terminal evidence for the remaining
frozen cases.  The selected campaign requirement is to traverse every case
without retrying a timed-out or failed request.

## Decision

M182 will represent an eligible case-local provider, Harness, or source-only
repair exception as that case's terminal result, checkpoint it, and continue
serially to the next frozen case.  Frozen-contract, authorization,
configuration, report-identity, and accounting-cap failures remain
campaign-global fail-closed errors.  No retry, resume, budget reuse, or policy
override is introduced.

## Rationale

This preserves attributable terminal evidence for every case while retaining
the existing egress, input, executor, and accounting safety boundaries.

## Consequences

- **Positive**: A timeout or case-local failure cannot silently reduce the
  campaign denominator.
- **Negative**: Terminal reports need a distinct, auditable case-local
  interruption classification.
- **Mitigation**: M182 freezes fresh report identities and adds offline tests
  for continuation, cap accounting, and global fail-closed conditions.

## Alternatives Considered

| Alternative | Rejection reason |
|---|---|
| Retain early batch termination | It cannot produce complete 33-case terminal evidence after one case-local failure. |
| Add retry or resume | It would alter the authorized request policy and permit budget reuse. |
