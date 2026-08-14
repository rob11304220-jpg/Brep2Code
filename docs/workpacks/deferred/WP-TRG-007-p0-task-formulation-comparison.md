# WP-TRG-007: P0 Task-Formulation Comparison

- Status: deferred
- Owner: unassigned
- Reviewer: Liaol
- Risk tier: G3

## Goal

Compare a small, preregistered set of task formulations on P0 only, after a
fresh P0 re-baseline has separated provider stability from CAD correctness.

## Preconditions

- The P0 rebaseline completes without its stopping condition.
- A new G3 preflight freezes the case/mode/model, exact formulations, ordering,
  request cap, deadline, metrics and unused report paths.
- The user separately authorizes the outbound content, provider/model, cases,
  formulations, deadlines and budget.

## Scope

- Compare only one-request formulations that retain the same observation
  transcript, model, compatibility mode, secure executor and geometry gates.
- Include the current direct formulation as a baseline and at most two
  predeclared alternatives that clarify geometric decomposition, OCP API
  constraints or executable-output requirements.
- Report response lifecycle, output length, script execution, bbox, volume and
  topology outcomes separately. Do not use a response to edit a later prompt.

## Stopping rule

Stop at any timeout, lifecycle failure, budget/report-path violation or
unclassified script failure. Do not tune, retry or replace a formulation after
observing a result.

## Out of scope

Repair, adaptive prompting, P1/held-out expansion, reference-script exposure,
model comparison, endpoint change, external data and general benchmark claims.
