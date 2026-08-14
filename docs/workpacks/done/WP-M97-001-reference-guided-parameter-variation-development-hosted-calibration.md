# WP-M97-001: Reference-Guided Parameter-Variation Development Hosted Calibration

- Status: done
- Milestone: M97
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Run the frozen card/no-card policy on the three M94 development rows to obtain
bounded calibration evidence before held-out evaluation.

## Scope

- For each development row, run the reference-assisted condition with exactly
  two requests and the no-card baseline with exactly one request.
- Freeze the model, endpoint, observation schema, card/index hashes, prompt,
  CLI policy, gates, deadline and report/monitor paths.
- Enforce no-input `wsl-bwrap`, zero repair and zero retry.

## Compatibility constraints

The maximum is nine issued requests.  No held-out row may be sent, inspected
for tuning, substituted or used to change the paired policy.

## Entry and authorization

M95 and M96 must be independently approved.  Before asking for authorization,
perform the hosted read-only preflight: hashes, manifest/split, no-input
sandbox, non-secret provider configuration, fresh report paths, budget rule
and deadline.  The user must explicitly authorize destination, derived egress,
provider/model, three rows, two conditions, nine-request cap, deadline and
zero-retry/repair boundary.

## Acceptance

Record terminal reports, request accounting and unchanged gates for all
authorized rows, then obtain independent G3 review.  A failure consumes only
its issued request budget and does not authorize another request.

## Owner offline readiness record

- Added a distinct DeepSeek-only `prepare`/`execute` lifecycle for the frozen
  three-row path. It creates a fresh, content-free `0/9` report checkpoint,
  records every issued request immediately before provider work, terminalizes
  on a handled lifecycle failure, and uses `wsl-bwrap` with no input mount.
  The established fake-provider CLI path remains fixed.
- Offline fixtures passed the fixed fake 9/9 request accounting, explicit
  hosted-authorization refusal, fresh checkpoint creation, six-condition
  `prepare`/`execute` accounting, and all three development reference scripts
  under no-input `wsl-bwrap`. The M96 transcript audit passed for exactly the
  frozen development rows.
- Read-only provider preflight is recorded in
  [`m97-reference-guided-development-hosted-preflight.md`](../../workflow/m97-reference-guided-development-hosted-preflight.md).
  It verifies the frozen hashes/split, non-secret configuration selection,
  executor, no-input evidence, nine-request rule, 120-second deadline, and
  unused report/monitor paths. It is not hosted authorization.
- Liaol supplied the required itemized G3 hosted authorization on 2026-08-10.
  It covers exactly one new `prepare` → M70 monitor → `execute` lifecycle with
  the frozen three development rows, paired conditions, nine-request maximum,
  120-second deadline, zero retry/repair, limited derived egress and no-input
  `wsl-bwrap`; no other M97 scope is authorized.

## Authorized execution record

- Liaol's itemized G3 authorization was recorded on 2026-08-10. The one
  authorized fresh lifecycle prepared
  `data/corpus-runs/m97-reference-guided-through-hole-development-calibration.json`,
  attached M70 state at
  `data/monitor-runs/m97-reference-guided-through-hole-development-calibration.monitor.json`,
  and executed once.
- M70 observed terminal `interrupted`. The report records exactly 3 issued
  requests and 6 unissued requests that cannot be reused. The low development
  card condition used two requests and reached `fail`; its generated script
  imported unavailable `OCP.gp.gp_DZ`, so the OCP API contract rejected it.
  The following baseline request reached `http_first_response_byte` at
  60,169 ms but timed out at the authorized 120-second deadline. No repair,
  retry, later row, held-out row, report reuse, or further provider request
  occurred.
- Liaol independently approved closure on 2026-08-10. Closure rationale: the
  one authorized lifecycle produced terminal non-passing evidence (an OCP API
  contract failure followed by a provider deadline timeout) after 3/9 issued
  requests. It therefore closes this bounded attempt without a calibration,
  capability, or parameter-generalization claim and does not unlock M98. Any
  later hosted attempt is out of scope and needs a new bounded workpack, fresh
  paths, and a new explicit authorization.

## Out of scope

Held-out evaluation, prompt/card tuning after a result, broad sampling or a
general parameter-generalization claim.
