# Handoff: M44 runtime-contract held-out evaluation

- **Date**: 2026-08-08
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M44-001-first-pass-runtime-contract-held-out-evaluation`

## Goal

Run the explicitly authorized held-out evaluation of the frozen runtime-contract
policy on ABC case 31.

## Done

- M43 development run was reviewed; user authorized this separate held-out run.
- Absolute local input paths are excluded from future first-pass provider summaries.

## In progress

- None.  The held-out run and review are complete.

## Next

- If the user selects it, design a bounded Q03 reconstruction-provenance gate;
  do not schedule another provider request by default.

## Decisions

- Frozen scope: DeepSeek V4-Pro, one held-out case, `wsl-bwrap`, one repair
  round, two requests maximum, 120-second deadline.

## Blockers

- None.  Hosted work is closed; no further provider request is authorized.

## Key paths

| Kind | Path |
|------|------|
| Branch | `main` |
| Files | `docs/workpacks/active/WP-M44-001-first-pass-runtime-contract-held-out-evaluation.md`; `data/corpus-runs/` |
| Commands | `uv run python -m brep2code.cli corpus --manifest docs\\corpus\\external\\abc-v00-m10-007-held-out-manifest.json --provider deepseek --first-pass --authorize-hosted --max-cases 1 --max-rounds 1 --request-budget 2 --provider-timeout 120 --executor wsl-bwrap` |

## Resume prompt

```
Continue Brep2Code work: decide whether to select a bounded Q03 reconstruction-provenance gate design.
Read docs/handoff/active/2026-08-08-m44-runtime-contract-held-out.md.
First action: read ADR-0047 and create a workpack only after the user selects the provenance-gate scope.
```
