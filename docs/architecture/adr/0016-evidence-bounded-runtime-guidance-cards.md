# ADR-0016: Preserve Reusable Agent Evidence as Bounded Runtime Guidance Cards

- **Status**: Accepted
- **Date**: 2026-08-04

## Context

Development agents accumulate useful operational observations while extending
and diagnosing cases.  Raw workpacks, ADRs, and traces are too broad and have
different permissions from a runtime LLM.  Treating a case-local repair as a
general instruction would repeat the M17 over-generalization risk.

## Decision

- Store concise, versioned experience cards under
  `runtime_resources/experience-cards/`, with a checked-in index, contract,
  source links, evidence level, supporting cases, counterexamples, safe action,
  and review trigger.
- Cards begin as `experimental`; a card is not automatically mounted, injected,
  retrieved, or used to change runtime behavior.
- Every future case-extension or diagnosis workpack must explicitly conclude
  with zero or more cards, a counterexample, or a recorded absence of reusable
  evidence.  Held-out results validate cards but do not by themselves create a
  general rule.
- Promotion to a runtime retrieval experiment requires at least three
  independent direct cases for one mechanism, development-split offline
  evaluation, and a separately scoped workpack.  Hosted comparisons retain the
  existing preflight and authorization requirements.

## Consequences

- The project gains an auditable bridge from development evidence to future
  runtime material without exposing development governance documents.
- The initial implementation is static and offline only; it changes no
  Harness, CLI, prompt, provider, helper, parser, gate, manifest, or schema.
- The card audit verifies metadata and source links but does not convert
  evidence into a model-quality claim.
