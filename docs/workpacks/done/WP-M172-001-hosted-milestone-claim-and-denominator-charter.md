# WP-M172-001: Hosted Milestone Claim and Denominator Charter

- Status: done
- Milestone: M172
- Owner: Codex
- Risk tier: G1

## Entry condition

M170's offline release closed, and the user-selected M171 fixture remediation
closed with independent G2 approval. This is the next unmet workpack in the
user-selected staged hosted-capability route.

## Goal

Freeze an interpretable, development-only claim and 30-case three-stratum
campaign charter before case assets, card dispositions, campaign inputs, or
any hosted request are considered.

## Scope

- State the sole supported claim, explicit non-claims, reporting population,
  and denominator arithmetic for three predeclared strata of ten: Q01-only/no
  card/no repair; Q01 plus one explicit card/no repair; and full bounded
  Q01/card/generation/gate/classified-repair.
- Freeze campaign-level terminal-gate and first-pass rates, repair
  eligibility/conversion/plateau, tool/card compliance, completion use,
  duration, failure classes, Wilson intervals, controls, attribution limits,
  stop rules, and incomplete-report handling.
- Define the boundary and required inputs for the following G2 case/reference
  qualification workpack, without selecting an asset, card disposition, or
  manifest row.
- Update durable route/contract documentation only for this charter-level
  clarification, keeping status, workpack, and handoff aligned.

## Decision-package impact

- Hypothesis ID: not applicable; campaign-interpretation charter only.
- Q01--Q04 decision: freezes how existing bounded strata will be interpreted;
  changes no interface, execution, repair policy, or provider behavior.
- Evidence role: pre-execution campaign denominator and reporting contract.
- Counterexample: a denominator that lacks a fixed stratum/control, mixes
  card effect with repair effect, or permits post-result cohort selection.
- Stop rule: any required case/card/manifest selection, interface change,
  provider configuration, hosted preflight/request, or a new repair policy
  ends this package and belongs to a later or separately selected scope.
- Adoption boundary: documentation/charter only; it authorizes neither case
  use nor a provider request.

## Compatibility constraints

Offline and credential-free. Do not inspect or select held-out assets; modify
cases, splits, manifests, registries, Harness/tool schema, runtime guidance
behavior, repair policy, provider configuration, model choice, prompts,
budgets, or report paths; or create retrieval/directory search.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the frozen charter and durable route/contract alignment, record
validation evidence, and update status/workpack/handoff. M173 may then be
claimed as the selected G2 case-and-reference qualification workpack.

## Owner completion evidence

- Published `docs/workflow/m172-hosted-milestone-claim-and-denominator-charter.md`.
  It fixes the supported claim, three 10-case strata, denominator arithmetic,
  outcome accounting, controls, attribution limits, and downstream stop rules.
- Linked the durable charter from the current project route without selecting a
  case, card, manifest, provider, model, report path, or hosted input.
- `uv run python tools\check_governance.py` passed; `git diff --check` passed
  with existing LF/CRLF warnings only.

## Closure rationale

M172 closes because the campaign can now be interpreted before any asset is
qualified or selected. Its G1 scope made no runtime, provider, case, manifest,
or hosted change. The route proceeds to the already selected M173 G2
qualification gate.

## Status transition

Update `status.md` first, then move this workpack to `done/` and update the
active handoff. Activate M173 only; no campaign execution or provider activity
is permitted.

## Permitted stop conditions

A required asset/manifest/card selection, a required runtime/provider/hosted
change, frozen-input drift, or a reproducible documentation/governance
validation blocker.

## Out of scope

Case or card qualification, manifest creation, campaign freeze, provider or
hosted activity, credentials, preflight, external data, held-out use, repair
changes, Harness/runtime changes, retrieval, model/prompt changes, and any
30-case execution.
