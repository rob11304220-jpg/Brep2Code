# ADR-0075: Explicit Hash-Bound GuidanceBundle Selection

- **Status**: Accepted
- **Date**: 2026-08-13

## Context

The opt-in `GuidanceCardBridge` previously accepted only the hard-coded
`vertical-cylinder-construction` card and a global role set. M157 therefore
could not evaluate a separately selected, hash-bound selector counterexample
card without changing Harness behavior outside its scope.

## Decision

Make each `GuidanceBundle` declare one selected card path and its compatible
roles when trusted Harness-side code creates the bundle. The Bridge verifies
the bundle's index and card hashes, checks the selected card is listed by its
exact path and matching ID, and exposes only the bundle-local role enum.

The runtime caller cannot submit a card ID. The Bridge does not enumerate,
rank, substitute, or search cards. Existing vertical-cylinder callers retain
their three legacy roles by default.

## Consequences

One separately selected experimental card can now be evaluated through the
existing opt-in bridge without introducing broad retrieval or changing default
no-card behavior. A new card, multi-card selection, retrieval, provider use,
or hosted use remains subject to its own workpack and authorization boundary.
