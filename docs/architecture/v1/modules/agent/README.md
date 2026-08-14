---
type: design
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - modules
  - agent
---

# 模块：agent/

`D:\codeai\Brep2Code\brep2code\agent\`

## 职责

Harness 运行时：通用 LLM tool-calling、workspace 管理、脚本执行、反馈汇总和 repair loop。

## 规划目录

```text
agent/
  harness.py
  llm_client.py
  runner.py
  feedback.py
  tools/
    __init__.py
    compile_script.py
    probe_brep.py
    compare_result.py
```

## 设计笔记

- [q03-harness/harness-overview.md](../../q03-harness/harness-overview.md)
- [q03-harness/action-space.md](../../q03-harness/action-space.md)
- [q04-repair/router.md](../../q04-repair/router.md)
- [contracts/signal-bundle.md](../../contracts/signal-bundle.md)
