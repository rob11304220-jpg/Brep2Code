---
type: design
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - q01
---

# Q01 — Probe-first B-Rep Access

v1 不优先建设 B-Rep 编码器。Harness 读入输入文件后，向 LLM 暴露小而稳定的 probe tools，让 LLM 按需查询拓扑、几何和采样结果。

核心契约见 [contracts/probe-tools.md](../contracts/probe-tools.md)。

## 实现重点

- 读入 STP / IGES / `.brep`。
- 为 face / edge / solid 提供 record 内稳定 ID。
- 支持 summary、topology、entity、sampling、compare 等工具。
- 控制 tool result 大小，大结果写 trace。

## 暂缓

- UV-Net / VHP / BrepLLM / JSON-DSL 等编码路线。
- 面向训练的统一 tensor/schema。
- 一次性把完整 B-Rep 塞入 prompt。
