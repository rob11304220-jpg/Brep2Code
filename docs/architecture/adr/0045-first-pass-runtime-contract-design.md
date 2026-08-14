# ADR-0045: Preregister a First-Pass Runtime-Contract Decision

- **Status**: Accepted
- **Date**: 2026-08-08

## Context

The bounded hosted first-pass evidence mixes provider lifecycle outcomes,
scripts that fail before output, and only one direct geometry pass.  M10-012
reproduced two direct sandbox host-path failures with fixed scripts and showed
that `/input/model.step` restores execution, while an unavailable OCP import is
a non-matching failure.  This does not establish that an LLM will model better.

## Decision

Create a G1 design-only decision package for a future, separately selected G3
development-first comparison.  The possible contract is limited to existing
runtime facts: sandbox input reference, output location, installed OCP import
compatibility, and execution expectations.  Existing gates and their report
schema remain authoritative.  Development must be reviewed before any held-out
request, and each hosted split requires a fresh preflight and explicit user
authorization.

## Consequences

The project can measure execution-readiness separately from modeling outcomes
without widening the CAD operation surface.  This ADR authorizes neither a
provider request nor a prompt/runtime implementation, helper, case change, or
benchmark claim.
