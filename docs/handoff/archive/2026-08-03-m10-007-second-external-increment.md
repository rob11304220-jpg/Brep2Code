# Handoff: M10-007 second deterministic external corpus increment

- **Date**: 2026-08-03
- **Subproject**: `brep2code`
- **Status**: `active`

## Goal

Admit a second small, deterministic local ABC STEP increment after completed M10-005/M10-006 evidence, then establish its hash-verified `wsl-bwrap` offline baseline without issuing provider requests.

## Done

- M10-005 development and held-out first-pass reports completed under separately authorized frozen `deepseek-v4-pro`/`wsl-bwrap` policy.
- M10-006 reviewed all three completed cases: one provider lifecycle outcome and two trace-supported unknown script failures; no geometry or direct-helper threshold was met.
- M10-006 selected the existing deterministic local increment route and activated M10-007.

## In progress

- Continued the existing local ABC archive in member order: `00000027` was accepted as a readable single-solid input (74 faces) and hash-verified; `00000028` was rejected because the existing probe reported three solids. The bounded scan currently ends at `00000028`.

## Next

- Continue at `00000029`, probe successive members only until the small split-preserving increment is complete, record metadata and hashes, create explicit manifests, then complete `wsl-bwrap` controls.

## Decisions

- The M10-005 evaluation review and M10-006 attribution review are local sanitized engineering evidence, not benchmark results.
- No hosted request, conversion, external script, prompt change, helper, IR, SDK, probe, or gate is authorized by M10-007.
- The new increment must preserve raw-asset ignoring and the local-research-only ABC license boundary.

## Blockers

- None. Any later hosted use requires a separate workpack and new explicit authorization.

## Key paths

- `docs/workpacks/active/WP-M10-007-second-deterministic-external-increment.md`
- `docs/architecture/v1/m10-005-external-first-pass-evaluation-review.md`
- `docs/architecture/v1/m10-006-external-failure-attribution-review.md`
- `docs/corpus/external/abc-v00-m10-003-selection.json`

## Resume prompt

```
Continue M10-007. Read the active workpack and M10-006 attribution review. Resume the bounded local archive scan at ABC source sample 00000029; 00000027 is accepted and 00000028 is rejected for three solids. Complete one split-preserving increment, then verify hashes, probes, manifests, and wsl-bwrap controls. Do not issue a provider request.
```
