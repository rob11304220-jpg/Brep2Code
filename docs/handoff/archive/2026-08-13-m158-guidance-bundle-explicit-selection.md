# Handoff: M158 GuidanceBundle explicit selection

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `done` (archived after G2 closure)
- **Related workpack**: `WP-M158-001-guidance-bundle-explicit-selection`

## Goal

Allow trusted Harness-side code to explicitly declare one hash-bound guidance
card and compatible roles without enabling runtime card discovery or retrieval.

## Done

- User selected the bounded M157 remediation workpack.
- The blocker is confirmed in `GuidanceCardBridge._dispatch`: it hard-codes
  `vertical-cylinder-construction` and global roles.

## In progress

- None. M158 is closed.

## Next

- M157 may resume its bounded projection and three-arm offline ablation. Do
  not activate case testing or hosted work.

## Decisions

- Selection remains trusted Harness-side construction from explicit paths; the
  runtime caller never supplies a card ID.
- Only the bundle's declared role enum is exposed. The selected card must be
  the exact hash-pinned file declared by the bundle and listed in its index.
- Focused bridge tests, fast tests, Ruff, runtime-guidance audit, and governance
  audit pass. M160's final full suite included M158's code and passed with
  `284 passed in 502.06s` after M159/M160 resolved the lifecycle/audit blockers.
- Liaol approved the independent G2 review on 2026-08-13, allowing M158 to
  close and M157 to resume without retrieval or authority widening.

## Blockers

- None. M159 closed the registry/case lifecycle conflicts without changing
  M158's Harness scope.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M158-001-guidance-bundle-explicit-selection.md` |
| Blocked successor | `docs/workpacks/archive/WP-M157-001-selector-ambiguity-runtime-projection-blocked.md` |
| Bridge | `brep2code/agent/guidance.py` |
| Tests | `tests/test_guidance_bridge.py` |

## Resume prompt

```
Continue Brep2Code M158: implement explicit hash-bound single-card GuidanceBundle
selection. Preserve opt-in, one-card, no-search behavior. Do not create the
M157 selector card or enter provider/hosted work.
```
