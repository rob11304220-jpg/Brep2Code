---
type: architecture
related-project: Brep2Code
status: active
tags:
  - B-Rep
  - modeling-knowledge
  - case-library
  - runtime-guidance
---

# Evidence-Bounded B-Rep Modeling Knowledge System

> 本页保留既有知识单元的详细维护约束。知识库的主定位、四层组织和案例角色见
> [面向 Harness 闭环的知识库架构](knowledge-base-architecture.md)（ADR-0035）。

## Purpose

Organize project evidence into an auditable reference for answering: given
observable B-Rep properties, which bounded construction hypotheses and kernel
operations are supported; how are their prerequisites, parameters, dependency
order, execution checks, and failure modes checked. A compact LLM guidance card
is only one possible later projection. This is a development knowledge system,
not a model-training corpus or a runtime document mount.

## Information flow and authority

```text
case assets / replay / audits / reviewed failures
  -> coverage matrix + modeling knowledge units
  -> reviewed, bounded development knowledge
  -> separately evaluated runtime projection (if selected)
```

| Layer | Authority | May contain | Must not contain |
|---|---|---|---|
| Case asset | `case.json`, registry, baseline, manifest | identity, hash, source, replay facts | general modeling claim |
| Knowledge system | `docs/corpus/knowledge/` | claim, scope, evidence, counterexample, gap | secrets, ignored trace content, runtime authorization |
| Runtime card | `runtime_resources/experience-cards/` | concise reviewed safe action | full governance history or unrestricted repository context |

## Required knowledge-unit dimensions

Every unit is bounded to one operation, operation family, B-Rep pattern, or
repair mechanism. It records:

1. **Kernel operation** — function/operation family, parameters, target/body,
   prerequisites, and unsupported conditions. Where tracked evidence supports
   it, an `operation_contract` also records parameter boundaries, expected
   B-Rep delta, topology invariants, numeric/tolerance boundary, and explicitly
   unverified properties; it is not an inferred kernel/API signature.
2. **B-Rep observables** — relevant solids, faces, edges, loops, curve/surface
   types, placement/orientation, topology, and measurable geometry clues.
3. **Sequence and dependency** — canonical sequence, required prefix,
   entity/coordinate dependencies, admissible alternatives, and order risks.
4. **Evidence** — source/oracle type, cases, development/held-out separation,
   replay/gate/editability results, and evidence level.
5. **Failure and repair** — observable failure signature, bounded diagnostic,
   safe repair action, stop condition, and counterexamples.
6. **Runtime projection** — whether a compact card is eligible, its review
   trigger, and the card ID if one is approved.

Evidence levels are `case_local`, `supported`, and `direct`. A level describes
the strength of this project evidence; it does not claim uniqueness of an
inverse construction sequence or generic CAD-history recovery.

## Coverage dimensions

The matrix is a planning authority for decision gaps, not an inventory or a
coverage target. Its dimensions include:

- sketch topology;
- feature semantics;
- sequence/dependency;
- parameter robustness;
- complex topology; and
- external native-history or B-Rep-only validation.

Each cell names current evidence, explicit gaps, an optional current trigger
reference, and an unlock condition. Historical workpacks remain evidence links,
not future-task selectors. A new workpack may address a cell only after its design
states the hypothesis, evidence sought, counterexamples, and stopping rule.

## Operating rules

- A future case family must cite its target matrix cells before candidate
  production. Its design does not change a knowledge-unit evidence level.
- Production and review update the matrix and either add/revise a knowledge
  unit, register a counterexample, or explicitly record no reusable knowledge.
- Runtime cards are projections, not the source of truth. ADR-0016 and M19
  continue to require independent direct evidence and an offline retrieval
  evaluation before retrieval is considered.
- The current matrix is deliberately incomplete. `uncovered` is a useful and
  auditable state, not a reason to infer a rule or schedule an operation.

## Related records

- [ADR-0014](../adr/0014-case-library-maintainability-contract.md)
- [ADR-0016](../adr/0016-evidence-bounded-runtime-guidance-cards.md)
- [ADR-0020](../adr/0020-two-phase-cross-family-sequence-pair-expansion.md)
- [ADR-0021](../adr/0021-evidence-sequenced-case-coverage-expansion.md)
- [ADR-0022](../adr/0022-modeling-knowledge-system.md)
- [Knowledge index](../../corpus/knowledge/README.md)
- [Knowledge maintenance runbook](../../runbooks/modeling-knowledge-maintenance.md)
