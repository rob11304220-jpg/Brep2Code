# WP-M89-003: Bounded-output Reference-assisted Retry Proposal

- Status: done
- Milestone: M89
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Implement and offline-validate an auditable positive token cap for one new,
fixed M89 reference-assisted `three_hole_plate` attempt.  Only after a new
read-only hosted preflight and a separate, itemized user authorization may the
workpack issue its two sequential requests.

## Attribution question and sampling intent

M89-001 reached its second provider request but timed out before a response
body byte. M89-002 added first-response-byte telemetry and a positive
`max_output_tokens` transport contract. This workpack tests one bounded
transport hypothesis: a fixed 4096-token maximum is propagated to both
non-streaming DeepSeek requests and makes a fresh run's lifecycle evidence
more diagnostic. It does not claim that the cap will prevent timeouts, improve
CAD correctness, diagnose the provider/network, or establish a model-wide
effect.

## Scope

- Add an explicit positive `--max-output-tokens 4096` contract to the fixed
  M89 path and propagate it to both provider calls without retaining prompts,
  responses, reasoning content, headers, request IDs, or credentials.
- Preserve the fixed P1 `three_hole_plate` case, `repeated boolean-cut tool`
  role, frozen index/card, top-k one, exactly two requests, zero repair and
  zero retry.
- Preserve `wsl-bwrap` with no input mount, the existing API/script,
  provenance, output, bbox, volume, and topology gates, and M89-002's
  timing-only first-response-byte event.
- Run focused, fast, full, Ruff, governance, and offline no-input sandbox
  validation. Then run a read-only hosted preflight with fresh report and
  monitor paths.

## Inputs and immutable boundaries

- `case-library/self-authored/three_hole_plate/input.step`
- `case-library/manifests/self-authored/p1.json`
- `runtime_resources/experience-cards/index.json`
- `runtime_resources/experience-cards/cards/vertical-cylinder-construction.json`
- M89-001 terminal report and M89-002 offline diagnostic evidence

The selected input, manifest membership, guidance index/card hashes, existing
report, and existing monitor are evidence only. They are never modified,
reused for budget, or interpreted as authorization.

## Planned hosted boundary (not yet authorized)

- Destination/model: `https://api.deepseek.com`, DeepSeek `deepseek-v4-pro`.
- Egress: first a bounded path-free observation transcript and fixed
  instructions; second that transcript plus the compact frozen guidance card.
  No raw STEP, local path, filename, reference script, trace, prior report,
  response content, headers, or credential leaves the workspace.
- Bound: one fixed case; exactly two sequential requests; zero repair, retry,
  replacement case, card mutation, or cost claim; 4096 maximum output tokens
  per request; proposed 300-second deadline per request.
- Fresh destinations: `data/corpus-runs/m89-003-three-hole-plate-bounded-output.json`
  and `data/monitor-runs/m89-003-three-hole-plate-bounded-output.monitor.json`.
- Execution: only through `wsl-bwrap` and a durable monitor. A timeout,
  provider/tool failure, script failure, sandbox/provenance failure, or
  geometry failure is terminal and consumes each issued-request budget.

## Code and documentation paths

- `brep2code/cli/__init__.py`
- `brep2code/agent/observed_build.py`
- `tests/test_observed_build_loop.py`
- `docs/modules/cli.md`
- `docs/runbooks/llm-provider-config.md`
- `docs/workflow/status.md`, this workpack, and active handoff

## Compatibility constraints

Default execution remains offline and credential-free. M85, M87, M89-001,
and M89-002 remain immutable historical evidence. No model/endpoint change,
thinking mode, prompt expansion, gate relaxation, manifest/card mutation,
external data, M90+ activation, or M73 activation is permitted.

## Acceptance

```powershell
uv run python -m pytest -m fast -q
uv run python -m pytest tests/test_agent_m3_provider_trace.py tests/test_observed_build_loop.py -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools/check_governance.py
git diff --check
```

The offline preflight must additionally verify the fixed hashes and manifest
scope, the no-input `wsl-bwrap` path, non-secret provider configuration and
model selection, actual two-request CLI accounting, absent/fresh report and
monitor paths, and the 300-second provider deadline. A failure prevents an
authorization request.

## Status transition

After owner acceptance and Liaol's independent G3 review of the offline scope,
ask the user to authorize every planned hosted-boundary item. Do not run
`prepare`, attach a monitor, or execute until that authorization is explicit.
After a hosted terminal result and independent review, update `status.md`
first, then close or block this workpack and archive the handoff.

## Implementation and offline preflight evidence

- Added the separate
  `reference-assisted-three-hole-plate-bounded-output-smoke` command. It
  preserves M89's fixed case, role, two-request accounting, zero-repair and
  no-input execution boundary while requiring `--max-output-tokens 4096`.
  Its fresh checkpoint policy is
  `m89-003-three-hole-plate-bounded-output-v1` and records the cap.
- `ObservedBuildLoopRunner` validates a positive token cap and propagates it
  to both the guidance and script-generation `ProviderRequest` objects.
  Deterministic fake-provider tests verify both requests receive `4096`, and
  the M89-003 CLI test verifies checkpoint accounting and rejection of `4095`.
