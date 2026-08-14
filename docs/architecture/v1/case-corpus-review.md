---
type: plan
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - M4
  - case-corpus
---

# M4 — Case Corpus Review

M4 uses a small, explicit case corpus to review the Harness-first loop before adding more abstractions. The goal is to collect concrete success/failure evidence, not to make benchmark claims.

## Goals

- Build a manifest-driven case corpus for B-Rep to executable CAD script experiments.
- Run current Harness gates across cases and produce corpus-level reports.
- Replay selected cases through the fake-provider repair loop or hand-authored replacement scripts.
- Identify whether failures point to prompt/context gaps, missing probe/action tools, geometry gates, or a need for IR/SDK/CAD workplace.

## Case Tiers

| Tier | Source | Purpose |
|------|--------|---------|
| P0 | Existing smoke fixtures: box, cylinder, block-with-hole | Keep baseline coverage small and deterministic. |
| P1 | Self-authored parametric shapes | Cover holes, chamfers, arrays, and boolean combinations. |
| P2 | Small real STEP samples | Expose real-world naming, units, and topology variation. |
| P3 | Edge/failure cases | Exercise thin walls, tiny faces, bad topology, unit mismatch, and unreadable inputs. |

P0 and P1 are enabled through committed local manifests. P2/P3 require separate workpacks when enabled.

## Case Manifest

The manifest should be structured data, with one entry per case:

| Field | Meaning |
|------|---------|
| `case_id` | Stable id used in record ids and reports. |
| `tier` | `P0`, `P1`, `P2`, or `P3`. |
| `input_step` | Repository-relative STEP input path. |
| `expected_bbox` | Optional expected bbox used for sanity checks. |
| `expected_counts` | Optional expected topology counts. |
| `expected_volume` | Optional expected volume. |
| `difficulty_tags` | Short tags such as `box`, `hole`, `boolean`, `thin-wall`. |
| `reference_script` | Optional repository-relative replacement script for fake-provider replay. |
| `notes` | Short implementation-side note. |

## Review Outputs

- Per-case Harness status, gate statuses, and key metrics.
- Corpus summary table grouped by tier and failure type.
- Repair replay summary for cases with reference scripts.
- Review notes that map observed failures to likely next actions:
  - improve repair context/prompt
  - add probe tool or action
  - strengthen gates
  - consider IR/SDK/CAD workplace
  - defer as dataset or hosted-provider concern

## Non-Goals

- No hosted LLM requirement.
- No dataset-scale evaluation.
- No quality claims about reconstruction.
- No commitment to IR, SDK, or CAD workplace before case evidence exists.
