# WP-M22-000: B-Rep Modeling Knowledge System Foundation

- Status: done
- Milestone: M22
- Owner: Codex

## Status transition

Selected by the user on 2026-08-05 after M21-004. This selects only the
documentation and evidence-organization foundation. It does not select
M22-001 or authorize candidate production.

## Goal

Establish the development-side knowledge layer that links case assets and
reviewed evidence to bounded modeling-operation guidance, before a new family
is designed or produced.

## Scope

- Finalize the knowledge-unit contract, coverage matrix, authority boundaries,
  and maintenance procedure defined by ADR-0022.
- Backfill the current capability-ladder, prismatic-hole, rounded-slot, Fusion,
  and ABC evidence only to the level supported by existing tracked records.
- Record explicit gaps and counterexamples; do not infer generic kernel rules
  from case-local results.
- Make M22-001 cite the resulting matrix cells and hypothesis.

## Acceptance

- Every coverage dimension has a current-evidence statement, known gap, and
  explicit unlock condition.
- Knowledge units distinguish operation facts, B-Rep observables, sequence/
  dependency claims, evidence level, and runtime projection boundary.
- Existing runtime experience cards remain unchanged unless independently
  justified under ADR-0016.
- Documentation checks and `git diff --check` pass.

## Out of scope

New candidate assets, case promotion, executable manifests, runtime retrieval,
prompt injection, provider/hosted use, training, parser/helper/SDK changes, or
IR.

## Result

Completed offline on 2026-08-05. The coverage matrix now gives all six
dimensions a source-linked evidence statement, explicit gap, and unlock
condition. Three reviewed, bounded knowledge units backfill the two
self-authored deterministic sequence families and the Fusion/ABC external
evidence boundary. The knowledge-unit template now identifies the unit kind
and distinguishes audit evidence from authority records. Existing runtime
experience cards were not changed. JSON structure/reference validation and
`git diff --check` passed; no assets, manifests, provider route, or runtime
behavior changed.
