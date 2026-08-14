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

# Q04 — Repair Loop

v1 的 repair loop 直接把 `signal_bundle.json`、相关 trace 摘要和可用 probe tools 返回给通用 LLM，让 LLM 修改 `build_sequence.py`。

## 最小策略

- 执行错误：给出异常摘要、相关代码片段和运行环境。
- 缺少输出：要求补齐导出路径。
- CAD 无效：提示检查构造顺序、布尔操作和单位。
- 几何偏差：建议调用 probe tools 查询对应实体或比较输出。

暂不实现复杂的 IR editor 或多级 repair router。
