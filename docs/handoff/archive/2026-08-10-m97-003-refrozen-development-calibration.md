# Handoff: M97-003 re-frozen development calibration

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M97-003-reference-guided-parameter-variation-refrozen-development-calibration`

## Goal

Freeze and preflight a fresh, development-only M97 calibration after the
completed M97-002 repair; no provider request may occur before a new itemized
authorization.

## Done

- M97-002 is closed with Liaol's independent G2 review.
- User selected this new bounded G3 development-calibration workpack.
- M97-003 policy and read-only hosted preflight passed; no provider was called.
- The one authorized run completed with 9/9 requests: card 3/3 pass, baseline
  2/3 pass. No retry, repair, held-out row or capacity reuse occurred.
- Liaol independently approved G3 closure on 2026-08-11.

## In progress

- None. M97-003 is closed.

## Next

1. Do not retry M97-003 or select M98 from this result.
2. Any later provider experiment requires a new user-selected workpack,
   preflight and itemized authorization.

## Decisions

- [ADR-0058](../../architecture/adr/0058-m97-observation-contract-remediation.md)
  requires a new experiment and authorization after M97-002.

## Blockers

- No implementation blocker. All M97-003 capacity is consumed; no retry or
  additional request is permitted.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M97-003-reference-guided-parameter-variation-refrozen-development-calibration.md` |
| Prior repair | `docs/workpacks/done/WP-M97-002-reference-guided-parameter-variation-observation-contract-remediation.md` |
| M96 policy | `docs/corpus/sequence-paired/reference-guided-through-hole-variation-v1-m96-policy.json` |
| M97-003 policy | `docs/corpus/sequence-paired/reference-guided-through-hole-variation-v1-m97-003-policy.json` |
| Preflight | `docs/workflow/m97-003-reference-guided-development-hosted-preflight.md` |
| Terminal report | `data/corpus-runs/m97-003-reference-guided-through-hole-development-calibration.json` |
| Monitor state | `data/monitor-runs/m97-003-reference-guided-through-hole-development-calibration.monitor.json` |
| ADR | `docs/architecture/adr/0058-m97-observation-contract-remediation.md` |

## Resume prompt

```
M97-003 is closed. Do not issue provider requests, reuse capacity or inspect
held-out rows based on this development-only result.
```
