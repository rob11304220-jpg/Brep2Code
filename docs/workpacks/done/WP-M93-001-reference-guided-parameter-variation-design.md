# WP-M93-001: Reference-Guided Parameter-Variation Design

- Status: done
- Milestone: M93
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Freeze an offline-only contract for testing whether a bounded derived reference
card can guide independent reconstruction of a family-isolated, unseen
parameter combination without exposing a reference answer.

## Scope

- Define the candidate mechanism as the already qualified
  `vertical-cylinder-construction` action only.
- Treat existing `param_through_hole_low`, `nominal`, and `high` records as
  development evidence only; `param_blind_hole_*` and M90 records are excluded
  because they change the semantic mechanism or lack a qualified card.
- Define required future preregistration, split isolation, offline fake-provider
  gates, source-leak audit, and a later held-out hosted authorization boundary.

## Compatibility constraints

Design only. Do not create cases, alter cards/manifests/Harness, expose scripts
or STEP, modify prompts, run a provider, or claim parameter generalization.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Status transition

After owner acceptance, Liaol independently reviews the exact candidate/
exclusion boundary, no-leak contract, split rule and hosted non-authorization.
On approval, archive this workpack; later production or evaluation requires a
new separately selected workpack.

## Out of scope

Any actual parameter-family production, card mutation, retrieval change,
hosted request, held-out evaluation, or new coverage family.

## Owner acceptance

- Added the through-hole design boundary, explicit exclusions, no-leak content
  contract, offline evidence gates and later G3 hosted requirements.
- Verified all referenced design targets exist; `check_governance.py` and
  `git diff --check` passed on 2026-08-10.

## Independent review required

Liaol must verify that the design does not convert development records into
held-out evidence, expose source material, authorize a card/runtime change or
pre-authorize hosted evaluation. The review decides only whether a successor
production workpack may be selected.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-10.
- Review scope: confirmed the existing through-hole rows remain development
  evidence only; blind-hole and M90 exclusions, source-leak controls, and the
  separate future hosted boundary remain explicit.
- Closure rationale: the design supports a separately selected preregistration
  package only; it creates no assets, card/runtime authority or hosted budget.
