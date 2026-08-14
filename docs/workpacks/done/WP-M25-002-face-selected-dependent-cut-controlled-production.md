# WP-M25-002: Face-Selected-Dependent-Cut Controlled Production

- Status: done
- Milestone: M25
- Owner: unassigned

## Goal

Produce and validate exactly the six rows frozen by M25-001, while proving the
unique boss-top face selector is consumed by the dependent blind cut.

## Entry criteria

- M25-001 and ADR-0028 remain unchanged.
- The user explicitly selects this workpack.

## Scope

- Build only the preregistered rows twice in clean directories.
- Audit geometry, exact selector sequence, editability, semantic invariants,
  hash stability, split isolation, and wrong/vertical/ambiguous face controls.
- Retain every failure with its frozen rejection reason; do not substitute a
  row or relax the selector.

## Compatibility constraints

Candidate outputs remain experimental. No automatic registry, manifest,
provider, training, runtime, parser/helper/SDK, IR, or external-data change.

## Acceptance

- Every candidate has byte-identical normalized STEP hashes across two clean
  builds.
- The family-specific audit distinguishes selected boss-top, wrong-face,
  vertical-face, and ambiguous-face outcomes.
- Focused tests, scoped audit, Ruff, and `git diff --check` pass.

## Evidence reuse / guidance-card disposition

No runtime experience card unless a later review establishes the independent
direct runtime-mechanism threshold.

## Result

Completed offline on 2026-08-05 under the selected M25-002 scope. The six
frozen candidates were each built twice in clean directories with byte-identical
normalized STEP hashes. The family audit passed geometry replay, exact seven-step
selector dependency, five editability mutations, semantic invariants, split
isolation, and wrong-face, vertical-face, and selector-ambiguity controls.
The candidates remain experimental and no manifest, provider, training, or
runtime path changed.

## Out of scope

Governance promotion, general face selection, native-history claims, B-Rep-to-
sequence recovery, hosted evaluation, and runtime changes.
