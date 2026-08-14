# WP-M62-001: Offline Test Feedback Baseline Refresh

- Status: done
- Milestone: M62
- Owner: Codex
- Risk tier: G1

## Goal

Refresh M53's local offline test-feedback baseline after M60 added process
boundary coverage and M61 established independent validation-command planning.

## Scope

- Run `fast`, `standard`, `sandbox`, and one full pytest suite as separate,
  independently bounded offline commands.
- Record counts, durations, and the longest full-suite calls using
  `--durations=0`.
- Update M53's baseline and M61 planning guidance with measured, non-normative
  command-window recommendations.

## Compatibility constraints

No test, marker, fixture, dependency, runtime, provider, hosted-policy, or
corpus-input change. Do not construct or call a provider, inspect credentials,
or retry M54. The measurements are local observations, not CI limits.

## Acceptance

```powershell
uv run python -m pytest -m fast -q
uv run python -m pytest -m standard -q
uv run python -m pytest -m sandbox -q
uv run python -m pytest --durations=0 -q
uv run python tools\check_governance.py
git diff --check
```

## Status transition

Record command outputs, owner acceptance, and closure rationale before
archiving. No independent review is required for this G1 measurement/document
work.

## Owner acceptance

- Refreshed M53 with independent local observations: fast 4.47s, standard
  12.40s, sandbox 180.26s, and full suite 190.77s; all 169 tests passed.
- Recorded the slowest current calls and non-normative independent windows of
  60 seconds for fast/standard and eight minutes for sandbox/full commands.
- Updated the M61 planning runbook with those windows.
- `uv run python tools\check_governance.py` and `git diff --check` passed.

## Closure rationale

M62 completed the bounded offline measurement and documentation objective. The
baseline is explicitly local and non-normative; it changes neither test
behavior nor any hosted boundary.

## Out of scope

Performance optimization, parallel execution, CI timeout policy, test-marker
changes, test-result claims beyond the local observation, hosted requests, or
M54 budget reuse.
