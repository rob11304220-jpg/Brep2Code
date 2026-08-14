# WP-TRG-042: Hosted Campaign Readiness Lifecycle

- Status: deferred
- Risk tier if selected: G2

## Trigger question

After an independently reviewed terminal report for the current asymmetric
33-case campaign, should campaign preparation be redesigned so that a frozen
case/card/Harness/budget configuration becomes a fake-executable and
machine-checkable authorization packet before hosted authorization is sought?

## Entry condition

The current M180 asymmetric campaign has completed under fresh itemized
authorization and has an independently reviewed terminal report.  The user
must separately select this trigger; it is not an automatic successor and it
does not authorize a new hosted call.

## Proposed goal

Implement and validate the readiness lifecycle described in
[`hosted-campaign-readiness-lifecycle-proposal.md`](../../architecture/v1/hosted-campaign-readiness-lifecycle-proposal.md), so a future frozen campaign can reach `reviewed_ready` before a user is asked for egress approval.

## Decision-package impact

- Hypothesis ID: not applicable; operational campaign-governance decision.
- Q01--Q04: preserve their frozen boundaries while making their campaign
  orchestration executable and inspectable before egress.
- Evidence role: one current terminal report plus fake-only readiness evidence;
  neither establishes model quality or a broader hosted capability claim.
- Counterexample: a `reviewed_ready` artifact requiring a new state machine,
  CLI/provider boundary, accounting rule, report rule, or policy choice before
  execution.
- Stop rule: the proposal requires changing a campaign's frozen policy,
  interpreting a hosted result, sending data, or widening runtime/provider
  authority.
- Adoption boundary: future preparation and authorization UX only; each hosted
  campaign still requires fresh preflight, independent review, and explicit
  itemized user authorization.

## Scope if selected

- Write an ADR for the lifecycle decision.
- Define the versioned campaign artifact and authorization-packet schemas.
- Implement fake-only lifecycle/doctor checks and a runbook.
- Demonstrate that a reviewed-ready artifact has no late orchestration gaps.

## Out of scope

Current M180 implementation or authorization; provider construction or
egress; credentials; retry/repair-policy changes; case/card changes;
evaluation or interpretation of the preceding hosted report; and any new
campaign selection.

## Acceptance if selected

- Schema, contract, runbook and concise ADR agree on every lifecycle state.
- Fake-only end-to-end tests prove exact accounting and every terminal state.
- `campaign doctor` rejects hash, split, card, executor, checkpoint, report
  freshness, accounting, and authorization-packet drift before egress.
- Independent G2 review, relevant tests, Ruff, governance audit, and diff
  checks pass.

## Route disposition

Future option.  It is considered only after the named terminal report, and
only through a new user-selected M-numbered workpack.  The durable proposal,
not this trigger, owns the suggested lifecycle.
