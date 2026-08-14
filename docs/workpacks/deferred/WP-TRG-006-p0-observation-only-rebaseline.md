# WP-TRG-006: P0 Observation-Only Hosted Re-Baseline

- Status: deferred
- Owner: unassigned
- Reviewer: Liaol
- Risk tier: G3

## Goal

Re-establish a small, current-contract hosted baseline on the committed P0
cases after the output-contract work is accepted.

## Preconditions

- A minimal end-to-end hosted path passes and is independently reviewed.
- The output-contract work is accepted.
- A fresh G3 preflight fixes case hashes, the observation-only egress boundary,
  model, compatibility mode, sequential order, deadline, per-report budget
  and unused report paths.
- The user separately authorizes every outbound boundary after that preflight.

## Scope

- Use the existing self-authored P0 cases sequentially: `box`, `cylinder`,
  then `block_with_hole`.
- Use one frozen current observation-only task formulation, no repair, one
  fresh report per case and no concurrency.
- Report provider lifecycle, script execution and geometry-gate outcomes
  separately.

## Stopping rule

Stop on any provider timeout, lifecycle failure, report-path/budget violation
or unclassified script failure. Record the terminal evidence; do not retry,
alter the task formulation, add cases or proceed to a formulation comparison.

## Out of scope

Prompt comparison, repair, P1/held-out cases, manifest changes, external data,
endpoint/model changes and model-quality claims.
