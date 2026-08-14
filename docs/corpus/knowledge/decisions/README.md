# Q01--Q04 Decision Packages

This directory is the development-side index of bounded Harness decisions. A
decision package joins the two kinds of knowledge needed by the same loop:

1. operation and sequence knowledge: observable B-Rep facts, a constrained
   hypothesis, and its permitted action; and
2. model-class and LLM-reference knowledge: the reasoning difficulty, evidence
   role, reference maturity, and adoption boundary.

It is not a second case registry, an executable manifest, or runtime material.
`case.json`, registries, manifests, operation units, and execution contracts
remain authoritative for their own concerns. A package only links them to one
auditable Q01--Q04 decision and declares the smallest missing evidence.

## Lifecycle

- `planned`: a documented decision gap; it authorizes no case production or
  implementation change.
- `reviewed`: existing evidence supports its stated, bounded decision.
- `deferred`: useful gap, but blocked by a stated evidence or authorization
  gate.
- `rejected`: evidence or counterexamples rule out the stated hypothesis.

Before a workpack changes a package, it must state the package ID, evidence
role, counterexample, stopping rule, and adoption disposition. A workpack that
finds no reusable result records that outcome here rather than leaving it only
in an archived report.

## Initial packages

- [`q01-selector-ambiguity-v1`](q01-selector-ambiguity-v1/decision.json) —
  distinguishes a uniquely resolvable downstream face selector from ambiguity.
- [`q03-local-geometry-feedback-v1`](q03-local-geometry-feedback-v1/decision.json)
  — tests whether local discrepancy information is useful before a repair rule
  is proposed.

See [the template](decision-package.template.json), [knowledge-base
architecture](../../../architecture/v1/knowledge-base-architecture.md), and the
[maintenance runbook](../../../runbooks/modeling-knowledge-maintenance.md).
