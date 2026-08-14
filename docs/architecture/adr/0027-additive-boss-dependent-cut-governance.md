# ADR-0027: Govern Only Validated Additive-Boss-Dependent-Cut Sequence Pairs

- **Status**: Accepted
- **Date**: 2026-08-05

## Context

M23-001 through M23-003 preregistered, deterministically produced, audited,
and reviewed exactly six `additive-boss-dependent-cut-v1` records: three
centered development and three offset held-out cases. Their frozen grammar is
a rectangular base extrusion, a joined rectangular boss, and a blind circular
cut constrained within that boss. All six passed hash-stability, geometry,
exact sequence, editability, semantic, and split controls.

The candidates remain experimental. Existing ADRs do not govern maintenance
of this family-specific add-then-subtract dependency.

## Decision

Promote a backward-compatible `sequence_pair` role only for the six records
named by `additive-boss-dependent-cut-v1-m23-001`. It retains grammar version,
deterministic-oracle provenance, exact canonical sequence, mutations, and a
local `candidate_sequence.json` that agrees with preregistration.

After the scoped offline audit passes, promote these six assets to active
self-authored library cases with authoritative metadata, deterministic
reference scripts, case cards, and registry pointers. Keep every executable
manifest unchanged. Re-run the family audit and case-library replay audit after
a change to one of the records, its reference script, or sequence metadata.

## Consequences

- The library gains a fourth narrow sequence-pair maintenance path.
- The evidence remains limited to the frozen axis-aligned boss-to-blind-cut
  grammar; it does not establish face identity discovery, edge references,
  native history, B-Rep-to-sequence recovery, or a general IR.
- No case gains automatic corpus, provider, training, or runtime admission.
