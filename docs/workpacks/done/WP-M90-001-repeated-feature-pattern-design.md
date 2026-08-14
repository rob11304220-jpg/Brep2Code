# WP-M90-001: Repeated-Feature Pattern Design and Preregistration

- Status: done
- Milestone: M90
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Freeze one small self-authored repeated-feature family before candidate
production: four cylindrical through cuts arranged as a rectangular 2x2 grid
in a rectangular base.

## Scope

- Preregister six family-isolated candidate rows: three centred development
  rows and three offset held-out rows.
- Freeze the four-operation oracle, count, positions, mutations, invariants,
  negative controls, rejection taxonomy and hash-stability requirements.
- Register M90-002 production, M90-003 evidence review and M90-004 promotion
  as separate non-active successors.

## Attribution question and sampling intent

Does one declared four-instance rectangular-grid through-cut operation retain
an observable cardinality-and-placement dependency under frozen variants? Stop
after the intake audit; do not produce candidates or increase counts to seek a
stronger result.

## Inputs

- `docs/architecture/v1/case-family-expansion-priorities.md`
- `docs/corpus/knowledge/coverage-matrix.json`
- `docs/corpus/sequence-paired/family-intake-template.json`

## Code paths

- `docs/corpus/sequence-paired/repeated-feature-pattern-v1-preregistration.json`
- Future only: `tools/build_m90_repeated_feature_pattern_candidates.py` and a
  family audit, owned by M90-002.

## Docs to update

`docs/workflow/status.md`, the priority route, coverage matrix, ADR-0054, this
workpack, successor workpacks and the active handoff.

## Trace/schema changes

None. This is a development-side preregistration, not a report, trace, CLI,
storage or manifest change.

## Decision-package impact

- `decision_id`: none; new bounded feature-semantic planning only.
- Q01/Q02 effect: local declared cardinality and placement oracle; no generic
  B-Rep pattern inference.
- Q03/Q04 effect: no gate, repair or lifecycle policy change.
- Evidence role: planned oracle and discriminating negative controls.
- Knowledge disposition: no reusable experience card.

## Compatibility constraints

Offline and credential-free. Existing cases, manifests, Harness gates,
reference-card index, provider paths and hosted budgets remain unchanged.
M90-002--004 are not activated.

## Acceptance

```powershell
uv run python tools/audit_sequence_paired_intake.py docs/corpus/sequence-paired/repeated-feature-pattern-v1-preregistration.json
uv run python tools/check_governance.py
git diff --check
```

## Evidence reuse / guidance-card disposition

No runtime experience card: planning contract only.

## Owner acceptance

- 2026-08-10: `uv run python tools/audit_sequence_paired_intake.py
  docs/corpus/sequence-paired/repeated-feature-pattern-v1-preregistration.json`
  passed.
- 2026-08-10: `uv run python tools/check_governance.py` passed; `git diff
  --check` passed.
- The record freezes six rows, with `repeated_feature_pattern_centered` only
  in development and `repeated_feature_pattern_offset` only in held-out. No
  candidate directory, producer output, manifest, provider request, or runtime
  card was created.

## Review required

Liaol must independently verify the isolated four-instance grammar, six-row
split, no-substitution rule, negative taxonomy, absence of assets/manifest or
provider changes, and the recorded acceptance commands before closure.

## Independent review and closure

- Reviewer: Liaol
- Status: approved on 2026-08-10.
- Review scope: confirmed the bounded four-instance grammar, the three/three
  family-isolated split, no-substitution rule, negative taxonomy, successful
  intake/governance/diff checks, and the absence of assets, manifest, provider
  or runtime changes.
- Closure rationale: this workpack freezes only the M90 production contract;
  it creates no direct-case evidence and does not promote a guidance card.

## Status transition

After intake audit and independent G2 review, update `status.md` first, move
this workpack to `done`, and update/archive the handoff. M90-002 remains
backlog until separately selected.

## Out of scope

Assets, producer/audit code, registry/catalog/manifest changes, promotion,
provider or hosted requests, runtime cards, training, external data, polar or
variable-count patterns, revolve, sweep, loft, repair and generic recovery.
