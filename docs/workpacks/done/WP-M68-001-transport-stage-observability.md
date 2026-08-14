# WP-M68-001: Transport-Stage Observability

- Status: done
- Milestone: M68
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Add offline-testable, privacy-preserving transport-stage evidence so a future
authorized request can distinguish worker start, HTTP dispatch, response
headers/first-byte availability, complete response, and transport failure.

## Scope

- Add strict lifecycle phases for response-header availability and completed
  response, with monotonic elapsed milliseconds.
- Preserve only phase/timing/status-class/request-id-presence fields; do not
  serialize prompt, response, URL, credential, headers, request id value, or
  environment data.
- Explicitly record that the non-streaming adapter cannot expose a separate
  response-header/first-byte timestamp; it exposes only complete-response
  arrival plus sanitized response metadata.
- Add deterministic worker/fake tests and update contract docs.

## Compatibility constraints

Offline only; no provider request, prompt change, provider selection change,
network probe, retry, or report/budget reuse.

## Acceptance

```powershell
uv run python -m pytest tests\test_agent_m3_repair_loop.py tests\test_observed_build_loop.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Closure rationale

M68 adds only strict complete-response phase and sanitized metadata; exact
first-byte timing remains explicitly unavailable. Liaol approved its privacy
boundary, limitation and 21-test acceptance on 2026-08-09; no request issued.

## Independent review

- Reviewer: Liaol
- Outcome: approved on 2026-08-09
