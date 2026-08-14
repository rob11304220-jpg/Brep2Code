# Handoff: Harness-first M3 planning active

- **Date**: 2026-08-01
- **Subproject**: `brep2code`
- **Status**: `active`

## Goal

维持已完成的 Harness-first v1 基线；若用户选择 hosted provider 与凭证策略，则创建并领取可选的 M3-004 实施任务。

## Done

- 建立当前交付状态唯一事实源：[`docs/workflow/status.md`](../../workflow/status.md)。入口、workflow、pipeline、里程碑、模块索引和 README 已改为链接该页，不再各自裁决 active workpack。
- 新增 Agent 文档治理评估与原则：[`docs/architecture/document-governance.md`](../../architecture/document-governance.md)。
- 明确区分开发治理平面（Codex/Cursor 管理项目代码与文档）和运行时执行平面（Harness 内 LLM 读案例、调用工具、编辑受限 workspace 脚本）；前者不自动成为后者上下文。
- 完成 M4-003 review：P0 primary 1/3 pass、P1 primary 0/4 pass；local fake-provider replay 修复 P0 2/2、P1 4/4 个失败。结论是不引入 IR/SDK/CAD workplace，优先实现 runtime sandbox。
- M5-001 已完成并归档：`WslBubblewrapExecutor` 支持 opt-in `run --executor wsl-bwrap`，提供 read-only input/resources、output/intermediates-only 写入、环境/网络隔离、CPU/内存限制、timeout、child cleanup 和 structured sandbox events。真实 OCP 与所有手动 probes 均通过；`pytest` 33 passed、Ruff 通过。
- 新增 ADR：[`docs/architecture/adr/0005-current-state-source-of-truth.md`](../../architecture/adr/0005-current-state-source-of-truth.md)。
- 修复已归档 M1 workpack 的错误 `active` 状态，并将 v1 模块索引的 `corpus` CLI 从计划更新为已实现。

