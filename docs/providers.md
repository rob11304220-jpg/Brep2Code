# Providers

`fake` is the default provider. A real provider must be selected explicitly;
credentials alone never activate hosted execution. Credentials are read only
from environment variables or an ignored local configuration file after the
hosted path has been selected, and are never persisted or included in errors,
object representations, or request artifacts.

The OpenAI-compatible adapter accepts an HTTPS endpoint, explicit model, and API
key. DeepSeek reads `DEEPSEEK_API_KEY`, `DEEPSEEK_MODEL`, and optionally
`DEEPSEEK_BASE_URL`; process environment values take precedence. Provider
pricing is supplied for the authorized run rather than hard-coded because it
may change.

## Provider responsibility

The adapter transports one provider-neutral Harness action. It owns:

- request construction and bounded response reading;
- provider-specific fields such as thinking mode;
- HTTP attempt, timeout, and retry handling;
- response normalization and action-contract parsing;
- prompt, completion, and total token accounting;
- cost calculation and enforcement;
- redacted request and response artifacts.

It does not own geometry probes, SDK or recipe content, controller state,
submission scheduling, secure execution, or success verification.

The following events are distinct:

| Event | Owner | Meaning |
|---|---|---|
| Model decision | Active controller | One requested Harness action |
| HTTP attempt | Provider adapter | One outbound transport attempt |
| Protocol retry | Provider adapter | Recovery from malformed action JSON |
| Submission | Submission pipeline | One complete candidate script |
| Execution | Secure backend | One untrusted build attempt |
| Repair | Active controller | One verifier-guided opportunity after failure |

A protocol retry does not consume another model decision, submission, execution,
or repair. Transport retries and protocol retries still consume provider HTTP
capacity and any reported token or cost usage.

Malformed responses are normalized only within the bounded action contract.
Empty, ambiguous, or invalid content is rejected with a redacted diagnostic.
When valid provider usage accompanies an invalid action, that usage remains
charged because the request already occurred.

## Model projection boundary

The adapter receives the projection assembled by the Active controller. It may
send only:

- task identity and unit;
- path-free observations;
- actions and tools available on the current turn;
- coarse session phase;
- selected CAD backend and export contract;
- prior bounded tool results;
- current revision and typed feedback.

It must remove internal compatibility fields such as task-contract hashes and
must never send controller limits or usage, provider ceilings or accounting,
retries, timeout, prices, cost, authorization, campaign policy, secure-executor
configuration, eval material, private oracles, repository files, host paths,
environment variables, or credentials.

Internal limits affect the projection only by removing unavailable actions and
tools. The model is not asked to manage numeric budgets.

## Provider limits and accounting

Every hosted run declares provider limits for HTTP attempts, bounded retries,
per-request timeout, response size, output tokens, aggregate tokens, aggregate
cost, and input/output prices. Reaching a request, token, or cost ceiling blocks
later requests. If a completed HTTP response moves aggregate usage beyond a
ceiling, the actual usage is recorded before the run stops.

Controller limits are separate and bound model decisions, probes, retrievals,
submissions, executions, and repairs. Provider capacity must be sufficient for
the declared model decisions and bounded retries, but provider accounting never
becomes model-visible controller state.

Current schema-v7 Active results store provider accounting separately from the
controller trace and usage. Accounting includes HTTP attempts, in-flight state,
protocol retries, prompt/completion/total tokens, cost, prices, and provider
ceilings. Frozen schema-v6 results remain valid under their original contract.

For schema-v7 live Active runs, the saved request messages are validated after
execution against the capability-only projection. Unknown or internal task
fields, nested limit/accounting fields, prompt/action disagreement, tool/action
disagreement, missing request artifacts, or retry/accounting drift invalidate
the run for the protocol-stabilization cohort.

Continuation restores the saved accounting with unchanged provider/model,
prices, ceilings, controller limits, timeout, retrieval policy, backend
contract, and revision root. An interrupted HTTP attempt remains consumed while
its in-flight marker is cleared. Authorization is never stored in or inherited
from a checkpoint.

## Hosted readiness and authorization

Readiness and execution are separate operations:

- preflight validates the case, task contract, outbound projection, limits, and
  root semantics without reading provider configuration or granting permission;
- config-check may read provider configuration but remains network-free and
  reports only redacted endpoint and plan information; it does not require or
  grant execution authorization;
- secure-backend readiness verifies the selected backend package without
  executing generated code;
- a hosted execution command separately validates the complete itemized
  authorization and performs network requests only after all gates pass.

Readiness never grants permission. Each initial or continuation execution needs
fresh authorization for the provider, endpoint host, model, case scope, backend,
knowledge condition, outbound projection, controller and provider limits,
prices, cost ceiling, and run root. A continuation additionally authorizes the
current complete revision and bounded feedback that may be sent.

The real Active HTTPS path is deliberately narrow: one explicitly selected
provider/model, a fresh runtime-case root, no provider fallback, bounded response
bytes, credential-free exchange artifacts, and generated-code execution only
through the secure backend. Stub commands remain network-free even when they
exercise the same controller, accounting, submission, and validation contracts.

Campaigns add an aggregate provider ceiling above fresh per-case limits. Cases
remain isolated: they never share scripts, feedback, revisions, or controller
state. The campaign artifact aggregates provider accounting without becoming a
second runtime context.

## Result policy

Hosted results are run artifacts, not permanent narrative documentation. Store
each run under its fresh root and retain provider/model identity, task and
contract identity, actions, requests, protocol retries, submissions, repairs,
executions, sandbox outcome, gates, failure classification, artifact paths,
tokens, and cost in validated JSON.

Generate comparisons from those artifacts. Do not copy individual hosted run
stories into README or `docs/`, and do not maintain an append-only evidence
ledger. CLI `--help` is the authority for current command flags and arguments.
