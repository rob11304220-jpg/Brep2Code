# Handoff: Fusion 360 local control manifest

- **Date**: 2026-08-04
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Create and audit separate, non-default local-only development and held-out
manifests for the three M14 replay-pass Fusion cases.

## Done

- M15 approved only this M16 route.
- The M14 selection/replay evidence fixes the 2 development/1 held-out cases,
  hashes, source families, official splits and existing gate outcomes.
- Parsed both manifests with `load_case_manifest`; all paths, SHA-256 values,
  official splits, source-family isolation and absent script fixtures passed.

## Next

- M17 remains conditional backlog; do not run a corpus or advance it
  automatically.

## Decisions

- Use separate development and held-out manifest files to preserve split
  boundaries even for local controls.
- No corpus run, provider request, hosted evaluation or replay-syntax expansion
  occurred in M16.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/done/WP-M16-001-fusion360-local-control-manifest.md` |
| Selection | `docs/corpus/external/fusion360-gallery-r1.0.1-m14-001-selection.json` |
| Manifests | `docs/corpus/external/fusion360-gallery-r1.0.1-m16-001-*-manifest.json` |
