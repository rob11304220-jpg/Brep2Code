# WP-M10-007: Second Deterministic External Corpus Increment

- Status: done
- Milestone: M10
- Owner: unassigned

## Goal

Admit one further small, deterministic local ABC STEP increment after the M10-006 completed-evidence review, preserving the local-only and offline boundary.

## Trigger condition

M10-006 found neither three executable geometry failures nor three direct repeated helper attributions in the completed M10-005 split reports.

## Scope

- Continue the existing local ABC archive in documented member order after M10-003 cutoff `00000026`.
- Use a bounded scan, record every rejection, retain source identity/SHA-256/probe/split/license/normalization metadata, and create explicit local manifests.
- Verify hashes, input probes, and `wsl-bwrap` fixed-scaffold controls before any later hosted consideration.

## Compatibility constraints

- Raw assets and reports remain ignored under `data/`; default tests and commands must not discover or download them.
- No provider request, conversion, external reference script, first-pass fixture, prompt change, probe, gate, helper, IR, SDK, or benchmark claim is in scope.

## Acceptance

- The admission is deterministic, bounded, split-preserving, and auditable from tracked metadata without asset redistribution.
- Each accepted local file hash-matches, probes successfully, and appears in a completed `wsl-bwrap` offline control.
- Existing committed corpus behavior and default offline commands remain unchanged.

## Status transition

When complete, write the admission review, update status and handoff, and move this workpack to `done/`. Any hosted use requires a later workpack and new explicit authorization.

## Implementation evidence

- Continued archive-member order from `00000027` through `00000031`; accepted 27, 30, and 31 as single-solid inputs and recorded 28/29 as multi-solid rejections.
- Tracked the 2/1 split, source identities, SHA-256 values, probe baselines, license boundary, and no-conversion decision; manifests have no reference or first-pass scripts.
- All selected files hash-matched, passed focused static audit coverage, and completed ignored development/held-out `wsl-bwrap` controls with readable inputs/outputs and script exits; fixed-scaffold geometry failures were expected controls.
