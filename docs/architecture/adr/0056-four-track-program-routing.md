# ADR-0056: Organize Development as Four Evidence-Gated Tracks

- **Status**: Accepted
- **Date**: 2026-08-10

## Context

The existing roadmaps record valid milestone dependencies, but reading them as
one linear program obscures four distinct questions: hosted lifecycle
reliability, bounded use of derived reference material, parameter variation
under a fixed mechanism, and expansion of the modeling-sequence surface.

## Decision

Organize future workpacks under one primary track:

1. **Hosted stability**: preserve the M80 → M73 → M76 → M77 → M78 gate.
2. **Reference-assisted construction**: admit only hash-bound, derived packs
   and declared role-to-card mappings; never expose raw STEP or full reference
   scripts.
3. **Reference-guided parameter variation**: first design and validate an
   offline, family-isolated contract; any held-out hosted attempt is a later,
   separately authorized G3 workpack.
4. **Modeling-sequence coverage**: select one isolated grammar at a time from
   the coverage priorities; the next unselected candidate is `revolve-v1`.

A workpack names one primary track. A cross-track dependency must be explicit;
completion on one track neither authorizes work on another nor turns a bounded
result into a model-quality claim.

## Consequences

- Hosted sampling remains forbidden without a fresh preflight and itemized
  authorization, including reference-guided parameter experiments.
- M90 remains governance-only and cannot enter a manifest, provider input or
  runtime path merely because it has parameterized records.
- The first parameter-variation design may reuse the qualified vertical-
  cylinder card as a bounded mechanism hypothesis, but needs a new
  family-isolated held-out contract before any evaluation.
