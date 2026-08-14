# WP-M107-001: Revolve Family Evidence Review

- Status: done
- Milestone: M107
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Review the completed six-row `revolve-v1` experimental release and decide one
family-scoped disposition: a later lifecycle-promotion proposal, a
counterexample, or no reusable knowledge.

## Activation condition

The user selected `WP-TRG-014`. M105-001's design freeze and M106-001's
controlled production both have independent review and terminal audit evidence.

## Scope

- Re-run read-only family and library replay audits against the frozen six rows.
- Review the fixed rows/split, clean-directory hash stability, Q01/Q02 facts,
  exact sequence, semantic/editability gates, and declared negative controls.
- Write one bounded evidence-review record and update only read-only portfolio
  navigation to reflect this active review.
- Propose at most one separately selected successor for lifecycle promotion.

## Attribution question and sampling intent

Does the frozen full-revolution stepped-radial grammar have sufficient
deterministic six-row evidence for a family-specific lifecycle-promotion
proposal? Stop after reviewing the existing release evidence: do not produce,
substitute, tune, or inspect additional rows, and do not make a generic
axisymmetric-reconstruction claim.

## Inputs

- `docs/corpus/sequence-paired/revolve-v1-preregistration.json`
- `docs/architecture/adr/0063-revolve-v1-design-freeze.md`
- `docs/workpacks/done/WP-M105-001-revolve-family-design-freeze.md`
- `docs/workpacks/done/WP-M106-001-revolve-family-controlled-production.md`
- `tools/audit_sequence_paired_revolve.py`

## Decision-package impact

- `decision_id`: none; this is a family-scoped offline evidence disposition.
- Q01/Q02 effect: reviews only the frozen planar stepped-radial profile,
  declared axis and constrained 360-degree revolve action.
- Q03/Q04 effect: reviews only existing no-input, geometry, semantic and
  editability evidence; shared gate policy remains unchanged.
- Evidence role: determines whether the existing experimental release supports
  one narrowly scoped future lifecycle-promotion proposal.
- Knowledge disposition: no runtime knowledge or experience card may result.

## Compatibility constraints

Offline and credential-free. Do not alter the preregistration, candidate
assets, registry, catalog, manifest, packs, cards, provider payloads, runtime,
training, Harness, report schema or hosted budget. A positive disposition is
not a promotion and cannot make candidates provider or runtime inputs.

## Acceptance

```powershell
uv run python tools\audit_sequence_paired_revolve.py
uv run python tools\audit_case_library.py
uv run python -m pytest tests\test_sequence_paired_revolve.py -q
uv run python -m pytest -m fast -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Collaboration plan

Codex is the sole owner of lifecycle records and this review artifact. Liaol,
as independent reviewer, verifies scope, audit output, evidence boundaries and
status/handoff alignment after owner acceptance. No contributor changes the
exclusive lifecycle paths.

## Evidence reuse / guidance-card disposition

Choose exactly one disposition after the acceptance evidence is recorded. No
disposition authorizes runtime retrieval, an experience card, provider use or
hosted work.

## Owner acceptance

- 2026-08-11: `tools/audit_sequence_paired_revolve.py` revalidated all six
  frozen rows: centred-only development/offset-only held-out split, exact
  two-operation sequence, clean-directory normalized STEP stability, required
  Q01 facts, geometry, semantic/editability checks and declared controls.
- `tests/test_sequence_paired_revolve.py` passed (1 passed); the fast suite
  passed (66 passed, 165 deselected); Ruff and governance passed; `git diff
  --check` passed.
- M106's terminal evidence already records a successful complete active-case
  replay. Three M107 attempts to repeat that *unrelated* global replay stopped
  in an existing active case when OCCT reported it could not create
  `output/model.step`; M107 neither reads nor writes active cases. The failure
  is retained as non-attributable environment/library evidence and is not used
  to support the disposition.

## Result

The frozen release supports exactly one narrow, future lifecycle-promotion
proposal: admit only the six listed `revolve-v1` rows as a family-scoped
self-authored mechanism unit after a separately selected promotion package.
It supports no claim about arbitrary profiles, multiple or non-vertical axes,
partial/helical revolutions, sweep/loft, signed direction recovery, generic
axis/profile recognition, B-Rep-to-sequence reconstruction, runtime retrieval,
cards, provider use or hosted capability.

## Independent review required

Liaol must independently verify the six fixed rows and 3/3 family-isolated
split; the clean-directory hash, sequence, Q01/Q02, semantic/editability and
negative-control evidence; the terminal command results; the recorded
non-attributable global-replay observation; and the absence of any promotion,
manifest, runtime, provider or hosted change. Approval closes this workpack;
it does not perform the later promotion.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-11.
- Review scope: confirmed the fixed six-row 3/3 split, clean-directory hash,
  exact sequence, Q01/Q02, semantic/editability and negative-control evidence;
  verified the recorded global-replay observation is not attributed to the
  experimental family; and confirmed no case lifecycle, manifest, runtime,
  provider or hosted scope changed.
- Closure rationale: M107 closes only the offline evidence disposition. A
  future lifecycle promotion must be separately selected and remains confined
  to the six frozen rows.

## Status transition

After owner acceptance, Liaol independently verifies the frozen release and
the review record. Only an approved, narrowly scoped proposal may be selected
later as a new promotion workpack. The reviewer does not perform the promotion.

## Out of scope

Case lifecycle promotion, executable manifest changes, reference pack/card or
runtime changes, provider use, hosted work, additional sampling, shell/rib
scope, sweep/loft scope, generic revolve/axisymmetric claims, or any
unfreezing of the six rows.
