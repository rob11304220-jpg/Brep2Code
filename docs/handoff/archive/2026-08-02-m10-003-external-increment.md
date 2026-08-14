# Handoff: M10-003 deterministic external corpus increment

- **Date**: 2026-08-02
- **Subproject**: `brep2code`
- **Status**: `active`

## Goal

Admit one small, deterministic local ABC STEP increment and establish its hash-verified `wsl-bwrap` offline baseline, without issuing provider requests or changing the default offline boundary.

## Done

- M9 development and held-out first-pass reports both completed under unchanged `deepseek-v4-pro`/`wsl-bwrap` policy.
- M10-001 reviewed completed split evidence and selected M10-003 because no helper attribution threshold or geometry-diagnostics trigger was established.

## In progress

- Identify the bounded deterministic scan and selection for one local external increment from the existing ABC archive.

## Next

- Read `WP-M10-003`, the M8 selection record and corpus governance; create the reviewed local selection/manifests, hash/probe them, then run `wsl-bwrap` offline controls.

## Decisions

- No hosted request, helper, IR, SDK, probe, gate, conversion, external reference script, or benchmark claim is in scope for M10-003.
- Preserve local research-only assets and tracked metadata-only evidence.
- The route selection is recorded in [`m9-abc-hosted-evaluation-review.md`](../../architecture/v1/m9-abc-hosted-evaluation-review.md) under [ADR-0009](../../architecture/adr/0009-evidence-gated-post-m9-evolution.md).

## Blockers

- None. Hosted use of any new external input requires a later workpack and new explicit authorization.

## Key paths

- `docs/workpacks/active/WP-M10-003-deterministic-external-corpus-increment.md`
- `docs/architecture/v1/m9-abc-hosted-evaluation-review.md`
- `docs/corpus/external/abc-v00-m8-001-selection.json`
- `docs/corpus/README.md`

## Resume prompt

```
Continue M10-003. Read docs/workflow/status.md, WP-M10-003, docs/corpus/README.md, and the M8 selection record. Admit one small deterministic local ABC increment, then verify its hashes, probes, manifests, and wsl-bwrap offline controls. Do not issue a provider request.
```
