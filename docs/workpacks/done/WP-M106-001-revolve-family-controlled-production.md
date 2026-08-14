# WP-M106-001: Revolve Family Controlled Production

- Status: done
- Milestone: M106
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Produce and audit only the six frozen `revolve-v1` candidate rows.

## Activation condition

M105-001 independently accepted `revolve-v1` with frozen rows, split, oracle,
controls and stop rule. Its preregistration cannot change in this workpack.

## Scope

- Add one deterministic offline producer and family-specific auditor.
- Build each frozen row twice in clean directories and retain normalized STEP
  hash-stability evidence.
- Verify reference replay, Q01-fact completeness, exact sequence, no-input
  execution, geometry, semantic/editability gates, split isolation and all
  declared negative controls.
- Retain every rejected or unsupported row without replacement; successful rows
  remain experimental.

## Attribution question and sampling intent

Can the one frozen full-revolution stepped-radial grammar produce its six
declared deterministic rows under the stated audit contract? Stop after those
six rows and their negative controls; do not add rows, tune parameters or make
a general revolve/reconstruction claim.

## Inputs

- `docs/corpus/sequence-paired/revolve-v1-preregistration.json`
- `docs/architecture/adr/0063-revolve-v1-design-freeze.md`

## Code paths

- `tools/build_m106_revolve_candidates.py`
- `tools/audit_sequence_paired_revolve.py`
- `tests/test_sequence_paired_revolve.py`
- Six experimental directories under `case-library/self-authored/param_revolve_*`

## Docs to update

- `docs/workflow/status.md`, this workpack and its active handoff
- Only directly affected corpus navigation or architecture records

## Trace/schema changes

None. Candidate-local `case.json` and `candidate_sequence.json` use the
existing case-library conventions; no report/trace, manifest, CLI or runtime
schema changes are permitted.

## Decision-package impact

- `decision_id`: none; this is family-scoped offline production.
- Q01/Q02 effect: validates only the frozen profile/axis facts and constrained
  full-angle revolve action.
- Q03/Q04 effect: validates the declared no-input, geometry and semantic gates
  without changing shared gate policy.
- Evidence role: deterministic oracle, editability and negative-control
  evidence for six experimental rows.
- Knowledge disposition: no reusable runtime knowledge or experience card.

## Compatibility constraints

Offline and credential-free. Do not promote candidates to active cases or add
them to registry/catalog/manifest, provider, training, runtime, packs or cards.
Do not modify the frozen preregistration, existing cases, shared Harness
behavior or hosted budgets.

## Acceptance

```powershell
uv run python tools\build_m106_revolve_candidates.py
uv run python tools\audit_sequence_paired_revolve.py
uv run python tools\audit_case_library.py --replay
uv run python -m pytest -m fast -q
uv run python -m pytest tests\test_sequence_paired_revolve.py -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Status transition

After owner acceptance, obtain Liaol's independent review before closure. Then
update `status.md` first, move this workpack to `done/`, and archive the
handoff. The evidence-review successor remains separately user-selected.

## Current acceptance evidence

- Passed: deterministic six-row generation with clean-directory hash checks,
  `tools/audit_sequence_paired_revolve.py`, focused revolve pytest, and Ruff.
- Pending: `tools/audit_case_library.py --replay` stopped in an existing
  active-library reference replay because `output/model.step` was absent. The
  failure did not identify an M106 experimental candidate, which is not in the
  active registry. Exact replay diagnosis did not reproduce it; the subsequent
  complete replay audit passed.

## Owner acceptance

- Six frozen rows passed clean-directory hash checks, family audit, complete
  case-library replay audit, fast tests (66 passed), focused test (1 passed),
  Ruff, governance and diff checks.
- No row was substituted and candidates remain experimental and outside all
  registry, manifest, provider and runtime paths.

## Review required

Liaol must verify the fixed six-row release, hashes, split/negative controls,
terminal acceptance evidence, and absence of promotion or hosted scope before closure.

## Independent review and closure

- Reviewer: Liaol
- Status: approved on 2026-08-11.
- Review scope: confirmed the fixed six-row experimental release, hash stability,
  split and negative-control boundaries, terminal acceptance evidence, and no
  promotion, manifest, provider, runtime or hosted changes.
- Closure rationale: this work establishes only controlled experimental release
  evidence; the separately selected evidence-review route controls any later
  disposition.

## Out of scope

Promotion to active cases, executable manifests, packs/cards, provider use,
hosted work, reference-assisted qualification, or any unfreezing/substitution
of the six rows.
