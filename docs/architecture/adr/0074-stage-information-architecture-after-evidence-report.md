# ADR-0074: Stage Evidence Information Architecture After the Matrix Report

- **Status**: Accepted
- **Date**: 2026-08-12

## Context

M145 collects the current distributed evidence expressions into a read-only
matrix. Existing records have intentionally separate authorities: case metadata
for assets, knowledge units for mechanisms, coverage matrix for decision gaps,
and admissions for evidence maturity. Consolidating them immediately would risk
creating a second authority before the information requirements are explicit.

## Decision

Deliver the M145 report first. Register deferred `WP-TRG-030` as the only
route for a later development-evidence information architecture. It may be
activated only through a fresh user-selected, bounded G2 workpack after the
report is reviewed or explicitly accepted.

## Consequences

- The report offers one readable cross-section now without changing existing
  source-of-truth boundaries.
- A future architecture must define stable IDs, ownership, derived views and
  drift checks rather than duplicating metadata by hand.
- No case, manifest, runtime, provider, training, hosted or projection
  authority changes through this ADR or trigger.
