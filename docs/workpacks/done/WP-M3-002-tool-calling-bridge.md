# WP-M3-002: Tool-Calling Bridge

- Status: done
- Milestone: M3
- Owner: unassigned

## Goal

Expose the existing M1 B-Rep probe tools as bounded LLM-callable tools so the repair loop can query geometry without placing the full B-Rep into prompt context.

## Scope

- Define the internal tool registry used by the agent loop.
- Expose `probe_summary`, `probe_topology`, `probe_entity`, and `sample_entity` through bounded tool calls.
- Validate tool names and arguments before dispatch.
- Enforce call count, sample count, entity selector, and result size limits.
- Save oversized full tool results to trace and return compact summaries to the provider.
- Preserve structured errors for missing input, invalid entity ids, unsupported formats, and backend failures.

## Inputs

- `docs/workpacks/done/WP-M3-001-llm-provider-trace-contract.md`
- `docs/workpacks/done/WP-M1-001-brep-probe-tools.md`
- `docs/architecture/v1/contracts/probe-tools.md`
- `docs/architecture/v1/q03-harness/action-space.md`
- `brep2code/brep/`

## Code paths

| Path | Purpose |
|------|---------|
| `brep2code/agent/tools/` | bounded LLM tool dispatch |
| `brep2code/brep/` | probe backend |
| `brep2code/storage/` | trace paths if needed |
| `tests/` | fake tool-call and limit tests |
| `docs/modules/` | agent/B-Rep module updates |

## Acceptance

- [x] Tool registry lists the supported probe tools and schemas.
- [x] Tool calls reject unknown tools and invalid arguments with structured errors.
- [x] Probe results remain size bounded; oversized payloads write full JSON to trace.
- [x] Tool call traces record arguments, compact result, status, and trace path when applicable.
- [x] Existing `python -m brep2code.cli probe ...` behavior remains unchanged.
- [x] `uv run python -m pytest` passes.
- [x] `uv run python -m ruff check .` passes.

## Result

- Added `brep2code.agent.tools.BRepToolBridge` with bounded registry, validation, call-count limits, probe dispatch, and `tool_calls.jsonl` trace writing.
- Added `tests/test_agent_m3_tool_bridge.py` covering schemas, invalid tools/arguments, result-size trace overflow, tool-call trace records, and call-count limits.
- Documented the bridge in `docs/architecture/v1/contracts/llm-tool-bridge.md`.
- Verified existing CLI probe behavior with `uv run python -m brep2code.cli probe --input case-library\self-authored\box\input.step`.

## Out of scope

- Hosted LLM SDK integration.
- Script editing or revision execution.
- New geometry gates beyond the existing M2 gates.