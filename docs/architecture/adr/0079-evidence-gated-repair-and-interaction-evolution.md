# ADR-0079: Evidence-Gated Repair and Interaction Evolution

- **Status**: Accepted
- **Date**: 2026-08-13

## Context

M139 freezes campaign intent, M140 implements a bounded tool-to-script turn,
and M141 admits one fake-provider source-only repair for three source-level
classes. The initial three-case release deliberately caps one Q01 call, one
card call, one initial script and one repair edit per case. This produces an
interpretable baseline but is not a permanent assertion that all CAD repair
needs exactly one edit or exactly two tool interactions.

## Decision

Treat repair counts and interaction limits as campaign policy parameters backed
by terminal evidence, not universal Harness constants. TRG-039/040 establish
the baseline. Only after their independently reviewed report may TRG-041 decide
whether to retain it, test a second source-only attempt for `execution_local`
after a changed failure signature, or specify one missing prerequisite for a
currently prohibited class. A changed policy always requires a fresh frozen
campaign and G3 authorization; it never changes a completed campaign in place.

ReAct informs the alternation of bounded information-seeking actions and
environment feedback; Toolformer informs typed, validated and traceable API
calls; RAG informs versioned provenance, hash binding and no-reference versus
reference ablation. None authorizes free-form tool access, model training,
automatic retrieval, generic CAD repair or a claim of CAD effectiveness.

## Consequences

The project can learn whether more interaction or repair is useful without
confounding it with case expansion, card mutation or prompt changes. Geometry,
selector and editability failures remain stop categories until separately
admitted locators/oracles exist; transport and sandbox failures remain
infrastructure evidence rather than CAD repair targets.
