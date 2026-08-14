# WP-M94-001: Reference-Guided Through-Hole Variation Preregistration

- Status: done
- Milestone: M94
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Freeze a six-row, family-isolated through-hole variation candidate contract for
later offline production; it must permit testing the M93 question without
creating a case, changing a card or exposing a reference answer.

## Scope

- Add one preregistration record with exactly three development and three
  held-out candidate rows, fixed parameters, canonical sequence, mutations and
  negative controls.
- Run only the generic preregistration intake audit and governance checks.

## Compatibility constraints

No candidate directory, STEP, reference script, registry entry, manifest,
card, runtime, prompt, provider request or hosted authorization is created or
changed.

## Acceptance

```powershell
uv run python tools\audit_sequence_paired_intake.py docs\corpus\sequence-paired\reference-guided-through-hole-variation-v1-preregistration.json
uv run python tools\check_governance.py
git diff --check
```

## Status transition

After owner acceptance, Liaol independently verifies the frozen 3/3 split,
geometry preconditions, exclusions and candidate-only boundary. A later
controlled-production workpack must be separately selected.

## Out of scope

Candidate production, parameter evaluation, card mutation/retrieval, provider
or hosted work, held-out result review, or any generalization claim.

## Owner acceptance

- Added one frozen 3/3 development/held-out candidate-only record with exact
  radius/x pairs, containment preconditions, mutations, semantic invariants,
  split isolation and source-leak rejection.
- `audit_sequence_paired_intake.py`, `check_governance.py`, and
  `git diff --check` passed on 2026-08-10.

## Independent review required

Liaol must verify the six frozen rows, family-isolated split, declared
containment bounds and candidate-only boundary. The review cannot create the
candidate directories, promote a card, or authorize a provider request.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-10.
- Review scope: confirmed the exact six rows, development/held-out family
  isolation, containment bounds, mutations, source-leak rejection and
  candidate-only boundary.
- Closure rationale: M94 freezes a future production contract only. It creates
  no candidate asset, registry entry, manifest, card/runtime authority or
  hosted budget.
