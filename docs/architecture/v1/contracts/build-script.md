---
type: contract
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - contract
---

# Contract: build_sequence.py

`build_sequence.py` 是 v1 中 LLM 主要编辑的 CAD 脚本。Harness 负责创建、运行、保存版本和收集反馈。

## 最小要求

- 脚本必须可由 harness 在受限 workspace 中执行。
- 脚本必须产生一个 CAD 输出文件，优先为 `output/model.step`。
- 脚本不得读写 record 目录以外的路径。
- 脚本不得访问网络或秘密凭据。
- 脚本应尽量把关键中间步骤导出到 `intermediates/`，方便 repair。
- CAD API 仅可使用当前 runtime 安装的 `OCP` bindings；不得导入 `cadquery`、
  `OCC` 或 `OCC.Core`。Harness 在 sandbox 启动前静态拒绝这些已知不支持的
  import，并把该拒绝与普通 script/sandbox error 区分记录。

## 推荐入口

```python
def build(ctx):
    """Create CAD result and return artifact paths or metadata."""
```

如果后端更适合脚本式执行，harness 可以兼容无 `build()` 的文件，但最终仍要产出 `output/model.step`。

## ctx 最小语义

`ctx` 是 Harness 注入的 runtime helper，不是建模 SDK。M0/M1 阶段只应承载：

- 当前 revision workspace 内的稳定路径。
- artifact / trace / log 的写入辅助。
- 输入文件和配置的只读引用。

`ctx` 不应在早期承载项目级建模 API，例如草图、拉伸、倒角、布尔等操作。若脚本需要这些能力，应直接使用当前 CAD backend 的原生 API，并由 Harness 捕获结果和错误。

## 暂缓内容

- 不要求返回固定 modeling IR。
- 不要求使用专用 SDK。
- 不要求绑定某个 CAD backend。
