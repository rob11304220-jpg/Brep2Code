# WP-TRG-016: One-Family Development Hosted Campaign

- Status: deferred
- Owner: unassigned
- Reviewer: independent reviewer required
- Risk tier: G3

## Entry condition

The user selects exactly one portfolio family after its offline dossier and a fresh readiness review pass. Hosted-stability prerequisites, including applicable `WP-TRG-005` -> `WP-TRG-008` gates, must be independently satisfied.

## Goal

Run one frozen development-only campaign for one named family and preserve separate provider lifecycle, script/API, sandbox/provenance and gate evidence.

## Required preflight and scope

Freeze case hashes/split/order, Q01 egress, model/endpoint, policy, conditions, deadline, request cap, executor and fresh report/monitor paths. Obtain itemized user authorization only after complete preflight passes. Run serially with no retry or adaptive prompt/card change. A card/no-card comparison must use its predeclared control and accounting; it cannot borrow another family's report.

## Stopping rule and handoff

Stop on any timeout, lifecycle error, budget/path violation, unclassified script/API error, sandbox/provenance failure or failed applicable gate. Independently review terminal reports before proposing a held-out run; then update the hosted registry only if terminal reviewed evidence exists.

## Out of scope

Held-out rows, additional families, provider/model switching, retry, repair unless frozen beforehand, global success rates or runtime promotion.
