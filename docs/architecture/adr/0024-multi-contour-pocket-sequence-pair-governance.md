# ADR-0024: Govern Only Validated Multi-Contour Pocket Sequence Pairs

- **Status**: Accepted
- **Date**: 2026-08-05

## Context

M22-001 through M22-003 preregistered, deterministically produced, audited,
and reviewed exactly six family-isolated `multi-contour-pocket-v1` records:
three centered development variants and three offset held-out variants. Each
records a four-operation `SketchRect → ExtrudeBase → SketchPocketLoops →
CutPocket` oracle, two nested rectangular loop roles, a blind annular-pocket
invariant, and four declared editability mutations. The producer is
hash-stable and the completed review supports only this frozen grammar.

Existing sequence-pair governance is family-specific: ADR-0019 applies to
`prismatic-hole-v1`, and ADR-0023 applies to `rounded-slot-v1`. Neither
governs this two-loop pocket grammar.

## Decision

Promote a backward-compatible `sequence_pair` metadata role only for the six
records named by `multi-contour-pocket-v1-m22-002`. The role records grammar
version, deterministic-oracle provenance, the canonical dependent sequence,
declared mutations, and a local `candidate_sequence.json` that must exactly
agree with the preregistration.

After the scoped offline audit passes, promote the six assets to active
self-authored library cases with authoritative metadata, deterministic
reference scripts, baselines, case cards, and registry pointers. Keep every
executable manifest unchanged. Re-run the family audit after a change to one
of these records, its reference script, or its sequence-pair metadata.

## Consequences

- The library gains a third, narrowly scoped sequence-pair maintenance path.
- The claim remains limited to the frozen nested-rectangle blind-annular-pocket
  grammar; it does not establish native history, B-Rep-to-sequence recovery,
  generic topology, face/edge dependencies, or a general IR.
- No case gains automatic corpus, provider, training, or runtime admission.
- Other families require their own selected workpack and ADR before using this
  metadata role.
