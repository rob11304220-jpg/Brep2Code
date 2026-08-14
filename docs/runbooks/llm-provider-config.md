# LLM Provider Configuration

Local tests use `FakeLLMProvider` and must not require network access or credentials. The supported hosted integration is DeepSeek V4; it is available only when explicitly selected and separately authorized for a bounded batch.

## Current Local Provider

- Provider: `FakeLLMProvider`
- Network: none
- Credentials: none
- Use: unit tests, offline smoke, deterministic repair-loop fixtures

## DeepSeek V4 local configuration

1. Open the ignored repository-root [`.env`](../../.env) file and set `DEEPSEEK_API_KEY`.
2. Keep `DEEPSEEK_MODEL=deepseek-v4-pro`. Set `deepseek-v4-flash` only when a faster, lower-cost smoke is preferred.
3. Leave `DEEPSEEK_BASE_URL=https://api.deepseek.com` unless DeepSeek supplies a replacement endpoint.

The tracked [`.env.example`](../../.env.example) documents the required keys. `.env` and all `.env.*` files except the example are ignored by Git.

Run a bounded repair with the secure executor:

```powershell
uv run python -m brep2code.cli repair --provider deepseek --record deepseek-smoke --script path\to\failing_build_sequence.py --input case-library\self-authored\box\input.step --max-rounds 1
```

For `--provider deepseek`, the CLI always uses `wsl-bwrap`; it never runs a provider-generated script through `unsafe-local`. The command returns a local configuration error when the key is missing. Do not place the key in a command line, source file, trace, or report.

The repair provider instructs models to use the installed `cadquery-ocp` `OCP` imports (not `OCC.Core`) and to satisfy the input geometry gates. Runtime imports are part of the repair contract, not a model assumption.

## Current DeepSeek transport compatibility

The adapter supports one non-streaming JSON-object completion mode. It does
not implement streaming, so first-byte, token-arrival and separate
response-header timings are unavailable. It retains only sanitized complete-
response metadata; it never records header values or request-id values.

`ProviderRequest.max_output_chars` is currently rejected locally before HTTP:
the adapter has no character-accurate remote output-cap mapping. Do not treat
that field as a request-size control or work around it with an undocumented
provider option. A later mode requires its own offline compatibility work and
fresh hosted authorization.

## Hosted corpus evaluation (manual and bounded)

`corpus` remains offline by default. Before a hosted P0/P1 run, the user must explicitly authorize the model, maximum cases, maximum rounds per case, and a cost or request budget. Do not infer that approval from the existence of `.env`.

After that approval, use a bounded command such as:

```powershell
uv run python -m brep2code.cli corpus --manifest case-library\manifests\self-authored\p0.json --provider deepseek --authorize-hosted --max-cases 3 --max-rounds 1 --request-budget 3 --provider-timeout 120 --data-root data --report data\corpus-runs\deepseek-p0.json
```

The command rejects absent authorization, invalid bounds, a request budget above `max-cases × max-rounds` (or `max-cases × (1 + max-rounds)` with `--first-pass`), non-positive `--provider-timeout`, missing configuration, or missing WSL before a provider request. Each DeepSeek request is run in a separately terminable worker; exceeding `--provider-timeout` records `provider_request_timeout` for that case instead of allowing the batch to wait indefinitely. `--repair` remains a mutually exclusive local fake-provider replay mode. Hosted reports use schema version 2 and retain only sanitized identifiers, bounds, result classifications, and revision trace paths under ignored `data/`; never attach `.env`, API keys, full provider responses, or environment snapshots.

## First-pass generation mode

`corpus --first-pass` asks the selected provider for an initial complete `build_sequence.py` using only the bounded B-Rep summary, then executes that script through Harness. The outbound summary contains only `file_name`, format/unit, bbox, topology counts, area, and volume; it excludes the local absolute input path and raw STEP content. It is explicit: ordinary corpus runs and `--repair` replay do not invoke it. Local fake first-pass runs require a `first_pass_script` fixture for every selected manifest case; use `--first-pass --repair` only when a separate `reference_script` fixture should replay a failed generation.

First-pass reports use schema version 3 and retain separate nullable `primary_generation`, `repair`, and `fake_provider_replay` results plus the `first-pass-summary-v1` policy marker. In hosted mode, budget capacity is at most `max-cases × (1 + max-rounds)` because each case can consume one first-pass request and up to `max-rounds` repair requests. Hosted first-pass evaluation remains subject to the same fresh explicit authorization and `wsl-bwrap` requirement; this runbook does not authorize a request.

## M85 reference-assisted smoke

