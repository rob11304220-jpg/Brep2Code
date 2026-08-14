# M115 Prismatic Development-Only Card-Effect Policy

## Status and boundary

This is the offline policy freeze required by [ADR-0065](../adr/0065-prismatic-end-to-end-card-effect-policy-design.md).
The normative machine-readable contract is
[`m115-prismatic-development-card-effect-policy-v1.json`](../../corpus/registry/m115-prismatic-development-card-effect-policy-v1.json).
It is neither a provider configuration nor a campaign: it selects no input,
card, prompt, model, endpoint, report path, monitor path or request budget.

Only a later, separately selected G3 package may select a fresh development
manifest. It must reject every non-development or unlabelled row before any
provider construction, preflight or request. Held-out inputs are outside this
policy.

## Frozen observation contract

For each paired row, both conditions must have equal policy, row, manifest,
input, measured-fact transcript, observation-contract, prompt, model,
provider, executor, sandbox, classifier and downstream-gate versions. The
sole permitted difference is the `card` versus `no_card` treatment, with a card
hash recorded only for `card`. Any mismatch terminates the whole policy as
`integrity_failed`; it yields no comparison and permits no retry or repair.

The versioned static classifier runs only after a generated script is present
and before sandbox launch. It accepts exactly the declared OCP import surface
and one box, cylinder, cut and STEP-writer construction recipe. Its result is
either `api_admissible` or `api_inadmissible`, making API use an explicit part
of the finite end-to-end estimand rather than a post-hoc exclusion.

## Terminal interpretation

After integrity passes, each condition has exactly one terminal category in
this order: `lifecycle_ended_before_script`, `static_api_inadmissible`,
`sandbox_execution_failed`, `downstream_gate_failed`, or `full_success`.
The first category is unavailable for the estimand; no script exists to
classify. A card full success paired with no-card static API inadmissibility is
only a finite observed end-to-end advantage at the preregistered API stage; a
later no-card failure is only a finite advantage at that later stage. Both
conditions succeeding shows feasibility under both conditions, not an
advantage.

No outcome supports a held-out result, a general card effect, model capability,
parameter generalization, conditional geometry quality, runtime knowledge, or
a Harness-gate change.

## Fresh lifecycle boundary

The policy reserves an M115-specific accounting namespace and nonce-based
future report and monitor identifiers. A later G3 preflight must prove they
are new and absent, including absence of reusable running or interrupted
checkpoints; all M97 policy, accounting, reporting, monitoring, budget and
authorization material remains terminal and excluded.
