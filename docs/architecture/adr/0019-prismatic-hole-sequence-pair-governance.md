# ADR-0019: Promote Only Validated Prismatic-Hole Sequence Pairs to Library Governance

- **Status**: Accepted
- **Date**: 2026-08-04

## Context

M20-001 and M20-002 completed a preregistered, family-isolated nine-case
offline evaluation of `prismatic-hole-v1`.  All cases passed geometry,
canonical-sequence, and editability evidence, and the counterbore producer was
shown hash-stable.  ADR-0014 otherwise governs the long-term case library but
does not describe paired sequence metadata or an audit for it.

## Decision

Promote a backward-compatible `sequence_pair` metadata role only for the nine
validated self-authored `prismatic-hole-v1` cases.  It records grammar version,
self-authored deterministic-oracle provenance, canonical sequence, declared
mutations, and an optional candidate sequence path that must exactly agree.

The three audited counterbore candidates become active self-authored library
cases after their per-case baselines, cards, registry pointers, and offline
audit checks are recorded.  They remain absent from executable manifests.
The family-specific audit is required for changes to this metadata or its
reference script.

## Consequences

- The library gains a narrowly scoped, versioned sequence-pair maintenance
  path without changing case authority under ADR-0014.
- No case gains automatic corpus, provider, training, or runtime admission;
  those routes still require explicit manifests and separate authorization.
- Other families remain governed solely by ADR-0014 until independently
  validated and promoted through a separate decision.
