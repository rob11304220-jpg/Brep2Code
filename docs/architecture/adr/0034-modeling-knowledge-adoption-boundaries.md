# ADR-0034: Keep Case-Derived Modeling Knowledge as a Development-Side Adoption Gate

- **Status**: Accepted
- **Date**: 2026-08-05

## Context

M25--M27 complete active self-authored case families with bounded design,
sequence, kernel-operation and semantic evidence. Their implementation history
is distributed across workpacks, preregistrations, reviews, and ADRs. The
existing modeling knowledge system is intended to preserve reusable claims, but
its matrix and units have not yet incorporated those families.

## Decision

Promote only concise, evidence-bounded projections into
`docs/corpus/knowledge/` and make `modeling-knowledge-adoption.md` the design
entry for later Harness adoption. Reviewed knowledge may guide development-side
case design and analysis. Any runtime card, helper, IR, DSL, SDK, manifest,
provider, training, or runtime behavior remains a separately selected and
validated decision with its existing authorization boundary.

## Consequences

- Archived workpacks remain evidence snapshots, not the sole long-term source
  for reusable design knowledge.
- Knowledge units retain explicit unsupported conditions and counterexamples;
  they do not turn deterministic reference sequences into generic inverse-CAD
  claims.
- This documentation decision changes no executable behavior or runtime scope.
