# WP-M182-001: Asymmetric Case-Local Continuation

- Status: done
- Milestone: M182
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Make the fixed asymmetric campaign record an eligible case-local timeout or
failure as a terminal case result and continue serially through all 33 frozen
development cases, without retry, resume, budget reuse, policy widening, or
provider egress during this workpack.

## Route decision

- Uncertainty: M180's early exception propagation leaves the frozen campaign
  without a complete denominator after a case-local provider or execution
  failure.
- Competing dispositions: retain early-stop semantics, or contain a
  case-local terminal failure and continue.  The user selected the latter.
- Discriminating evidence: offline fake-provider and injected-exception tests
  must prove every remaining case is visited, the failed case is retained with
  a sanitized terminal classification, and the fixed 102-slot/69-request
  caps remain enforced.
- Counterexample: any frozen-contract, authorization, configuration,
  report-identity, or accounting-cap error that is continued rather than
  rejected fails this workpack.
- Stop rule: scope drift, failed offline continuation/cap test, or independent
  review rejection stops before fresh hosted preflight.
- Adoption boundary: a closed M182 changes only the offline execution
  contract.  It creates no hosted authority; a new M182 freeze, preflight,
  independent review, and exact itemized authorization are still required.

## Scope

- Define the M182 continuation/report contract and fresh identities.
- Change the fixed execution path to checkpoint eligible case-local terminal
  failures and move to the next case.
- Preserve per-case request issuance, no-retry behavior, 4096 output tokens,
  120-second provider deadline, `wsl-bwrap` no-input execution, M141's one
  `source_only` repair limit, and the 102 completion-slot/69 HTTP-request
  ceilings.
- Add focused offline tests and update contract/module documentation.
- Obtain Liaol's independent G3 review.

## Compatibility constraints

No provider construction, credential access, external data, or hosted egress.
M179/M181 reports, monitor files, input hashes, authorization packet, and
authorization text are historical readiness evidence only and may not be
reused.  M182 must receive fresh report/monitor identities and, later, fresh
itemized authorization.

## Acceptance

- Offline tests demonstrate continuation after initial provider timeout/error,
  source-only repair timeout/error, and case-local Harness exception.
- Tests demonstrate that global frozen-contract, authorization, configuration,
  report identity, and accounting-cap failures remain fail-closed.
- The full M182 fake campaign reaches all 33 cases while retaining 102/69 cap
  accounting; no retry or resume path exists.
- Relevant module/contract docs and ADR-0088 reflect the behavior.
- `uv run python -m pytest`, `uv run python -m ruff check .`,
  `uv run python tools/check_governance.py`, and `git diff --check` pass.
- Liaol records an independent G3 review before any future hosted preflight.

## Owner completion boundary

Implement, document, and offline-validate the continuation contract; then
obtain independent review and stop before any provider or credential action.

## Owner completion evidence

- Added M182's cryptographically bound continuation spec and four fresh
  `data/hosted/m182-*` report/monitor identities.
- Added M182-only preflight, admission, and execute entrypoints.  Provider
  exceptions from a case are retained as that case's terminal
  `provider_error`, while contract, authorization, configuration, identity,
  and accounting failures remain campaign-global errors.
- Focused regression: `uv run python -m pytest
  tests\\test_asymmetric_campaign.py` — 5 passed.
- Full offline suite: `uv run python -m pytest` — 294 passed in 564.26 s.
- `uv run python -m ruff check .`, `uv run python tools\\check_governance.py`,
  and `git diff --check` passed.
- Local-only M182 preflight and admission passed with 102 completion slots and
  69 provider HTTP requests; neither constructed a provider nor sent data.

## Review state

Owner-side scope is complete.  Await Liaol's independent G3 review of the
continuation/global-failure boundary, fresh identities, request and completion
accounting, offline evidence, and absence of credential/provider/egress work.
Review does not authorize egress.

Liaol approved the independent G3 review on 2026-08-14.  The review confirms
the M182 continuation/global-failure boundary, fresh identities, accounting,
offline evidence, and absence of credential/provider/egress work.  It does not
authorize egress.

## Authorization readiness evidence

- Fresh M182 admission passed: 102 completion slots and 69 provider HTTP
  requests, with zero issued requests.
- M175 qualification audit passed: 30 main rows across 10 mechanism groups
  and three annex rows.
- Boolean-only local checks passed: API-key presence, fixed model/base URL,
  and `wsl.exe` availability.  No credential value was printed, persisted, or
  placed in a report, and no provider was constructed.
- Frozen authorization packet:
  `docs/corpus/knowledge/m182-asymmetric-hosted-authorization-packet-v1.json`,
  SHA-256 `f879a633aa9f4ba4416941379d101deee6798e4880c60675e71c7de245c085a3`.
- `uv run python tools\\check_governance.py` and `git diff --check` passed.

## Closure rationale

The authorized M182 batch reached completed terminal reports for all 33 frozen
development cases.  It used 36 provider HTTP requests and 69 completion slots,
within the 69-request/102-slot caps, with no retry or resume.  M182 establishes
continuation and terminal-report completeness only; interpretation of the
provider outcomes and any subsequent route decision require a separately
selected independent terminal-review workpack.

## Permitted stop conditions

Independent review, a failed acceptance check, frozen-scope drift, or a
required policy/runtime/provider change outside this continuation contract.

## Out of scope

Hosted execution, credential access, provider construction, new cases/cards,
input or manifest changes, retry, resume, budget reuse, token/deadline/model
changes, executor changes, held-out use, and interpretation of provider
results.
