---
type: plan
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - milestones
---

# v1 Milestones — Harness-first

## M0 — Harness Skeleton

- record/workspace/storage 布局。
- `build_sequence.py` 模板。
- 脚本执行、日志捕获、revision 保存。
- 无 LLM 时可手动运行一轮。

## M1 — B-Rep Probe Tools

- 读入输入 B-Rep。
- `probe_summary`、`probe_topology`、`probe_entity`、`sample_entity`。
- tool result 大小限制和 trace 落盘。

## M2 — CAD Execution + Gates

- 生成并导出 `output/model.step`。
- 输出可重新读入。
- bbox、体积、mesh distance 等基础 gate。
- `signal_bundle.json` 稳定输出。

## M3 — Generic LLM Repair Loop

- 调用 hosted/general LLM。
- 支持 tool-calling。
- 基于 `signal_bundle.json` 迭代修改脚本。
- 保存 LLM 消息、工具调用和每轮产物。

M3 按 workpack 拆分推进：

1. `WP-M3-001` Provider + trace contract。
2. `WP-M3-002` Tool-calling bridge。
3. `WP-M3-003` Repair loop runner。
4. `WP-M3-004` Hosted provider integration（可选收尾）。

其中 M3-001 到 M3-003 是 Harness 完整搭建的必需范围；M3-004 负责接真实 hosted provider 和运行文档。

## M4 — Case Corpus Review

- 建立 manifest-driven 小型案例集。
- 先覆盖 P0 smoke fixtures，再按 workpack 扩展 P1/P2/P3。
- 批量运行 Harness gates，输出 corpus-level report。
- 对有 reference script 的案例运行 fake-provider repair replay。
- 汇总成功/失败模式，判断下一步是改 prompt/context、加 probe/action/gate，还是考虑 IR、SDK、CAD workplace 或专用 B-Rep 表示。

M4 入口文档：[`docs/architecture/v1/case-corpus-review.md`](../case-corpus-review.md)。

M4-001、M4-002 与 M4-003 已完成；review 结论见 [`m4-review-report.md`](../m4-review-report.md)。

## M5 — Runtime Sandbox Foundation

- 为 provider-generated script 建立 OS 强制的 filesystem/network/process 边界。
- 当前 cwd-only executor 仅允许作为明确标注的 `unsafe-local` 测试路径。
- hosted provider integration 必须等待 runtime sandbox contract 验收。

M5-001 已完成：WSL bubblewrap backend 及 runtime sandbox contract 已验证。M3-004 DeepSeek V4 hosted provider integration 也已完成。动态状态以 [`docs/workflow/status.md`](../../../workflow/status.md) 为准。
