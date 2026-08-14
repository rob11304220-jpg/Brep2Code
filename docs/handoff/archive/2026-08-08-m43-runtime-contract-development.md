# Handoff: M43 runtime-contract development evaluation

- **Date**: 2026-08-08
- **Subproject**: `brep2code`
- **Status**: `active`
- **Related workpack**: `WP-M43-001-first-pass-runtime-contract-development-evaluation`

## Goal

Run the explicitly authorized, development-only DeepSeek first-pass evaluation
for ABC cases 27 and 30 under the bounded M42 runtime contract.

## Done

- M42 design-only preregistration completed.
- User authorized the exact development scope and acts as independent reviewer.

## In progress

- Add the minimal contract, finish the required preflight, then execute only
  the two authorized development cases.

## Next

- Review the completed development report and request separate held-out
  authorization only if the user selects it.

## Decisions

- Development uses DeepSeek `deepseek-v4-pro`, `wsl-bwrap`, two cases, one
  repair round, four-request maximum, and a 120-second provider deadline.
- Outbound material is the bounded probe summary, case identifier, and runtime
  contract; raw STEP is not sent.

## Blockers

- Held-out is intentionally unauthorized.

## Key paths

| Kind | Path |
|------|------|
| Branch | `main` |
| Files | `docs/workpacks/active/WP-M43-001-first-pass-runtime-contract-development-evaluation.md`; `data/corpus-runs/` |
| Commands | `uv run python -m brep2code.cli corpus --manifest docs\\corpus\\external\\abc-v00-m10-007-development-manifest.json --provider deepseek --first-pass --authorize-hosted --max-cases 2 --max-rounds 1 --request-budget 4 --provider-timeout 120 --executor wsl-bwrap` |

## Resume prompt

```
Continue Brep2Code work: complete M43's authorized development-only runtime-contract evaluation.
Read docs/handoff/active/2026-08-08-m43-runtime-contract-development.md.
First action: verify the preflight artifacts and report path, then run only the authorized development command.
```
