# WP-M135-001: Frozen Hosted Batch Epoch Preflight and Execution

- Status: blocked
- Milestone: M135
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Turn M134's frozen `existing-family-development-v1` cohort into one
preflight-verifiable, monitorable, serial 18-condition epoch.  No provider
request may be constructed or issued unless the complete local preflight and
independent G3 review pass and the user later grants itemized authorization.

## Scope

- Freeze a single epoch policy identity, condition order, outbound-content
  contracts, provider/model, deadline, output cap, executor, request cap, and
  fresh report and monitor paths from the completed M120 and M123--M126
  charters without changing their cases, cards, prompts, or family claims.
- Implement only the dedicated local epoch checkpoint/runner surface required
  to prove 18-condition accounting, serial scheduling, per-condition terminal
  continuation, and M134's epoch-integrity stops with a fake provider.
- Complete the local G3 preflight: exact input/card/policy hashes and split
  membership, no-input `wsl-bwrap` controls, non-secret configuration/model
  check, fixed budget/deadline/cap validation, and report/monitor freshness.
- Record the later itemized authorization payload only if all checks pass.

## Attribution question and sampling intent

This package distinguishes whether the already frozen 18 development
conditions can be issued and interpreted under one accountable epoch boundary.
It does not estimate a capability rate or alter a family question.  Stop on a
preflight failure, an epoch-integrity fault, independent review, or after the
authorized epoch reaches a terminal state.

## Inputs

- `docs/workflow/m134-frozen-hosted-batch-epoch-policy.md`
- `docs/architecture/adr/0067-frozen-hosted-batch-epochs.md`
- `docs/workflow/m120-prismatic-development-campaign-charter.md`
- `docs/workflow/m123-repeated-feature-development-campaign-charter.md`
- `docs/workflow/m124-axisymmetric-revolve-development-campaign-charter.md`
- `docs/workflow/m125-dependent-face-selection-development-campaign-charter.md`
- `docs/workflow/m126-multi-inner-loop-pocket-development-campaign-charter.md`
- `docs/workflow/m127-shared-hosted-stability-reentry-preflight.md`
- `docs/runbooks/llm-provider-config.md`

## Code paths

- `brep2code/**` and focused `tests/**` only for the dedicated frozen epoch
  checkpoint and fake-provider accounting path.
- `tools/check_governance.py`

## Docs to update

- `docs/workflow/status.md`
- this workpack and one active handoff
- a M135 preflight record under `docs/workflow/`
- `docs/runbooks/llm-provider-config.md` and relevant contracts only if the
  runner introduces a lasting CLI/checkpoint contract

## Trace/schema changes

One new epoch report/checkpoint contract is expected.  It must preserve the
frozen epoch identity, all 18 condition identities and states, request
accounting, integrity-stop classification, provider/model, and no secrets or
raw provider content.  Any schema decision must be documented before hosted
authorization.

## Decision-package impact

- `decision_id`: no Q01--Q04 decision package; hosted evaluation governance.
- Q01/Q02 effect: no observable, sequence, case, card, or prompt change.
- Q03/Q04 effect: implements M134's frozen accounting and terminal-routing
  policy only.
- Evidence role: development-only comparative hosted observation readiness.
- Knowledge disposition: no reusable knowledge until M136 independently
  reviews a terminal epoch.

## Compatibility constraints

Default operation remains offline and credential-free.  Do not alter an input,
split, reference script, guidance card, provider, model, endpoint, system
instruction, executor, family charter, prompt, runtime behavior, or held-out
scope.  Do not construct a provider, call a provider, print a credential, or
reuse an old report, monitor, budget, or authorization.  At most one request
may be in flight once authorized; repair and retry are zero.

## Acceptance

```powershell
uv run python -m pytest tests\test_observed_build_loop.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

The owner must additionally record every required hosted-preflight result.

## Owner completion boundary

Publish the frozen epoch runner/policy and M135 local preflight record; pass
the listed checks, obtain Liaol's independent G3 review, and then request (not
issue) itemized hosted authorization.  If granted, execute only the frozen
epoch and preserve its terminal evidence for M136.

## Permitted stop conditions

Independent review; explicit hosted authorization; frozen-input drift;
out-of-scope dependency; or reproducible local preflight/validation blocker.

## Evidence reuse / guidance-card disposition

No reusable knowledge.  The prismatic card remains a hash-pinned treatment
input only; the other twelve family conditions remain no-card.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff.  Run governance audit after every lifecycle-record edit.  M136 is the
separately selected offline remediation; the terminal review is rescheduled as
M137.

## Out of scope

Any held-out run, new case/card, card promotion, prompt/model/provider change,
repair/retry, in-epoch policy mutation, external data, runtime promotion, or
post-epoch remediation.

## Owner blocker (2026-08-12)

The frozen no-card `wsl-bwrap` preflight failed reproducibly at
`axisymmetric_revolve:param_revolve_centered_low:no_card`.  The prismatic
three-row control passed, but M135 requires every frozen condition to pass its
local preflight before authorization.  No provider was constructed, no data was
sent, and no request budget was issued.  This workpack cannot repair, replace,
or skip the failed condition; a later user-selected bounded workpack is needed.

## Blocked closure rationale (2026-08-12)

The designated no-input preflight test was rerun after the blocker was recorded
and failed at the same frozen condition (`1 failed, 3 deselected in 26.48s`).
The mandatory preflight record is
[`m135-frozen-epoch-preflight-blocked.md`](../../workflow/m135-frozen-epoch-preflight-blocked.md).
The owner-completion boundary is unmet. M136-001 is the separately selected,
offline-only remediation; it does not reopen M135, alter its frozen cohort, or
grant hosted authority.
