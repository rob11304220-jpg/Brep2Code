# WP-TRG-028: Reference-Knowledge Projection and Evaluation

- Status: deferred
- Owner: unassigned
- Reviewer: independent reviewer required
- Risk tier: G2

## Entry condition

`WP-TRG-027` has produced an independently reviewed immutable admission record
for one bounded knowledge unit, `WP-TRG-029` has independently reviewed its
development-side admission-profile crosswalk, and the user selects this
workpack. The activation package must also cite
`docs/architecture/v1/runtime-and-hosted-entry-boundary-v1.md` and show which
required authority inputs it is reusing plus which runtime-projection artifact
it will freeze separately. A card, SDK, IR or retrieval system is not presumed
by this entry condition.

## Goal

Decide, derive and evaluate the smallest safe runtime projection from that
admission record for one declared task, while preserving the separate
authorities of case cards, reference packs, runtime cards, SDK/IR and case
library.

## Scope

- Produce a comparison and explicit selection criteria for: human case cards,
  development reference packs, hash-bound runtime action/diagnosis cards,
  SDK/tool schemas, IR/sequence records and retrieval indexes.
- Require a compact, applicability-scoped, provenance-linked runtime projection
  with source-record linkage, source/projection hashes, split boundary,
  applicability/prohibition conditions, counterexamples and a review trigger;
  prohibit scripts, raw STEP, local paths, held-out answers and unrestricted
  directory/index retrieval.
- Implement only the selected minimal projection and a no-reference/wrong-
  reference/explicit-reference offline ablation with fixed case/split/budget
  contracts.
- Treat RAG as evidence for retrieval provenance and ablation discipline, not
  as evidence that general retrieval or any CAD card is useful.
- Reuse the M155 entry-boundary document as a selection gate only: it fixes the
  required authority inputs and separate-freeze obligations, but does not
  choose the projection form in advance.

## Compatibility constraints

Admission records remain immutable evidence sources. Case cards remain
human/development navigation; packs remain development-only; the case library
remains evidence/oracle storage; an SDK is an action surface; and an IR is a
representation/validation surface. None becomes LLM context or retrieval
material merely because it exists. This workpack is offline and cannot
authorize hosted use or broad card promotion.

## Acceptance

```powershell
uv run python -m pytest tests -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Out of scope

Provider calls, training/fine-tuning, vector-store ingestion of the case
library, multi-family generalization claims and changes to completed M135/M138
evidence.