- 保留实现仓 / 论文库分工：本仓只记录当前实现决策，论文细节按需从 `D:\paper` 查。
- 更新根入口、README、架构概览和 Q01–Q04 pipeline。
- 精简 `docs/architecture/v1/`：删除过早的编码器、IR、SDK 分层和路线细节，替换为 harness-first 文档。
- 新增核心契约：`probe-tools`、`build-script`、`signal-bundle`。
- 新增 ADR：[`docs/architecture/adr/0003-harness-first-v1.md`](../../architecture/adr/0003-harness-first-v1.md)。
- 新增开发工作路由：[`docs/workflow/README.md`](../../workflow/README.md)。
- 新增 workpack 分发目录，并完成 M0 任务包：[`docs/workpacks/done/WP-M0-001-harness-skeleton.md`](../../workpacks/done/WP-M0-001-harness-skeleton.md)。
- 新增模块文档对照入口：[`docs/modules/README.md`](../../modules/README.md)。
- 明确 `docs/`、项目内 Harness/LLM 可调用材料、项目外论文库的边界：[`docs/architecture/v1/runtime-boundaries.md`](../../architecture/v1/runtime-boundaries.md)。
- 新增 ADR：[`docs/architecture/adr/0004-document-and-runtime-boundaries.md`](../../architecture/adr/0004-document-and-runtime-boundaries.md)。
- 整理 agent 可执行性文档：入口明确 active workpack 以 `docs/workflow/README.md` 为准；pipeline 标出 M0 active；WP-M0 补充计划 CLI、最小目录树和验收命令；v1 模块索引统一到 `brep2code/...` 包路径。
- 将 v1 残留目录名从 `q01-encoding` / `q02-sdk` / `modules/sdk` 调整为 `q01-brep-probes` / `q02-script-authoring` / `modules/deferred-sdk`，并补齐缺失的 `docs/architecture/v1/modules/cad/README.md`。
- 明确 M0/M1 的 SDK 边界：只实现 runtime helper 和 CAD execution adapter，不实现项目级 CAD 建模 API、固定 modeling IR 或建模序列 DSL；相关约束已写入 Q02、build-script contract、CAD/deferred-sdk 模块、runtime boundaries、M0 workpack 和 v1 decisions。
- 创建 Python 项目脚手架：`pyproject.toml`、`justfile`、`brep2code/` 包、`tests/`。
- 实现 M0 手动 harness：`python -m brep2code.cli run --record demo`。
- 实现 record/revision/workspace 布局、默认 `build_sequence.py` 模板、subprocess 执行、stdout/stderr trace、`execution.json`、`signal_bundle.json`。
- 补充 M0 测试：成功 revision 和失败 revision 日志保留。
- 更新 README、模块文档、pipeline/workflow 和 WP-M0 状态。
- 创建 M1 B-Rep probe 最小实现：`brep2code/brep/`、CLI `probe`、`run --input`、STEP smoke fixtures 和 probe tests。
- M1 当前使用 `cadquery-ocp` 提供的 `OCP` OpenCascade 绑定；当前 Python 环境为 3.14.2，已确认本机可导入 `OCP`。
- 已验证 M1 smoke：`python -m brep2code.cli probe --input case-library\self-authored\box\input.step`。
- 已验证测试：`python -m pytest`，11 passed。
- 补充开发环境 runbook：[`docs/runbooks/dev-environment.md`](../../runbooks/dev-environment.md)。Python 目标范围为 `>=3.12,<3.15`；runtime 依赖为 `cadquery-ocp>=7.9,<8`；dev group 包含 `pytest>=8`、`ruff>=0.8`。
- M1 workpack 已归档到 [`docs/workpacks/done/WP-M1-001-brep-probe-tools.md`](../../workpacks/done/WP-M1-001-brep-probe-tools.md)。
- 创建并完成 M2 workpack：[`docs/workpacks/done/WP-M2-001-cad-output-gates.md`](../../workpacks/done/WP-M2-001-cad-output-gates.md)。
- M2 最小实现完成：默认 `build_sequence.py` 使用 OCP 写真实 STEP；Harness 对输入/输出运行 probe summary，并写入 `output_model_step_readable`、`bbox_delta`、`volume_delta`、`topology_count_delta` gates。
- 已验证 M2：`uv run python -m brep2code.cli run --record box-smoke --input case-library\self-authored\box\input.step`，status `pass`。
- 已验证质量：`uv run python -m pytest`，13 passed；`uv run python -m ruff check .`，All checks passed。
- 创建 M3 active workpack，并在 2026-07-22 将原大包拆分为 provider/trace、tool-calling bridge、repair-loop runner 和 hosted-provider integration 四个 workpack。
- M3-001 workpack 已完成并归档：[`docs/workpacks/done/WP-M3-001-llm-provider-trace-contract.md`](../../workpacks/done/WP-M3-001-llm-provider-trace-contract.md)。
- M3-002 workpack 已完成并归档：[`docs/workpacks/done/WP-M3-002-tool-calling-bridge.md`](../../workpacks/done/WP-M3-002-tool-calling-bridge.md)。
- M3-003 workpack 已完成并归档：[`docs/workpacks/done/WP-M3-003-repair-loop-runner.md`](../../workpacks/done/WP-M3-003-repair-loop-runner.md)。
- 创建 M4 Case Corpus Review 规划：[`docs/architecture/v1/case-corpus-review.md`](../../architecture/v1/case-corpus-review.md)。
- 创建 M4-001 workpack（现已归档）：[`docs/workpacks/done/WP-M4-001-case-corpus-manifest-and-runner.md`](../../workpacks/done/WP-M4-001-case-corpus-manifest-and-runner.md)。
- M3-004 hosted provider integration 保留在 backlog，只有需要真实 hosted LLM 时再领取。
- M3 backlog workpacks：
  - [`docs/workpacks/done/WP-M3-004-hosted-provider-integration.md`](../../workpacks/done/WP-M3-004-hosted-provider-integration.md)
