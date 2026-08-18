# Providers

`fake` is the default provider. Real providers must be selected explicitly.
Credentials are read only from environment variables and are never persisted.
Every hosted command must declare model, case scope, maximum rounds, maximum
requests, request timeout, and a token or cost ceiling. Hosted execution is
never inferred from an earlier run or from the presence of credentials.

The shared OpenAI-compatible adapter accepts an HTTPS base URL, explicit model,
and API key. DeepSeek configuration reads `DEEPSEEK_API_KEY`,
`DEEPSEEK_MODEL`, and optionally `DEEPSEEK_BASE_URL` from the ignored local
`.env` file or process environment. Process environment values take precedence.
The file is read only after explicit hosted selection and authorization. API
keys are excluded from object representations, request
artifacts, responses, and sanitized errors.

Callers must construct `ProviderLimits` with maximum HTTP attempts, retries,
per-request timeout, output tokens, total tokens, total cost, and explicit
input/output token prices. Retries consume the same request budget. Responses
that make aggregate token or cost usage exceed a ceiling are rejected after
their provider-reported usage is committed, because that HTTP cost has already
occurred. The terminal artifact preserves the actual overrun; reaching or
crossing a ceiling blocks every later request before HTTP. Provider pricing is
deliberately not hard-coded because it can change.

Thinking mode is provider policy, not part of CAD modeling capability or the
generic Harness action contract. DeepSeek V4 defaults to thinking behavior, so
hosted CAD generation explicitly requests disabled thinking to preserve bounded
final-output capacity. Provider-specific request and response fields stay in
the adapter. Empty, fenced, explanatory, or otherwise malformed responses are
normalized or rejected there, and any reported usage from a malformed response
still counts toward request, token, and cost ceilings.

The adapter transports a provider-neutral Harness action envelope; it does not
supply OCP API knowledge, modeling recipes, probes, or case-specific hints.
Those belong respectively to the approved reference projection, Harness tools,
and session controller described in `architecture.md`.

Active hosted readiness has two offline gates. `active-hosted-preflight` does
not read provider configuration; `active-hosted-config-check` reads it but
makes no network request and emits only the endpoint host and bounded plan.
Both require fresh itemized authorization for initial observations, bounded
tool results, complete current revision source, and typed feedback. The
declared outbound projection excludes eval references, target solutions,
private oracles, repository files, host paths, and secrets.

Active sessions retain two independent budget layers. Controller limits bound
model turns, probes, retrievals, submissions, executions, repairs, tokens, and
cost. Provider limits separately bound HTTP attempts, retries, timeout, output
tokens, aggregate tokens, and aggregate cost. Controller token and cost limits
may not exceed the provider aggregate ceilings, while provider attempts must
cover every model turn without exceeding its retry capacity. Continuing an
interrupted hosted session requires a fresh itemized authorization and the same
case, provider/model, controller budgets, build timeout, and revision root.
Neither readiness gate authorizes hosted execution.

`active-hosted-readiness` composes the full ordered gate set. It requires a
validated successful fake active baseline and fresh itemized authorization,
distinguishes fresh initial roots from continuation roots, probes the secure
backend read-only, and reads provider configuration only with
`--check-provider-config`. It never sends requests, runs generated code, or
creates run artifacts.

Hosted active checkpoint schema version 4 adds a separate
`provider_accounting` object. It records HTTP attempts, an in-flight request
marker, aggregate prompt/completion/total tokens, aggregate cost, the selected
token prices, and provider ceilings. Malformed responses with valid usage are
still charged. A terminal provider-budget failure may therefore record actual
tokens or cost above its declared ceiling, while nonterminal continuation state
may not. Continuation must restore the saved accounting with unchanged prices
and ceilings; an in-flight attempt remains consumed while its marker is cleared.
The checkpoint contract alone does not expose a hosted execution command.

The initial `active-hosted-run` slice is deliberately HTTP-stub-only. A local
stub response is mandatory, unified readiness must pass first, and generated
code still runs through the secure executor. The command validates the final
schema version 4 artifact and remains network-free.

