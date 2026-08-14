# Handoff: M135-003 Frozen Epoch CLI and Monitor Contract

- **Date**: 2026-08-12
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M135-003-frozen-epoch-cli-contract`

## Goal

Build and offline-validate the missing executable CLI/report/monitor contract
for M134's unchanged frozen 18-condition epoch, without provider construction,
credentials or egress.

## Done

- M135-002 established that hashes, fake accounting and no-input controls pass.
- M135-002 also established that the actual M135 CLI/monitor surface is absent.
- M135-003 adds `m135-epoch-preflight`, a local-only 0/18 checkpoint and
  distinct monitor-state preparation command with fixed frozen contract values.
- Focused tests, fast regression, full suite and Ruff passed; no provider was
  constructed, credential read or data sent.

## In progress

- Complete. M135-004 is the separately selected successor.

## Next

- Run M135-004's full fresh local preflight. Do not construct a provider, send
  data or request authorization until every local control and an independent
  G3 review pass.

## Decisions

- M135-003 preserves the frozen M134 cohort and the M135-001/M135-002 no-reuse
  boundary.
- This workpack cannot authorize, construct or invoke a hosted provider.

## Blockers

- None for M135-003. Liaol approved the independent G3 review on 2026-08-12.

## Key paths

| Kind | Path |
|---|---|
| Active workpack | `docs/workpacks/active/WP-M135-003-frozen-epoch-cli-contract.md` |
| Prior blocker | `docs/workflow/m135-002-fresh-reentry-preflight.md` |
| Epoch helpers | `brep2code/agent/m135_epoch.py` |
| CLI | `brep2code/cli/__init__.py` |
| Epoch tests | `tests/test_m135_epoch.py` |
| Evidence record | `docs/workflow/m135-003-frozen-epoch-cli-contract.md` |

## Resume prompt

    M135-003 is complete. Resume M135-004 using its active handoff and
    workpack. Complete only the full credential-free local preflight; do not
    construct a provider, access credentials, send data or request
    authorization.
