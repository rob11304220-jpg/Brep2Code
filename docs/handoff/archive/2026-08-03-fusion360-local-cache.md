# Handoff: Fusion 360 Gallery local complete cache

- **Date**: 2026-08-03
- **Subproject**: `brep2code`
- **Status**: done

## Goal

Prepare a verified ignored local cache of the official Fusion 360 Gallery
Reconstruction r1.0.1 archive, while deferring all case admission and Harness
use.

## Done

- M12-002 documented source, license, asset format, units, and the narrow future
  sketch/extrude selection rule without downloading data.
- User authorized local archive acquisition and complete extraction only.
- Added M13-001 and ADR-0015 with raw-data and runtime boundaries.
- Verified archive SHA-256, ZIP CRC and safe extraction; the ignored catalog
  records 120,461 ZIP members, 120,459 extracted files, and `train_test.json`.

## In progress

- None.

## Next

- Create a separate workpack before selecting any candidate or running replay.

## Decisions

- Retain the archive plus a complete ignored extraction cache under ADR-0015.
- No sample selection, STEP probe, local replay, manifest, provider request, or
  runtime change belongs to this workpack.

## Blockers

- None known; a failed download or archive validation must leave the catalog
  incomplete and be resolved before claiming cache readiness.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/done/WP-M13-001-fusion360-gallery-local-cache.md` |
| Decision | `docs/architecture/adr/0015-fusion360-gallery-local-complete-cache.md` |
| Tool | `tools/prepare_fusion360_gallery_cache.py` |
| Local root | `data/datasets/fusion360_gallery/r1.0.1/` |

## Resume prompt

```
Continue Brep2Code work: complete the authorized Fusion r1.0.1 local cache.
Read docs/handoff/active/2026-08-03-fusion360-local-cache.md.
First action: inspect the ignored cache catalog; if absent, run the cache tool
with --download and do not select any sample.
```
