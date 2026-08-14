# WP-M95-001: Reference-Guided Through-Hole Controlled Production

- Status: done
- Milestone: M95
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Produce and offline-audit only the six M94-frozen through-hole candidates so
that a later evaluation has deterministic, family-isolated assets.

## Scope

- Implement the planned M94 candidate producer for exactly its three
  development and three held-out rows.
- Verify canonical sequence, geometry, semantic, editability and
  clean-directory normalized-STEP hash-stability checks for every row.
- Audit split isolation and source-leak rejection.

## Attribution question and sampling intent

Distinguish deterministic candidate-production and family-isolation readiness
from any LLM capability claim.  Stop after the six frozen rows have either
passed the declared audits or produced a classified rejection; no substitution
or additional sampling is allowed.

## Inputs

- `docs/corpus/sequence-paired/reference-guided-through-hole-variation-v1-preregistration.json`
- Existing self-authored case-library candidate conventions and sequence-pair
  intake/audit helpers.

## Code and documentation paths

- `tools/build_m94_reference_guided_through_hole_variation_candidates.py`
- `tools/audit_sequence_paired_reference_guided_through_hole_variation.py`
- focused tests for those tools
- `docs/workflow/status.md`, this workpack and active handoff

## Trace/schema changes

No Harness, provider, runtime, report-schema or manifest change.  Candidate
metadata and deterministic reference scripts remain inside experimental
candidate directories only.

## Decision-package impact

- `decision_id`: M93/M94 reference-guided through-hole parameter-variation
  question.
- Q01/Q02 effect: creates no new observable, prompt, card or runtime action;
  it verifies deterministic oracle assets for later offline evaluation.
- Q03/Q04 effect: reuses existing offline geometry and sequence checks without
  altering a gate, repair rule or stopping policy.
- Evidence role: deterministic oracle, split-isolation and negative-control
  evidence only.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

Do not alter a manifest, provider payload, runtime resource, card, prompt,
Harness, executable registry, or hosted authorization.  Candidate assets stay
experimental and cannot become provider input.

## Acceptance

Run the M94 production checks, the generic intake audit, relevant focused
tests, Ruff, governance audit and `git diff --check`; record terminal outputs.

## Evidence reuse / guidance-card disposition

Experimental candidate evidence only; no experience card is created, mutated,
mounted or promoted.

## Owner acceptance

- Implemented the M94-only deterministic producer and family audit.  Each of
  the exact three development and three held-out rows was independently
  written in two clean temporary directories; normalized STEP bytes and
  SHA-256 digests matched before the experimental candidate was written.
- The audit passed all six input/replay geometry gate triplets, exact
  four-operation oracle sequences, one-solid/one-through-cut semantics, and
  all three declared mutations per row.  It separately rejects a candidate
  metadata `provider_payload` as a source leak and rejects split drift.
- Candidate metadata marks every asset `experimental` and records that no
  manifest, provider, training, runtime or registry path may consume it.
- 2026-08-10 terminal validation: M94 generic intake audit passed; focused
  tests passed (7 passed); fast suite passed (66 passed, 149 deselected);
  full pytest completed successfully; Ruff passed; governance audit passed;
  `git diff --check` passed.

## Status transition

After owner acceptance, Liaol independently verifies the exact six-row scope,
split isolation, candidate-only boundary and terminal audit evidence.  Update
`status.md` first, then move this workpack to `done/` and archive the active
handoff.  The only successor eligible for selection is M96; passing production
does not authorize hosted work.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-10.
- Review scope: confirmed the frozen six-row 3/3 family split, candidate-only
  boundary, clean-directory hash-stability evidence, sequence/geometry/
  semantic/editability audits and source-leak negative control.
- Closure rationale: M95 supplies only deterministic experimental oracle assets
  for M96.  It makes no runtime, provider, hosted or generalization claim.

## Out of scope

Runtime admission, provider use, card mutation, manifest promotion or a
parameter-generalization claim.
