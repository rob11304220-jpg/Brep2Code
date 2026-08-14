---
type: design
related-project: Brep2Code
version: v1
status: deferred
tags:
  - Brep2Code
  - v1
  - modules
  - sdk
---

# 模块：deferred-sdk/（暂缓）

v1 不优先建设完整 Domain SDK。先允许 LLM 编写受控 CAD 脚本，Harness 负责执行与反馈。若案例显示重复操作和错误模式稳定，再从脚本中提炼 SDK 或 IR。

当前只保留 `build_sequence.py` 的最小脚本契约，见 [contracts/build-script.md](../../contracts/build-script.md)。

## 允许先沉淀的内容

早期可沉淀的是 runtime helper，而不是 modeling SDK：

- workspace 路径 helper。
- artifact / trace / log helper。
- 输入文件引用和后端配置读取。
- 可选的 modeling event 记录格式，用于复盘脚本行为。

这些 helper 只能降低 Harness 读写路径和 trace 的重复代码，不能定义 CAD 操作语义。

## 升级条件

只有当 case corpus 显示稳定重复结构时，才重新评估 SDK / IR：

- 多个案例反复出现同类 CAD 操作模板。
- 失败信号能映射到稳定的建模步骤类型。
- 不同 CAD backend 之间存在值得抽象的共同接口。
- LLM 直接写 backend 原生 API 的错误率成为主要瓶颈。
