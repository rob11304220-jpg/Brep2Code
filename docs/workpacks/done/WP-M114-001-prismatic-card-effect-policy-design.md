# WP-M114-001: Prismatic Card-Effect Policy Design

- Status: done
- Milestone: M114
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Freeze a successor-policy design that can make a bounded, finite prismatic
end-to-end card-effect observation discriminating without modifying or reusing
M97 and without inspecting held-out inputs.

## Scope

- Select one estimand and pre-register mutually exclusive terminal categories.
- Specify the required static API-admissibility boundary, equal-context checks,
  attribution rules and stop conditions.
- Specify the separate future development-only policy/review and held-out
  policy/authorization gates. Write an ADR and a compact design record.

## Decision-package impact

- `decision_id`: M93/M94 reference-guided through-hole parameter variation.
- Q01/Q02 effect: no observation or construction action changes; defines how a
  later policy may classify its fixed measured-fact/Q02 result.
- Q03/Q04 effect: separates lifecycle, static API-admissibility, sandbox and
  downstream geometry/provenance outcomes before a later comparison.
- Evidence role: policy-design only; no oracle, hosted or held-out evidence.
- Knowledge disposition: no reusable runtime knowledge.

## Compatibility constraints

Offline and credential-free. Do not inspect held-out cases or inputs; create a
new policy, modify M96/M97, cards, prompts, cases, splits, gates, manifests,
runtime, provider, budget, report or monitor; construct a provider; run
preflight; or issue a request.

## Acceptance

```powershell
uv run python -m pytest -m fast -q
uv run python tools\check_governance.py
git diff --check
```

## Stopping rule

Stop after one design disposition. It may define later prerequisites but cannot
select a development policy, held-out policy or hosted campaign.

## Status transition

Record owner acceptance, then obtain Liaol's independent review before closure.

## Owner acceptance

- [ADR-0065](../../architecture/adr/0065-prismatic-end-to-end-card-effect-policy-design.md)
  and the [M114 design record](../../architecture/v1/m114-prismatic-card-effect-policy-design.md)
  choose one finite end-to-end estimand and preregister its discriminating
  interpretation boundary.
- The design leaves M97 terminal; it neither creates a successor policy nor
  names inputs, provider, request budget, report path or authorization.
- The required future order is a separately selected development-policy freeze,
  independent review, then (only after separate G3 gates) a development
  calibration and possible later held-out policy.
- Validation: `uv run python -m pytest -m fast -q` passed (66 passed, 165
  deselected); governance and `git diff --check` passed. A PowerShell runner
  emitted a non-terminal out-of-memory message, but all three commands reached
  their documented terminal success results; it is not design evidence.

## Independent review required

Liaol must verify the design does not reinterpret M97, that static API
admissibility is classified before sandbox/downstream gates, that paired
interpretations are bounded, and that no policy/provider/held-out authority was
created.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-11.
- Review scope: confirmed the finite end-to-end estimand, predeclared failure
  taxonomy, M97 non-reuse boundary, later development/held-out separation and
  absence of provider, held-out or runtime authority.
- Closure rationale: M114 supplies an offline design prerequisite only. A
  future development-only policy freeze remains separately user-selected and
  cannot activate hosted work.

## Out of scope

Any policy implementation, calibration, held-out evaluation, provider
construction, preflight, authorization, retry, repair, capacity reuse or
generalization claim.