- 更新 workflow、pipeline、milestones、workpacks README、README 和模块文档，使 active 状态从旧 M2/M3 大包同步到 M3-001 provider/trace。
- 完成 M3-001 provider/trace contract：
  - 新增 `brep2code/agent/provider.py`，定义 `ProviderRequest`、`ProviderResponse`、`ScriptUpdate`、`LLMProvider` 和本地 `FakeLLMProvider`。
  - 新增 `brep2code/agent/trace.py`，支持 revision `traces/llm_messages.jsonl` append-only 写入和 `traces/provider_response.json` 摘要写入。
  - 新增 `tests/test_agent_m3_provider_trace.py`，覆盖 fake provider 的 replace/edit 响应和 trace 截断/脱敏。
  - 新增 provider/trace contract 文档与 hosted provider 配置 runbook。
  - 已验证 `uv run python -m pytest`：16 passed；`uv run python -m ruff check .`：All checks passed。
- 将 M3-002 Tool-Calling Bridge 提升为当前 active workpack。
- 完成 M3-002 tool-calling bridge：
  - 新增 `brep2code/agent/tools/`，实现 `BRepToolBridge`、`ToolSpec`、`ToolCallResult`。
  - 支持 `probe_summary`、`probe_topology`、`probe_entity`、`sample_entity` 的有界工具注册、参数校验和 dispatch。
  - 支持 unknown tool、非法 selector/sample count/max_entities、call count limit 的结构化错误。
  - 支持 oversized probe result 写完整 JSON trace，并在 compact tool result 中返回 `trace_path`。
  - 支持 `traces/tool_calls.jsonl` 记录参数、compact result、status、error 和 trace path。
  - 新增 `tests/test_agent_m3_tool_bridge.py`。
  - 新增 `docs/architecture/v1/contracts/llm-tool-bridge.md`。
  - 已验证 `uv run python -m pytest`：21 passed；`uv run python -m ruff check .`：All checks passed；`uv run python -m brep2code.cli probe --input case-library\self-authored\box\input.step` 正常。
- 将 M3-003 Repair Loop Runner 提升为当前 active workpack。
- 完成 M3-003 repair-loop runner：
  - 新增 `brep2code/agent/repair.py`，实现 `RepairLoopRunner`、`RepairLoopResult`、`RepairAttempt`。
  - repair context 包含 current `build_sequence.py`、execution summary、stdout/stderr previews、signal bundle gates 和 repair hints。
  - fake provider replacement script 会进入新的 revision workspace，旧 revision 不变。
  - 保存每轮 `llm_messages.jsonl`、`provider_response.json`、`script_update.json` 和各 revision 的 `signal_bundle.json`。
  - CLI 新增 `repair --fake-replacement-script`，用于本地无凭证 smoke。
  - 新增 `tests/test_agent_m3_repair_loop.py`，覆盖 successful repair、max_rounds、provider_error 和 CLI repair。
  - 新增 `docs/architecture/v1/contracts/repair-loop.md`。
  - 已验证 `uv run python -m pytest`：25 passed；`uv run python -m ruff check .`：All checks passed。
- M3-001 到 M3-003 必需 workpack 已完成；M3-004 真实 hosted provider integration 保持 backlog/可选。
- M4-001 workpack 已完成并归档：[`docs/workpacks/done/WP-M4-001-case-corpus-manifest-and-runner.md`](../../workpacks/done/WP-M4-001-case-corpus-manifest-and-runner.md)。
- 新增 `brep2code/corpus/`：
  - `load_case_manifest(path)` 加载并校验 manifest。
  - `CorpusRunner` 批量执行 `ManualHarness`。
  - `write_corpus_report(...)` 写 compact report。
- 新增 P0 manifest：[`case-library/manifests/self-authored/p0.json`](../../../case-library/manifests/self-authored/p0.json)，注册 `box`、`cylinder`、`block_with_hole`。
- 新增本地 fake-provider repair replay reference scripts：
  - [`case-library/self-authored/cylinder/reference_build_sequence.py`](../../../case-library/self-authored/cylinder/reference_build_sequence.py)
  - [`case-library/self-authored/block_with_hole/reference_build_sequence.py`](../../../case-library/self-authored/block_with_hole/reference_build_sequence.py)
- CLI 新增 corpus 命令：

```powershell
uv run python -m brep2code.cli corpus --manifest case-library\manifests\self-authored\p0.json --data-root data
```

