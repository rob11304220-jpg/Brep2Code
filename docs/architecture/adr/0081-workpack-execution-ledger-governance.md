# ADR-0081: Workpacks Are Execution Ledgers, Not Durable Route Authorities

- **Status**: Accepted
- **Date**: 2026-08-13

## Context

Completed and deferred workpacks are currently cited widely in project
navigation.  That preserves provenance but makes one-off execution records
serve as long-lived route, decision and evidence summaries.  It also obscures
the distinction between a deferred trigger's lifecycle and whether its route
is still relevant.

## Decision

Treat workpacks as bounded execution ledgers.  Promote durable conclusions at
closure to ADRs, routes, contracts or evidence authorities; retain the
workpack for provenance.  Maintain route disposition separately from workpack
lifecycle, and move consumed triggers to archive once their durable successor
has closed.  Start the inventory incrementally with the current closed-loop
cluster; do not make an unreviewed bulk disposition of historical routes.

## Consequences

New navigation should lead with durable authorities and use workpack links for
execution detail.  Existing historical citations are not mechanically removed
by this ADR.  A future selected inventory review must migrate or replace them
by route cluster, preserving source traceability and never treating archive as
deletion.
