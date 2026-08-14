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

# Q03 — Harness Overview

Harness 是 v1 的优先实现对象。它把通用 LLM、B-Rep probe tools、CAD 脚本执行、门控和 repair loop 串成可重复实验。

## 一轮执行

1. 创建或读取 record。
2. 将任务、当前脚本、可用 tools、上轮 `signal_bundle.json` 提供给 LLM。
3. LLM 按需调用 probe tools。
4. LLM 修改 `build_sequence.py`。
5. Harness 执行脚本并收集 artifacts。
6. Gates 生成 `signal_bundle.json`。
7. 若失败，进入下一轮 repair。

## Harness 必须记录

- LLM messages 和 tool calls。
- 每个 revision 的脚本快照。
- stdout/stderr、异常摘要和耗时。
- 输入、输出、中间文件和门控结果。

## v1 边界

- 不托管本地模型。
- 不要求固定 IR。
- 不把 B-Rep 全量编码进 prompt。
