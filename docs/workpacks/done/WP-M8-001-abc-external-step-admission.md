# WP-M8-001: ABC External STEP Admission and Offline Baseline

- Status: done
- Milestone: M8
- Owner: unassigned

## Goal

Create a small, reproducible local ABC v00 STEP baseline without committing external CAD assets or changing the default Harness path.

## Scope

- Lock ABC v00 source, terms boundary, archive identity, deterministic selection record and 8/4 development/held-out split.
- Keep raw archives, extracted STEP files and reports only under ignored `data/datasets/abc/v00/` and `data/corpus-runs/`.
- Run existing probe and corpus paths locally; no hosted provider, repair replay, data conversion, new gate, probe, IR or SDK.

## Inputs

- [ABC selection](../../corpus/external/abc-v00-m8-001-selection.json)
- [Case corpus contract](../../architecture/v1/contracts/case-corpus.md)
- [Case corpus review runbook](../../runbooks/case-corpus-review.md)

## Acceptance

- Twelve unique selected samples retain source ID, STEP path, SHA-256 and exactly eight development plus four held-out labels.
- All selected files hash-match, load through the manifest and have baseline bbox/count/volume evidence from the existing input probe.
- A completed local corpus report exists under ignored `data/corpus-runs/`; fixed-scaffold geometry failures are control evidence, not an admission failure.
- Full pytest and Ruff pass. Existing P0--P3 behavior remains unchanged.

## Out of scope

- Committing or redistributing ABC assets, hosted evaluation, source conversion, and architecture expansion.

## Implementation evidence

- Locked ABC `v00`, its official STEP index and local-research/no-redistribution boundary in the external registry and selection record.
- Downloaded one ignored STEP archive, scanned the first 24 archive members and selected the first 12 single-solid inputs after 11 recorded multi-solid rejections; the split is 8 development and 4 held-out.
- SHA-256 verified all 12 local files. Their explicit manifest loaded and its `wsl-bwrap` corpus report completed with all scripts exiting 0; 2 fixed-box controls passed and 10 cases produced expected geometry-gate failures.
- Added static selection/manifest audit coverage and an explicit offline corpus `--executor wsl-bwrap` option while retaining `unsafe-local` as the default.
- Verification: focused corpus tests 32 passed; full pytest 61 passed; Ruff passed.
