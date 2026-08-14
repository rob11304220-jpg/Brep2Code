# WP-TRG-009: Reference-Guided Parameter-Variation Held-Out Evaluation

- Status: deferred
- Owner: unassigned
- Reviewer: independent reviewer required
- Risk tier: G3

## Goal

Evaluate the unchanged paired card/no-card policy on all three frozen,
family-isolated frozen held-out rows.

## Scope

- Run exactly the frozen development-calibration reference-assisted two-request condition and
  no-card one-request baseline for each held-out row.
- Retain the frozen observation schema, hashes, prompts, model/endpoint,
  CLI policy, scoring, gates and terminal disposition.

## Compatibility constraints

The maximum is nine issued requests.  No card, prompt, case, order, gate,
model or endpoint change; no retry, repair, replacement row or budget reuse.

## Entry and authorization

The completed development calibration and attribution review do not select this
package. A separately user-selected readiness decision
must retain this frozen policy and confirm that a held-out outcome remains
interpretable after the nominal baseline counterexample. It must not inspect
held-out inputs, mutate policy or issue a request. Only then conduct a fresh
hosted preflight and obtain a new itemized user authorization for this separate
three-row scope, destination/derived egress, provider/model, budget, deadline,
executor and fresh report/monitor paths.

## Acceptance

All terminal evidence is independently reviewed for split isolation, request
accounting, no-input sandbox/provenance and predeclared gate/scoring outcomes.

## Out of scope

Development tuning, extra sampling, a retry, generalized model-quality claims
or automatic promotion of the card.
