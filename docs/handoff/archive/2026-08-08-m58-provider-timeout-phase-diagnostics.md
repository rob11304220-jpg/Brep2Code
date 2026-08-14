# Handoff: M58 provider timeout phase diagnostics

- **Date**: 2026-08-08
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M58-001-provider-timeout-phase-diagnostics`

## Goal

Add offline, non-sensitive lifecycle diagnostics that distinguish provider
worker startup, in-flight HTTP wait, and returned provider error paths.

## Done

- M54 has two timeout observations; both were terminated at the 120-second
  outer deadline and neither supports a model-quality conclusion.
- Implemented local lifecycle diagnostics for worker startup failure, HTTP
  wait at the outer deadline, and returned worker error. The diagnostic payload
  is restricted to phase names, monotonic elapsed milliseconds, and a
  sanitized error class.
- Owner checks passed: focused 17 tests, 76 sandbox tests, full 168-test suite,
  and Ruff. No provider was constructed for a real request or contacted.

## In progress

- None. Liaol independently approved M58 on 2026-08-08.

## Next

- No active workpack. A new bounded package is required before further work;
  M54 remains blocked and no hosted retry is authorized.

## Decisions

- M58 is offline only and cannot authorize a network probe or M54 retry.

## Blockers

- None for offline diagnostic implementation.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M58-001-provider-timeout-phase-diagnostics.md` |
| Provider boundary | `brep2code/agent/repair.py` |
| M54 report | `data/corpus-runs/m54-parametric-development-deepseek-observation-rerun-20260808.json` |

## Resume prompt

```
M58 is complete. Do not resume M54 or call a provider without a new bounded
workpack, fresh preflight, and explicit per-item authorization.
```
