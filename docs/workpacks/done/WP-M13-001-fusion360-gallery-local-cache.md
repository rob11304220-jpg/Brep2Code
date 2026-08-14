# WP-M13-001: Fusion 360 Gallery Local Complete Cache

- Status: done
- Milestone: M13
- Owner: unassigned

## Goal

Acquire, hash, and safely fully extract the official Fusion 360 Gallery
Reconstruction r1.0.1 archive as an ignored local cache, without admitting any
case to the Harness.

## Scope

- Download the official approximately 2 GB archive to
  `data/datasets/fusion360_gallery/r1.0.1/archives/` and retain it after
  extraction.
- Verify its ZIP integrity and SHA-256, reject unsafe member paths, then fully
  extract to the ignored `extracted/` cache and write an ignored completion
  catalog.
- Record the non-commercial research/no-full-redistribution license boundary
  and the absence of data egress to any model provider.

## Inputs

- Official source: `https://fusion-360-gallery-dataset.s3.us-west-2.amazonaws.com/reconstruction/r1.0.1/r1.0.1.zip`
- [M12-002 admission audit](../done/WP-M12-002-fusion360-offline-admission-audit.md)
- [ADR-0015](../../architecture/adr/0015-fusion360-gallery-local-complete-cache.md)

## Compatibility constraints

Default execution remains offline and credential-free. No external raw asset is
committed; no case, manifest, provider request, reference replay, probe, gate,
CLI, schema, helper, IR, SDK, or prompt changes are permitted.

## Acceptance

- Archive SHA-256, byte size, ZIP member count, listed bytes, extraction file
  count, root, and detected split paths are recorded in an ignored catalog.
- ZIP CRC and safe-member validation pass; extracted paths remain below the
  ignored data root; archive and cache are not Git-tracked.
- `uv run python -m pytest`, `uv run python -m ruff check .`, and
  `git diff --check` pass.

## Implementation evidence

- Archive SHA-256: `485601de3d23e25a5d63a75588ca780fa7881d7a0bea1ab6c24dbcefa57ad5c9`;
  2,103,449,157 bytes; 120,461 ZIP members and 5,166,881,935 listed bytes.
- ZIP CRC and safe-member validation passed; 120,459 files were extracted to
  ignored `data/`. The catalog detects `r1.0.1/train_test.json`.

## Out of scope

Sample selection, STEP probing, local reference replay, manifests, Harness
execution, hosted evaluation, or any data egress.
