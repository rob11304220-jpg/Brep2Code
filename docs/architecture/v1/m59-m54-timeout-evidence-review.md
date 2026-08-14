---
type: review
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - M54
  - M58
  - M59
  - provider-lifecycle
---

# M59: M54 Timeout Evidence Review and Next-Diagnostic Design

## Scope and evidence boundary

This review uses only the local M54 report/logs, preflight records, committed
checkpoint boundary, and M58 deterministic lifecycle regressions. It creates
no provider request and does not inspect credentials, request content, raw
provider output, or environment values.

## Observed evidence

| Artifact | Observed fact | Supported conclusion |
|---|---|---|
| First M54 stderr record | The request raised `ProviderRequestTimeoutError` at the configured 120-second outer deadline; no usable terminal batch report was written. | An outer worker deadline fired. This observation does not identify a worker or HTTP phase. |
| Fresh M54 report (`...rerun-20260808.json`) | `run_status` is `interrupted`; `param_additive_boss_low` was current; one request was issued; no case completed or later case began. | M57's handled interruption and request accounting held for the fresh run. Its 23 nominal remaining requests are not reusable. |
| Fresh M54 record metadata | Only the record and staged input exist; no completed revision evidence exists. | The timeout occurred before a generated script could become a completed Harness case result. No geometry, gate, or script conclusion is available. |
| M58 deterministic simulations | Startup failure, in-flight HTTP wait, and returned worker error produce distinct sanitized lifecycle outcomes. | The current boundary can classify those paths in future runs without adding request content or sensitive data to diagnostics. |

The earlier M6 `box_cylinder_union` timeout is historical provider-lifecycle
context, not a replicate of the fixed M54 input or its observation-only
request. It confirms that a timeout classification alone is insufficient for a
causal provider/model claim.

## What remains unobserved

The M54 reports predate M58 diagnostic projection and retain only the timeout
exception classification. They do not establish whether the worker failed to
start, reached the HTTP attempt, received an HTTP/provider error too late for
the outer deadline, or encountered a remote/network condition. They also do
not establish model quality, B-Rep complexity sensitivity, sandbox failure,
or a geometry-gate defect.

## Decision

Keep M54 blocked. Do not use the two timeout observations as a basis for a
retry, model-quality result, or request-budget reuse.

The single recommended follow-on is **WP-M60-001: observed-development
lifecycle-diagnostic checkpoint projection** (G2, offline only). It should:

1. Project the existing M58-sanitized timeout diagnostics into the
   `observed-development` `interruption` object atomically, without changing
   request issuance, termination, case order, or default offline behavior.
2. Extend the observed-development contract to permit only `last_phase`, phase
   events with monotonic elapsed milliseconds, and sanitized `error_class`.
3. Add deterministic startup-unobserved, HTTP-wait, and returned-worker-error
   checkpoint regressions; verify no request content, credentials, URL, path,
   raw output, environment value, or timeout configuration is serialized.

M60 would make a later, separately authorized fresh hosted batch more
diagnosable. It would not authorize that batch. Any such batch still needs a
new report path, fresh preflight, and explicit authorization for destination,
egress content, provider/model, case/round bounds, per-request deadline, and
request or cost budget.

## Knowledge disposition

This is local lifecycle reliability evidence only. It contributes no reusable
modeling knowledge and does not alter Q01/Q02 observation-build separation.
