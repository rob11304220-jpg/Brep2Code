# WP-M177-001: Asymmetric Hosted Preflight and Execution

- Status: deferred
- Milestone: M177
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Entry condition

M176 independently froze the asymmetric campaign inputs. The user explicitly
selected this G3 package and authorized egress to DeepSeek V4 Pro: bounded Q01
facts only for the 30-case main cohort; bounded Q01 facts plus one returned
hash-bound card for the three-case annex; 33-case scope; serial/no-retry;
4096 output tokens; 120-second request deadline; `wsl-bwrap` no-input executor;
four fresh report/monitor identities; and 102 maximum completions.

## Goal

Complete fresh, credential-safe offline preflight and independent review, then
preserve the authorized execution handoff for the next session without issuing
a provider request in this session.

## Scope

- Verify the M176 freeze audit, intended input/guidance hashes, report-path
  freshness, CLI budget boundary, WSL secure executor, and local DeepSeek
  configuration/model availability without printing credentials or environment
  values.
- Publish a sanitized preflight record with zero issued requests and an
  execution-resume command/sequence that cannot alter frozen bounds.
- Obtain Liaol's independent G3 preflight review before the next session's
  authorized execution.

## Authorized egress

Destination `https://api.deepseek.com`; provider/model `deepseek / deepseek-v4-pro`.
Main outbound content is bounded Q01 facts only; annex content is bounded Q01
facts plus one returned hash-bound card. No raw STEP, paths, reference scripts,
reference packs, provider credentials, or environment snapshots may leave the
machine. Scope is 30 main cases plus 3 annex cases, serial/no-retry, 4096
output tokens, 120 seconds per request, and 102 maximum completions. The four
M176 report/monitor identities are mandatory and fresh.

## Compatibility constraints

This session performs no provider construction or request. Do not inspect or
print `.env` values; do not create report checkpoints, reuse a report, change
the frozen spec, access held-out assets, or alter Harness/repair/provider/
runtime behavior. Any preflight failure stops execution.

## Acceptance

Run M176 freeze audit; local secure-executor and configuration availability
checks; CLI-boundary checks; report-path freshness check; governance and diff
checks. Record zero issued requests and Liaol's independent G3 preflight
review. Execution occurs only in the following session.

## Owner completion boundary

Publish passing sanitized preflight evidence and an execution handoff; then
obtain Liaol's independent G3 review. Do not execute in this session.

## Permitted stop conditions

Independent review, any hash/path/config/executor/CLI preflight failure, or
any request to alter egress/content/budget/deadline/cohort/repair bounds.

## Deferred state

M176's input/path audit passes with zero issued requests and local WSL is
available. However, the existing `observed-development` CLI exposes only one
manifest/report path and does not expose M176's `--max-output-tokens 4096`,
the annex's explicit hash-bound card/role contract, independent report/monitor
identities, or its 90 + 12 completion accounting. Running it would silently
substitute a different policy.

Do not execute under an approximation. Re-entry requires a newly selected G2
implementation workpack that adds and offline-validates only the frozen
dual-product CLI/preflight surface without widening egress, repair, card,
case, or provider authority. It must then receive independent review; after
that, M177 is recreated with fresh preflight and fresh itemized authorization.

## Out of scope

Actual provider request or execution in this session, new authorization,
cohort/card/prompt/model changes, retries, held-out use, report reuse, and
terminal review.
