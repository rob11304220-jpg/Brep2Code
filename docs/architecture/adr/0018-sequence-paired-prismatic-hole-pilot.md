# ADR-0018: Start with a Sequence-Paired Prismatic-Hole Pilot

- **Status**: Accepted
- **Date**: 2026-08-04

## Context

The Harness, self-authored case library, and restricted Fusion replay have
established executable CAD and geometry-gate evidence.  They do not establish
that a generated script recovers an editable construction sequence: ABC inputs
have no source history, while the current Fusion work is intentionally a narrow
offline replay subset.  Incrementing B-Rep-only external samples therefore has
limited information gain for Q02 sequence recovery.

## Decision

Start the next implementation route with a local-only, sequence-paired pilot
for one restricted family: a single planar sketch/base extrusion followed by
one cylindrical subtractive feature (through, blind, or counterbore hole).

The pilot creates a versioned canonical sequence representation and a small,
family-disjoint paired benchmark.  Its evidence is evaluated in three layers:

1. executable STEP and existing geometry gates;
2. operation, parameter, and dependency agreement with a declared sequence
   oracle; and
3. preregistered parameter-editability checks.

These rules apply only to the pilot until its completed review explicitly
promotes them to case-library governance.  The representation is not a runtime
IR, an LLM prompt resource, or a project CAD SDK.

## Rationale

- The family has meaningful feature dependencies but remains representable by
  direct OCP operations already used in committed self-authored cases.
- A paired oracle makes sequence claims testable rather than inferring a unique
  history from a final B-Rep.
- A bounded pilot can reject a poor schema or audit design before it creates an
  automatic case-generation path or a permanent repository-wide requirement.

## Consequences

- **Positive**: Subsequent case growth can be driven by source-linked sequence
  evidence and editability, not only final-shape similarity.
- **Positive**: The existing Harness and geometry gates remain stable and keep
  their value as the first evidence layer.
- **Negative**: The first workpack deliberately covers only a narrow family and
  cannot make a general B-Rep-to-history claim.
- **Mitigation**: The roadmap requires family-isolated held-out evidence and a
  review before any production-process or runtime promotion.

## Alternatives Considered

| Alternative | Reason not selected |
|---|---|
| Continue generic ABC increments as the main route | ABC is useful OOD B-Rep material but has no sequence oracle. |
| Start a full modeling IR or CAD SDK | The pilot has not yet shown a repeated cross-family dependency representation need. |
| Expand all Fusion feature types immediately | Existing Fusion evidence is restricted and explicitly fail-closed. |
