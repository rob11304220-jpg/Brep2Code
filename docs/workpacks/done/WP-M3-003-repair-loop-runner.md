# WP-M3-003: Repair Loop Runner

- Status: done
- Milestone: M3
- Owner: unassigned

## Goal

Implement the finite repair loop that builds repair context from script revisions, execution traces, gates, and tool results, asks the provider for a script update, then creates and executes the next revision.

## Scope

- Build compact repair context from input probe, current `build_sequence.py`, stderr/stdout previews, `execution.json`, `signal_bundle.json`, gates, and repair hints.
- Support one-shot repair and a bounded multi-round loop.
- Apply provider script output into a new revision workspace without mutating prior revisions.
- Execute each revision with the existing `ScriptExecutor`.
- Save per-round messages, tool calls, script snapshots, and signal bundles.
- Add CLI flags for repair-loop execution while preserving manual harness operation without credentials.

## Inputs

- `docs/workpacks/done/WP-M3-001-llm-provider-trace-contract.md`
- `docs/workpacks/done/WP-M3-002-tool-calling-bridge.md`
- `docs/workpacks/done/WP-M2-001-cad-output-gates.md`
- `docs/architecture/v1/contracts/build-script.md`
- `docs/architecture/v1/contracts/signal-bundle.md`
- `docs/architecture/v1/q03-harness/harness-overview.md`
- `docs/architecture/v1/q04-repair/router.md`

## Code paths

| Path | Purpose |
|------|---------|
| `brep2code/agent/` | repair runner and feedback context |
| `brep2code/cli/` | repair-loop command/flags |
| `brep2code/cad/` | script execution reuse |
| `data/records/<record_id>/revisions/<rev_id>/` | per-round artifacts and traces |
| `tests/` | fake-provider loop tests |

## Acceptance

- [x] A failing script can be repaired by a fake provider in a bounded loop.
- [x] Each attempted script lives in a separate immutable revision.
- [x] Failing feedback includes execution summary, stderr preview, gates, and repair hints.
- [x] The loop stops on pass, max rounds, or provider/tool error with structured status.
- [x] Existing manual `run` path remains usable without LLM credentials.
- [x] `uv run python -m pytest` passes.
- [x] `uv run python -m ruff check .` passes.

## Result

- Added `brep2code.agent.repair.RepairLoopRunner` with bounded fake-provider repair rounds.
- Saves per-round LLM messages, provider response summary, script update metadata, and immutable revision workspaces.
- Added CLI command `repair` with `--fake-replacement-script` for local no-credential smoke runs.
- Added `tests/test_agent_m3_repair_loop.py` covering successful repair, max-round stop, provider error, and CLI repair execution.
- Documented the runner in `docs/architecture/v1/contracts/repair-loop.md`.

## Out of scope

- Real hosted provider calls.
- Dataset-scale evaluation.
- Complex planner or multi-agent framework.
- Final CAD reconstruction quality claims.
