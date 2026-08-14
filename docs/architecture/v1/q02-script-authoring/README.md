---
type: design
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - q02
---

# Q02 — Script-first CAD Authoring

v1 让通用 LLM 先编写可执行 CAD 脚本，Harness 负责运行和反馈。固定 IR、完整 Domain SDK 和 CAD workplace 暂缓，等案例和资产足够后再决定。

核心契约见 [contracts/build-script.md](../contracts/build-script.md)。

## 当前边界

在未确认具体 CAD 建模方式、建模序列表达和后端能力前，Q02 的稳定边界是脚本文件和执行产物，而不是建模 API。

- `build_sequence.py` 是 LLM 主要编辑对象。
- `build(ctx)` 是推荐入口，不是固定 IR。
- `ctx` 可以提供路径、artifact、日志等 runtime helper。
- 不提供 `extrude`、`fillet`、`sketch` 等会提前锁定建模范式的项目级 API。
- 建模步骤、参数和失败模式先作为 trace / case corpus 观测数据沉淀。

## 实现重点

- 提供 `build_sequence.py` 模板。
- 限制脚本运行 workspace。
- 支持一个可用 CAD backend，后续再抽象多个 backend；Harness core 不依赖具体后端语义。
- 保存每轮脚本版本和 LLM 消息。
- 可选记录 `traces/modeling_events.jsonl`，用于后续复盘是否需要 IR / SDK。

## 暂缓

- Tier1/Tier2/Tier3 SDK 分层。
- OCCT/CadQuery 映射细节路线。
- 固定 modeling sequence IR。
- 项目级 CAD modeling DSL。
