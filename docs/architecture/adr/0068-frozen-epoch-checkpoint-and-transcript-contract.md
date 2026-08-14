# ADR-0068: Freeze Epoch Checkpoints and Transcript Hashes Before Authorization

- **Status**: Accepted
- **Date**: 2026-08-12
- **Context**: M134 fixes an 18-condition hosted epoch but the existing CLI
  only provides one-, two-, and nine-request checkpoint paths. Four no-card
  family charters specify bounded Q01 facts but have no executable transcript
  derivation contract. Reusing M97's two-request guidance-tool lifecycle would
  change M134's fixed denominator from 18.

## Decision

M135 provides one dedicated, durable epoch checkpoint whose policy freezes all
18 ordered condition identities, input and transcript hashes, provider/model,
deadline, output cap, executor, zero-repair/zero-retry boundary, and fresh
report/monitor paths before authorization. Each condition has exactly one
provider request. The prismatic treatment condition appends only the already
hash-pinned derived card in that single request; no guidance-tool request is
issued. The four no-card transcripts are derived locally from their frozen
development parameters and validated against an allowlisted family fact shape.

## Rationale

The checkpoint makes request accounting and M134's distinction between a
condition terminal and an epoch-integrity fault mechanically testable. Local,
hash-pinned transcripts prevent paths, raw STEP, reference scripts, provider
responses, and held-out rows from entering the outbound boundary.

## Consequences

- **Positive**: The M134 denominator remains exactly 18 and every issued
  request has a attributable frozen condition.
- **Negative**: M135 adds a narrowly scoped report/checkpoint contract and
  transcript validators before it can complete its hosted preflight.
- **Mitigation**: Validate the entire lifecycle with a fake provider and run
  no-input executor controls before independent G3 review or authorization.

## Alternatives Considered

| Option | Rejected because |
|---|---|
| Reuse M97's card-tool path | It consumes two requests for a card condition and violates the fixed 18-condition denominator. |
| Use generic probe summaries | They do not encode the family-local frozen Q01 fact contracts. |
| Dispatch independent family commands | It cannot preserve one epoch identity, one serial accounting boundary, or M134 integrity stops. |
