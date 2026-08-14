# ADR-0011: Permit a Complete Local Cache of the Registered ABC Archive

- **Status**: Accepted
- **Date**: 2026-08-03

## Context

ABC `v00` is already present as one ignored local archive.  The former per-member extraction rule limits external-data scope, but the archive's 10,000 STEP members are stored in a form for which individual extraction repeatedly incurs substantial decode cost and exceeds an interactive command window.  The local disk has sufficient capacity for the approximately 12.76 GiB listed uncompressed STEP payload.

## Decision

- Permit one complete extraction of the already acquired `abc_0000_step_v00.7z` into ignored `data/datasets/abc/v00/step/`.
- Retain the archive as the immutable local source and treat `step/` as a reconstructable cache.  Write an ignored completion catalog only after the archive hash, member count, and listed byte total have been verified.
- A complete cache does not enable a full corpus, default test discovery, a tracked full manifest, provider input, redistribution, or use of any member without an approved selection record and explicit manifest.
- M10-010 expands only to prepare and verify this local cache before continuing its deterministic 2/1 admission after `00000031`.

## Consequences

- Raw assets, extraction catalog, logs, and reports remain under ignored `data/` and preserve the existing local-research/no-redistribution boundary.
- The Harness, CLI, report schema, probes, gates, provider policy, and default offline path remain unchanged.
- Interrupted extraction is not a completed cache.  In the absence of the completion catalog, every selected file remains subject to its individual existence and SHA-256 check.
