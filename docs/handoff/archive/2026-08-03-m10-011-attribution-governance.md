# Handoff: M10-011 attribution ledger and repair governance

- **Date**: 2026-08-03
- **Subproject**: `brep2code`
- **Status**: `completed`

## Goal

Verify the cumulative six-case external attribution ledger after completed M10-010 admission, then select exactly one evidence-gated successor route without changing runtime behavior or contacting a provider.

## Done

- M10-010 completed: the existing local ABC archive cache is verified, the 32/33/35 split has completed offline controls, and no provider request occurred.
- ADR-0010 established attribution-driven repair governance; ADR-0011 established the local-cache boundary.
- Documentation consistency review clarified historical M9 wording, post-M10-010 routing authority, the M10-012 activation condition, and hosted-provider availability wording.
- The verified ledger selected M10-012.  Its two host-path baselines reproduced the direct mechanism; `/input/model.step` produced readable output for both cases, and the non-matching import control retained its failure.  No provider request or production change occurred.

## In progress

- None.  M10-011 and its selected M10-012 experiment are completed.

## Next

- Read `docs/workflow/status.md` before activating any new evidence-gated workpack.  The M10-012 conclusion is limited to fixed-script sandbox compatibility.

## Decisions

- Use the ledger before further sampling or repair work; only `direct` evidence counts toward the narrow-helper threshold.
- Any offline experiment remains deterministic and does not make a model-quality claim.  Hosted development comparison and held-out remain separately authorized work.

## Blockers

- No active workpack.  Any hosted evaluation remains unauthorized.

## Key paths

- `docs/workpacks/done/WP-M10-011-attribution-ledger-and-repair-governance.md`
- `docs/architecture/v1/m10-external-attribution-ledger.md`
- `docs/architecture/adr/0010-attribution-driven-repair-governance.md`
- `docs/architecture/adr/0011-local-external-archive-cache.md`

## Resume prompt

```
M10-011 and M10-012 are complete.  Resume only from `docs/workflow/status.md`; do not treat the fixed-script result as authorization for hosted evaluation or production changes.
```
