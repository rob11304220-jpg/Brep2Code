# WP-M10-003: Deterministic External Corpus Increment

- Status: done
- Milestone: M10
- Owner: unassigned

## Goal

Admit one small, deterministic external STEP increment to improve failure coverage while preserving the local-only and offline baseline boundary.

## Trigger condition

`WP-M10-001` selects this route when no attributable helper pattern reaches the roadmap threshold or when completed M9 evidence is insufficient to establish a stable failure pattern.

## Scope

- Create a new reviewed selection record from an existing local upstream archive using a documented deterministic order and bounded scan.
- Record source identity, SHA-256, license boundary, probe admission, split, and normalization decision for every accepted input.
- Create explicit local manifests and run hash-verified `wsl-bwrap` offline controls.

## Inputs

- [External corpus governance](../../corpus/README.md)
- [M8 selection record](../../corpus/external/abc-v00-m8-001-selection.json)
- [Post-M9 roadmap](../../architecture/v1/post-m9-evidence-gated-roadmap.md)

## Code paths

- `docs/corpus/external/`
- `tests/test_corpus_m4.py`

## Docs to update

Update the external registry/selection records, corpus documentation, review, status, active handoff, and runbook only when repeatable procedure changes.

## Trace/schema changes

None expected. Use the existing manifest and report schema unless a separate ADR approves a contract change.

## Compatibility constraints

Raw assets remain ignored under `data/datasets/`; no default test downloads or discovers them. No accepted external entry contains `reference_script` or `first_pass_script`. This workpack does not authorize hosted evaluation.

## Acceptance

- Selection is deterministic, bounded, split-preserving, and auditable from tracked metadata without raw-asset redistribution.
- Every selected local file hash-matches, probes successfully, and completes a `wsl-bwrap` offline control.
- Existing committed self-authored corpus and default commands remain unchanged.

## Status transition

When done, record the admission review, update status and handoff, and move this workpack to `done/`. Any hosted use of the new split requires a separate workpack and explicit authorization.

## Implementation evidence

- Continued archive-member order after M8-001 cutoff `00000022`, scanned `00000023` through `00000026`, accepted 23/24/26 as single-solid inputs, and recorded 25 as a three-solid rejection.
- Recorded the 2/1 development/held-out split, hashes, source identities, normalization boundary, and probe baselines in `abc-v00-m10-003-selection.json`; manifests contain no reference or first-pass scripts.
- Reverified all three hashes and completed ignored `wsl-bwrap` development and held-out controls. Every input and output was readable and every script exited 0; all fixed-scaffold geometry failures were expected control evidence.

## Out of scope

Bulk archive extraction, provider calls, source conversion, external reference scripts, benchmark claims, helper, IR, SDK, FEA, VLM judging, and multi-agent orchestration.
