---
type: design
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - harness
---

# Q03 — Geometry Gate

Geometry gate 的目标是给 repair loop 足够具体的失败信号，而不是一次性定义最终评测体系。

## 初始指标

- bbox 偏差。
- 体积/面积偏差。
- 输入和输出的 mesh sampling distance。
- 输出 shape 有效性。

所有指标写入 [contracts/signal-bundle.md](../contracts/signal-bundle.md)，带单位、阈值和摘要。
