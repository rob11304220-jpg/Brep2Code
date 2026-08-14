# ADR-0023: Promote Only Validated Rounded-Slot Sequence Pairs to Library Governance

- **Status**: Accepted
- **Date**: 2026-08-05

## Context

M21-001 through M21-003 froze, produced, audited, and reviewed exactly six
family-isolated `rounded-slot-v1` records.  The three existing `rounded_slot`
development cases and three deterministic `offset_rounded_slot` held-out
candidates each passed geometry replay, the exact four-operation
SketchRect → ExtrudeBase → SketchRoundedSlot → CutThrough contract, and three
directional editability mutations.  The held-out producer was hash-stable and
the audit rejects both rectangular-profile degeneration and a family split
leak.

ADR-0019 governs only `prismatic-hole-v1`; ADR-0014 does not otherwise define
paired sequence metadata or family-specific audit requirements.

## Decision

Promote a backward-compatible `sequence_pair` metadata role only for the six
validated self-authored `rounded-slot-v1` records named by its frozen
expansion.  The role records grammar version, deterministic-oracle provenance,
the canonical dependent profile sequence, declared mutations, and a local
candidate sequence that must exactly agree.

Promote the three audited `offset_rounded_slot` assets to active self-authored
library cases after recording deterministic reference scripts, authoritative
baselines, case cards, registry pointers, and the scoped offline audit.  They
remain absent from every executable manifest.  The scoped audit is required
after a change to one of these records, its reference script, or its
sequence-pair metadata.

## Consequences

- The library gains a second narrowly scoped, versioned sequence-pair
  maintenance path without changing case authority under ADR-0014.
- No case gains automatic corpus, provider, training, or runtime admission;
  those routes still require an explicit manifest and separate authorization.
- Other families remain governed solely by ADR-0014 until independently
  validated and promoted through a selected workpack and separate ADR.
