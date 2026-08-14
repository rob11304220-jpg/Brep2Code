# Handoff: M97 reference-guided parameter-variation development calibration

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M97-001-reference-guided-parameter-variation-development-hosted-calibration`

## Goal

Implement and offline-validate the frozen M97 development card/no-card
calibration path, then conduct a read-only hosted preflight.  No provider
request may occur without separate itemized user authorization.

## Done

- M93 design and M94 preregistration froze the exact three-development and
  three-held-out rows.
- ADR-0057 and the M95--M99 backlog route define the paired hosted experiment
  only after offline readiness.
- M95 is complete and independently approved: exactly six experimental
  candidates passed hash-stability, sequence, geometry, semantic, editability,
  split-isolation and source-leak audits.
- M96 is complete and independently approved: development-only measured facts,
  source-field rejection and M97/M98 policy/card/hash pins are frozen.
- M97 is now active; no provider request has been made.

## In progress

- M97 has a distinct fixed three-development-row card/no-card fake-provider
  CLI path. Its six terminal conditions passed locally with exact 9/9 request
  accounting. A DeepSeek-only 0/9 → issued → terminal durable checkpoint path
  and all required offline/no-input/preflight checks are complete. The one
  authorized hosted lifecycle terminalized as `interrupted` after 3/9 issued
  requests; the remaining capacity is not reusable.

## Next

1. Obtain Liaol's independent review of M97's terminal report and M70 state.
2. Do not run another provider request. A new hosted attempt needs a new
   bounded workpack, new report/monitor paths, and new itemized authorization.

## Decisions

- Parameter variation uses offline production → offline admission → paired
  development hosted calibration → paired held-out evaluation → independent
  review; see [ADR-0057](../../architecture/adr/0057-reference-guided-parameter-variation-evaluation-route.md).
- M96 is offline only; it cannot authorize hosted egress or an LLM/generalization claim.

## Blockers

- M97 is closed after Liaol's independent review. The sole authorization
  terminalized after 3/9 issued requests: low-row card generation failed the
  OCP API contract, then the following baseline request timed out at the
  120-second deadline. This is non-passing terminal evidence only; retry,
  repair, later rows and capacity reuse are prohibited.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/active/WP-M97-001-reference-guided-parameter-variation-development-hosted-calibration.md` |
| Frozen contract | `docs/corpus/sequence-paired/reference-guided-through-hole-variation-v1-preregistration.json` |
| Frozen policy | `docs/corpus/sequence-paired/reference-guided-through-hole-variation-v1-m96-policy.json` |
| Preflight | `docs/workflow/m97-reference-guided-development-hosted-preflight.md` |
| Terminal report | `data/corpus-runs/m97-reference-guided-through-hole-development-calibration.json` |
| Terminal monitor | `data/monitor-runs/m97-reference-guided-through-hole-development-calibration.monitor.json` |
| Route | `docs/architecture/v1/four-track-program-roadmap.md` |
| Commands | `uv --cache-dir .uv-cache run python tools/check_governance.py` |

## Resume prompt

```
M97 is closed. Do not resume it from this handoff. A future hosted attempt
requires Liaol to select a new bounded workpack with fresh paths and a new
itemized authorization; M98 held-out evaluation remains unauthorized.
```
