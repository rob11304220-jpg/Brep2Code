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

# Q03 — Script Execution Pipeline

`compiler` 在 v1 中只表示脚本执行管线，不暗示固定 IR 编译器，也不暗示项目级建模 SDK。

```text
build_sequence.py
  -> sandboxed run
  -> CAD backend
  -> output/model.step
  -> gates
  -> signal_bundle.json
```

执行失败也必须产出 `signal_bundle.json`，方便下一轮 repair。

Harness core 只依赖脚本路径、workspace、执行结果和 artifact 检查；具体 CAD backend 的建模 API 留在 `build_sequence.py` 内部。
