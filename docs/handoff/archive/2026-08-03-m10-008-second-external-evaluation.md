# Handoff: M10-008 second external frozen-policy evaluation

- **Date**: 2026-08-03
- **Subproject**: `brep2code`
- **Status**: `done`

## Goal

Complete the split-preserving frozen-policy first-pass evaluation for the M10-007 2/1 external split.

## Done

- M10-007 admitted `00000027`, `00000030`, and `00000031` after bounded archive-order scanning; all hashes/probes/manifests and `wsl-bwrap` controls passed.
- M10-007 made no provider request or runtime behavior change.
- The separately authorized M10-008 development run completed at `data/corpus-runs/abc-v00-m10-008-development-pro-authorized-20260803.json` under the frozen two-case policy. It used 4/4 requests: both first passes were `script_failure` with no output STEP; `00000030` passed after one repair, while `00000027` ended `repair_exhausted`.
- The separately authorized held-out run completed at `data/corpus-runs/abc-v00-m10-008-held-out-pro-authorized-20260803.json` under the frozen one-case policy. Its first pass was `script_failure` with no output STEP; its one repair passed, using 2/2 requests.
- Published the sanitized split-preserving review at `docs/architecture/v1/m10-008-second-external-first-pass-evaluation-review.md`.

## In progress

- None.

## Next

- Create a separate evidence/routing workpack before selecting any next route; do not infer authorization for new hosted requests or Harness changes.

## Decisions

- Keep `deepseek-v4-pro`, `first-pass-summary-v1`, `wsl-bwrap`, existing gates, case order, one repair round, and the 120-second deadline frozen across splits.
- Held-out was preflighted and separately authorized; policy remained frozen across the completed splits.

## Blockers

- None for M10-008. Future hosted work remains subject to fresh explicit authorization.

## Key paths

- `docs/workpacks/active/WP-M10-008-second-external-first-pass-evaluation.md`
- `docs/corpus/external/abc-v00-m10-007-selection.json`
- `docs/corpus/external/abc-v00-m10-007-development-manifest.json`
- `docs/corpus/external/abc-v00-m10-007-held-out-manifest.json`

## Resume prompt

```
M10-008 is complete. Before any further work, read the M10-008 review and create or select a separate evidence/routing workpack; do not issue a new hosted request without fresh explicit authorization.
```
