# B-Rep Modeling Knowledge Index

This directory is the development-side decision base for the Harness loop. It
organizes what Q01 can observe, what Q02 may hypothesize, how Q03/Q04 execute,
gate and repair it, and the evidence that bounds every claim. It is not a
fixture authority, executable manifest, prompt bundle, or training dataset.
The primary architecture is
[`knowledge-base-architecture.md`](../../architecture/v1/knowledge-base-architecture.md).

## Contents

- `coverage-matrix.json` — current decision evidence, gaps, workpack links,
  and unlock conditions; it is the planning index, not a case-count dashboard.
- [`development-evidence-crosswalk-v1.md`](development-evidence-crosswalk-v1.md)
  — source-linked views from bounded modeling hypotheses to mechanism,
  difficulty, evidence maturity, admission risk, and decision gaps; derived
  navigation only, never a replacement authority.
- [`case-evidence-relationships-v1.md`](case-evidence-relationships-v1.md) —
  source-linked companion mapping from selected reviewed case/documentary
  evidence sets to M146 hypotheses and evidence roles; not a case registry.
- [`implementation-contract-relationships-v1.md`](implementation-contract-relationships-v1.md) —
  source-linked companion mapping from selected reviewed hypotheses to their
  current Q01--Q04 implementation-contract representation; not runtime
  authority.
- [`implementation-contract-coverage-v1.md`](implementation-contract-coverage-v1.md) —
  source-linked coverage view showing which reviewed hypotheses already have a
  published implementation-contract mapping and which remain `missing_link`,
  `contract_only`, or `unsupported`; not runtime authority.
- `evidence-disposition.json` — the migration index for legacy cases, reviews,
  and experience cards. It records whether each is a knowledge unit, a
  boundary/counterexample, or a retained asset with no reusable claim.
- `templates/modeling-knowledge-unit.template.json` — required shape for an
  operation, B-Rep pattern, sequence, or repair knowledge unit.
- [`observables/`](observables/README.md) — Q01 measurement vocabulary and
  ambiguity boundaries; do not infer feature history from B-Rep facts.
- `operations/` — reviewed, family-bounded operation units.
- [`execution/`](execution/README.md) — Q03/Q04 gates, diagnostics and repair
  knowledge; it is not an API catalogue.
- [`admissions/`](admissions/README.md) — immutable, source-hash-bound
  development-side admission evidence; never runtime knowledge or case
  lifecycle authority.
- [`runtime-projections/selector-cardinality-stop-v1.json`](runtime-projections/selector-cardinality-stop-v1.json)
  — the M157 experimental, hash-bound comparison from selector-ambiguity
  admission evidence to one explicitly selected counterexample card; it does
  not authorize runtime adoption, retrieval, provider use, or held-out access.
- `patterns/` — reviewed cross-layer boundary and counterexample units. Units
  are organized by their decision question rather than by fixture path.

The reviewed units are deliberately narrow: `prismatic-hole-v1`,
`rounded-slot-v1`, `multi-contour-pocket-v1`,
`additive-boss-dependent-cut-v1`, `face-selected-dependent-cut-v1`,
`multi-inner-loop-pocket-v1`, and `oriented-rounded-slot-v1` describe only
their frozen, self-authored deterministic sequence families.
`external-history-boundary` records why the current Fusion and ABC records
cannot be elevated to a general reconstruction claim. These units do not create
an experience card or authorize runtime use; the adoption gates are defined in
[`modeling-knowledge-adoption.md`](../../architecture/v1/modeling-knowledge-adoption.md).

## Authority and lifecycle

`case.json` remains authoritative for case identity and baselines; the case
registry remains authoritative for lifecycle; manifests remain executable
selections. A knowledge unit links to those records but cannot promote an
asset, modify a manifest, or authorize provider/runtime use.

Use `case_local`, `supported`, or `direct` for evidence strength. Retain a
counterexample or explicit absence-of-knowledge result whenever a proposed
rule fails to generalize. See the maintenance runbook before adding a unit.

Where evidence supports an operation claim, its `operation_contract` captures
the bounded function family, parameter boundary, expected B-Rep delta, and
topology invariants, while naming anything not yet established. It is not a
generic CAD-kernel API catalogue.

The current layer migration is intentionally uneven: reviewed Q02 operation
units, one Q01 selector-cardinality observable, and one Q03/Q04 execution
boundary exist. A directory or a planned decision package is not evidence that
the corresponding capability is implemented.
