# ADR-0083: Historical Guidance-Index Fixtures Preserve Frozen Policies

- **Status**: Accepted
- **Date**: 2026-08-14

## Context

M96/M97 freeze the SHA-256 of the then-current guidance index and the unchanged
`vertical-cylinder-construction` card.  A later, unrelated addition of
`selector-cardinality-stop.json` changed the shared index hash, leaving five
historical regression assertions red while M170's focused release evidence
remained green.

## Decision

Keep the frozen M96/M97 policy hashes and their selected card unchanged.  M171
will restore reproducibility through an explicit, versioned historical guidance
index fixture, used only by the M96/M97 regression checks and any matching
historical validation.  The live default index remains unchanged.

## Consequences

The historical policy retains its original identity without removing a newer
card or broadening guidance selection.  M171 must independently verify that
the fixture hash is the recorded historical hash, the selected card hash is
unchanged, and current guidance behavior is unaffected.  No provider, hosted,
case, manifest, Harness, retrieval, or runtime-authority change follows.
