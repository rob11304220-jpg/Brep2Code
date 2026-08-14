---
type: contract
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - contract
  - probe
---

# Contract: B-Rep Probe Tools

v1 的 Q01 采用 probe-first：LLM 不接收完整 B-Rep 编码，而是在需要时调用工具查询输入几何。

## 初始工具集

| Tool | Purpose |
|------|---------|
| `probe_summary(record_id)` | 返回文件类型、单位、bbox、实体计数、体积/面积摘要。 |
| `probe_topology(record_id, selector)` | 查询 solid/shell/face/edge 层级和邻接摘要。 |
| `probe_entity(record_id, entity_id)` | 查询指定 face/edge 的类型、参数范围、面积/长度、bbox。 |
| `sample_entity(record_id, entity_id, n)` | 对 face/edge 采样点和法向/切向。 |
| `compare_result(record_id, revision_id)` | 对当前输出和输入运行轻量几何对比。 |

## 返回约束

- 返回 JSON，可直接进入 LLM tool result。
- 每次调用返回应有大小上限；大结果写入 trace，tool result 返回摘要和路径。
- entity id 必须在同一 record 内稳定。
- 工具失败也返回结构化错误，不抛给 LLM 原始栈。
- Harness 对输入模型 summary 使用 45 秒独立进程 deadline；对 provider 生成的输出 artifact summary 保持 15 秒 deadline。超时返回 `probe_timeout`，不会产生 partial summary。

## 非目标

- 不承诺完整还原 B-Rep 语义。
- 不承诺训练模型所需的统一 tensor/schema。
- 不把所有拓扑一次性塞入 prompt。
