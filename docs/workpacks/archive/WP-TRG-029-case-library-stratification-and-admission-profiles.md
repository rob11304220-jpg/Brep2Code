# WP-TRG-029: Case-Library Stratification and Admission Profiles

- Status: deferred
- Trigger: M142 admission record is independently reviewed; the user selects a
  fresh bounded package.
- Risk tier on activation: G2
- Reviewer on activation: independent reviewer required

## Goal

Audit the existing development-side case library and its reviewed evidence to
define a versioned, evidence-bound `admission-profile-v1`.  The profile must
describe which evidence and fail-closed conditions apply to a case mechanism;
it must not itself admit a case or create a runtime projection.

## Scope on activation

- Build a deterministic inventory from the tracked case metadata, registry,
  coverage matrix, decision packages, preregistrations, and reviewed audit
  links. Reconcile any count or metadata disagreement at its authoritative
  source.
- Classify the existing assets across explicit axes: modeling intent/mechanism,
  entity-reference stability, sequence-dependency structure, parameter/split
  role, evidence maturity, and admission risk.
- Define observable profile criteria and minimum evidence for `admit`,
  `needs-evidence`, `fail-closed`, and `counterexample-only` dispositions.
  Difficulty is a derived, explainable profile, never a subjective rank.
- Map the independently reviewed M142 selector-ambiguity record to the profile
  and confirm that cardinality-one binding and cardinality-two ambiguity remain
  distinct dispositions.
- Recommend at most three next decision gaps or pilot mechanisms, with their
  missing evidence and stopping conditions. Recommendations do not select,
  create, inspect, or execute a successor case.

## Decision-package impact

- `decision_id`: no new Q01--Q04 decision package; this is a read-only
  crosswalk over existing reviewed decision packages.
- Q01/Q02 effect: none. Existing observable and sequence hypotheses remain
  unchanged.
- Q03/Q04 effect: none. Existing gates, repair dispositions, and terminal
  stopping rules remain unchanged.
- Evidence role: inventory and classify existing oracle, discriminating,
  negative-control, regression, OOD, and native-history evidence only.
- Knowledge disposition: `no reusable runtime knowledge`; the output is a
  development-side admission rubric.

## Compatibility constraints

- Remain offline and credential-free. Do not add or modify a case, fixture,
  manifest, reference script, provider configuration, Harness behavior, or
  runtime resource.
- Held-out material may be represented only by declared split metadata and
  already-reviewed, hash-pinned audit links. Do not newly inspect, replay, or
  execute it.
- A profile classification does not change case lifecycle, admission status,
  reference-pack status, runtime visibility, retrieval eligibility, or hosted
  authority.
- Parameter-family and split boundaries remain those declared by their
  authoritative records; no split may be inferred from a difficulty tier.

## Trace/schema changes

The work may add a versioned, development-side profile schema and derived
inventory/audit artifact. It must not change `signal_bundle.json`, provider or
tool traces, corpus manifest/report schemas, storage layout, or CLI JSON.

## Acceptance on activation

```powershell
uv run python -m pytest tests -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the source-linked inventory, `admission-profile-v1`, deterministic
audit, M142 mapping, and bounded recommendation list; run the declared offline
checks and obtain independent G2 review.

## Permitted stop conditions

Independent review; a reproducible conflict in an authoritative inventory or
frozen split record; an out-of-scope need for new production, held-out
inspection/execution, manifest or runtime change, hosted authority, or a
reproducible local validation blocker.

## Evidence reuse / guidance-card disposition

No reusable runtime evidence. The profile may guide a later user-selected
admission pilot, but it does not authorize a card, pack, SDK/IR fragment,
retrieval index, or runtime use.

## Status transition

On activation, assign a new milestone, owner, and independent reviewer, then
update `docs/workflow/status.md`, this workpack, and the active handoff. On
closure, retain the reviewed profile as development-side governance evidence;
leave `WP-TRG-028` deferred until the user selects it.

## Out of scope

New case production, open-ended corpus expansion, held-out inspection,
manifest expansion, replay of frozen candidates, runtime projection, cards,
packs, SDK/IR work, retrieval, provider calls, training, or hosted execution.
