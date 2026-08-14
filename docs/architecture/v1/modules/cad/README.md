---
type: design
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - modules
  - cad
---

# 模块：cad/

`D:\codeai\Brep2Code\brep2code\cad\`

## 职责

执行 `build_sequence.py`，适配 CAD backend，并把输出限制在当前 revision workspace 内。M0/M1 阶段本模块是 execution adapter，不是 CAD 建模 SDK。

## 规划文件

| 文件 | 职责 |
|------|------|
| `executor.py` | `unsafe-local` subprocess 与 opt-in `wsl-bwrap` sandbox executor；捕获 exit code、stdout、stderr、耗时与 sandbox metadata |
| `template.py` | 提供默认 `build_sequence.py` 模板 |
| `backend.py` | CAD backend 选择与最小执行适配层 |

## 契约

- 输入脚本契约见 [contracts/build-script.md](../../contracts/build-script.md)。
- runtime sandbox 契约见 [contracts/runtime-sandbox.md](../../contracts/runtime-sandbox.md)。
- 执行摘要进入 [contracts/signal-bundle.md](../../contracts/signal-bundle.md) 的 `execution` 字段。

## 非职责

- 不定义项目级 modeling sequence IR。
- 不提供草图、拉伸、倒角、布尔等高层建模 API。
- 不把某个 CAD backend 的对象模型泄漏为 Harness core 的依赖。
