# WP-M71-001: DeepSeek Compatibility Diagnostics

- Status: done
- Milestone: M71
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

Offline-test DeepSeek request compatibility modes, including safe control
transport metadata, streaming/non-streaming policy boundaries, JSON-output
contract and bounded output controls. No provider request or prompt-policy
selection occurs in this workpack.

## Goal

Produce a tested compatibility matrix for the next stability experiment while
keeping every diagnosis deterministic, offline and content-safe.

## Scope

- Specify candidate request/response modes as fixtures: current non-streaming
  behavior, unsupported streaming boundary, JSON-output envelope, bounded
  response-size behavior and safe control-report transport metadata.
- Test worker lifecycle, serialization and failure classification without a
  provider construction or network connection.
- State which timing signals each mode can and cannot expose; do not represent
  unavailable first-byte, token or header times as measurements.
- Update the provider contract and runbook only to clarify supported and
  fail-closed unsupported boundaries.

## Dependencies and stopping rule

M70's durable-monitor contract is accepted. Stop if a candidate mode cannot
preserve the existing credential, prompt-redaction, secure-executor or
atomic-report contracts. Record it as unsupported; do not silently fall back
or choose a remote mode.

## Compatibility constraints

Offline and credential-free only. Preserve default provider selection,
`wsl-bwrap` enforcement for hosted execution, existing non-streaming behavior,
request accounting and report compatibility. No prompt-policy selection,
provider call, external data, manifest change, retry or hosted authorization.

## Collaboration plan

- Owner: Codex; exclusive paths are `brep2code/agent/provider.py`, provider
  compatibility tests, provider contract/runbook updates and this workpack.
- Independent reviewer: Liaol; review the compatibility matrix, fail-closed
  unsupported modes, no-egress evidence and acceptance output.
- Closure condition: all acceptance gates pass and Liaol records an
  independent scope/evidence review. Closure does not select or authorize M72.

## Acceptance

```powershell
uv run python -m pytest tests\test_agent_m3_provider_trace.py tests\test_agent_m3_repair_loop.py tests\test_observed_build_loop.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Validation plan

The changed provider/worker boundary is covered first by the three focused
test modules above. The full suite is then run once in its own command window;
Ruff, governance and diff checks remain separate. No command constructs a
remote provider connection.

## Status transition

Owner implementation and acceptance are complete. Liaol must independently
review the matrix, unsupported-mode disposition, no-egress boundary and
acceptance output before closure. Approval records the review decision here,
then moves the workpack to `done/`; it does not choose or authorize M72.

## Compatibility matrix

| Candidate | Disposition | Offline evidence | Observable timing / metadata |
|---|---|---|---|
| Current Chat Completions, non-streaming JSON request | supported | Pure payload fixture requires `response_format: {"type":"json_object"}` and has no `stream` field. | Complete-response arrival only; no TTFT/token/header time. |
| Streaming request/response | unsupported | No request field, parser or worker event contract exists for stream chunks. | Do not represent first byte, token arrival or partial response as measured. |
| JSON script-replacement envelope | supported with strict execution boundary | Pure response fixture accepts only `script_update.kind="replace"` with string content. | Complete-response metadata remains sanitized; nonconforming content reaches the existing missing-update path. |
| Character-accurate remote output cap | unsupported, fail-closed | `max_output_chars` raises before HTTP because it has no current provider mapping. | No implied output-size limit, token count or truncation measurement. |
| Control response metadata | supported, sanitized | Existing response fixture retains only id/model/created before the HTTP layer adds status class and request-id presence. | No raw header, request-id value, URL, prompt or credential retention. |

## Implementation evidence

- Extracted the current request serializer into `_deepseek_payload`, so JSON,
  non-streaming and unsupported-output-cap behavior are testable without
  provider construction or network activity.
- A supplied `max_output_chars` now fails before HTTP instead of silently
  pretending to enforce a remote character cap.
- Added deterministic fixtures for the non-streaming payload, the bounded
  output rejection, and the strict script-replacement/sanitized-summary
  response envelope.
- Clarified the same boundaries in the LLM provider contract and provider
  configuration runbook. No prompt, endpoint, executor, report budget or
  hosted policy changed.

## Validation record

- Initial focused run reached a terminal 28 passed / 1 failed because the new
  test omitted its `DeepSeekProviderError` import; the test-only error was
  corrected before acceptance.
- Initial post-review full run reached a terminal 178 passed / 2 failed
  because this active-directory workpack was temporarily labelled
  `Status: review`; governance requires active-directory workpacks to retain
  `Status: active`. The lifecycle label was corrected without changing the
  implementation.
- `uv run python -m pytest tests\\test_agent_m3_provider_trace.py tests\\test_agent_m3_repair_loop.py tests\\test_observed_build_loop.py -q` — final pass: 29 passed in 54.97s.
- `uv run python -m pytest tests\\test_governance_audit.py -q` — pass: 7 passed in 0.92s.
- `uv run python -m pytest -q` — final pass: 180 passed in 188.13s.
- `uv run python -m ruff check .` — pass.
- `uv run python tools\\check_governance.py` — pass.
- `git diff --check` — pass.

## Review status

- Owner: Codex — accepted implementation and validation on 2026-08-09.
- Independent reviewer: Liaol — approved on 2026-08-10. Reviewed the matrix,
  fail-closed output-cap disposition, no-egress scope, committed
  implementation, and terminal acceptance evidence. Independent focused
  rerun: 29 passed in 53.36s; Ruff and `git diff --check` passed.

## Closure rationale

M71 is closed as an offline compatibility diagnosis. It preserves the existing
non-streaming transport, rejects an unenforceable character cap before HTTP,
and records only sanitized response metadata. This closure neither selects nor
authorizes M72 or any hosted request.

## Out of scope

Hosted transport tests, endpoint changes, streaming rollout, prompt rewrite,
output-quality claims, CAD-script changes, model comparisons and any request
budget use.
