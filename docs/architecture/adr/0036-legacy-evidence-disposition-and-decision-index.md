# ADR-0036: Reconcile Legacy Evidence into the Harness Decision Base

- **Status**: Accepted
- **Date**: 2026-08-06

## Context

ADR-0035 reorganizes development knowledge around Q01--Q04 decisions, while
earlier case, attribution, and runtime-guidance records remain distributed
across catalogs, reviews, and experience cards. Preserving those records alone
does not say whether each is reusable knowledge, a bounded counterexample, or
an asset awaiting a decision-specific audit.

## Decision

Maintain `docs/corpus/knowledge/evidence-disposition.json` as a migration
index. Every legacy evidence family is assigned one disposition: a reviewed
knowledge unit, a boundary/counterexample, or a retained evidence asset with
no reusable knowledge claim. Decision packages are the implementation-side
index for literature-supported Q01--Q04 hypotheses; a package cannot override
an existing workpack's trigger or authorize production/runtime changes.

## Consequences

- Case counts remain asset-lifecycle facts, not knowledge-coverage measures.
- Existing experience cards must link through the disposition index to their
  reviewed source unit or explicitly named migration exception.
- A new family, diagnostic, or repair route is selected only through one
  decision package with a compatible workpack trigger and stopping rule.
