# WP-M177-002: Asymmetric Hosted Preflight

- Status: done
- Milestone: M177
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Entry condition

M178 independently reviewed and froze the local dual-product campaign CLI.
The user selected this new G3 M177 package. The former M177-001 authorization
is archived and cannot be reused.

## Goal

Perform fresh, credential-safe, local-only preflight for M176's 30-case
no-card main cohort and three-case hash-bound-card annex. Publish the outcome
for independent review; do not construct a provider or issue a request.

## Route decision

- M146 hypothesis: a fixed closed-loop campaign can yield attributable hosted
  terminal evidence only when its Q01--Q04 boundaries remain inspectable.
- Q01--Q04 decision: verify frozen Q01 input/card boundaries and the Q03
  secure-executor/report gate before any future Q02/Q04 hosted interaction.
- Evidence role: admission evidence only; it establishes neither model quality
  nor a provider result.
- Counterexample: any hash, role, identity, executor, accounting, or admission
  failure rejects this run and prevents an authorization request.
- Stop rule: stop after independent review, any preflight failure, frozen-input
  drift, or a request to change egress/content/budget/deadline/cohort/repair
  boundaries.
- Adoption boundary: a passing result permits only a subsequent itemized
  authorization request; it does not authorize or execute hosted work.

## Scope

- Run the fixed `m176-asymmetric-campaign-preflight` command exactly once
  against the four M176 identities and record its sanitized result.
- Run `m176-asymmetric-campaign-admission` to prove both local checkpoints
  remain zero-request and not authorized.
- Independently verify the M175/M176 freeze audits, the local `wsl-bwrap`
  no-input executor availability, and the fixed 102 completion-slot / 69
  provider-request ceilings.
- Record a fresh preflight handoff for Liaol's independent G3 review.

## Frozen proposed egress (not authorized)

If a later independent review passes, the only proposed destination is
`https://api.deepseek.com`, provider/model `deepseek / deepseek-v4-pro`.
The main cohort would send bounded Q01 facts only; the annex would send bounded
Q01 facts plus its one returned hash-bound card. The fixed scope is 30 main
plus 3 annex cases, serial/no retry, 4096 output tokens, 120-second per-request
deadline, 102 completion slots, and at most 69 provider HTTP requests. This
paragraph records a future authorization candidate only.

## Compatibility constraints

Do not inspect or print `.env` values; construct a provider; issue a provider
request; reuse or alter a report/monitor identity; change M175/M176 inputs,
cards, model, token cap, deadline, repair/retry policy, executor, runtime, or
Harness behavior; or access held-out assets. The command writes only its four
fresh local checkpoints/monitor states.

## Acceptance

- `uv run python tools/audit_m175_asymmetric_qualification.py` passes.
- `uv run python tools/audit_m176_campaign_freeze.py` passes.
- `uv run python -m brep2code.cli m176-asymmetric-campaign-preflight` returns
  `prepared_offline`, with 102 completion slots, 69 provider requests, 30 main
  cases, and 3 annex cases.
- `uv run python -m brep2code.cli m176-asymmetric-campaign-admission` returns
  `fresh_execute_admission_candidate` while both products remain unissued and
  unauthorized.
- `uv run python tools/check_governance.py` and `git diff --check` pass.
- Liaol completes independent G3 review; only then may the owner request
  itemized egress authorization from the user.

## Owner completion boundary

Publish the passing, sanitized local preflight/admission evidence and active
handoff, then obtain Liaol's independent G3 review. Do not request
authorization or execute hosted work before that review.

## Owner evidence

- 2026-08-14 `uv run python tools/audit_m175_asymmetric_qualification.py`
  passed: 30 main rows, 3 annex rows, and all 10 frozen mechanism groups.
- 2026-08-14 `uv run python tools/audit_m176_campaign_freeze.py` passed:
  `prepared_offline`, 30 main cases, 3 annex cases, and 102 completion slots.
- 2026-08-14 `uv run python -m brep2code.cli
  m176-asymmetric-campaign-preflight` returned `prepared_offline` with 102
  completion slots, a 69 provider-request ceiling, 30 main cases, and 3 annex
  cases. It created only the four fixed local checkpoint/monitor identities.
- 2026-08-14 `uv run python -m brep2code.cli
  m176-asymmetric-campaign-admission` returned
  `fresh_execute_admission_candidate` with the same 102/69 ceilings.
- 2026-08-14 `uv run python tools/check_governance.py` and `git diff --check`
  passed. No credential inspection, provider construction, or provider request
  occurred.

## Review state

Liaol independently approved the G3 review on 2026-08-14. Review confirmed
the frozen contract, local-only evidence, zero-request/unauthorized checkpoint
state, and status/handoff alignment. The review does not authorize hosted
egress.

## Closure

M177-002 is closed after independent G3 review. Its durable execution boundary
remains the M176 freeze and the M178 CLI contract; the package supplies only
fresh local-preflight provenance. A subsequent hosted execution requires a new
selected workpack and the user's fresh itemized authorization.

## Permitted stop conditions

Independent review; any audit, hash, path, executor, report freshness, CLI, or
admission failure; frozen-input drift; or a requirement to widen the fixed
hosted contract.

## Status-transition plan

`active -> review -> done` after all acceptance evidence and independent review.
A preflight failure moves the package to `blocked` or `deferred` with its exact
re-entry condition. Passing review leaves hosted execution blocked on new,
itemized user authorization.

## Out of scope

Any provider construction or request, credential inspection, egress
authorization, execution, cohort/card/prompt/model changes, retries, held-out
use, report reuse, runtime/Harness/provider changes, or terminal evidence
claims.
