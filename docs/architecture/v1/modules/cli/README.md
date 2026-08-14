---
type: design
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - modules
  - cli
---

# 模块：cli/

`D:\codeai\Brep2Code\brep2code\cli\`

## 当前命令

| 命令 | 说明 |
|------|------|
| `python -m brep2code.cli run --record demo` | 创建或打开 record 并执行一轮 Harness |
| `python -m brep2code.cli run --record box-smoke --input case-library\self-authored\box\input.step` | 带 STEP 输入运行当前 gates |
| `python -m brep2code.cli probe --input case-library\self-authored\box\input.step` | 调试 B-Rep probe tools |
| `python -m brep2code.cli repair --record box-repair --script broken_build.py --fake-replacement-script replacement_build.py` | 本地 fake-provider repair replay |
| `python -m brep2code.cli corpus --manifest case-library\manifests\self-authored\p0.json --data-root data` | M4 manifest-driven case corpus review |

## Deferred

`compile` 和独立 `eval` 命令当前未实现；现阶段重执行和 gates 通过 `run` 完成。