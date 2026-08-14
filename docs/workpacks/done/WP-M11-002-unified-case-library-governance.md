# WP-M11-002: Unified Case-Library Governance and Consolidation

- Status: done
- Milestone: M11
- Owner: unassigned

## Goal

Create a development-only unified case-library index that relates existing B-Rep fixtures, optional reference sequences, external raw-asset boundaries, candidate datasets, and runtime evidence without moving assets or changing Harness behavior.

## Scope

- Establish the tracked catalog, external admission template, maintenance runbook, and architecture decision.
- Index the existing self-authored and ABC collections and record the candidate order: self-authored families, Fusion 360 Gallery Reconstruction, DeepCAD, Brep2Seq synthetic data, then ABC robustness use.
- Update corpus/module/workflow documentation and create a handoff.

## Inputs

- `docs/corpus/registry/self-authored.json`
- `docs/corpus/external/registry.json`
- Current committed fixtures and ignored `data/` layout

## Trace/schema changes

None.  The catalog is development governance only; it does not change `signal_bundle.json`, corpus manifest/report schema, CLI JSON, or record storage.

## Compatibility constraints

- Existing `tests/fixtures` paths, p0--p3 manifests, ignored raw external assets, default offline commands, gates, and hosted authorization boundaries remain unchanged.
- No download, provider request, fixture promotion, new IR, or dataset-ingestion runtime module.

## Acceptance

- A developer can locate the current input B-Rep, reference-script/sequence status, manifest, and runtime-evidence role for self-authored and ABC collections from one tracked catalog.
- The next three candidates and their admission prerequisites are explicit.
- The maintenance procedure prevents raw-data redistribution and implicit runtime activation.
- Documentation link and JSON syntax checks pass.

## Status transition

When complete, update `docs/workflow/status.md`, this workpack, the workpack index, and the active handoff; move this workpack to `done/`.

## Out of scope

Fusion/DeepCAD/Brep2Seq download or admission, source-history translation, corpus-runner changes, fixture relocation, hosted evaluation, or benchmark claims.

## Completion

Completed offline on 2026-08-03. Added the tracked unified library catalog, candidate-admission template and maintenance runbook; indexed existing self-authored and ABC collections; and recorded the no-relocation boundary in ADR-0012. JSON parsing and `git diff --check` passed. No fixture, raw asset, Harness, CLI, schema, gate, provider, or hosted-policy change occurred.
