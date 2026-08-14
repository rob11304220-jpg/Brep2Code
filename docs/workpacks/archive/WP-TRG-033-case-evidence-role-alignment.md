# WP-TRG-033: Case-Evidence Role Alignment

- Status: deferred
- Owner: unassigned
- Reviewer: independent reviewer required
- Risk tier: G2

## Entry condition

`WP-TRG-031` and `WP-TRG-032` are complete and independently reviewed or
explicitly accepted, the M146 crosswalk audit passes, and the user selects this
package.

## Goal

Align existing case metadata/documentary evidence with the bounded modeling
hypotheses it supports or refutes, including each asset's evidence role.

## Scope

- Add a versioned, source-linked **case-evidence relationship layer** from
  selected existing cases to M146 `hypothesis_id` values and oracle,
  discriminating, negative-control, regression, or documentary roles. It must
  be a companion mapping, not an expansion of the M146 crosswalk into a case
  registry.
- Record evidence scope and any known non-generalization through derived
  navigation or approved metadata/documentary links. For held-out material,
  record only previously reviewed documentary relations; do not read a fixture,
  script, raw answer, or unreviewed held-out metadata.
- Audit referential integrity between the companion mapping, hypothesis IDs,
  declared documentary sources, and source authorities after the alignment.

## Compatibility constraints

`case.json`, registry, manifest, and admission records retain authority for
identity, split, hash, lifecycle, executable selection, and disposition. Do
not inspect or execute fixtures/scripts, including held-out material; do not
produce cases or alter splits, lifecycle, manifests, runtime resources, or the
M146 crosswalk's primary hypothesis relationships.

## Acceptance

```powershell
uv run python -m pytest tests -q --ignore tests/test_m29_selector_ambiguity.py
uv run python -m ruff check .
python tools\audit_development_evidence_crosswalk.py
uv run python tools\check_governance.py
git diff --check
```

## Out of scope

Automatic admission/promotion, generic difficulty scoring, Harness behavior,
provider use, training, runtime projection, and hosted evaluation.
