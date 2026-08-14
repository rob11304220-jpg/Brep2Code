# ADR-0015: Permit a Complete Local Cache of the Fusion 360 Gallery Reconstruction Archive

- **Status**: Accepted
- **Date**: 2026-08-03

## Context

The official Fusion 360 Gallery Reconstruction r1.0.1 archive is the approved
source for a future sequence-supervised local study.  Repeated archive access
would make later deterministic inspection unnecessarily expensive.  The user
has authorized a local-only complete cache, while explicitly deferring sample
selection, replay, manifests, and hosted use.

## Decision

- Retain the official `r1.0.1.zip` as immutable raw input under ignored
  `data/datasets/fusion360_gallery/r1.0.1/archives/` and extract its complete
  contents to ignored `extracted/` below the same root.
- Before extraction, verify ZIP CRCs and reject empty, absolute, traversal, and
  symbolic-link members.  Publish an ignored completion catalog only after
  archive hashing and extraction succeed.
- The cache catalog records source identity, archive hash and size, member and
  file counts, extraction root, and discovered official split layout.
- A complete cache is not a case selection, manifest, default fixture, runtime
  resource, provider input, or authorization to replay or evaluate a sample.

## Consequences

- The raw archive and cache remain local, ignored, and subject to the official
  non-commercial research/no-full-redistribution license boundary.
- Later work can inspect only needed candidates from a stable local source, but
  must use an independent workpack to select official train/test-isolated cases
  and to perform any local replay.
- The Harness, CLI, schemas, probes, gates, helpers, IR, SDK, prompts, and
  default offline behavior remain unchanged.
