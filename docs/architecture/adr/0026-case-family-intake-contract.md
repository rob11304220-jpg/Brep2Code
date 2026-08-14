# ADR-0026: Standardize Offline Case-Family Intake Before Candidate Production

- **Status**: Accepted
- **Date**: 2026-08-05

## Context

M20--M23 independently converged on the same safeguards: coverage-led family
selection, preregistered rows and family-isolated splits, deterministic
candidate production, three-layer validation, semantic anti-degeneration, and
an explicit separation between experimental candidates and library promotion.
The evidence is reliable, but its common contract was previously distributed
across family-specific records and audit scripts.

## Decision

Add a reusable sequence-paired family intake template, an offline generic
intake auditor, and a runbook. Before candidate production, every new
self-authored sequence-paired family must freeze its grammar, producer
boundary, exact rows/splits, preconditions, semantic invariants, directional
mutations, production checks, and rejection taxonomy in a record satisfying
that contract.

The generic auditor validates only the shared governance invariants. A
family-specific auditor remains mandatory after production for exact sequence,
geometry replay, editability, and domain semantics. Passing either audit does
not promote a candidate or authorize manifests, providers, training, or
runtime use.

## Consequences

- Agents can detect incomplete preregistration and split leakage before assets
  exist, rather than after a producer has biased the sample choice.
- Future family audits retain specialized geometry semantics without forcing a
  premature general IR or universal CAD representation.
- Existing frozen family records remain valid; new optional fields are added
  only when their own selected workpack performs the compatible migration.
