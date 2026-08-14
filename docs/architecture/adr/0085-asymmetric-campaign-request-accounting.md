# ADR-0085: Separate Asymmetric Interaction Slots from Provider Requests

- **Status**: Accepted
- **Date**: 2026-08-14

## Context

M176 fixes 90 main and 12 annex completion slots: Q01 observation, initial
generation, and at most one repair for each main case; plus one returned card
for each annex case. Those 102 slots are not all outbound provider requests.
Q01 is a local Harness tool interaction. The annex card exchange is one
provider request, and initial generation plus an eligible repair are provider
requests.

## Decision

The fixed M178 preparation contract records both ceilings. It retains M176's
102 interaction-completion upper bound and adds a derived, tighter provider
HTTP request ceiling of 69: `30 × 2` for main plus `3 × 3` for annex. Future
reports must expose each independently and may never label all 102 slots as
issued provider requests.

## Consequences

The existing 102 authorized upper ceiling remains conservative, while future
G3 authorization can state the actual egress/request maximum precisely. This
does not alter cohort, card, repair, prompt, provider or token limits, and it
does not authorize a provider request.
