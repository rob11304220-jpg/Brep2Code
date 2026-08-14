# WP-M86-001: Multi-role Reference-assisted Offline Admission

- Status: done
- Milestone: M86
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Extend the M85 two-stage path offline to the three already-qualified roles of
the frozen `vertical-cylinder-construction` card.  A provider may request only
the preregistered role for each fixed development case; the Harness resolves
that role to one hash-bound card, then applies the unchanged OCP, sandbox,
provenance, output, and geometry gates.

## Scope

- Add a bounded, revision-scoped role-to-card selection contract that rejects
  undeclared, ambiguous, unavailable, or hash-drifted selections.
- Run deterministic fake-provider acceptance for exactly `cylinder` (final
  primitive), `block_with_hole` (single boolean-cut tool), and
  `three_hole_plate` (repeated boolean-cut tool).
- Preserve M85's fixed one-card `cylinder` API and all default no-guidance
  behavior.

## Attribution question and sampling intent

Distinguish a correctly constrained role selection from a broad retrieval or
quality claim.  The fixed three cases are the direct-evidence cases recorded
by M84; no parameter variants, P1 cases, held-out cases, or new cards may
replace a failing member.  Stop after deterministic fake-provider evidence;
hosted use requires a separate selected workpack and explicit authorization.

## Inputs

- `runtime_resources/experience-cards/index.json`
- `runtime_resources/experience-cards/cards/vertical-cylinder-construction.json`
- `docs/corpus/reference-packs/m84-cylinder-construction-qualification-v1.json`

## Code paths

- `brep2code/agent/guidance.py`
- `brep2code/agent/observed_build.py`
- `brep2code/agent/provider.py`
- `tests/test_guidance_bridge.py`
- `tests/test_observed_build_loop.py`

## Docs to update

- `docs/architecture/v1/contracts/llm-tool-bridge.md`
- `docs/modules/harness.md`
- `docs/workflow/status.md`
- active handoff and this workpack

## Trace/schema changes

The additive `guidance` signal metadata continues to record only index hash,
returned card ID, tool result, and now the selected role.  It must not record
raw STEP, reference scripts, local paths, prompts, or provider content.

## Decision-package impact

- `decision_id`: none; this is a development-only runtime-contract admission.
- Q01/Q02 effect: a bounded provider tool call can select one predeclared role
  from a frozen card mapping before script generation.
- Q03/Q04 effect: no gate, repair, or stopping rule changes.
- Evidence role: deterministic regression and negative-control evidence.
- Knowledge disposition: no new reusable knowledge; M84's existing card is
  reused only within its declared scope.

## Compatibility constraints

Offline only; no provider request, external data, credential use, manifest
change, card mutation, new card, retry, repair, held-out use, or gate
relaxation.  The default remains network-free and has no guidance access.

## Acceptance

```powershell
uv run python -m pytest -m fast -q
uv run python -m pytest tests/test_guidance_bridge.py tests/test_observed_build_loop.py -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools/check_governance.py
git diff --check
```

## Evidence reuse / guidance-card disposition

Reuse only the existing source-linked `vertical-cylinder-construction` card.
No new card is created and no quality/generalization claim is permitted.

## Status transition

On owner acceptance, record terminal commands and await Liaol's independent
G2 review.  On approval, update `docs/workflow/status.md` first, move this
workpack to `done/`, and archive the active handoff.  No hosted work starts.

## Owner acceptance record

- The two-stage provider request now carries the one preregistered guidance
  role, and the provider-adapter instruction serializes that exact role rather
  than assuming `final primitive`. The existing M85 `cylinder` role remains
  unchanged.
- The bounded guidance trace and additive signal metadata now record the
  selected role alongside the existing index hash and returned card ID.
- Deterministic fake-provider runs passed the fixed M84 matrix: `cylinder` /
  `final primitive`, `block_with_hole` / `single boolean-cut tool`, and
  `three_hole_plate` / `repeated boolean-cut tool`. Each used exactly two fake
  requests and passed unchanged OCP script-contract, `wsl-bwrap`, provenance,
  output, bbox, volume, and topology gates.
- Existing malformed-call, unavailable-bundle, undeclared-card, and hash-drift
  tests retain the fail-closed negative paths.
- 2026-08-10 owner checks passed: fast suite (64 passed, 140 deselected),
  focused guidance/observed-build suite (28 passed), full suite (204 passed),
  Ruff, governance audit, and `git diff --check`.

## Independent review

- Reviewer: Liaol
- Outcome: approved on 2026-08-10.
- Review scope: verify the role is predeclared by the Harness rather than
  selected from a path or broad card corpus; verify M85 compatibility, trace
  redaction, fail-closed negative paths, and no hosted/generalization claim.

## Closure rationale

Liaol independently approved the bounded role-selection change and its
offline evidence. The fixed M84 three-case matrix passes only with the one
qualified vertical-cylinder card and unchanged gates. This closes M86's
offline admission only; it does not authorize a new card, broad retrieval,
hosted evaluation, retry, or M73 activation.

## Out of scope

Hosted validation, broader retrieval, card ranking, automatic card authoring,
P1 expansion, M73 activation, or a claim that the model can infer arbitrary
feature roles from B-Rep observations.
