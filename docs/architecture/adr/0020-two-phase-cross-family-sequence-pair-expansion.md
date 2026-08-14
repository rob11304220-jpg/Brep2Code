# ADR-0020: Require Two Phases for Cross-Family Sequence-Pair Expansion

- **Status**: Accepted
- **Date**: 2026-08-04

## Context

ADR-0019 promotes only the verified `prismatic-hole-v1` family.  Its nine
self-authored deterministic-oracle records prove maintenance of that narrow
grammar; they do not establish that the next family, its producer, or its
evidence contract can be selected without bias.

The Zero-to-CAD study separates catalog design, candidate production, and
validation.  Its million-scale agentic mining is outside this project's scope,
but the separation prevents the producer from silently choosing what counts as
evidence.

## Decision

Every proposed family after `prismatic-hole-v1` uses two distinct workpacks:

1. a **design and preregistration** workpack, which freezes a capability
   matrix, grammar boundary, exact cases/splits, oracle provenance, semantic
   anti-degeneration predicates, editability mutations, rejection taxonomy,
   and producer-stability checks; and
2. a **controlled production and validation** workpack, which executes only
   that frozen plan and reviews the resulting evidence.

The design workpack may create a tracked preregistration record but may not
create case assets, alter manifests, or claim a candidate has passed.  The
production workpack may create candidate assets, but no successful candidate
is automatically admitted to a manifest, provider, training, or runtime path.
Any later governance promotion remains a separately reviewed ADR/workpack.

## Consequences

- Cross-family success and failure remain attributable to the grammar,
  producer, and audit rather than to post-hoc sample selection.
- Rejected candidates become retained offline evidence with stable reason
  classes, rather than invisible omissions.
- This adds one planning/review step before each family, but avoids treating
  parameter-count growth as evidence of a general sequence representation.