- Owner validation on 2026-08-10 passed: observed-build suite (`28 passed`),
  provider-trace suite (`10 passed`), fast suite (`66 passed, 146 deselected`),
  full suite (`212 passed`), Ruff, governance audit, and `git diff --check`.
- Read-only preflight on 2026-08-10 passed. The input SHA-256 is
  `34ef08fd81be048d1ba09066f21f162931d91a2001701f7ad737fb3722ae4418`;
  `p1.json` includes one matching `three_hole_plate` case; the frozen guidance
  index SHA-256 is
  `dfa731d597581b3b4d306782c1078c7de5b79672462229baaf5d7248fa230517`; and
  the selected card SHA-256 is
  `55341683e3e7df3e058a845193e34fba20b0650c0db28a31489ad5d343b60d30`.
- Non-secret configuration verification found DeepSeek `deepseek-v4-pro` at
  `https://api.deepseek.com`. The planned report and monitor paths are absent.
  The fixed CLI requires exactly two requests and 300 seconds is a valid
  positive provider deadline; the cap is exactly 4096 on both requests.
- A local `wsl-bwrap` `--build-without-input` reference-script preflight at
  `C:\\tmp\\brep2code-m89-003-preflight` passed: sandbox and provenance
  coverage are true, the input mount was absent, no input access was recorded,
  and API, output, bbox, volume, and topology gates all passed. No provider
  request, report preparation, or monitor setup occurred.

## Review and authorization blocker

Liaol independently approved the M89-003 offline scope on 2026-08-10 after
reviewing the code/trace boundary, fixed scope, offline evidence, fresh-path
checks, and terminal disposition. The approval does not grant provider
authority. The user must still explicitly authorize the planned destination
and derived outbound content, `deepseek-v4-pro`, one fixed case/role/card,
exactly two requests, zero retry/repair, 4096-token cap, 300-second
per-request deadline, `wsl-bwrap` no-input execution, and the two fresh
paths.

## Hosted authorization

Liaol explicitly authorized the complete M89-003 hosted boundary on
2026-08-10: destination and derived egress content; DeepSeek
`deepseek-v4-pro`; the fixed `three_hole_plate` hash and declared role/card;
exactly two sequential requests; zero retry and repair; 4096 tokens per
request; a 300-second provider deadline; `wsl-bwrap` without the input mount;
and the new report/monitor paths. Account pricing was not inspected, so the
authorization is bounded by two issued requests rather than a currency cap.

## Hosted execution record

- The authorized run prepared the fresh content-free checkpoint, attached the
  durable monitor, and executed exactly once on 2026-08-10. The terminal
  report is `data/corpus-runs/m89-003-three-hole-plate-bounded-output.json`;
  it is `completed`, with `requests_used: 2`, `requests_remaining: 0`, and
  `max_output_tokens: 4096`.
- The terminal result is `pass`. It retained the fixed selected role
  `repeated boolean-cut tool`, returned only
  `vertical-cylinder-construction`, used the no-input `wsl-bwrap` path, and
  passed the build-script API, output, bbox, volume, and topology gates.
  Provenance coverage is true, no input access was recorded, and the output is
  classified `independent_reconstruction`.
- Sanitized timing evidence records a first response byte at 42,771 ms, script
  response completion at 42,997 ms, provider wait of 35,675 ms, and end-to-end
  duration of 56,702 ms. These values describe this bounded run only; they do
  not establish model-wide, network, or transport causality.
- The monitor at
  `data/monitor-runs/m89-003-three-hole-plate-bounded-output.monitor.json`
  observed terminal `completed` and issued its required review handoff. No
  retry, repair, replacement case, or further provider request was made.

## Final review required

Liaol must independently verify the terminal report's 2/2 accounting,
authorized case/role/card/hash boundary, 4096-token checkpoint contract,
no-input sandbox/provenance result, all gate statuses, and absence of retry or
repair. This review cannot authorize a new provider budget. After approval,
update `status.md` first, move this workpack to `done/`, archive the handoff,
and retain the terminal report and monitor only as bounded evidence.

## Independent review and closure

- Reviewer: Liaol
- Status: approved on 2026-08-10.
- Review scope: confirmed the terminal report's exact 2/2 accounting, the
  authorized fixed input/role/card/hash boundary, the required 4096-token
  checkpoint contract, no-input `wsl-bwrap` and provenance evidence, all gate
  passes, durable-monitor terminal state, and absence of retry or repair.
- Closure rationale: M89-003 is one successful, fully bounded development
  run. It shows that this fixed reference-assisted path completed within the
  authorized run under the recorded constraints. It does not establish a
  general CAD capability, model-wide reliability, causal effect of the token
  cap, network/transport diagnosis, card quality beyond this declared role, or
  authorization for further sampling. The 2/2 budget is exhausted.

## Out of scope

Any additional provider request, repair, retry after a terminal result,
replacement case, card promotion, raw-response retention, provider/model or
endpoint change, M90--M98 activation, or M73 activation.
