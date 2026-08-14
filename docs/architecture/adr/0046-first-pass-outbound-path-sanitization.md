# ADR-0046: Remove Local Absolute Paths from First-Pass Provider Context

- **Status**: Accepted
- **Date**: 2026-08-08

## Context

M43's local, sanitized request traces showed that the existing bounded probe
summary included `input`, an absolute path within the local workspace.  The
provider did not receive raw STEP content, but the path was unnecessary for
B-Rep reconstruction and outside the intended minimal derivative.

## Decision

Before a first-pass provider request, project the probe summary to only
`file_name`, format/unit, bbox, topology counts, area, volume, and `ok`.
Keep the full local probe summary in records and signal bundles.  Do not alter
the report schema or gate authority.

## Consequences

Future first-pass requests disclose less local environment detail while
retaining the geometry facts used by the existing policy.  Completed M43
requests remain historical evidence and cannot be retroactively sanitized.
