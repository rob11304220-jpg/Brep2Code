# WP-M0-001: Harness Skeleton

- Status: done
- Milestone: M0
- Owner: unassigned

## Goal

搭建最小 Harness skeleton，使项目可以在无 LLM 的情况下创建 record、准备受限 workspace、运行 `build_sequence.py`、捕获日志并保存 revision。

## Scope

- Python 项目脚手架。
- record / revision / workspace / artifact 的最小目录结构。
- `build_sequence.py` 初始模板。
- 手动执行一轮脚本。
- 生成基础执行摘要，后续可扩展为 `signal_bundle.json`。
- 仅提供 runtime helper / execution adapter 级能力，不引入 CAD 建模 SDK、固定 IR 或 modeling sequence schema。

## Inputs

- `AGENTS.md`
- `docs/handoff/active/2026-07-10-agent-framework-init.md`
- `docs/architecture/v1/milestones/README.md`
- `docs/architecture/v1/contracts/build-script.md`
- `docs/architecture/v1/contracts/signal-bundle.md`
- `docs/architecture/v1/q03-harness/harness-overview.md`

## Code paths

计划路径以实际脚手架为准：

| Path | Purpose |
|------|---------|
| `brep2code/storage/` | record、revision、workspace 路径管理 |
| `brep2code/agent/` | harness orchestration skeleton |
| `brep2code/cad/` | script execution adapter, not modeling SDK |
| `brep2code/cli/` | manual run command |
| `data/records/` | 本地运行产物，默认不提交 |

## Planned CLI

M0 先提供无 LLM 的手动闭环，命令名可在实现时微调，但必须在 README 或 CLI help 中可发现：

```powershell
python -m brep2code.cli run --record demo
python -m brep2code.cli run --record demo --script path\to\build_sequence.py
```

第一条命令应创建或打开 `demo` record、写入默认 `build_sequence.py` 模板并执行一轮。第二条命令用于复制外部脚本到当前 revision workspace 后执行。

## Minimum tree

M0 完成后至少应形成：

```text
brep2code/
  __init__.py
  agent/
  cad/
  cli/
  storage/
data/
  records/
```

## Docs to update

- `docs/modules/README.md`
- 相关模块文档
- `docs/handoff/active/`
- 若目录契约发生变化，更新 `docs/architecture/v1/modules/README.md`

## Acceptance

- [x] 可以用一个命令创建或打开 record。
- [x] Harness 能写入或复制 `build_sequence.py` 模板。
- [x] Harness 能执行脚本并捕获 exit code、stdout、stderr、耗时。
- [x] 每次执行产生独立 revision。
- [x] 输出路径按 record/workspace 布局保存；M0 执行器以 workspace 为 cwd 并只汇总 workspace 内约定 artifact。
- [x] 失败时保留足够日志用于下一轮 repair。
- [x] M0 不新增项目级 CAD operation API；默认脚本使用占位逻辑。

建议验收命令：

```powershell
python -m brep2code.cli run --record demo
```

验收时至少检查：

- `data/records/demo/record.json` 存在。
- `data/records/demo/revisions/<rev_id>/workspace/build_sequence.py` 存在。
- 当前 revision 保存 stdout、stderr、exit code 和耗时摘要。
- 脚本失败时仍保留 revision 和 trace。

已验证：

```powershell
python -m brep2code.cli run --record demo
python -m pytest
```

## Out of scope

- LLM API 调用。
- B-Rep probe tools。
- CAD 几何 gate。
- 固定 IR 或专用 SDK。
- 建模序列 DSL / schema。
