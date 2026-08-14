# WP-TRG-008: P1 Progressive Hosted Evaluation

- Status: deferred
- Owner: unassigned
- Reviewer: Liaol
- Risk tier: G3

## Goal

Advance one frozen, reviewed P0 formulation through existing P1 feature
complexity without mixing provider stability or prompt selection with CAD
correctness evidence.

## Preconditions

- The P0 formulation comparison is independently reviewed and identifies a preregistered formulation
  that meets its no-timeout and executable-output disposition.
- A new G3 preflight freezes the selected formulation, P1 case order, hashes,
  egress boundary, deadline, budget and report paths.
- The user separately authorizes the provider/model, cases, formulation,
  deadline and budget.

## Scope

- Run sequentially through `filleted_block`, `chamfered_block`,
  `three_hole_plate` and `box_cylinder_union`.
- Keep the observation-only boundary, `wsl-bwrap`, one request per case and
  existing gates unchanged.
- Record lifecycle, script execution and geometry gates independently.

## Stopping rule

Stop after any timeout, lifecycle failure, unclassified script failure or
geometry-gate failure. Preserve the one-case report and do not advance or add
cases to seek a success.

## Out of scope

Prompt revision, repair, held-out evaluation, manifest/corpus changes,
reference-script exposure, external data, model comparison and benchmark
claims.
