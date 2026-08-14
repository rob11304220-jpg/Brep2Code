# ADR-0065: Design a Discriminating Prismatic End-to-End Card-Effect Policy

- **Status**: Accepted
- **Date**: 2026-08-11

## Context

M112 independently closed the M96/M97 held-out comparison as `inconclusive`.
Its card-pass/baseline-fail asymmetry had no predeclared category separating a
generated-script API-use failure from a card effect. M97 capacity, policy,
reports and authorization are terminal and cannot be reused.

## Decision

Use one finite **end-to-end card-effect** estimand for a future prismatic
successor policy: under the same frozen path-free measured-fact transcript and
other fixed conditions, does the card treatment produce a better terminal
end-to-end outcome than the no-card control? API-admissibility is part of this
estimand, not an unclassified confound.

The successor must pre-register integrity, provider-lifecycle, static
API-admissibility, sandbox/execution, downstream gate and full-success
categories before any development policy is frozen. It must state which paired
differences are bounded observed treatment advantages and which are
unavailable/inconclusive; neither category is a general card-effect or model
quality claim.

## Rationale

The card's declared action guidance can affect whether a generated script uses
the supported API. Excluding that outcome after observing M97 would discard a
relevant end-to-end mechanism; treating it as causal without a predeclared
classifier made the old comparison uninterpretable. A future frozen classifier
and equal-context integrity predicate make this a limited, reviewable
observation while retaining fail-closed stop rules.

## Consequences

- **Positive**: a future comparison can distinguish its failure family before
  interpreting the paired terminal outcome.
- **Negative**: it does not identify geometry quality conditional on API-valid
  scripts, nor estimate general card utility.
- **Mitigation**: a different conditional-geometry estimand requires a new,
  separately selected design; M97 and held-out authority remain unchanged.

## Alternatives Considered

| Alternative | Reason not selected |
|---|---|
| Reuse M97/`TRG-009` | M112 closed it `inconclusive`; its policy and capacity are terminal. |
| Treat API failure as always excluded | The card can affect supported API use, so exclusion would answer a different question. |
| Claim a general causal card effect | Three finite rows and one provider/policy cannot support it. |
