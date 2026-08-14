# Handoff: M71 DeepSeek compatibility diagnostics

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done` (archived after independent approval)
- **Related workpack**: `WP-M71-001-deepseek-compatibility-diagnostics`

## Goal

Produce a deterministic, credential-free compatibility matrix for the current
DeepSeek adapter before any later stability experiment.

## Done

- User selected M71 after M70/M75 closure.
- `status.md` now records M71 as the sole active G2 workpack with Codex as
  owner and Liaol as independent reviewer.
- M71 was moved from backlog to active with a validation and collaboration
  plan; no provider request has been issued.
- Implemented a pure non-streaming JSON serializer, fail-closed rejection of
  unenforceable `max_output_chars`, and offline response-envelope fixtures.
- Added M76--M78 as backlog-only route planning; none grants hosted authority.
- Owner acceptance passed: final focused provider/worker tests (29), final
  full suite (180), Ruff, governance audit and `git diff --check`. The
  workpack records two earlier, corrected local test/lifecycle formatting
  failures for auditability.
- The post-M69 route is fully registered through M78: M72/M73 retain their
  existing backlog workpacks, and M76/M77/M78 are new backlog-only workpacks
  linked from the roadmap and workpack index.

## In progress

- None.

## Next

- Retain M72 as backlog pending fresh G3 preflight and itemized authorization.
- M72 → M73 → M76 → M77 → M78 remains a dependency-gated route; every hosted
  workpack still needs its own fresh preflight and itemized user authorization.

## Decisions

- Current non-streaming behavior is the only supported transport mode;
  streaming remains explicitly unsupported.
- `max_output_chars` fails before HTTP rather than silently suggesting an
  unenforced provider-side cap.

## Blockers

- None. M71 has been independently approved and closed.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M71-001-deepseek-compatibility-diagnostics.md` |
| Provider | `brep2code/agent/provider.py` |
| Tests | `tests/test_agent_m3_provider_trace.py`, `tests/test_agent_m3_repair_loop.py`, `tests/test_observed_build_loop.py` |
| Route | `docs/workpacks/backlog/WP-M72-001-bounded-deepseek-stability-experiment.md` through `WP-M78-001-p1-progressive-hosted-evaluation.md` |
| Commands | `uv run python -m pytest tests\\test_agent_m3_provider_trace.py tests\\test_agent_m3_repair_loop.py tests\\test_observed_build_loop.py -q` |

## Resume prompt

```
Review M71 DeepSeek compatibility diagnostics.
Read docs/handoff/active/2026-08-09-m71-deepseek-compatibility-diagnostics.md.
First action: inspect the active workpack's compatibility matrix and validation record, then record Liaol's independent approval or requested changes.
```
