# Handoff: M10-005 frozen-policy external first-pass evaluation

- **Date**: 2026-08-02
- **Subproject**: `brep2code`
- **Status**: `blocked`

## Goal

Complete the read-only development-split hosted preflight for the M10-003 ABC increment, then obtain separate explicit authorization before any provider request; keep held-out execution frozen until development evidence is reviewed.

## Done

- M10-003 admitted a deterministic local ABC increment: archive members 23–26 were boundedly scanned, 23/24/26 accepted, and 25 rejected for three solids.
- The 2-case development and 1-case held-out manifests have tracked source identity, SHA-256, probe baselines, local-only license boundary, and no external scripts.
- All three hashes matched and both ignored `wsl-bwrap` controls completed with readable inputs/outputs and successful scripts; fixed-scaffold geometry failures are expected control evidence.
- The separately authorized development first-pass run completed under frozen `deepseek-v4-pro`/`wsl-bwrap` policy with 3/4 requests: one provider lifecycle result, one script failure, and one repair pass.
- Held-out preflight passed its hash, configuration, executor, frozen 1-case/1-round/120-second policy, 2-request capacity, and new report-path checks; no held-out request was issued.

## In progress

- Wait for held-out authorization. The development report is complete; the held-out preflight is complete but it has not been authorized.

## Next

- Obtain explicit held-out authorization covering `deepseek-v4-pro`, bounded probe-summary egress, 1 case, one repair round, 120-second provider deadline, and up to 2 requests.
- After the held-out report completes, write the sanitized split-preserving review before activating M10-006.

## Decisions

- No provider request is authorized by M10-003 or this handoff; each split requires fresh explicit user authorization.
- The M10-003 metadata-only admission review is [`m10-003-abc-external-increment-review.md`](../../architecture/v1/m10-003-abc-external-increment-review.md); raw assets and reports remain ignored.
- Keep existing model, `first-pass-summary-v1` context policy, `wsl-bwrap`, existing gates, case order, one repair round, and 120-second deadline unchanged across splits.

## Blockers

- Held-out requires explicit user authorization after its completed preflight.

## Key paths

- `docs/workpacks/active/WP-M10-005-frozen-policy-external-first-pass-evaluation.md`
- `docs/corpus/external/abc-v00-m10-003-selection.json`
- `docs/corpus/external/abc-v00-m10-003-development-manifest.json`
- `docs/corpus/external/abc-v00-m10-003-held-out-manifest.json`
- `docs/runbooks/llm-provider-config.md`

## Resume prompt

```
Continue M10-005. Development completed under the frozen policy; held-out preflight is complete. Do not issue a held-out provider request until the user explicitly authorizes deepseek-v4-pro, bounded probe-summary egress, 1 case, one repair round, a 120-second deadline, and a 2-request maximum.
```
