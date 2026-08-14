# Handoff: M8-001 ABC external STEP admission

- **Date**: 2026-08-02
- **Subproject**: `brep2code`
- **Status**: `complete`

## Goal

Record the completed explicit, local-only ABC v00 STEP admission baseline for twelve selected single-solid samples.

## Done

- Locked the official ABC v00 STEP source and local-research/no-redistribution boundary.
- Downloaded only `abc_0000_step_v00.7z` into ignored `data/datasets/abc/v00/archives/`.
- Extracted and probed the first 24 archive STEP entries; selected the first 12 single-solid inputs (8 development, 4 held-out) and recorded 11 multi-solid rejections before the selection cutoff.
- Added tracked selection metadata, explicit local manifest, static audit coverage and M8 workpack.

## In progress

- No active implementation workpack.

## Boundaries

- ABC assets, extraction output and reports remain ignored under `data/`.
- Do not use hosted provider, fake replay, conversion, new probes, gates, IR or SDK without a new workpack.
- Default tests and corpus commands must not discover or download this local corpus.

## Resume prompt

```
Continue Brep2Code after M8-001 completion. Read docs/workflow/status.md and wait for explicit direction before creating or activating a new workpack.
```
