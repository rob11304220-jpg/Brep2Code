# Handoff: M6-001 complete and awaiting next workpack

- **Date**: 2026-08-01
- **Subproject**: `brep2code`
- **Status**: `active`

## Goal

Maintain the completed Harness-first baseline while no workpack is active; resume only after the user selects the next research or productization objective.

## Done

- M0 through M5-001 and M3-004 are complete; the current state is recorded in [`docs/workflow/status.md`](../../workflow/status.md).
- M3-004 routes explicit DeepSeek V4 provider-generated scripts through `wsl-bwrap`; its credential smoke passed output/readability and geometry gates without recording credentials in traces.
- Documentation cleanup on 2026-08-01 reconciled the sandbox contract, M4 review, and governance record with the completed hosted-provider integration and Git baseline.
- Created and completed [`WP-M6-001`](../../workpacks/done/WP-M6-001-hosted-corpus-evaluation.md) to extend the P0/P1 corpus into a bounded hosted-evaluation workflow without changing the default offline path.
- Implemented the M6-001 offline-safe increment: explicit hosted CLI bounds/authorization, DeepSeek-to-`wsl-bwrap` enforcement, preflight refusal, schema-v2 sanitized evaluation metadata, repair failure taxonomy, contract/module/runbook updates, and five pure preflight/serialization/sandbox-refusal tests.
- Completed the user-authorized P0 `deepseek-v4-flash` evaluation: 3 cases, 1 round per case, 3-request budget, and 2 requests used. Primary result was 1/3 pass; both failed geometry-gate cases repaired successfully in one round. The ignored report is `data/corpus-runs/deepseek-p0-flash-20260801.json`.
- A separately authorized P1 Flash batch was interrupted before its final report. Completed revisions show `chamfered_block` and `three_hole_plate` passing after repair, `filleted_block` failing after one round, and `box_cylinder_union` incomplete. This pre-checkpoint partial evidence is not a corpus result.
- Implemented the M6 recovery follow-up: reports atomically checkpoint `running` before work and after each completed case, and handled interruption/runner exceptions write `interrupted` while retaining prior case evidence. Focused checkpoint/preflight tests: 7 passed; changed-file Ruff passed.
- A newly authorized P1 Flash retry validated the external-stop boundary: its checkpoint retained three completed one-round repair passes (`filleted_block`, `chamfered_block`, `three_hole_plate`) and 3/4 requests used when `box_cylinder_union` ran long and the process was stopped. The report correctly remains `running`; it is partial evidence, not a completed P1 result.
- Offline diagnosis found the P1 fourth-case delay after its second ~1-second `wsl-bwrap` execution: request trace exists but no provider response trace. Added a separately terminable DeepSeek provider worker, default `--provider-timeout 120`, and structured `provider_request_timeout`; focused watchdog/checkpoint tests: 10 passed, changed-file Ruff passed.
- New authorized one-case `box_cylinder_union` Flash validation confirmed the watchdog: the 120-second deadline yielded a completed report with `provider_request_timeout` and no corpus hang. Its historical report incorrectly says `requests_used: 0` despite one request trace; request accounting is now fixed to increment on issuance, including timeout/error paths, with focused tests passing.
- Completed M6 review and failure taxonomy: [`m6-hosted-evaluation-report.md`](../../architecture/v1/m6-hosted-evaluation-report.md). M6 workpack is archived as done; the result does not justify IR, project CAD SDK, CAD workplace, new probes, or new gates.

## In progress

- No active workpack.
- `uv run python -m ruff check .` passed on 2026-08-01 after the documentation cleanup. Full-suite `uv run python -m pytest` attempts exceeded the 60-second execution window; the current verification instead completed in three bounded groups with 42 passed. The earlier 37-pass result remains historical acceptance evidence.

## Next

- Ask the user to select the next research or productization objective. The M6 review contains evidence-driven follow-up candidates.

## Decisions

- Current delivery state is owned by [`docs/workflow/status.md`](../../workflow/status.md); see [`ADR-0005`](../../architecture/adr/0005-current-state-source-of-truth.md).
- Hosted-provider execution requires the OS-enforced sandbox backend; see [`ADR-0006`](../../architecture/adr/0006-runtime-sandbox-before-hosted-provider.md).

## Blockers

- None. A larger hosted batch still requires explicit provider/model, case/round, provider-timeout, and cost or request budget authorization.

## Key paths

| Kind | Path |
|------|------|
| Branch | `main` |
| M6 review | `docs/architecture/v1/m6-hosted-evaluation-report.md` |
| Current state | `docs/workflow/status.md` |
| Completed hosted provider workpack | `docs/workpacks/done/WP-M3-004-hosted-provider-integration.md` |
| Sandbox contract | `docs/architecture/v1/contracts/runtime-sandbox.md` |
| Verification commands | `uv run python -m pytest`; `uv run python -m ruff check .` |

## Resume prompt

```
Continue Brep2Code from the completed M6 hosted-evaluation baseline.
Read AGENTS.md, docs/handoff/active/2026-08-01-project-idle.md, and docs/workflow/status.md.
First action: ask the user to select the next workpack; do not make another hosted request without explicit budget authorization.
```
