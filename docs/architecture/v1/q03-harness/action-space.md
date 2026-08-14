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

# Q03 — Action Space

LLM 在 v1 中主要有三类动作：

| Action | 说明 |
|--------|------|
| Probe | 调用 [contracts/probe-tools.md](../contracts/probe-tools.md) 查询输入或输出。 |
| Edit | 修改 `build_sequence.py`。 |
| Compile/Eval | 请求 harness 执行脚本并返回 [contracts/signal-bundle.md](../contracts/signal-bundle.md)。 |

动作空间应保持小而稳定，避免提前暴露复杂 CAD workplace。
