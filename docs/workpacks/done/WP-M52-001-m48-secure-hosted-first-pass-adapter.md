# WP-M52-001: M48 Secure-Hosted First-Pass Adapter

- Status: done
- Milestone: M52
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Replace the old filename-bearing hosted first-pass context with the M48 bounded
observation transcript, preserving secure `wsl-bwrap` no-input execution and
making the path testable entirely with fake or loopback providers.

## Scope

- Add a provider-agnostic observed-build path that accepts M48 observation
  calls, emits only their path-free transcript, and runs the returned script
  through the selected executor with no original STEP mount.
- Route the future hosted single-case first-pass path through that adapter.
- Add fake/loopback regressions for no raw input, file name, host path,
  reference script, or trace-path egress; secure-executor refusal; report and
  provenance fields.

## Compatibility constraints

No hosted request, no credential read into output, no external input, no
manifest/split change, no repair, and no provider/model claim. Existing corpus
first-pass behavior remains unchanged unless an explicitly selected M51 call
uses the new adapter.

## Acceptance

```powershell
uv run python -m pytest tests\test_observed_build_loop.py tests\test_corpus_m4.py tests\test_harness_m2.py -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Acceptance evidence and interpretation

- Expanded focused regression: `22 passed in 29.66s`.
- Final full offline suite: `162 passed in 136.31s (0:02:16)`.
- Ruff, governance audit, and diff check passed; no hosted provider request
  was issued.

M52 supplies a single-case path that uses only the M48 observation transcript
and runs the generated script without an input STEP mount. The hosted branch
is fail-closed until authorization, a one-request budget, deadline, and
`wsl-bwrap` are all present. This is adapter/sandbox-boundary evidence only;
it makes no model-quality claim.

## Proposed next direction for reviewer

If Liaol accepts M52, close it and reactivate M51 for a fresh configuration
check and the required itemized authorization request: destination/provider
and model, bounded transcript egress, one `box` case, zero repair rounds, a
single request budget, and provider deadline. Do not issue the request until
that authorization is explicit.

## Closure rationale

Liaol approved M52 on 2026-08-08. The adapter closes with 162 passing offline
tests and no provider request; M51 may now resume its G3 preflight.

## Status transition

Record acceptance and Liaol independent review; then unblock M51 for a fresh
read-only preflight and explicit hosted authorization request.

## Out of scope

Any provider call or hosted evaluation.
