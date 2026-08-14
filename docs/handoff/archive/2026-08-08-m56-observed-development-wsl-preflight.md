# Handoff: M56 observed-development WSL preflight

- **Date**: 2026-08-08
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M56-001-observed-development-wsl-preflight`

## Goal

Prove the explicit multi-case M48 observation-only path with a fake provider
through `wsl-bwrap` before M54 can resume its hosted preflight.

## Done

- M54 is blocked and archived pending this G2 evidence.
- Fake two-case `observed-development --executor wsl-bwrap` regression passes
  with no input mount and path-free provider messages.
- Owner acceptance passed: focused 8/8 in 32.55s, sandbox 72/72 in 167.37s,
  and full suite 164/164 in 181.39s; Ruff, governance and whitespace checks
  passed.
- Liaol completed the independent G2 review on 2026-08-08 and approved M56.

## In progress

- M56 is complete and its workpack/handoff should be archived.

## Next

- Ask Liaol to independently review M56 scope, WSL no-input/egress regression,
  acceptance output, and lifecycle alignment. Do not resume M54 before it
  passes fresh preflight after M56 closes.

## Decisions

- The new executor option applies only to explicit observed-development fake
  preflight; hosted routing remains separately authorization-gated.

## Blockers

- None for M56. M54 remains blocked until this workpack closes and a fresh
  hosted preflight passes.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/active/WP-M56-001-observed-development-wsl-preflight.md` |
| CLI | `brep2code/cli/__init__.py` |
| Regression | `tests/test_observed_build_loop.py` |

## Resume prompt

```
Continue M56 offline only. Run its acceptance gates and obtain Liaol review.
Do not resume M54 or issue a provider request.
```
