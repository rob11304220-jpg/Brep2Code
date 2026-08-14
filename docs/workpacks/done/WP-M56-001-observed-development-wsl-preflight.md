# WP-M56-001: Observed-Development WSL Preflight Regression

- Status: done
- Milestone: M56
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Add a deterministic fake-provider multi-case `observed-development` regression
through `wsl-bwrap`, proving first-pass and bounded repair execute without an
input mount before M54 can seek hosted authorization.

## Scope

- Permit the explicit offline command/test path to select `wsl-bwrap`.
- Cover two manifest cases, first pass and one repair, path-free messages and
  no-input capability attestations.
- Preserve hosted authorization gates and all legacy corpus behavior.

## Compatibility constraints

Offline and credential-free only. No provider call, manifest change, prompt
change, external data, or M54 authorization.

## Trace/schema changes

None planned.

## Decision-package impact

- `decision_id`: `q01-q02-observation-build-separation-v1`.
- Evidence role: offline secure-executor boundary regression only.
- Knowledge disposition: no reusable modeling knowledge.

## Acceptance

```powershell
uv run python -m pytest tests\test_observed_build_loop.py -q
uv run python -m pytest -m sandbox -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Status transition

Close only after output and Liaol independent review. M54 then needs a fresh
preflight and explicit itemized authorization.

## Implementation and owner acceptance

- Added `--executor wsl-bwrap` and optional runtime resources to the explicit
  fake-provider `observed-development` path only.
- The two-case regression verifies fake-provider first pass through
  `wsl-bwrap`, no input mount, and path-free provider messages.
- Owner acceptance (2026-08-08): focused WSL regression `8 passed in 32.55s`;
  sandbox selection `72 passed, 92 deselected in 167.37s`; full suite
  `164 passed in 181.39s`; Ruff, governance audit, and `git diff --check`
  passed.
- Pending: Liaol independent G2 review.

## Independent review and closure

- Liaol independently reviewed the fake-provider WSL boundary, no-input and
  egress assertions, acceptance output, and lifecycle records on 2026-08-08.
- Review outcome: approved. M56 is offline security evidence only and does not
  authorize a provider request.

## Out of scope

Hosted calls, credentials, changes to fixed development split, or use of old
corpus first-pass context.
