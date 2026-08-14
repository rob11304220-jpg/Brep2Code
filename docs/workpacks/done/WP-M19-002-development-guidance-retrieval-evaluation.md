# WP-M19-002: Development-Only Guidance Retrieval Evaluation

- Status: done
- Milestone: M19
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Determine offline and on the development split whether retrieving a small,
evidence-bounded set of experience cards improves repair routing without
introducing gate regressions or invalid generalization.

## Entry criteria

- One candidate mechanism has at least three independent `direct` cases in
  source-linked experience cards.
- The supporting cases, counterexamples, card version, development manifest,
  baseline policy, and fixed evaluation metric are preregistered.
- No held-out result has been used to author the candidate general rule.

Do not select this workpack merely because cards exist or a case-local
treatment passed.

## Scope

- Build an offline-only retrieval fixture over the explicit card index; return
  a bounded top-k list with source identifiers and no broad document reads.
- Compare a frozen no-card baseline with the same development cases and policy
  using deterministic/fake-provider or fixed-script controls.
- Record retrieval precision, unsupported-action rate, execution/output
  readability, and existing gate outcomes.  Treat any new gate regression as
  a stop signal.

## Preregistration

- Mechanism/card: `vertical-cylinder-construction-v1` and only
  `vertical-cylinder-construction` at the indexed experimental version.
- Fixed development cases: `cylinder`, `block_with_hole`, and
  `three_hole_plate`; no held-out input, extra case, or card is admissible.
- Policies: baseline returns no cards; treatment applies deterministic top-k=1
  selection only when the case's predeclared role matches the card scope.
- Metric: report per-case selection precision, unsupported-action rate, fixed
  action/contract agreement, output-readability fixture disposition, and gate
  disposition. Expected information gain is whether bounded selection can be
  distinguished from no-card without a new unsupported action or gate
  regression.
- Stopping condition: stop and reject runtime promotion on any unsupported
  action, new gate regression, missing fixture/source hash, or non-determinism.

## Code paths

- `tools/evaluate_reference_pack_retrieval.py`
- `tools/audit_reference_pack_retrieval.py`
- `tests/test_reference_pack_retrieval.py`
- `docs/corpus/reference-packs/`

## Docs to update

- `docs/runbooks/runtime-guidance-cards.md`
- `docs/workflow/status.md`
- active handoff

## Decision-package impact

- `decision_id`: none; this is an ADR-0016-gated offline evaluation.
- Q01/Q02 effect: none; evaluation consumes fixed, already observed roles and
  does not alter B-Rep observation or CAD construction behavior.
- Q03/Q04 effect: records a frozen retrieval-selection comparison only; it
  must not alter execution, gates, or repair routing in production.
- Evidence role: development-only discriminating baseline/treatment evidence.
- Knowledge disposition: retain the card as experimental or reject retrieval;
  no runtime promotion is implied.

## Trace/schema changes

No production `signal_bundle.json`, provider trace, corpus-report schema, CLI,
or runtime-resource mount change is allowed.  Evaluation evidence may use a
separate ignored local report with the card-index hash and manifest hash.

## Compatibility constraints

Remain offline, credential-free, and development-only.  Do not mount cards in
the production executor, modify prompts, add a provider request, broaden a
helper/parser/IR/SDK, or use held-out as an authoring input.

## Acceptance

- The preregistration states the mechanism, evidence rows, counterexamples,
  split, metric, expected information gain, and stopping condition.
- Every selected card passes `uv run python tools/audit_runtime_guidance.py`.
- The baseline and treatment are reproducible under the same executor and
  case policy.
- The review either rejects retrieval, retains it as experimental, or selects
  one separately scoped runtime-integration workpack.  It makes no hosted or
  model-quality claim.

```powershell
uv run python -m pytest -m fast -q
uv run python -m pytest tests\test_reference_pack_retrieval.py -q
uv run python tools\audit_runtime_guidance.py
uv run python tools\audit_reference_pack_retrieval.py
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Evidence reuse / guidance-card disposition

Retain `vertical-cylinder-construction` as experimental only if the treatment
has no unsupported action or gate regression. The result is not a new card and
does not mount, inject, or retrieve cards in production.

## Owner acceptance record

- Added a fixed M19 preregistration and fail-closed audit for exactly three
  development cases and top-k=1. The baseline always returns no cards; the
  treatment selects only `vertical-cylinder-construction` for the three
  declared roles and rejects every other case/role.
- The isolated evaluator supplies the card only as an explicit local evaluator
  input. It runs the same fixed local reference-script control under both
  policies and reports card/index/contract hashes, selection precision,
  unsupported-action rate, output readability, and existing geometry gates.
- Result: treatment selected the expected card for all 3/3 cases with
  precision 1.0 and unsupported-action rate 0; baseline selected no cards.
  Both policies' fixed controls were readable and passed existing gates for
  all 3/3 cases. This is no evidence of LLM quality or Harness runtime access.
- 2026-08-10 owner checks passed: M83/M84/M19 audits; runtime-guidance audit
  (4 cards); M19 focused tests (3 passed); fast suite (64 passed, 130
  deselected); full suite (194 passed in 183.88s); full Ruff; governance audit;
  and `git diff --check`.
- Owner disposition: retain the card and retrieval evaluator as experimental.
  Pending independent review, do not select M19-003 or make runtime changes.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-10.
- Closure rationale: The frozen no-card versus top-k=1 comparison passed with
  no unsupported action or gate regression. The result is bounded to the three
  development controls and justifies this separately selected M19-003 only; it
  makes no hosted/model claim and does not itself mount a card in runtime.

## Status transition

Update `docs/workflow/status.md`, this workpack, the active handoff, the
guidance-card runbook, and any affected contract/module documentation.  An ADR
is required if the evidence threshold or runtime boundary changes.

## Out of scope

Hosted comparison, held-out evaluation, production retrieval, prompt injection,
automatic trace mining, model training, and all changes to unrelated active
workpacks.