- 已验证：
  - `uv run python -m pytest`，30 passed。
  - `uv run python -m ruff check .`，All checks passed。
- M4-002 workpack 已完成并归档：[`docs/workpacks/done/WP-M4-002-p1-parametric-case-expansion.md`](../../workpacks/done/WP-M4-002-p1-parametric-case-expansion.md)。
- 新增 P1 fixtures：[`case-library/self-authored/`](../../../case-library/self-authored/)。
  - `filleted_block.step`
  - `chamfered_block.step`
  - `three_hole_plate.step`
  - `box_cylinder_union.step`
- 新增 P1 manifest：[`case-library/manifests/self-authored/p1.json`](../../../case-library/manifests/self-authored/p1.json)。
- 新增 P1 local reference scripts：
  - `filleted_block_build_sequence.py`
  - `chamfered_block_build_sequence.py`
  - `three_hole_plate_build_sequence.py`
  - `box_cylinder_union_build_sequence.py`
- P1 CLI smoke 已运行：

```powershell
uv run python -m brep2code.cli corpus --manifest case-library\manifests\self-authored\p1.json --data-root data --report data\corpus-runs\p1-smoke.json
```

该 smoke 返回非零，因为 primary default runs 全部失败 M2 geometry gates；这是预期 evidence，默认 `build_sequence.py` 仍只输出 P0 box。

- 已验证：
  - `uv run python -m pytest`，33 passed。
  - `uv run python -m ruff check .`，All checks passed。

## In progress

- 当前无 active workpack。M3-004 已完成：DeepSeek V4-Pro credential smoke 通过全部输出与几何 gates，provider-generated scripts 经 `wsl-bwrap` 执行。
- B-Rep 输入来源优先级已沉淀到 [`docs/links/brep-input-sources.md`](../../links/brep-input-sources.md)；当前仍只启用 P0 自制 STEP smoke fixtures。

## Next

- 等待用户选择下一项研究或产品化工作；保持默认路径 network-free、无凭证。
- 保持默认路径 network-free、无凭证；保留现有 `run`、`probe`、`repair` CLI 行为。

## Decisions

- v1 采用 Harness-first，见 ADR-0003。
- 调用通用 hosted LLM；不做本地部署、训练或微调。
- Q01 采用 probe-first，不先做 B-Rep 编码器。
- Q02 采用 script-first，IR / SDK / CAD workplace 等案例充分后再决定。
- 在建模方式和建模序列表达未收敛前，Harness core 只依赖脚本路径、workspace、执行结果、artifact 和 trace；`ctx` 仅承载路径、artifact、trace、log 等 runtime helper。
- 开发协作文档使用 `docs/workflow/`；`workspace` 一词保留给 Harness runtime workspace，见 ADR-0004。
- 运行时 LLM 的上下文、SDK/案例/操作材料属于项目内可调用材料，由 Harness 注入或通过 tool 读取，不作为 `docs/` 默认上下文库，见 ADR-0004。
- M0 runtime 保持零第三方依赖；`pyproject.toml` 是 Python 依赖入口，dev 依赖为 `pytest` 和 `ruff`。
- M0 默认 `build_sequence.py` 只写占位 `output/model.step`，不绑定 CAD backend。
- M3 workpack 采用小步验收：M3-001 到 M3-003 是 Harness 完整搭建必需范围；M3-004 是真实 hosted provider 接入和文档收尾。
- 当前交付状态统一由 [`docs/workflow/status.md`](../../workflow/status.md) 维护；见 [`docs/architecture/adr/0005-current-state-source-of-truth.md`](../../architecture/adr/0005-current-state-source-of-truth.md)。
- Hosted provider 必须等待 OS 级 runtime sandbox；见 [`docs/architecture/adr/0006-runtime-sandbox-before-hosted-provider.md`](../../architecture/adr/0006-runtime-sandbox-before-hosted-provider.md)。

## Blockers

- 无。

## Key paths

