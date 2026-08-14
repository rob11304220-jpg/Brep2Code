# Handoff: M10-010 third deterministic external increment

- **Date**: 2026-08-03
- **Subproject**: `brep2code`
- **Status**: `done`

## Goal

Prepare and verify the complete ignored local cache of the existing ABC v00 archive, admit a third small deterministic split after M10-007 cutoff `00000031`, and complete local `wsl-bwrap` controls without contacting a provider.

## Done

- M10-009 combined all six completed M10-005/M10-008 cases. Two direct sandbox-path failures, one direct unavailable-import failure, two generic STEP-read failures, and one provider lifecycle failure did not create a three-case single-root-cause threshold.
- M10-009 selected this offline deterministic increment; no runtime behavior or hosted policy changed.
- ADR-0010, the cumulative six-case attribution ledger, and the M10-011/M10-012 successor workpacks are documented.  They do not change M10-010 or authorize a provider request.
- ADR-0011 authorized complete local extraction of the already acquired archive as an ignored reconstructable cache.  Its completion catalog validated archive hash, 10,000 members, and listed bytes.
- M10-010 accepted 32/33/35 as a 2/1 split, rejected 34 as three-solid, and completed both ignored `wsl-bwrap` controls.  See the M10-010 review.

## In progress

- None.

## Next

- Continue with the active M10-011 handoff and verify the cumulative attribution ledger before selecting any repair or additional sampling route.

## Decisions

- Keep existing admission criteria, source/license boundary, `wsl-bwrap`, probes, gates, and default offline boundary unchanged.
- Any later hosted evaluation needs a new workpack, fresh preflight, and separate authorization for each split.
- ADR-0010 replaces automatic post-M10 fallback expansion with cumulative attribution routing; it applies only after M10-010 completes.
- ADR-0011 permits only a complete ignored local cache; it does not enable a full manifest, default corpus, provider input, or redistribution.

## Blockers

- None for offline admission. A later hosted run remains unauthorized.

## Key paths

- `docs/workpacks/done/WP-M10-010-third-deterministic-external-corpus-increment.md`
- `docs/architecture/v1/m10-009-cross-batch-generation-attribution-review.md`
- `docs/architecture/v1/m10-external-attribution-ledger.md`
- `docs/architecture/adr/0011-local-external-archive-cache.md`
- `docs/architecture/v1/m10-010-abc-external-increment-review.md`
- `docs/workpacks/active/WP-M10-011-attribution-ledger-and-repair-governance.md`
- `docs/corpus/external/abc-v00-m10-007-selection.json`

## Resume prompt

```
Continue M10-010. Starting strictly after M10-007 cutoff 00000031, perform deterministic archive-order admission for a 2/1 ABC v00 split and complete only offline hash/probe/wsl-bwrap controls. Do not contact a provider.
```
