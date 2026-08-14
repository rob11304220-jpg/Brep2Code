# WP-M84-001: Reference-Pack Direct-Evidence Qualification

- Status: done
- Milestone: M84
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Determine whether one candidate reference-pack mechanism has three independent
direct, source-linked development cases and bounded counterexamples sufficient
to satisfy ADR-0016's entry threshold for M19-002.

## Scope

- Preregister one mechanism, three independent development cases, their
  counterexamples, source links, fixed fake/fixture policy, and stopping rule.
- Produce offline direct evidence that the pack selects only its declared OCP
  action/contract and never produces an unsupported API recommendation.
- Create or reject source-linked experimental experience cards; record why the
  M19 threshold is or is not satisfied.

## Inputs

- `docs/corpus/reference-packs/reference-pack-contract-v1.json`
- ADR-0016 and the three fixed source records for `cylinder`,
  `block_with_hole`, and `three_hole_plate`

## Code paths

- `docs/corpus/reference-packs/m84-cylinder-construction-qualification-v1.json`
- `runtime_resources/experience-cards/cards/vertical-cylinder-construction.json`
- `tools/audit_reference_pack_qualification.py`
- `tests/test_reference_pack_qualification.py`

## Trace/schema changes

Additive development evidence and one experimental static card only. Do not
change signal bundles, provider/tool traces, corpus or executable manifests,
storage layout, CLI output, or runtime resource mounting.

## Attribution question and sampling intent

The preregistered mechanism is `vertical-cylinder-construction-v1`: creating a
vertical circular primitive with `OCP.BRepPrimAPI.BRepPrimAPI_MakeCylinder`.
The fixed cases are `cylinder` (final primitive), `block_with_hole` (single
boolean-cut tool), and `three_hole_plate` (repeated boolean-cut tool). Their
different geometry/operation roles establish independence; no parameter
variant, extra case, or held-out case may replace a failed member. Stop after
the static source/action audit and record either qualification or rejection.

## Compatibility constraints

No runtime retrieval, prompt injection, resource mount, provider call,
held-out authoring, manifest change, or model-quality claim. A passing oracle
or repeated parameter family does not count as independent direct evidence.

## Acceptance

- An independent review identifies three truly independent direct cases or
  records the exact unmet criterion.
- Every candidate card passes `tools/audit_runtime_guidance.py`.
- The outcome explicitly either unlocks M19-002 or leaves it backlog.

```powershell
uv run python tools\audit_reference_packs.py
uv run python tools\audit_reference_pack_qualification.py
uv run python tools\audit_runtime_guidance.py
uv run python -m pytest tests\test_reference_packs.py tests\test_reference_pack_qualification.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Evidence reuse / guidance-card disposition

Create one source-linked experimental card only if the three fixed cases pass
the audit. The card remains unmounted and does not authorize retrieval; M19-002
becomes eligible for separate user selection, not automatically active.

## Status transition

After independent review, update `docs/workflow/status.md` first, move this
workpack to `done/`, and archive the active handoff. Record whether M19-002 is
eligible for later selection; do not start it as part of this workpack.

## Owner acceptance record

- Preregistered and qualified `vertical-cylinder-construction-v1` using only
  `cylinder`, `block_with_hole`, and `three_hole_plate`. Their roles are,
  respectively, final primitive, single boolean-cut tool, and repeated
  boolean-cut tool; they are fixed distinct cases, not parameter variants.
- Added a source-action audit that checks all three available local scripts
  directly invoke `OCP.BRepPrimAPI.BRepPrimAPI_MakeCylinder`, retain the M83
  source/hash boundary, and reject duplicate roles or case substitutions.
- Added one source-linked experimental experience card. It is unmounted and
  bounded to observed +Z circular primitive/tool roles and their recorded
  counterexamples; it does not grant retrieval or runtime authority.
- 2026-08-10 owner checks passed: M83 pack audit; M84 qualification audit;
  runtime-guidance audit (4 cards); focused tests (4 passed); full Ruff;
  governance audit; and `git diff --check`.
- Pending independent G2 review by Liaol: verify directness/independence, the
  static card boundary, counterexamples, and that M19-002 is merely eligible
  for separate selection rather than active.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-10.
- Closure rationale: The three fixed source-linked cases establish only the
  stated +Z cylinder-construction action across distinct final-primitive and
  cut-tool roles. The experimental card remains unmounted and bounded by its
  counterexamples. This satisfies ADR-0016's entry threshold, making M19-002
  eligible for separate selection without changing runtime behavior.

## Out of scope

M19 retrieval evaluation, production runtime behavior, hosted comparison, or
changing the ADR-0016 threshold.

## Repair hypothesis and evaluation boundary

This is offline, development-only source/action qualification, not a repair or
model evaluation. It cannot claim reconstruction quality or general cylinder
handling beyond the exact observed +Z primitive/tool roles and counterexamples.
