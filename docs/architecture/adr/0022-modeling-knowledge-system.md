# ADR-0022: Establish an Evidence-Bounded B-Rep Modeling Knowledge System

- **Status**: Accepted
- **Date**: 2026-08-04

## Context

The case library governs fixture identity, lifecycle, replay, and admission.
Workpacks explain a bounded change, while ADRs record its decision. These
records do not yet form a common account of which B-Rep observations support a
modeling interpretation, which kernel-operation properties have been
demonstrated, which cases or counterexamples support a claim, and which
knowledge may safely inform a future LLM.

Existing runtime experience cards are intentionally small and operational.
They cannot become a comprehensive modeling reference by copying workpacks,
traces, or unreviewed case-local observations into the runtime bundle.

## Decision

Add a development-side modeling knowledge system with three explicitly
separated layers:

1. a coverage matrix records target capability dimensions, current evidence,
   known gaps, unlock conditions, and the workpack that may address a gap;
2. versioned modeling knowledge units connect a bounded kernel operation or
   sequence pattern to B-Rep observables, prerequisites, parameters,
   dependencies, evidence, counterexamples, safe repair actions, and review
   triggers; and
3. experimental runtime experience cards remain concise, derived projections
   of reviewed knowledge units, never a direct view of the knowledge store.

The matrix and unit templates live under `docs/corpus/knowledge/`; the system
design lives under `docs/architecture/v1/`; maintenance is governed by a
runbook. `case.json`, registries, executable manifests, ignored traces, and
runtime-resource indexes keep their existing authorities.

M22-000 establishes this layer before M22-001 designs the multi-contour pocket
family. Every future case-family design must identify its target matrix cells;
every production/review workpack must update the resulting evidence or record
why no reusable knowledge unit was produced.

## Consequences

- Case acquisition becomes hypothesis-driven: an asset is selected to test a
  named operation/property/repair question, rather than merely increasing
  corpus count.
- A case-local replay result is not a general kernel rule. Evidence level,
  counterexamples, and applicability boundaries are required before any
  runtime projection.
- This decision changes no Harness behavior, runtime prompt, retrieval,
  provider policy, training input, parser, helper, SDK, gate, or manifest.
  M19's existing evidence threshold still controls any future retrieval
  experiment.
