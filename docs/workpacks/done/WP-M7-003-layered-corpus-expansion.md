# WP-M7-003: Layered Self-Authored Corpus Expansion

- Status: done
- Milestone: M7
- Owner: unassigned

## Goal

Expand the committed, self-authored STEP corpus to approximately 20–50 reproducible cases so first-pass and repair evaluation has broader, controlled coverage before any external dataset ingestion.

## Scope

- Define tiers and case-selection rules covering feature interaction, modeling-sequence length, scale or unit conditions, and similar exterior shapes with differing topology.
- Add small, version-controlled STEP fixtures, manifest expectations, geometry gates, and local reference scripts for every new case.
- Keep the full corpus usable through local, network-free manifest runs and fake-provider replay.
- Produce a review input that identifies whether new helper, probe, gate, IR, or SDK work is justified by completed evidence.

## Inputs

- [M7 evaluation roadmap](../../architecture/v1/m7-evaluation-roadmap.md)
- [Case corpus contract](../../architecture/v1/contracts/case-corpus.md)
- [M6 hosted evaluation report](../../architecture/v1/m6-hosted-evaluation-report.md)
- [Development case governance](../../corpus/README.md)
- Completed M7-001 and M7-002 evidence.

## Code paths

| Path | Purpose |
|------|---------|
| `case-library/self-authored/` | New self-authored STEP fixtures. |
| `case-library/manifests/self-authored/` | Manifest entries and reference scripts. |
| `brep2code/corpus/` | Manifest support only if a reviewed need emerges. |
| `tests/` | Manifest, gate, and replay coverage. |

## Docs to update

- Update the case-corpus contract, corpus review runbook, module map, status, handoff, and this workpack as needed.
- Record an ADR only if the completed corpus review justifies a lasting new abstraction or external-data policy.

## Trace/schema changes

Preserve the current manifest and report schema unless a documented, tested compatibility need arises. Each added case must have expected bbox, volume and/or topology expectations sufficient for its geometry gates, difficulty tags, and a local reference script.

## Compatibility constraints

- Existing P0/P1 cases and local replay behavior remain stable.
- New fixtures are self-authored, committed, and offline reproducible.
- Do not download, redistribute, or run public datasets in this workpack.
- Do not introduce an IR, project CAD SDK, CAD workplace, new probe, or new gate without a completed evidence review.

## Acceptance

- The committed corpus contains approximately 20–50 cases with documented tier coverage.
- Every added case validates through manifest loading, local Harness gates, and fake-provider reference replay.
- Full local corpus execution is repeatable without credentials or network access.
- A review report explicitly assesses the evidence threshold for narrow helpers, IR, SDK, probes, and gates.
- Full pytest and Ruff pass.

## Out of scope

- Public dataset ingestion, licensing review, normalization, or benchmark-scale execution.
- Hosted model comparison without a separately authorized evaluation workpack.

## Implementation evidence

- Added 14 committed, self-authored STEP fixtures and deterministic reference scripts, bringing the corpus to 21 cases: P0=3, P1=4, P2=9, P3=5.
- Added P2/P3 manifests, registry baselines and hashes, case cards, catalog entries, coverage design, and manifest-load coverage without changing the Harness, manifest schema, probes, or gates.
- Local `--repair` reports completed for every tier. P0 had 1 primary pass plus 2 replay passes; P1 had 4 replay passes; P2 had 9 replay passes; P3 had 5 replay passes. The 20 non-baseline primary failures are expected fixed-scaffold controls.
- Verification: focused corpus tests 30 passed; full pytest 59 passed; full Ruff passed. Registry audit verified all 21 fixture/script/card paths and SHA-256 values.
- Review: [`m7-corpus-expansion-review.md`](../../architecture/v1/m7-corpus-expansion-review.md) finds no evidence for a helper, IR, SDK, new probe, or new gate.
