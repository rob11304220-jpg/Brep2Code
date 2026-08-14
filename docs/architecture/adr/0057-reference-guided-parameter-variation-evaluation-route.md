# ADR-0057: Evaluate Parameter Variation with Frozen Paired Controls

- **Status**: Accepted
- **Date**: 2026-08-10

## Context

M93 and M94 define a bounded question and a frozen 3-development/3-held-out
through-hole candidate set.  A single reference-assisted hosted success would
show only a constrained feasibility observation.  It cannot distinguish a
useful finite action card from an unassisted model success, nor show that the
outbound observation supplied the required parameters.

## Decision

Use the serial M95--M99 route: offline candidate production; offline
observation/card admission; paired card/no-card development hosted
calibration; the unchanged paired policy on all three held-out rows; then an
independent evidence review.  The reference condition has two requests per
row and the no-card baseline one, so each three-row hosted package has a
maximum of nine issued requests.

Before held-out execution, freeze the observation schema, card/index hashes,
prompt and CLI policy, scoring, rows and evaluation order.  A hosted package
still requires its own preflight and itemized authorization.  Each issued
request is terminal: no retry or repair is implied by the paired design.

## Consequences

- A held-out-only reference run may be selected as a lower-budget feasibility
  observation, but it cannot make a card-effect claim.
- M89-003 remains historical single-case development evidence and neither
  supplies budget nor substitutes for a parameter-variation control.
- Any conclusion remains limited to the fixed mechanism, cases, model,
  endpoint and policy; it is not a general parameter-generalization claim.
