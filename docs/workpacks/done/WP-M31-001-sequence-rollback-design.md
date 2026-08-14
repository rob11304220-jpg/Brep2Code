# WP-M31-001: Verified-Prefix Sequence Rollback Design

- Status: done
- Milestone: M31
- Owner: Codex

## Goal

Freeze the smallest Q04 experiment that can determine whether a correct
sequence prefix remains unchanged while only a localized suffix is regenerated.

## Scope

- Reuse one centered development and one offset held-out deterministic
  additive-boss-dependent-cut oracle only as fixed replay inputs.
- Freeze three step-indexed intermediate artifacts, one suffix-only defect and
  one earlier non-matching defect.
- Define prefix hash, prefix checks, final-gate comparison and fail-closed
  conditions before implementation.

## Decision-package impact

- `decision_id`: `q04-sequence-rollback-v1`.
- Q03/Q04 effect: diagnosis may identify a verified prefix only after a
  retained artifact and its checks succeed; rollback may regenerate only the
  suffix after that boundary.
- Evidence role: oracle, injected-error control, verified-prefix regression
  and non-matching control.
- Knowledge disposition: design only; no execution unit is reviewed.

## Execution-boundary result

The secure executor already exposes writable `intermediates/`, but the Harness
does not require step-indexed artifacts, preserve prefix hashes or compare
them. M31-002 must remain an isolated offline experiment rather than alter the
default execution or repair schema.

## Compatibility constraints

Offline-only. No provider call, manifest, runtime behavior, public Harness
schema, parser, helper, IR, SDK or existing gate change.

## Acceptance

- Preregistration freezes steps, artifacts, treatments, control and stop rule.
- Existing executor/Harness boundary is documented accurately.
- JSON parsing and `git diff --check` pass.

## Completion

- ADR-0038 and the preregistration freeze a six-step family, its artifact
  contract, suffix-only invalid-depth defect and early-defect non-match control.
- M31-002 is the only permitted follow-up and must remain offline/fixed-script.

## Out of scope

Automatic repair, provider evaluation, history recovery, public trace schema,
runtime rollback, helpers, IR/SDK and generic sequence reconstruction.
