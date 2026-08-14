# WP-M179-001: Asymmetric Execution Adapter and Refreeze

- Status: done
- Milestone: M179
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Add only the offline-testable, fail-closed execution-adapter seam missing from
M178, and freeze fresh local report/monitor identities for the unchanged M176
dual-product campaign. It must accept an injected fake provider in tests but
must neither construct nor contact a hosted provider.

## Scope

- Introduce a versioned M179 freeze that preserves the M175 cohort, M176 input
  and card hashes, DeepSeek V4 Pro declaration, 4096-token cap, 120-second
  deadline, serial/no-retry rule, 102 completion slots, and 69-request ceiling
  while replacing only report/monitor identities.
- Add a typed, provider-injected execution adapter that admits only a freshly
  prepared M179 checkpoint, preserves per-product accounting and fail-closed
  terminal classification, and is fully testable with fake responses.
- Add fixed local CLI preparation/admission commands for the M179 identities;
  no CLI command in this package may construct `DeepSeekProvider` or read an
  env file.
- Add focused tests, contract/module documentation and an ADR.

## Route decision

- M146 hypothesis: attributable hosted terminal evidence requires every
  Q01--Q04 boundary to remain inspectable and fixed.
- Decision: introduce a provider-injected local seam (Q02--Q04 structure) and
  new Q03 report identities without altering the frozen Q01/card/repair policy.
- Evidence role: offline contract evidence only; no model, provider or hosted
  outcome is established.
- Counterexample: hash, role, identity, accounting, admission, fake-runner, or
  terminal-classification failure rejects the adapter for hosted use.
- Stop rule: stop for independent review, frozen-input drift, test failure, or
  any requirement to construct a provider, read credentials, alter execution
  policy, or issue a request.
- Adoption boundary: after independent G2 review, a distinct G3 package must
  conduct fresh preflight and obtain itemized authorization before egress.

## Compatibility constraints

Do not modify M175 cohort membership, M176 input/card contents, model/token/
deadline/repair/retry/executor limits, generic CLI behavior, provider protocol,
Harness policy, or held-out access. Do not inspect `.env`, construct a provider,
or issue a request. M179's identities must be new, distinct, and unused.

## Acceptance

- M179 freeze audit verifies inherited hashes/policy and fresh distinct paths.
- Focused adapter/CLI tests cover fake-only successful and terminal paths plus
  hash, identity, accounting and admission rejection.
- `uv run python -m pytest -m fast -q`, changed-area tests, one full pytest
  suite, Ruff, governance audit and `git diff --check` pass.
- Independent Liaol G2 review confirms no provider, credential or network
  action and no frozen-boundary widening.

## Owner completion boundary

Publish code, documentation, ADR and passing offline evidence; then obtain
Liaol's independent G2 review. Stop there.

## Owner evidence

- M179 adds `m179-asymmetric-campaign-refreeze-v1.json`, new distinct unused
  identities, fake-only adapter functions, and local-only preflight/admission
  CLI commands; non-fake providers fail closed.
- 2026-08-14 audits passed: M175 qualification and M179 fresh identity freeze.
- 2026-08-14 `uv run python -m pytest -m fast -q` passed (67 passed); focused
  `tests/test_asymmetric_campaign.py` passed (3 passed); Ruff and py_compile
  passed.
- 2026-08-14 full `uv run python -m pytest --durations=0 -q` passed (292
  passed, 503.68s). A prior 8-minute command window ended without a terminal
  result; the independent longer rerun produced the passing terminal result.

## Review state

Liaol independently approved the G2 review on 2026-08-14. Review confirmed
frozen-boundary preservation, fake-only/provider-injection enforcement,
evidence, and lifecycle alignment; it does not authorize hosted egress.

## Closure

M179-001 is closed after independent G2 review. ADR-0086 owns the durable
adapter/identity decision. A later G3 package must use M179's fresh identities
for credential-safe preflight and obtain fresh itemized user authorization
before any provider construction or request.

## Permitted stop conditions

Independent review; frozen hash/identity drift; reproducible test failure; or
a requirement to cross the provider/credential/egress boundary.

## Status-transition plan

`active -> review -> done` after the listed evidence and independent review.
Drift or an unrepresentable fixed boundary moves the package to `blocked` or
`deferred` with a precise re-entry condition.

## Out of scope

Any DeepSeek construction/request, egress authorization, hosted execution,
credential access, changed cases/cards/prompts/model/token/deadline/budget,
retries, held-out use, or generic runtime/provider changes.
