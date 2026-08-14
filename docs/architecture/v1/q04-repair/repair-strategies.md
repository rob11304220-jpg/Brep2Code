---
type: design
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - repair
---

# Q04 — Repair Strategies

当前只保留通用策略：

- 先修脚本运行错误，再修 CAD 有效性，再修几何偏差。
- 每轮 repair 都保留 revision，避免覆盖历史。
- 失败信号不够具体时，优先让 LLM 调用 probe tools，而不是猜测。
- 从反复出现的修复动作中提炼未来 SDK、IR 或 CAD workplace。
- 在 SDK / IR 未收敛前，repair hint 只描述可验证失败和建议 probe，不要求 LLM 改写为某种固定建模序列。
