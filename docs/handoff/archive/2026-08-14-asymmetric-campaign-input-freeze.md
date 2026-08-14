# Handoff: asymmetric campaign input freeze

- **Date**: 2026-08-14
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M176-001-asymmetric-campaign-input-freeze`

## Goal

Freeze the two M175 evidence products and their bounded operational inputs
without provider construction, credentials, report checkpoints, or egress.

## Done

- M175's 30 no-card rows and three-role annex are independently approved.
- User selected M176 with DeepSeek V4 Pro, 4096 output tokens, 120 seconds,
  serial issuance, no retry, and 102 maximum completions.

## In progress

- M176 independently approved and closed.

## Next

- A separately selected G3 workpack must run fresh preflight and receive
  itemized hosted authorization before egress.

## Decisions

- Main and annex remain unpooled. Main has 90 completion capacity; annex 12.
- G3 requires a fresh preflight, independent review, and explicit itemized
  hosted authorization despite M176 closure.

## Blockers

- None. No G3 workpack or hosted authorization is selected.

## Key paths

| Kind | Path |
|---|---|
| Files | `docs/workpacks/active/WP-M176-001-asymmetric-campaign-input-freeze.md` |
| Cohort | `docs/corpus/knowledge/m175-asymmetric-cohort-qualification-v1.json` |
| Commands | `uv run python tools/check_governance.py` |

## Resume prompt

```
Continue Brep2Code work: complete M176's asymmetric campaign input freeze.
Read this handoff and active workpack. First derive metadata-only input
fingerprints without reading credentials or creating a provider/report.
```
