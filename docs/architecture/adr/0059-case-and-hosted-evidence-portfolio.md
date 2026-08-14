# ADR-0059: Add Read-Only Case and Hosted Evidence Portfolios

- **Status**: Accepted
- **Date**: 2026-08-11

## Context

Case identity, lifecycle and baselines already have authoritative records;
reference packs, runtime cards, knowledge units and hosted reports have
separate, intentionally bounded authorities. This prevents accidental runtime
or provider adoption, but makes it costly to answer two cross-cutting
questions: which cases have which kind of development support, and what a
hosted result actually established.

## Decision

Add two read-only Markdown navigation projections:

1. `docs/corpus/case-portfolio.md` groups active and experimental cases by
   their case-card, reference-script, reference-pack, runtime-card and
   evidence status.
2. `docs/workflow/hosted-experiment-registry.md` records bounded experiment
   scope, terminal disposition, report path and interpretation boundary.

Neither page is a registry, executable manifest, report schema, evidence
ledger, runtime resource or authorization record. They link to their existing
authorities and label ignored local evidence paths explicitly. A maintenance
runbook defines when to refresh the projections.

## Consequences

- Low-context review can distinguish a deterministic reference script from a
  runtime-visible card and a hosted pass from a broader capability claim.
- Historical reports remain immutable and non-comparable unless their frozen
  policy says otherwise; the registry does not compute a global success rate.
- Maintaining the projections is an additional documentation duty after a
  case, pack/card, workpack or hosted terminal-review change; it cannot
  authorize any such change.