`reference-assisted-smoke` is a separate, fixed two-request path. It accepts
only P0 `cylinder`, role `final primitive`, the reviewed guidance index/card,
`--request-budget 2`, and `--max-repair-rounds 0`. The first completion must
request exactly `get_guidance_card({"role":"final primitive"})`; Harness
validates the frozen hashes and returns the compact card locally. Only then may
the second completion return a replacement `build_sequence.py`. The input STEP
remains local; the second outbound request contains only the bounded observation
transcript and the returned derived card. Any malformed tool request, card
failure, timeout, script failure, or geometry failure is terminal with no retry.

## M87 reference-assisted block-with-hole smoke

`reference-assisted-block-with-hole-smoke` is the separate fixed two-request
M87 path. It accepts only P0 `block_with_hole`, role `single boolean-cut tool`,
the reviewed guidance index/card, `--request-budget 2`, and
`--max-repair-rounds 0`. M85 remains fixed to `cylinder`. The first completion
must request the declared M87 role; the Harness verifies frozen hashes and
returns the compact card locally before script generation. The input STEP
remains local; failures are terminal and never authorize retry or a next case.

## M89 reference-assisted three-hole-plate smoke

`reference-assisted-three-hole-plate-smoke` is the separate fixed two-request
M89 path. It accepts only P1 `three_hole_plate`, role `repeated boolean-cut
tool`, the reviewed guidance index/card, `--request-budget 2`, and
`--max-repair-rounds 0`. M85 and M87 remain fixed to their own cases. The first
completion must request the declared M89 role; the Harness verifies frozen
hashes and returns the compact card locally before script generation. The
input STEP remains local; any failure is terminal and never authorizes retry,
repair, an extra case, card promotion, or M90.

## Authorization preflight and risk disclosure

## M135 offline fixed-epoch preparation

`m135-epoch-preflight` is a local-only preparation command for the frozen
18-condition M134 epoch. It creates one fresh report plus a distinct
monitor-owned state file, validates all frozen input hashes and ordering, and
writes zero issued requests. It never constructs a provider, reads an env
file, or sends data.

```powershell
uv run python -m brep2code.cli m135-epoch-preflight --report data\m135-epoch\epoch-report.json --monitor-state data\m135-epoch\epoch-monitor.json
```

The command fixes `deepseek / deepseek-v4-pro`, `wsl-bwrap`, an 18-request
cap, a 120-second provider deadline, zero repair/retry, and no selected token
output cap. Both paths must be fresh and distinct. Its `prepared_offline`
result is local contract evidence only: it is not hosted preflight completion,
provider configuration validation, authorization, or execution. A later
workpack must use new report and monitor identities and repeat the full
credential-free preflight before it can request itemized authorization.

Before asking the user to authorize any hosted request, complete and report this minimum read-only review:

1. State the destination, provider/model, outbound content (including whether it is raw input or a bounded derivative), exact cases or split, rounds, request or cost budget, and provider deadline.
2. Verify selected input SHA-256 values, manifest/split membership, and the corresponding offline `wsl-bwrap` preflight. Do not request authorization after a hash, manifest, input-probe, or sandbox failure.
3. Verify the local provider configuration entry, selected model, and secure executor without printing credentials or environment snapshots.
4. Verify the actual CLI budget rule and report destination: normal hosted repair allows at most `max-cases × max-rounds`; hosted `--first-pass` allows at most `max-cases × (1 + max-rounds)`.
5. Inspect the intended report path. A pre-existing `running` or `interrupted` checkpoint is partial evidence only; do not reuse its remaining budget. Use a new report path and obtain a new explicit authorization.
6. Disclose the data-egress scope, bounded budget, provider deadline, and any host/outer-command timeout that could terminate the process. If the batch can outlast an interactive command limit, use a durable monitored launch rather than relying on that limit.

The authorization must explicitly approve the destination and outbound content, as well as provider/model, case scope, rounds, deadline, and request or cost budget.

## M89-002 lifecycle diagnostics

M89-002 is offline-only. It may map an explicit positive provider-token limit
to `max_tokens` and record only the elapsed time to the first response body
byte. It remains a non-streaming JSON request and does not persist a byte,
thinking/reasoning content, raw response, header, request ID, prompt, or
credential. These diagnostics do not grant hosted authority or turn a timeout
into a CAD repair signal.

## M89-003 bounded-output reference-assisted retry proposal

`reference-assisted-three-hole-plate-bounded-output-smoke` is the separate
M89-003 fixed two-request path. It accepts only P1 `three_hole_plate`, role
`repeated boolean-cut tool`, `--request-budget 2`, `--max-repair-rounds 0`,
and `--max-output-tokens 4096`. The same positive token cap is sent with both
the guidance and script-generation requests and is recorded in the fresh
two-request checkpoint. This contract is offline-testable; hosted invocation
remains subject to a fresh preflight and explicit itemized authorization.

