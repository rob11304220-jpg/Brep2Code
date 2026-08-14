# WP-TRG-019: Prismatic Card-Effect Policy Design

- Status: archived-trigger
- Owner: consumed by `WP-M114-001`
- Reviewer: independent reviewer required on the consuming M workpack
- Risk tier: G2

## Historical note

This deferred trigger was consumed when the user selected a fresh bounded
package and activated `WP-M114-001-prismatic-card-effect-policy-design`. Its
follow-on development-only policy freeze completed as `WP-M115-001`. This file
remains historical navigation evidence only and must not be reactivated as a
current deferred workpack.

## Original goal

Design, but do not execute, a successor policy that can distinguish its chosen
prismatic card-effect estimand from script/API, lifecycle, sandbox and
geometry failure families after M112's `inconclusive` disposition.

## Original trigger

M112 is independently closed as `inconclusive` and the user explicitly selects
this offline policy/design work. The trigger grants no access to held-out input
and no provider authority.

## Original scope

- Choose exactly one estimand: end-to-end card effect including API-validity,
  or geometry effect conditional on a predeclared API-valid stratum.
- Pre-register mutually exclusive terminal categories, their stop rules and
  which categories can answer the selected estimand.
- Specify separation from M97: new development-only policy, fresh accounting
  and no reuse of M97 report, monitor, budget or authorization.
- State the later gates for any separately selected development review and
  fresh held-out policy; do not create either policy in this workpack.

## Out of scope

Held-out inspection, provider construction, preflight, authorization, request,
retry, repair, M97 mutation/reuse, card/prompt change, case/split change,
manifest/runtime change or a generalization claim.
