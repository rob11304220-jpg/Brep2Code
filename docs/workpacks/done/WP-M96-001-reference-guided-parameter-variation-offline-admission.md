# WP-M96-001: Reference-Guided Parameter-Variation Offline Admission

- Status: done
- Milestone: M96
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Establish offline that a finite, path-free observation transcript supplies the
facts required by the existing bounded cylinder card, and freeze the paired
hosted evaluation policy before any held-out row is observed.

## Scope

- Use only the M95 development assets for deterministic fake-provider
  card/no-card acceptance.
- Require observed radius, axis, through-cut and x-position facts; absence or
  ambiguity must fail closed.
- Retain no-input `wsl-bwrap`, script API, provenance, output and geometry
  gates, and add source-leak negative controls for transcript/card payloads.
- Preregister card/index hashes, prompts, CLI policy, scoring, held-out order
  and the M97/M98 request accounting before held-out execution.

## Attribution question and sampling intent

Distinguish a bounded observation/card admission from an LLM or hosted result.
The fixed M95 development assets may test deterministic fake-provider behavior;
held-out assets must not tune the card, policy, prompt or observation schema.

## Inputs

- M95's six experimental candidate records and the M94 frozen contract.
- `runtime_resources/experience-cards/index.json` and the existing
  `vertical-cylinder-construction` experimental card.
- Existing observed-build fake-provider and no-input `wsl-bwrap` test paths.

## Trace/schema changes

Any additive offline transcript/policy fixture must remain path-free and
cannot include raw STEP, local paths, reference scripts, hashes or concrete
reference parameter answers.  No hosted report/schema change is allowed.

## Compatibility constraints

Offline only.  No provider call, manifest promotion, broad retrieval, card
mutation, held-out inspection for tuning, gate relaxation or credential use.

## Acceptance

Run focused fake-provider and leak-control tests, full applicable tests, Ruff,
governance audit, `git diff --check`, and the no-input sandbox preflight.

## Owner acceptance

- Added a development-only M96 measured-fact adapter.  It derives a path-free
  transcript from the B-Rep itself, requiring one +Z cylindrical face and two
  exterior openings; it emits only base bbox plus radius, axis, centre and
  through extent.  It rejects any held-out-row transcript derivation.
- Extended the generic observation-context rejection set to cover reference
  scripts, source hashes and provider payload fields.  No raw STEP, path,
  reference script, hash or case-specific answer can enter the M96 transcript.
- Added the pre-held-out frozen M96 policy: fixed existing card/index hashes,
  `single boolean-cut tool` role, no-card baseline, no-input executor, zero
  retry/repair, explicit three-row held-out order and nine-request maximum for
  each later G3 package.  This is a policy record only, not a provider path.
- Existing observed-build fake-provider regressions retain card/no-card and
  no-input Harness behavior; the new M96 tests verify measured facts,
  held-out fail-closed behavior, source-field rejection and policy/hash pins.
- 2026-08-10 terminal validation: M96 focused tests and observed-build suite
  completed successfully; fast suite passed (66 passed, 153 deselected); full
  pytest completed successfully; Ruff passed; governance audit passed; and
  `git diff --check` passed.

## Status transition

Independent G2 approval makes M97 eligible for separate selection.  It does
not provide a hosted budget or authorization.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-10.
- Review scope: confirmed the development-only measured-fact boundary,
  held-out fail-closed rule, source-field rejection, and frozen policy/card
  hash/request-budget contract.
- Closure rationale: M96 establishes offline readiness only.  It does not send
  provider data or authorize M97's separate development hosted budget.

## Out of scope

Hosted execution, held-out result review, model-quality claims and generic
feature inference.
