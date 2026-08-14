# Handoff: M97 observation-contract remediation

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M97-002-reference-guided-parameter-variation-observation-contract-remediation`

## Goal

Complete the offline, development-only M97-002 repair so the actual
parameter-variation provider context equals the frozen M96 measured-fact
contract and unsupported OCP API usage fails closed before any future hosted
package is selected.

## Done

- M97-001 is closed as non-passing terminal evidence: three requests issued,
  generic context mismatch, invalid `gp_DZ` import, then provider timeout.
- ADR-0058 and WP-M97-002 route the smallest offline remediation; M98 remains
  unauthorized.
- M97 CLI now derives a measured M96 transcript for every development row and
  validates it before either provider boundary; generic `probe_summary` is no
  longer the M97 outbound context.
- Added the versioned local `gp_Dir(0, 0, 1)` through-cut recipe and
  pre-execution unavailable-OCP-symbol classification (`gp_DZ` is rejected).
- Owner validation passed: focused M96/observed suite (41 tests), OCP script
  contract controls (2 tests), Ruff, governance audit and `git diff --check`.
- Liaol independently confirmed the G2 review on 2026-08-10.

## In progress

- None. M97-002 is closed; no provider request is authorized.

## Next

1. If the user selects it, create one bounded G3 development calibration
   workpack with newly frozen experimental inputs and report/monitor paths.
2. Run hosted preflight and obtain new itemized authorization before any
   provider request; do not inspect held-out rows or select M98.

## Decisions

- [ADR-0058](../../architecture/adr/0058-m97-observation-contract-remediation.md)
  requires M97-002 before a new G3 calibration can be selected.

## Blockers

- No implementation blocker. Hosted execution remains out of scope until a
  new G3 workpack, hosted preflight and itemized authorization exist.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M97-002-reference-guided-parameter-variation-observation-contract-remediation.md` |
| M96 policy | `docs/corpus/sequence-paired/reference-guided-through-hole-variation-v1-m96-policy.json` |
| ADR | `docs/architecture/adr/0058-m97-observation-contract-remediation.md` |
| Terminal evidence | `data/corpus-runs/m97-reference-guided-through-hole-development-calibration.json` |
| Validation | `uv --cache-dir .uv-cache run python -m pytest tests\test_m96_reference_guided_through_hole_observation.py tests\test_observed_build_loop.py -q` |

## Resume prompt

```
M97-002 is closed. Do not issue provider requests or inspect held-out rows.
Only create a new G3 development calibration workpack if the user explicitly
selects that bounded package.
```