## M118 fresh hosted stability

`reference-assisted-three-hole-plate-stability-smoke` is the separate M118
fixed two-request path. It accepts only P1 `three_hole_plate`, role
`repeated boolean-cut tool`, `--request-budget 2`, `--max-repair-rounds 0`,
and `--max-output-tokens 4096`. It preserves the path-free observation-plus-
card egress boundary while using the M118 policy namespace and fresh M118
report/monitor paths. Hosted use remains subject to a fresh offline preflight,
independent G3 review, and explicit itemized authorization.

## M127 shared hosted-stability re-entry

`reference-assisted-three-hole-plate-stability-reentry-smoke` is the separate
M127 fixed two-request shared hosted-stability re-entry path. It accepts only
P1 `three_hole_plate`, role `repeated boolean-cut tool`,
`--request-budget 2`, `--max-repair-rounds 0`, and `--max-output-tokens 4096`.
It preserves the M118 path-free observation-plus-card egress boundary while
moving to a fresh M127 policy, report path, monitor path, and authorization
scope. Hosted use remains subject to a fresh offline preflight, independent G3
review, and explicit itemized authorization; no M118 report, budget, or prior
authorization may be reused.

## M64 provider-response control

`provider-control` is a diagnostic-only command for the fixed outbound user
text `Return exactly OK.`. It has no local input, observation transcript, or
generated-script execution. Hosted use still requires a fresh explicit
authorization, `--provider deepseek`, `--authorize-hosted`, a one-request
budget, a positive provider deadline, and a new report path. Its durable
report stores only policy, terminal status, provider/model and request
accounting; it never stores prompt or provider-response content. A successful
control is a response-baseline observation, not evidence that a CAD task will
complete within the same deadline.

For a monitored single control or `observed-first-pass` request, invoke
`--phase prepare` first after the ordinary hosted authorization checks have
passed. It creates one fresh, content-free `running` report with zero requests
used. Attach M70 to that report, then invoke the same command with
`--phase execute`; execute accepts only that prepared report, marks one request
issued immediately before provider work, and writes `completed` or
`interrupted`. A prepared report is a new run capacity, not an old report to
reuse; never overwrite it or use it without the same separately authorized
bound.

Before a first-pass request, the input summary runs in an isolated process with a 45-second deadline. If it is unavailable, the case records `input_probe_failure` with zero provider requests and the batch does not send a request for that case. Provider-generated output artifacts retain the 15-second probe deadline; neither deadline changes the provider timeout.

The report path is an atomic checkpoint: it is written as `running` before the first case and after every completed case, then `completed` at normal termination. A handled interruption or runner exception writes `interrupted` with the current case id and a non-sensitive error class. For `observed-development`, a first-pass provider deadline increments `requests_used`, writes `provider_request_timeout`, and stops the batch without retrying or starting later cases. An externally killed process cannot run cleanup code, but the last completed-case checkpoint remains valid. Treat an `interrupted` report as partial evidence only; inspect its completed cases and revision traces, then obtain a **new** explicit hosted budget authorization before starting a new run. Do not silently reuse the unspent portion of a terminated batch's budget.

## Provider reliability and recovery review

Before scheduling another hosted batch, run the offline or loopback reliability tests defined by the active workpack and review their output. Confirm that provider deadlines terminate their worker, request accounting increments when a request is issued (including timeout/error paths), and corpus reports preserve the latest completed-case checkpoint.

Use report status precisely during review:

- `completed`: the runner reached its terminal report; it may be used for the bounded run summary.
- `interrupted`: the runner handled the event and retained completed cases; it is partial evidence, not an aggregate result.
- `running`: the process may have been externally stopped; inspect only completed checkpoints and do not claim a terminal outcome.

Do not attribute a provider timeout to the model, CAD script, sandbox, or geometry gates without trace-supported reproduction. If a targeted hosted validation is necessary after offline review, obtain a new explicit authorization stating provider/model, cases, rounds, timeout, and request or cost budget; do not reuse a prior batch's remaining budget.

## Hosted Provider Rules

Future hosted integrations should follow these rules:

- Store API credentials in environment variables, not repo files.
- Use provider-specific variable names documented by the integration workpack; DeepSeek uses `DEEPSEEK_API_KEY`.
- Do not copy full environment snapshots into `metadata`, `raw_summary`, traces, or signal bundles.
- Write only small response summaries to `traces/provider_response.json`.
- Keep full raw hosted responses out of revision bundles unless a later ADR defines a secure storage policy.

DeepSeek uses the OpenAI-compatible Chat Completions endpoint at `https://api.deepseek.com` with model names `deepseek-v4-flash` and `deepseek-v4-pro`.
