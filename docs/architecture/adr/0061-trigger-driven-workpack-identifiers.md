# ADR-0061: Use Trigger Identifiers for Deferred Workpacks

- **Status**: Accepted
- **Date**: 2026-08-11

## Context

The remaining unstarted packages carried historical M numbers. That made a
deferred possibility look like an approved execution sequence and encouraged
reading old milestone order as current authorization.

## Decision

Completed workpacks keep their M identifiers as immutable historical evidence.
Future work that awaits a factual, review, or authorization trigger is stored
under `docs/workpacks/deferred/` with a stable `WP-TRG-*` identifier. It
becomes executable only after its trigger is independently recorded, a user
selects a fresh bounded scope, and a new active workpack receives the next M
number. A superseded hosted rerun plan is archived as evidence rather than
kept as a runnable deferred package.

## Consequences

- A trigger ID is navigation only; it does not reserve a milestone, owner,
  budget, report path, provider authorization, or runtime change.
- Historical reports and completed workpacks continue to use their original M
  labels and are not rewritten.
- Current roadmaps describe pending work by semantic trigger and dependency,
  rather than by a preallocated milestone sequence.
