# WP-M58-001: Provider Timeout Phase Diagnostics

- Status: done
- Milestone: M58
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Distinguish a hosted provider worker that fails to start, reaches its HTTP
attempt but does not return, or returns a classified error before the outer
deadline, using offline deterministic tests only.

## Scope

- Add local-only worker lifecycle events with monotonic elapsed timing.
- Reserve an outer-deadline grace interval so a shorter inner HTTP timeout can
  return its sanitized error classification.
- Preserve request issuance accounting and M57 interrupted checkpoint rules.
- Add deterministic worker simulations for startup, HTTP wait, and error paths.

## Attribution question and sampling intent

The two M54 reports establish only that the worker did not exit before the
120-second outer deadline. This work distinguishes worker startup from an
in-flight HTTP wait and from a returned provider error without creating a new
hosted sample. Stop after offline phase classification and regression evidence;
do not use repeated hosted requests as diagnosis.

## Inputs

- M54 timeout reports and local stderr records.
- Existing DeepSeek provider boundary and multiprocessing worker tests.

## Code paths

- `brep2code/agent/repair.py`
- `brep2code/agent/observed_build.py`
- `tests/test_agent_m3_repair_loop.py`
- `tests/test_observed_build_loop.py`

## Docs to update

- `docs/architecture/v1/contracts/case-corpus.md`
- `docs/modules/harness.md`
- `docs/workflow/status.md`
- this workpack and its active handoff

## Trace/schema changes

Additive local timeout diagnostics may contain only phase names, monotonic
elapsed milliseconds, and sanitized error class. They must not contain request
content, credentials, URLs, local paths, raw provider output, or environment
values. Update the case-corpus contract.

## Decision-package impact

- `decision_id`: `q01-q02-observation-build-separation-v1`.
- Q01/Q02 effect: none; the path-free observation/build boundary is unchanged.
- Q03/Q04 effect: provider lifecycle failures become more precisely classified
  before a future repair decision.
- Evidence role: offline provider-lifecycle diagnostic regression.
- Knowledge disposition: no reusable modeling knowledge.

## Compatibility constraints

Default execution remains network-free. No provider call, model, prompt,
manifest, executor policy, request budget, M54 report path, or timeout budget
reuse is authorized. A timeout remains fail-closed and terminates the worker.

## Acceptance

```powershell
uv run python -m pytest tests\test_agent_m3_repair_loop.py tests\test_observed_build_loop.py -q
uv run python -m pytest -m sandbox -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Evidence reuse / guidance-card disposition

No reusable modeling knowledge; diagnostics are local provider-lifecycle
evidence only.

## Status transition

Record owner acceptance and Liaol independent review before closure. M54 stays
blocked; M58 does not authorize a connectivity probe or hosted retry.

## Closure rationale

Liaol independently approved the owner acceptance on 2026-08-08 after review
of scope, diagnostic sanitization, offline regression output, and governance
alignment. M54 remains blocked; M58 made no provider call and did not reuse a
request budget.

## Owner acceptance

- Added a terminable-worker lifecycle diagnostic with only phase names,
  monotonic elapsed milliseconds, and a sanitized error class. A startup
  failure, in-flight HTTP wait at the outer deadline, and returned worker error
  are deterministically distinguished without request content or configuration
  in the diagnostic payload.
- Confirmed the inner HTTP timeout remains shorter than the outer worker
  deadline, retaining the existing termination and issued-request accounting.
- Offline checks passed on 2026-08-08:
  - `uv run python -m pytest tests\test_agent_m3_repair_loop.py tests\test_observed_build_loop.py -q` — 17 passed
  - `uv run python -m pytest -m sandbox -q` — 76 passed, 92 deselected
  - `uv run python -m pytest` — 168 passed
- `uv run python -m ruff check .` — passed

## Independent review

- Reviewer: Liaol
- Outcome: approved on 2026-08-08
- Verified: G2 scope, local-only diagnostic field boundary, deterministic
  startup/HTTP-wait/error regressions, acceptance outputs, and M54 non-retry
  boundary.

## Out of scope

Hosted connectivity tests, credential inspection, provider retries, changing
the fixed M54 scope, or inferring model quality.
