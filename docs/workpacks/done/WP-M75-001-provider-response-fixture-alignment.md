# WP-M75-001: Provider Response-Fixture Alignment

- Status: done
- Milestone: M75
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Restore the offline suite by making one DeepSeek response test double match the
existing HTTP response contract used for non-sensitive request-id telemetry.

## Scope

- Add an empty `headers` mapping to the response fixture in
  `tests/test_agent_m3_provider_trace.py`.
- Verify the fixture still exercises configuration loading, request shape,
  JSON response parsing and absent-request-id behavior.
- Run the focused test, fast suite, full suite, Ruff, governance audit and
  patch-format check.

## Compatibility constraints

Test-only change. Do not modify provider production code, provider/model
selection, credentials, outbound behavior, trace schema, report schema,
Harness, manifests or hosted authorization.

## Acceptance

```powershell
uv run python -m pytest tests\test_agent_m3_provider_trace.py -q
uv run python -m pytest -m fast -q
uv run python -m pytest -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Status transition

On closure, update `docs/workflow/status.md` first, move this workpack to
`done/`, archive its handoff and record acceptance output.

## Out of scope

Provider hardening, telemetry changes, provider requests, credential handling,
hosted evaluation and any change to M70's monitor behavior.

## Closure rationale

- Added only an empty `headers` mapping to the response fixture and asserted
  the intended absent-request-id telemetry result. Production provider code
  and all hosted boundaries remain unchanged.
- Acceptance on 2026-08-09: focused provider fixture test (5 passed), fast
  suite (58 passed, 119 deselected), full suite (177 passed in 186.31s), Ruff,
  governance audit and `git diff --check` all passed.
