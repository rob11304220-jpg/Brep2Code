# Handoff: M82 generated-script API contract alignment

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M82-001-generated-script-api-contract-alignment`

## Goal

Fail closed before sandbox execution when a generated build script imports a
known unavailable CAD API, while retaining OCP-script compatibility.

## Done

- User selected M82 after M80 classified the generated `cadquery` import as
  the end-to-end failure.
- Implemented and locally verified the static OCP/CAD-import contract gate.

## In progress

- None.

## Next

- M82 is reviewed and closed. Start the separately selected M83 reference-case
  taxonomy and candidate-reference-pack workpack when implementation begins.

## Decisions

- This is offline API alignment only; it does not retry or otherwise change
  M80's provider request, prompt, case, executor, or consumed budget.

## Blockers

- None for M82. M19 retrieval remains evidence-gated.

## Key paths

| Kind | Path |
|------|------|
| Branch | `main` |
| Workpack | `docs/workpacks/active/WP-M82-001-generated-script-api-contract-alignment.md` |
| Code | `brep2code/agent/harness.py` |
| Commands | `uv run python -m pytest tests\\test_harness_m2.py tests\\test_observed_build_loop.py -q` |

## Resume prompt

```
Continue Brep2Code M82 generated-script API contract alignment.
Read docs/handoff/active/2026-08-10-m82-generated-script-api-contract.md.
First action: implement the static pre-execution OCP/CAD-import validator and
its deterministic regression tests; do not make any hosted request.
```