The separate `active-hosted-live-run` command provides the narrowly scoped real
HTTPS path for one fresh runtime case and one explicitly selected DeepSeek
model. It cannot continue a prior session or fall back to another provider. It
reruns unified readiness with provider configuration enabled, binds controller
and provider request/round/timeout/token/cost ceilings, requires fresh itemized
authorization, and executes generated code only through the secure backend.
Each attempt writes a bounded request artifact without headers or credentials
and a response artifact without reasoning content. The response body itself is
read with a fixed ceiling derived from the declared output-token limit.

`active-hosted-continue` applies the same stub-only boundary. It requires new
itemized authorization on every invocation, restores controller and provider
accounting, rejects identity/price/ceiling/timeout/root drift, and consumes only
remaining limits. Authorization is never stored in or inherited from the
checkpoint.

Campaign contracts have two budget scopes. `max_requests`,
`max_total_tokens`, and `max_cost_usd` are cumulative campaign ceilings passed
to the shared provider. `case_max_requests`, `case_max_total_tokens`, and
`case_max_cost_usd` are freshly instantiated for every runtime case. Thus a
campaign is a serial orchestrator and experiment container: cases have separate
scripts, feedback, revision roots, and case accounting, while the campaign
artifact records the cumulative provider accounting. A successful campaign
therefore means that the selected cases completed under the declared aggregate
budget; it does not mean that one case's script or repair state was reused by
another case.

The `run` command exposes DeepSeek only through explicit `--provider deepseek`
selection. It rejects the command before reading provider configuration unless
`--authorize-hosted` is present, and then requires explicit HTTP request,
retry, provider deadline, output/total token, token-price, and total-cost
limits. Without an initial script, `--max-requests` may not exceed
`max_rounds * (1 + max_retries)`.
Every generated script executes through the verified `wsl-bwrap` backend, and
`result.json` records the declared provider limits plus HTTP-attempt, token,
and cost accounting. A fresh itemized user authorization must cover the exact
provider/model, case, outbound context, rounds, limits, and new run path before
the flag is used. Offline fake-provider runs do not grant hosted authorization.

When `--initial-script` is present, it occupies the first revision without a
provider call. Hosted request bounds apply only to the remaining
`max_rounds - 1` provider-generated revisions. Fresh authorization must also
itemize the complete initial script and the bounded feedback that may be sent
back to the provider; authorization for case observations alone is not enough.
For hosted runs the seed must be a standalone authorized artifact under the
new run root's parent, never a source, test, case, or documentation file.

Example shape only—this is not authorization and the numeric prices must be
declared by the caller for the specific run:

```powershell
brep2code run --provider deepseek --authorize-hosted --case-id box `
  --run-root runs/<fresh-run> --max-rounds 1 --max-requests 1 `
  --provider-timeout 120 --max-retries 0 --max-output-tokens 4096 `
  --max-total-tokens 8192 --max-cost-usd 0.10 `
  --input-cost-per-million <price> --output-cost-per-million <price>
```

## Hosted result policy

Hosted results are run artifacts, not permanent route documentation. Store a
fresh run under runs/<run-id> and retain the declared provider/model, case and
mechanism identity, prompt mode, request and repair counts, execution and
sandbox status, gate results, failure class, output artifact paths, and
token/cost accounting in that run's JSON. Summaries used for comparison must
be generated by the Harness from those artifacts and grouped by mechanism and
`capability_level`; do not maintain an append-only evidence ledger in docs/ or
at the repository root.

## Archived hosted smoke example

The following is a preserved example artifact, not a progress ledger or
authorization for a retry. New hosted runs must follow the result policy above.

The freshly authorized 2026-08-15 `deepseek-v4-pro` controlled repair used
path-free probes of `smoke/block_with_hole`, one authorized initial script,
and exactly one HTTP attempt. It sent no case summary, tags, expected metadata,
STEP content, repository file, host path, or raw process output. The terminal
ignored report is
`runs/hosted-block-with-hole-controlled-repair-20260815-01/result.json`; it
records 2946 total tokens and $0.00197142 against a $0.01 ceiling. Revision
zero securely executed a centered through-hole with radius 3 mm; its bounding
box and topology passed while its volume exceeded the B-Rep observation by
175.92918860103418 cubic millimetres. The single provider revision received
the complete authorized script and structured geometry feedback, changed the
radius to 4 mm, executed securely, and passed bounding-box, volume, and
topology gates. This validates the bounded model-driven geometry repair path.
This record authorizes no retry or follow-up hosted call.
