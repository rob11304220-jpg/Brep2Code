# ADR-0080: Route Decision Map Above Workpack Selection

- **Status**: Accepted
- **Date**: 2026-08-13

## Context

The project has strong execution controls: status selects work, workpacks bound
changes, and case/provider records bound assets and egress.  It also has a
theory map for evaluating one bounded hypothesis.  These do not yet provide a
single entry for comparing route-level decisions across interaction/repair
policy, case denominators and experience representations.  Consequently,
historical deferred workpacks can be mistaken for a standing route queue.

## Decision

Add a route decision map as navigation above workpack selection.  It frames
the three supporting dimensions as independent decisions, requires a stated
uncertainty, competing disposition, discriminating evidence, counterexample,
stop rule and adoption boundary before a workpack is proposed, and separates
route disposition from a workpack's `deferred` lifecycle state.

## Consequences

The map helps decide why a case, repair-budget or knowledge-representation
route should exist before defining how to execute it.  It grants no authority
and does not audit, alter, reactivate or retire any existing workpack; applying
its disposition vocabulary to the historical inventory requires a separately
selected governance review.
