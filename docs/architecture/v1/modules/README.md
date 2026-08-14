---
type: design
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - modules
---

# Brep2Code v1 — 代码模块索引

实现仓库：`D:\codeai\Brep2Code`。本页记录 harness-first v1 的规划模块。

## 顶层布局

```text
D:\codeai\Brep2Code/
  brep2code/
    brep/            # Q01: read input + probe backend
    agent/           # LLM loop + harness
    cad/             # CAD backend adapters
    corpus/          # manifest-driven case review
    eval/            # deferred standalone gates module
    storage/         # records, revisions, traces
    cli/             # brep2code commands
    scaffold.py      # build_sequence.py template
  docs/              # architecture, ADR, runbook, handoff
  data/              # gitignored local data root
```

技术栈规划：Python 3.12 + uv + just。CAD 后端先保持可插拔，按实现便利选择 pythonOCC、CadQuery 或其他。LLM 使用通用 hosted model。M0/M1 只实现 Harness runtime helper 和 CAD execution adapter，不实现项目级建模 SDK。

## 模块职责

| 代码目录 | 职责 | 设计笔记 |
|----------|------|----------|
| `brep2code/brep/` | 读入 B-Rep 并支撑 probe tools | [contracts/probe-tools.md](../contracts/probe-tools.md) |
| `brep2code/agent/` | LLM loop、harness、feedback、repair | [q03-harness/harness-overview.md](../q03-harness/harness-overview.md) |
| `brep2code/cad/` | CAD 脚本执行和后端适配，不承载建模 DSL | [contracts/build-script.md](../contracts/build-script.md) |
| `brep2code/corpus/` | case manifest、批量 Harness 运行、compact report | [contracts/case-corpus.md](../contracts/case-corpus.md) |
| `brep2code/eval/` | 独立 gates 模块暂缓；当前 gates 由 Harness 内实现 | [q03-harness/geometry-gate.md](../q03-harness/geometry-gate.md) |
| `brep2code/storage/` | records、revisions、artifacts、traces | 下文 storage 布局 |
| `brep2code/cli/` | `run`、`probe`、`repair`、`corpus` | [q03-harness/harness-overview.md](../q03-harness/harness-overview.md) |

## Storage 布局（规划）

```text
<data-root>/
  records/<record_id>/
    record.json
    input/
      part.step
    revisions/<rev_id>/
      workspace/
        build_sequence.py
        intermediates/
        output/
          model.step
      llm_messages.jsonl
      signal_bundle.json
      traces/
  records_manifest.jsonl
```

`workspace/` 专指 Harness 运行时受限工作区。开发协作文档使用 `docs/workflow/`，避免与 runtime workspace 混淆。

## CLI 速查（规划）

| 命令 | 说明 |
|------|------|
| `python -m brep2code.cli run --record demo` | M0 手动创建或打开 record 并执行一轮 |
| `python -m brep2code.cli run --record box-smoke --input case-library\self-authored\box\input.step` | 执行一轮 Harness，并运行当前 gates |
| `python -m brep2code.cli probe --input case-library\self-authored\box\input.step` | 调试 B-Rep probe tools |
| `python -m brep2code.cli repair --record box-repair --script broken_build.py --fake-replacement-script replacement_build.py` | 本地 fake-provider repair replay |
| `python -m brep2code.cli corpus ...` | 已实现的 manifest-driven 批量 review 命令 |