| Kind | Path |
|------|------|
| Branch | `main` |
| Agent 入口 | `AGENTS.md` |
| v1 入口 | `docs/architecture/v1/README.md` |
| v1 架构 | `docs/architecture/v1/architecture.md` |
| v1 里程碑 | `docs/architecture/v1/milestones/README.md` |
| 开发路由 | `docs/workflow/README.md` |
| 当前交付状态 | `docs/workflow/status.md` |
| 文档治理原则 | `docs/architecture/document-governance.md` |
| M0 Workpack | `docs/workpacks/done/WP-M0-001-harness-skeleton.md` |
| M1 Workpack | `docs/workpacks/done/WP-M1-001-brep-probe-tools.md` |
| M2 Workpack | `docs/workpacks/done/WP-M2-001-cad-output-gates.md` |
| M3 Done Workpack | `docs/workpacks/done/WP-M3-001-llm-provider-trace-contract.md` |
| M3 Done Workpack | `docs/workpacks/done/WP-M3-002-tool-calling-bridge.md` |
| M3 Done Workpack | `docs/workpacks/done/WP-M3-003-repair-loop-runner.md` |
| M3 Done Workpack | `docs/workpacks/done/WP-M3-004-hosted-provider-integration.md` |
| M4 Plan | `docs/architecture/v1/case-corpus-review.md` |
| M4 Review | `docs/architecture/v1/m4-review-report.md` |
| Runtime sandbox contract | `docs/architecture/v1/contracts/runtime-sandbox.md` |
| M5 Done Workpack | `docs/workpacks/done/WP-M5-001-runtime-sandbox-foundation.md` |
| M4 Done Workpack | `docs/workpacks/done/WP-M4-001-case-corpus-manifest-and-runner.md` |
| M4 Done Workpack | `docs/workpacks/done/WP-M4-002-p1-parametric-case-expansion.md` |
| Corpus Module | `brep2code/corpus/` |
| P0 Corpus Manifest | `case-library/manifests/self-authored/p0.json` |
| P1 Corpus Manifest | `case-library/manifests/self-authored/p1.json` |
| P1 B-Rep fixtures | `case-library/self-authored/` |
| B-Rep 输入来源 | `docs/links/brep-input-sources.md` |
| 模块对照 | `docs/modules/README.md` |
| v1 模块索引 | `docs/architecture/v1/modules/README.md` |
| Runtime 边界 | `docs/architecture/v1/runtime-boundaries.md` |
| Dev environment | `docs/runbooks/dev-environment.md` |
| ADR | `docs/architecture/adr/0003-harness-first-v1.md` |
| ADR | `docs/architecture/adr/0004-document-and-runtime-boundaries.md` |
| Python config | `pyproject.toml` |
| CLI | `brep2code/cli/__init__.py` |
| Harness | `brep2code/agent/harness.py` |
| B-Rep | `brep2code/brep/` |
| B-Rep fixtures | `case-library/self-authored/` |
| Storage | `brep2code/storage/store.py` |
| Executor | `brep2code/cad/executor.py` |
| Tests | `tests/test_harness_m0.py` |
| Tests | `tests/test_brep_m1.py` |
| Tests | `tests/test_harness_m2.py` |
| Command | `python -m brep2code.cli run --record demo` |
| Command | `python -m brep2code.cli probe --input case-library\self-authored\box\input.step` |
| Command | `uv run python -m brep2code.cli run --record box-smoke --input case-library\self-authored\box\input.step` |
| Command | `uv run python -m pytest` |
| Command | `uv run python -m ruff check .` |

## Resume prompt

```
Continue Brep2Code after M5 Runtime Sandbox Foundation.
Read AGENTS.md, docs/handoff/active/2026-07-10-agent-framework-init.md, docs/workflow/status.md, docs/workpacks/done/WP-M3-004-hosted-provider-integration.md, docs/runbooks/llm-provider-config.md, docs/architecture/v1/contracts/runtime-sandbox.md, and docs/architecture/adr/0006-runtime-sandbox-before-hosted-provider.md.
M3-004 DeepSeek V4 integration is complete: provider-generated scripts route through `wsl-bwrap`. First action: read the status page and wait for the user to select the next workpack.
```