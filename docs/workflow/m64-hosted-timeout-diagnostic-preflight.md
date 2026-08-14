# M64 Hosted Timeout-Diagnostic Preflight — Awaiting Authorization

- **Date**: 2026-08-09
- **Workpack**: `WP-M64-001-hosted-timeout-cause-discrimination`
- **Mode**: read-only; no provider request issued

## Proposed isolated experiments

| Experiment | Destination/model | Outbound content | Bound | Deadline | Report |
|---|---|---|---|---|---|
| Control | `https://api.deepseek.com`, DeepSeek `deepseek-v4-pro` | Fixed user text `Return exactly OK.` plus the provider adapter's generic JSON-object instruction; no local data | exactly 1 request | 120 seconds | `data/corpus-runs/m64-deepseek-control.json` |
| Fixed-case comparison | `https://api.deepseek.com`, DeepSeek `deepseek-v4-pro` | Only the existing M48 path-free bounded observation transcript for `param_additive_boss_low`; no raw STEP, paths, filenames, reference scripts, docs, traces, credentials, or environment values | exactly 1 first-pass request; no repair | 300 seconds | `data/corpus-runs/m64-param-additive-boss-low-deepseek-extended.json` |

The control has no generated-script execution. The fixed-case comparison uses
`observed-development` with `--max-cases 1 --max-rounds 0 --request-budget 1`
and `wsl-bwrap`; it does not mount the original STEP during generated build
execution.

## Read-only checks

- The fixed manifest SHA-256 is
  `DC4C6E8F3302367A3B1082FAD602FE36FF2A59901E59079695DA75724892A593`,
  matching M63; its first selected case is the M63 interrupted case
  `param_additive_boss_low`.
- The local non-secret configuration parses as `deepseek-v4-pro` at
  `https://api.deepseek.com`. No credential value was printed, written, or
  otherwise exposed.
- WSL reports `bubblewrap 0.9.0`. The current offline M64 regression confirms
  the control command enforces hosted authorization before provider
  construction and writes no fixed prompt or response content to its report.
- Both proposed report paths do not exist and have no `running` or
  `interrupted` checkpoint. No M54/M63 report or nominal request remainder is
  eligible for reuse.

## Interpretation boundary

A completed control provides only an endpoint/model response-baseline
observation. If it completes within 120 seconds and the same case completes
within 300 seconds, task latency becomes a plausible contributor to M63's
120-second timeout; this is not causal proof from one sample. A control
timeout/failure instead supports a transport/provider-response problem. Any
mixed result, repeated timeout, or provider failure remains inconclusive.

## Authorization gate

This preflight does not authorize egress. Each row of the table requires its
own explicit user approval of destination, model, exact outbound content,
one-request cap, deadline, report path, and the fixed-case `wsl-bwrap`
boundary. The two calls must be durably monitored and must not reuse M54/M63
budget, authorization, or checkpoint.

## Authorized run outcome

On 2026-08-09, the user separately authorized both table rows. The control
report reached `completed` with one issued request under its 120-second bound.
The fixed-case report reached `interrupted` after one issued request at its
300-second provider deadline; it retained only `worker_started` and
`http_started`, with zero completed cases and no `http_failed` event.

This rules out a simple blanket inability to authenticate to or obtain any
response from the selected endpoint/model. It supports the narrower inference
that the fixed request has request-specific latency or handling behavior beyond
both deadlines. It does **not** establish that CAD-task complexity is the
cause: the control differs in prompt length/content, and the reports do not
identify server-side queueing, content handling, or transport behavior after
the HTTP call begins. Both M64 budgets are consumed; no retry is authorized.
