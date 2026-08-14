# WP-M3-001: LLM Provider + Trace Contract

- Status: done
- Milestone: M3
- Owner: unassigned

## Goal

定义最小 LLM provider 边界、repair trace 格式和本地 fake provider，使后续 repair loop 可以在无网络、无真实 hosted LLM 凭证的情况下先被测试。

## Scope

- 定义 provider request/response 的最小数据结构。
- 实现 fake provider，用于单元测试和本地 smoke。
- 保存 LLM messages 到 revision trace，例如 `llm_messages.jsonl`。
- 保存 provider metadata / raw-ish response 摘要，避免把 secrets 或超大响应写入 bundle。
- 文档化 hosted provider 配置原则，但本 workpack 不接入真实 SDK。
- 保留现有无 LLM manual harness 路径。

## Inputs

- `docs/workpacks/done/WP-M0-001-harness-skeleton.md`
- `docs/workpacks/done/WP-M1-001-brep-probe-tools.md`
- `docs/workpacks/done/WP-M2-001-cad-output-gates.md`
- `docs/architecture/v1/contracts/build-script.md`
- `docs/architecture/v1/contracts/signal-bundle.md`
- `docs/architecture/v1/q03-harness/harness-overview.md`
- `docs/architecture/v1/q04-repair/router.md`
- `docs/runbooks/dev-environment.md`

## Code paths

| Path | Purpose |
|------|---------|
| `brep2code/agent/` | provider interface, repair trace helpers |
| `brep2code/storage/` | revision trace path helpers if needed |
| `data/records/<record_id>/revisions/<rev_id>/traces/` | LLM messages and provider trace output |
| `tests/` | fake provider and trace tests |
| `docs/modules/` | module boundary updates |

## Acceptance

- [x] Provider interface can be tested with a local fake model, without network.
- [x] Fake provider can return a script edit or full `build_sequence.py` replacement payload.
- [x] A revision can save `llm_messages.jsonl` or equivalent append-only trace.
- [x] Trace format avoids committing API keys, environment variables, or full oversized responses.
- [x] Hosted provider configuration is documented at the level of env var names and secret handling only.
- [x] Manual harness remains usable without LLM credentials.
- [x] `uv run python -m pytest` passes.
- [x] `uv run python -m ruff check .` passes.

## Result

- Added `brep2code.agent.provider` with `ProviderRequest`, `ProviderResponse`, `ScriptUpdate`, `LLMProvider`, and deterministic `FakeLLMProvider`.
- Added `brep2code.agent.trace` with append-only `llm_messages.jsonl` and sanitized `provider_response.json` writers.
- Added provider/trace tests in `tests/test_agent_m3_provider_trace.py`.
- Documented the contract in `docs/architecture/v1/contracts/llm-provider-trace.md` and hosted provider secret-handling rules in `docs/runbooks/llm-provider-config.md`.

## Out of scope

- Real hosted LLM SDK integration.
- Probe tool-calling execution.
- Multi-round repair loop.
- Complex planner/agent framework.
- Final CAD reconstruction quality claims.

## Follow-up workpacks

- `docs/workpacks/done/WP-M3-002-tool-calling-bridge.md`
- `docs/workpacks/done/WP-M3-003-repair-loop-runner.md`
- `docs/workpacks/done/WP-M3-004-hosted-provider-integration.md`
