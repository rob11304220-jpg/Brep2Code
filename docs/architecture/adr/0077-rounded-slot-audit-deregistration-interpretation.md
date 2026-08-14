# ADR-0077: Rounded-Slot Audit Deregistration Interpretation

- **Status**: Accepted
- **Date**: 2026-08-13

## Context

The M21 expansion contains three active development rounded-slot rows and three
offset-rounded-slot experimental candidates. M159 deregistered the latter in
accordance with their authoritative case metadata, but the historical M21 audit
treated all six expansion entries as active registry rows.

## Decision

Interpret M21 expansion entries with `case_record` as active registry evidence.
Interpret entries with `candidate_directory` as retained experimental history:
they must not appear in the active registry and are not read by the active
metadata audit.

## Consequences

The audit remains fail closed for active rounded-slot membership and sequence
drift, while no longer conflicts with M159's three-row deregistration. This
changes no case, registry, fixture, script, manifest, runtime, provider, or
hosted behavior.
