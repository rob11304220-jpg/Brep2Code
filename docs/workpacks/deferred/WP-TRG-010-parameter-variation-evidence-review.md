# WP-TRG-010: Reference-Guided Parameter-Variation Evidence Review

- Status: deferred
- Owner: unassigned
- Reviewer: independent reviewer required
- Risk tier: G2

## Goal

Independently assess whether the preregistered paired experiment was executed
within its frozen boundaries and state its limited evidence result.

## Scope

- Audit the frozen production, admission, calibration and held-out-evaluation
  hashes, split isolation, policy/card pinning, report
  accounting, no-input sandbox/provenance and gate outcomes.
- Compare the predeclared card/no-card outcome only under the fixed three-row
  held-out scope.
- Record any rejection or inconclusive outcome without backfilling samples.

## Compatibility constraints

No provider request, retry, card/runtime promotion, manifest change, gate
relaxation or conclusion beyond the fixed mechanism/model/policy.

## Acceptance

Run governance audit, relevant offline report/schema checks and `git diff
--check`; obtain independent review before closing.

## Out of scope

Any new hosted budget, generic parameter-generalization claim, model ranking
or automatic next workpack.
