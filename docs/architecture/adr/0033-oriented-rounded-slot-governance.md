# ADR-0033: Govern Only Validated Oriented Rounded-Slot Sequence Pairs

- **Status**: Accepted
- **Date**: 2026-08-05

## Context

M27 preregistered, deterministically produced, audited, and independently
reviewed exactly six `oriented-rounded-slot-v1` records: three +X development
and three +Y held-out cases. Each is a rectangular XY base followed by one
through rounded-slot cut with an explicit axis-aligned local frame. All six
passed hash stability, geometry, exact sequence, editability, semantic, and
split controls.

## Decision

Promote only the six records named by `oriented-rounded-slot-v1-m27-001` to
active self-authored governance cases. They retain their frozen two-frame
sequence contract, deterministic reference scripts, case metadata, case cards,
and registry pointers. The library audit validates this grammar only against
these six records; executable manifests remain unchanged.

## Consequences

The claim remains limited to XY +X/+Y axis-aligned rounded slots and a through
cut on one rectangular base. It does not establish arbitrary angles, splines,
generic frame recognition, B-Rep-to-sequence recovery, provider input,
training input, or runtime behavior.
