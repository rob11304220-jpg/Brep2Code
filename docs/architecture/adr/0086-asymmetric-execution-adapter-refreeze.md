# ADR-0086: Keep the Asymmetric Execution Adapter Provider-Injected

- **Status**: Accepted
- **Date**: 2026-08-14

## Context

M177's approved local preflight consumed M176's four fixed identities, while
M178 exposed no M176 execute surface. Reusing those identities or substituting
the generic observed-development CLI would alter the frozen campaign contract.

## Decision

M179 freezes four new identities bound by the M176 spec hash and exposes only
local preparation/admission commands plus a `FakeLLMProvider`-only serial
adapter. Non-fake providers fail before request material is prepared.

## Consequences

- **Positive**: accounting and identity lifecycle can be regression-tested
  without credential or network access.
- **Negative**: M179 is not a hosted executor.
- **Mitigation**: a later G3 package must add any provider construction,
  conduct fresh preflight, and obtain itemized user authorization.
