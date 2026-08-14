---
type: design
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - runtime
  - harness
---

# v1 Runtime Boundaries

本文定义两个主体的边界：**开发 Agent**（Codex、Cursor、人工开发者）与 **运行时 LLM**（由 Harness 调用以完成一次 record/revision 的模型重建）。它进一步区分三类材料：`docs/` 开发治理文档、项目内 Harness/LLM 可调用材料、项目外论文库。

开发 Agent 可以读写仓库代码和治理文档、领取 workpack、更新 handoff/ADR；运行时 LLM 只能在 Harness 授权的 record/revision 范围内调用工具、编辑脚本和读取运行时材料。二者不得因都被称为“agent”而混为同一权限或上下文域。

## 三类材料

| 类型 | 位置 | 读者 / 调用方 | 用途 |
|------|------|---------------|------|
| 开发治理文档 | `docs/` | 人类开发者、Codex/Cursor 等开发 Agent | 架构、ADR、runbook、workpack、模块对照；不注入运行时 LLM |
| 项目内可调用材料 | 代码包、runtime helper、案例资源、record runtime workspace | Harness、运行时 LLM、tool calls | 注入上下文、读取操作材料、编辑脚本、保存 trace |
| 项目外研究文档 | `D:\paper` | 人类开发者、coding agent 按需查询 | 文献、研究综述、路线依据 |

## Harness 注入上下文

运行时 LLM 不应直接把 `docs/` 当作默认 prompt 上下文。Harness 负责组装短上下文，包括：

- 当前任务说明。
- record metadata。
- 当前 revision 状态。
- 可用 tool 列表和 tool schema。
- 上轮 `signal_bundle.json` 摘要。
- 当前 `build_sequence.py` 或相关片段。

长材料通过 tool 读取，而不是一次性塞入 prompt。

## 项目内可调用材料

以下材料属于项目内运行时能力，不归入 `docs/` 治理文档：

- runtime helper API 的操作说明。
- CAD backend 的最小用法示例。
- 成功/失败案例片段。
- Harness tool 可读取的手册、样例和错误说明。
- record/revision 下的受限 workspace、artifacts、traces。

这些材料应随代码版本演进，并由 Harness 控制可见范围、大小上限和读取方式。

早期 runtime helper 只覆盖路径、artifact、trace、log 和输入引用。它不定义 CAD 建模操作语义；完整 Domain SDK、建模 DSL 或固定 IR 必须等案例复盘后再决定。

## 受限 workspace

`workspace` 在 v1 中专指 Articraft 式运行时受限工作区：LLM 编辑脚本、Harness 执行脚本、产物写入 record/revision 范围内。

因此，开发协作文档不使用 `docs/workspace/` 命名，避免和 runtime workspace 混淆。

## 不变边界

- `docs/` 不复制论文库正文。
- `D:\paper` 不承载实现仓的代码契约。
- Harness 注入给 LLM 的上下文应短、稳定、可追踪。
- LLM 需要更多操作材料时，通过 Harness tool 读取项目内资源。
