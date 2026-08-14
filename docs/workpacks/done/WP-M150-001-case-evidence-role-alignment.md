# WP-M150-001: Case-Evidence Role Alignment

- Status: done
- Milestone: M150
- Trigger consumed: `WP-TRG-033`
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

M148/M149 are complete, the M146 crosswalk audit passes, and the user selected
TRG-033.

## Goal

Add a versioned, source-linked companion relationship layer from selected
existing cases and documentary evidence to M146 bounded modeling hypotheses
and declared evidence roles.

## Scope

- Add only relationships already explicit in reviewed knowledge units,
  admission records, or documentary review sources.
- Use case IDs, hypothesis IDs, controlled evidence-role labels, documentary
  source paths/hashes where declared, and non-generalization boundaries; do not
  copy case facts into the mapping.
- Represent held-out evidence only through reviewed documentary relations; do
  not read or record fixture, raw-answer, sequence, input-hash, parameter, or
  case-metadata details for held-out assets.
- Add a deterministic audit and compact navigation that validate companion
  mapping references without changing M146 crosswalk relationships.

## Decision-package impact

- `decision_id`: none; M150 links existing decision evidence only.
- Q01/Q02 and Q03/Q04 effects: none.
- Evidence role: source-linked oracle, discriminating, negative-control,
  regression, and documentary relationships only.
- Knowledge disposition: no runtime knowledge, promotion, lifecycle, split, or
  authority change.

## Compatibility constraints

`case.json`, registry, manifest, and admission records retain authority for
identity, split, hash, lifecycle, executable selection, and disposition. Do
not inspect or execute fixtures/scripts, including held-out material; do not
alter source metadata, manifests, runtime resources, Harness/provider behavior,
or M146 crosswalk source hashes/primary relationships.

## Acceptance

```powershell
uv run python -m pytest tests -q --ignore tests/test_m29_selector_ambiguity.py
uv run python -m ruff check .
python tools\audit_development_evidence_crosswalk.py
python tools\audit_case_evidence_relationships.py
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the companion mapping, navigation, audit, update guidance, validation
record, and obtain Liaol's independent G2 review.

## Owner implementation evidence

- Added `docs/corpus/knowledge/case-evidence-relationships-v1.json`: a
  versioned companion mapping with 14 source-linked relationships to M146
  hypotheses. It retains only controlled role/mode labels, declared case IDs
  where reviewed sources already name them, documentary held-out relationships
  with no held-out case details, and explicit non-generalization boundaries.
- Added `docs/corpus/knowledge/case-evidence-relationships-v1.md` and linked it
  from the knowledge index. It states that rollback has no forced case mapping,
  because its evidence is a fixed-script execution boundary rather than a
  case-evidence relationship.
- Added `tools/audit_case_evidence_relationships.py` and maintenance guidance.
  The audit validates crosswalk/source hashes, hypothesis IDs, controlled roles
  and modes, source-declared case references, forbidden paths, and the absence
  of held-out case IDs in documentary-only relationships.
- Validation on 2026-08-13: Python compilation, companion audit, crosswalk
  audit, Ruff, governance audit, and `git diff --check` passed. The required
  full pytest command produced no output and reached its 180-second outer
  deadline; this is recorded as a non-terminal timeout, neither a pass nor a
  failure.

## Independent review

- Liaol approved the independent G2 review on 2026-08-13 after checking source
  authority preservation, the 14 relationship boundaries, held-out documentary
  isolation, forbidden-path enforcement, audit coverage, and validation record.
- Review result: approved. Companion audit, crosswalk audit, Ruff, governance
  audit, and `git diff --check` passed. The full pytest timeout remains a
  non-terminal limitation and was not represented as a passing run.

## Closure rationale

M150 closes because the bounded companion mapping, navigation, audit, and
maintenance guidance are complete and independently approved. No case source,
lifecycle, split, manifest, runtime, provider, or hosted boundary changed.
Any successor remains deferred until explicitly selected.

## Permitted stop conditions

Independent review; source-authority conflict; required fixture/held-out access;
or a required lifecycle, manifest, runtime, provider, or hosted change.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and active handoff.
On closure archive M150; do not activate TRG-034, TRG-035, or TRG-028.

## Out of scope

Full case inventory classification, automatic admission/promotion, generic
difficulty scoring, code/Harness changes, provider use, training, runtime
projection, and hosted evaluation.
