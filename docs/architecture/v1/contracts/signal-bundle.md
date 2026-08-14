---
type: contract
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - contract
---

# Contract: signal_bundle.json

`signal_bundle.json` 是 Harness 给 LLM repair loop 的结构化反馈。它应短、稳定、可直接进入下一轮 prompt。

## 顶层字段

```json
{
  "record_id": "string",
  "revision_id": "string",
  "status": "pass|fail",
  "execution": {},
  "artifacts": {},
  "gates": [],
  "guidance": null,
  "probe_suggestions": [],
  "repair_hints": []
}
```

## 必填语义

| 字段 | 说明 |
|------|------|
| `execution` | 退出码、异常摘要、stdout/stderr 摘要、耗时 |
| `artifacts` | 输入、输出、中间文件路径和是否存在 |
| `gates` | 每个 gate 的 `name/status/metric/message` |
| `probe_suggestions` | 下一轮可能需要查询的 B-Rep 信息 |
| `repair_hints` | Harness 可确定的修复方向，不替 LLM 编完整方案 |
| `guidance` | `null`（默认）或 revision-scoped guidance 调用的启用状态、index hash、返回 card ID 与紧凑错误；不含卡正文或路径 |

## 原则

- 保存完整日志到 trace 文件；bundle 只放摘要。
- 数值指标保留单位和容差。
- 失败信号优先具体，例如缺少输出、无效 shape、bbox 偏差过大。
- 提供输入 STEP 时，`input_model_step_readable` 必须反映 input summary 是否可用；input probe failure 是失败，不能仅通过 comparison gate 的 `skip` 使 revision 通过。
