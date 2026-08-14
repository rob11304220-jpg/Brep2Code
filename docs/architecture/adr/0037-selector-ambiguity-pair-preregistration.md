# ADR-0037: Preregister a Fail-Closed Selector-Ambiguity Pair

- **Status**: Accepted
- **Date**: 2026-08-07

## Context

The existing `face-selected-dependent-cut-v1` family demonstrates a unique
maximum-Z boss-top selector but explicitly excludes multiple eligible faces.
Q01 requires a discriminating counterexample: the same live predicate must
stop as ambiguous rather than bind an arbitrary face or fall back to a
coordinate-only rule.

## Decision

Freeze a design-only `selector-ambiguity-v1` preregistration. It reuses the
existing unique-selector family as an oracle and proposes two self-authored
twin-boss rows where two planar +Z faces share the maximum output Z. The
predicate is intentionally unchanged; its expected cardinality changes from
one to two. A wrong-face injection is a required negative control, not a
candidate asset. A separately selected production workpack is required before
any asset, producer, registry, or manifest change.

## Consequences

- The work isolates selector cardinality as its only intended decision change.
- Ambiguity is an expected fail-closed result, not a geometry-gate failure to
  repair.
- The design does not establish persistent naming, generic face selection, or
  a runtime selector/helper.
