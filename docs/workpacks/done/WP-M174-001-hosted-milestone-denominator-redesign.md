# WP-M174-001: Hosted Milestone Denominator Redesign

- Status: done
- Milestone: M174
- Owner: Codex
- Risk tier: G1

## Entry condition

M173 deferred because the current runtime CAD card supports only three direct
roles, not the twenty distinct card-qualified rows required by M172. The user
explicitly selected a no-card 30-case cohort plus a three-case card feasibility
annex on 2026-08-14.

## Goal

Replace the infeasible equal-card-strata denominator with two unpooled,
interpretable development-only evidence products before M173 selects any row.

## Scope

- Freeze a 30-case no-card main-cohort claim, controls, completion accounting,
  repair boundary, metrics, non-claims, and stop rules.
- Freeze a distinct three-case card-assisted feasibility annex using only the
  existing direct `vertical-cylinder-construction` roles.
- Reconcile the current authoritative self-authored registry total and split
  counts with the older M145 descriptive inventory, without inspecting case
  geometry or held-out assets.
- Update ADR-0084, durable route/charter documentation, M173's re-entry
  criteria, status, and handoff.

## Decision-package impact

- Hypothesis ID: not applicable; campaign-denominator redesign.
- Q01--Q04: preserves existing bounded interfaces; it changes interpretation
  and accounting only.
- Evidence role: no-card main cohort plus unpooled three-role card feasibility.
- Counterexample: a pooled metric, inferred card eligibility, an undeclared
  split, or registry/report discrepancy that cannot be explained stops adoption.
- Stop rule: a need to select rows, alter repair/Harness/provider/runtime,
  inspect held-out assets, or add a card is outside this G1 scope.
- Adoption boundary: charter only; M173 remains the sole row-qualification gate.

## Compatibility constraints

Offline and credential-free. Do not select cases, create a manifest, access
held-out assets, issue provider requests, alter a card/index/Harness/repair
policy, or expand reference/retrieval behavior.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the two-denominator charter, reconciled metadata result, and durable
route alignment. M173 may then resume under its revised qualification criteria.

## Owner completion evidence

- Reconciled the source-count discrepancy from metadata and local history:
  the current authoritative registry has 84 rows (36 development, 27 held-out,
  21 undeclared). Commit `2994fd0` removed three historical
  `param_offset_rounded_slot` held-out rows after M145's 87-row descriptive
  snapshot. No held-out asset was read.
- Published the binding asymmetric charter. It separates the 30 distinct
  no-card main-cohort rows from the three existing direct card roles, retains
  the one-edit source-only repair surface, and states three versus four maximum
  completions respectively.
- Marked M172's equal-strata charter historical and updated M173's re-entry
  condition to require a fresh qualification ledger after M174 closure.

## Validation evidence

- `uv run python tools\check_governance.py` passed.
- `git diff --check` passed with existing LF/CRLF warnings only.

## Closure rationale

M174 closes because it replaced the infeasible equal-card denominator with two
unpooled, evidence-compatible products and reconciled the authoritative
registry count without reading held-out assets. The user confirmed re-entry to
qualification through M175; no campaign freeze or hosted authority follows.

## Status transition

Update `status.md` first, then move this workpack to `done/` and update the
active handoff. Activate only M175's G2 qualification ledger.

## Permitted stop conditions

A registry/source ambiguity that cannot be reconciled from metadata, or any
needed case, manifest, runtime, repair, provider, or hosted change.

## Out of scope

Actual case qualification, card projection, campaign freeze/execution,
provider/hosted activity, held-out use, manifests, and model/prompt changes.
