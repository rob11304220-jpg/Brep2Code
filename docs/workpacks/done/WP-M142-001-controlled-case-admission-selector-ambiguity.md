# WP-M142-001: Controlled Case Admission — Selector-Ambiguity Pilot

- Status: done
- Milestone: M142
- Trigger consumed: `WP-TRG-027`
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

M141 is complete and independently reviewed. The user selected the planar-face
selector decision gap: unique binding versus a twin-boss multi-candidate result
that must stop fail-closed. No open-ended case hunt is permitted.

## Frozen pilot

- Decision source: `docs/corpus/knowledge/decisions/q01-selector-ambiguity-v1/decision.json`.
- Fixed unique oracle: the existing `face-selected-dependent-cut-v1` record;
  cardinality one is the sole permitted bind.
- Fixed discriminating candidates:
  `param_selector_ambiguity_twin_centered_nominal` (development) and
  `param_selector_ambiguity_twin_offset_nominal` (held-out). Both must report
  cardinality two and end at `FailClosedAmbiguous` before a dependent action.
- Fixed negative controls: `wrong-face-injection` and
  `coordinate-tie-breaker-injection`.

The held-out candidate is existing evidence only: this workpack must not inspect
or execute it beyond the already-reviewed, hash-pinned audit material.

## Goal

Define and validate an admission-record specification by which a bounded B-Rep
case may become a reviewed reference modeling sequence. The admission record is
an auditable evidence source, not runtime LLM context, a card, a retrieval
document or a hosted input.

## Scope

- Define and pilot one immutable admission record for the user-selected
  coverage-matrix decision gap, using an existing bounded case/pair before any
  new-case production: family/grammar, input hash, parameters,
  development/held-out split, expected sequence, editability mutation and
  negative controls.
- Implement or strengthen deterministic replay/hash, geometry/topology,
  semantic, sequence-contract, editability and split-isolation audits.
- Require stable failure taxonomy and independent review; rejected candidates
  remain evidence and may not be replaced to preserve a desired denominator.
- Define evidence-source fields: observables, operation/parameter dependencies,
  entity-reference stability/ambiguity policy, alternatives, counterexamples,
  repair signatures and source hashes. These fields may support a later
  projection but carry no runtime exposure authority.

## TRG-028 handoff boundary

This workpack produces reviewed admission records only. It must not create or
compile a guidance card, case pack, SDK reference, IR fragment or retrieval
index. `WP-TRG-028` may later select and derive one such projection only from
an approved record, with source linkage, applicability and prohibition fields,
version/hash, split boundary and offline evaluation evidence.

## Compatibility constraints

No external dataset download, provider request, training data creation,
manifest expansion, runtime-card promotion or held-out inspection occurs unless
a later selected package explicitly grants that scope.  Replaying a script is
not sufficient to claim a unique native history or runtime suitability.

## Owner completion boundary

Publish the admission-record schema and selector-pilot audit, with source hashes
and links to the frozen oracle/discriminating/negative-control evidence; run the
required offline checks and obtain Liaol's independent G2 review. Do not create
runtime projections or select TRG-028 as a completion substitute.

## Implementation evidence

- Contract: `docs/architecture/v1/contracts/admission-record-v1.md`.
- Schema and pilot: `docs/corpus/knowledge/admissions/`.
- Offline auditor: `tools/audit_admission_record.py`; it reports the pilot
  record digest and `held_out_access=not_performed`.
- Validation: focused audit tests passed (2); split-safe full test selection
  passed (264, excluding only `tests/test_m29_selector_ambiguity.py`, which
  reconstructs the held-out candidate); full Ruff, governance audit, and
  `git diff --check` passed.

## Closure

Liaol completed the independent G2 review and approved closure on 2026-08-12.
The admission record remains immutable, evidence-only, and held-out-isolated;
no case, manifest, runtime, provider, or hosted authority was added.

## Permitted stop conditions

Independent review; a reproducible conflict with the frozen selector evidence
or M141 policy; out-of-scope need for new case production, held-out execution,
manifest change, runtime projection or hosted authority; frozen-input drift; or
a reproducible local validation blocker.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff. On closure, archive this workpack and leave TRG-028 deferred.

## Acceptance

```powershell
# M29's existing test reconstructs the held-out candidate; M142 must not do so.
uv run python -m pytest tests -q --ignore tests/test_m29_selector_ambiguity.py
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Out of scope

Open-ended corpus production, broad hosted benchmarking, automatic card
creation, runtime projection, broad retrieval and generic CAD-history recovery
claims.
