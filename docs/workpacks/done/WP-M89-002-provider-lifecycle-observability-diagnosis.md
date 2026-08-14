# WP-M89-002: Provider Lifecycle Observability and Bounded-output Diagnosis

- Status: done
- Milestone: M89
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Diagnose the unobservable boundary exposed by M89-001 without sending another
provider request: add a sanitized first-response-byte lifecycle event and an
explicit DeepSeek token-limit mapping, while keeping reasoning content, raw
responses, credentials, and prompt text out of durable reports and traces.

## Scope

- Preserve the existing non-streaming Chat Completions request semantics.
- Record only timing/event metadata for the first response body byte; retain no
  body fragment or reasoning content.
- Add an explicit positive `max_output_tokens` request field mapped to
  DeepSeek's `max_tokens`; retain `max_output_chars` as fail-closed.
- Project the new timing only through existing sanitized telemetry/report
  paths, with deterministic fake/worker tests.
- Write ADR-0053 and update the provider trace and case-corpus contracts.

## Attribution question and sampling intent

Distinguish a provider request that receives no response body before its
deadline from one that starts responding but fails later. This adds diagnostic
resolution only; it cannot attribute a timeout to model quality, network,
prompt difficulty, CAD, or the reference card. Stop after offline tests and
review; no hosted control, retry, or comparison is in scope.

## Inputs

- M89 terminal report and monitor state
- `brep2code/agent/provider.py`
- `brep2code/agent/repair.py`
- `brep2code/agent/observed_build.py`
- provider trace and corpus-report contracts

## Code paths

- `brep2code/agent/provider.py`
- `brep2code/agent/repair.py`
- `brep2code/agent/observed_build.py`
- `brep2code/cli/__init__.py`
- `brep2code/agent/trace.py` only if its whitelist requires adjustment
- focused provider/lifecycle/observed-build tests

## Docs to update

- `docs/architecture/adr/0053-provider-first-byte-and-token-cap-diagnostics.md`
- `docs/architecture/v1/contracts/llm-provider-trace.md`
- `docs/architecture/v1/contracts/case-corpus.md`
- `docs/modules/cli.md` if a visible parameter is added
- `docs/runbooks/llm-provider-config.md`
- `docs/workflow/status.md`, this workpack, and active handoff

## Trace/schema changes

Extend sanitized provider lifecycle telemetry with an optional first-response-
body-byte event/offset and add the explicit `max_output_tokens` request
contract. No raw bytes, reasoning content, request IDs, response headers,
prompt content, credentials, or full response envelopes may be persisted.

## Decision-package impact

- `decision_id`: none; offline transport diagnosis after M89.
- Q01/Q02 effect: none; no observation or build sequence changes.
- Q03/Q04 effect: no gate or repair-policy change; diagnostic timing does not
  turn a timeout into a repairable CAD failure.
- Evidence role: timeout-discriminating negative-control instrumentation.
- Knowledge disposition: no reusable guidance card or CAD knowledge.

## Compatibility constraints

Default operation remains network-free. Existing DeepSeek payloads remain
non-streaming JSON requests unless a caller explicitly supplies a positive
token cap. Thinking mode and `reasoning_content` are out of scope; no prompt
may ask for or retain unrestricted chain-of-thought. M89's terminal report,
request count, and no-retry disposition remain immutable.

## Acceptance

```powershell
uv run python -m pytest -m fast -q
uv run python -m pytest tests/test_agent_m3_provider_trace.py tests/test_agent_m3_repair_loop.py tests/test_observed_build_loop.py -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools/check_governance.py
git diff --check
```

## Evidence reuse / guidance-card disposition

No guidance card is read, changed, promoted, or retrieved by this workpack.

## Status transition

After owner acceptance and Liaol's independent G2 review, update
`status.md` first, move this workpack to `done/`, and archive the handoff.
Its closure can only enable a separately user-selected G3 retry proposal; it
does not authorize one.

## Closure rationale

Liaol independently approved closure on 2026-08-10 after confirming the
timing-only, privacy-bounded lifecycle event; positive-only token-cap mapping;
unchanged fail-closed character cap; updated contracts/ADR; and terminal
offline acceptance. No provider request, report preparation, retry, or M89-001
reinterpretation occurred. This closes only the diagnostic prerequisite; it
does not authorize a new hosted run.

## Implementation and offline acceptance

- Added `http_first_response_byte`, emitted only after the DeepSeek worker has
  read one response body byte. The worker retains its existing start, HTTP
  start, complete-response and failure events; byte content is discarded.
- Added positive `ProviderRequest.max_output_tokens`, mapped directly to
  DeepSeek `max_tokens`. The existing `max_output_chars` behavior remains
  fail-closed; neither a visible CLI option nor a hosted caller was added.
- Added ADR-0053 and updated the provider trace, case-corpus, and provider
  runbook contracts. The adapter remains non-streaming and JSON-only; thinking
  mode and `reasoning_content` are neither requested nor persisted.
- 2026-08-10 owner checks passed: provider/worker focused suite (`18 passed`),
  first-response-byte observed-build test (`1 passed, 24 deselected`), fast
  suite (`66 passed, 143 deselected`), full suite (`209 passed`), and Ruff.
  No provider configuration, endpoint, monitor, report preparation, or hosted
  request was accessed by this workpack.

## Independent review

- Reviewer: Liaol
- Status: approved on 2026-08-10.
- Required scope: verify that the new event is timing-only and monotonic, no
  response/reasoning content or headers are retained, `max_output_tokens` is
  token-semantic and positive-only, existing character-cap behavior is
  unchanged, and M89-001 was neither retried nor reinterpreted.

## Out of scope

- Any provider request, retry, report preparation, monitor setup, or hosted
  authorization.
- Prompt expansion, thinking mode, reasoning-content persistence, repair,
  card mutation, model/endpoint changes, or CAD/Harness gate changes.
- M90--M98 activation and M73 activation.

## Repair hypothesis and evaluation boundary

No repair is proposed. M89 timed out before a script existed, so a repair loop
has no fixed failing artifact to act on. A future retry, if selected, must
first state a separate transport hypothesis and use this workpack's bounded
diagnostic evidence.
