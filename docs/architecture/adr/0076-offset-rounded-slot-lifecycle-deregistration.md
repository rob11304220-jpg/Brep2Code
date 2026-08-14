# ADR-0076: Offset Rounded-Slot Lifecycle Deregistration

- **Status**: Accepted
- **Date**: 2026-08-13

## Context

M144 promoted three offset-rounded-slot rows to active registry status. Their
authoritative `case.json` records are now explicitly downgraded to
`experimental`, declare no reference script, and state that they are absent
from the registry. This made the metadata-only admission-profile audit fail.

## Decision

Treat the per-case `case.json` lifecycle metadata as authoritative and remove
only the three matching rows from the active self-authored registry. Replace
the current-state M144 audit assertion with an M159 audit that verifies
deregistration and the existing experimental metadata without reading fixtures
or scripts.

## Consequences

The active registry drops from 87 to 84 rows. The three assets remain on disk
as experimental candidates, absent from registry, manifests, runtime, provider,
training, and hosted paths. M144's active-promotion conclusion is superseded
for these rows only; no case data or runtime authority changes.
