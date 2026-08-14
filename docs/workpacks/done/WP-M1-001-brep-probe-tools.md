# WP-M1-001: B-Rep Probe Tools

- Status: done
- Milestone: M1
- Owner: unassigned

## Goal

实现最小 B-Rep 输入读取与 probe tools，使 Harness 能从 record 输入读取 STEP/B-Rep 样例，并以受限大小 JSON 返回 LLM 可调用的几何/拓扑查询结果。

## Scope

- 建立 `brep2code/brep/` 模块边界。
- 定义并实现最小输入发现逻辑：从 `data/records/<record_id>/input/` 选择单个 CAD 输入文件。
- 优先支持 STEP smoke fixtures；IGES / `.brep` 可以先保留扩展点。
- 实现 `probe_summary`、`probe_topology`、`probe_entity`、`sample_entity` 的最小可测接口。
- 对 tool result 设置大小上限；超过上限时写入 revision trace 或 record-level trace，并返回摘要和路径。
- 新增 CLI 调试入口，用于本地验证 probe tools。
- 新增小型 STEP fixtures 或 fixture 生成/获取说明，优先启用 P0 输入来源。

## Inputs

- `AGENTS.md`
- `docs/handoff/active/2026-07-10-agent-framework-init.md`
- `docs/workflow/README.md`
- `docs/architecture/v1/contracts/probe-tools.md`
- `docs/architecture/v1/q01-brep-probes/README.md`
- `docs/architecture/v1/modules/brep/README.md`
- `docs/links/brep-input-sources.md`

## Code paths

| Path | Purpose |
|------|---------|
| `brep2code/brep/` | B-Rep 读入、实体索引、probe backend |
| `brep2code/cli/` | `probe` 调试命令 |
| `brep2code/storage/` | record input 与 trace 路径复用 |
| `case-library/self-authored/` | 小型 STEP fixture |
| `tests/` | probe tools 单元测试 / smoke tests |
| `data/records/<record_id>/input/` | 本地 record 输入，不提交 |

## Planned CLI

命令名可在实现时微调，但必须在 README 或 CLI help 中可发现：

```powershell
python -m brep2code.cli probe --record box-smoke
python -m brep2code.cli probe --input case-library\self-authored\box\input.step
python -m brep2code.cli run --record box-smoke --input case-library\self-authored\box\input.step
```

## Probe contract

| Tool | Minimum result |
|------|----------------|
| `probe_summary(record_id)` | 文件名、格式、单位或 unknown、bbox、solid/shell/face/edge 计数、体积/面积摘要或 unknown |
| `probe_topology(record_id, selector)` | solid/shell/face/edge 层级摘要，支持分页或限制数量 |
| `probe_entity(record_id, entity_id)` | entity 类型、bbox、参数范围、面积/长度、相邻 entity 摘要 |
| `sample_entity(record_id, entity_id, n)` | face 点/法向或 edge 点/切向采样；`n` 有上限 |

## Data source policy

当前 workpack 只启用 P0 自制 STEP smoke fixtures。ABC Dataset、Fusion 360 Gallery、DeepCAD、Thingi10K 只作为后续输入池记录在 `docs/links/brep-input-sources.md`，本 workpack 不下载、不提交、不依赖。

## Docs to update

- `docs/modules/README.md`
- 新增或更新 `docs/modules/brep.md`
- `docs/workflow/README.md`
- `docs/architecture/pipeline.md`
- `README.md`
- `docs/handoff/active/`

## Acceptance

- [x] `brep2code/brep/` 模块存在，模块边界与 docs 对齐。
- [x] 可以从 record input 或显式 `--input` 读取一个 STEP smoke fixture。
- [x] `probe_summary` 对 smoke fixture 返回结构化 JSON，不抛原始栈给调用方。
- [x] `probe_topology`、`probe_entity`、`sample_entity` 对至少一个 face/edge 可用。
- [x] entity id 在同一 record / 同一输入文件内稳定。
- [x] tool result 有大小上限；大结果落 trace，返回摘要和 trace path。
- [x] CLI probe 命令可手动运行。
- [x] 测试覆盖成功读取、缺失输入、非法 entity、result size limit。
- [x] 不引入项目级 CAD modeling SDK、固定 IR 或 B-Rep tensor/schema。

建议验收命令：

```powershell
python -m brep2code.cli probe --input case-library\self-authored\box\input.step
python -m pytest
```

已验证：

```powershell
python -m brep2code.cli probe --input case-library\self-authored\box\input.step
python -m pytest
python -m py_compile brep2code\brep\__init__.py brep2code\brep\readin.py brep2code\brep\serialize.py brep2code\brep\probes.py brep2code\cli\__init__.py brep2code\agent\harness.py
```

Lint 状态：当前 Python 环境未安装 `ruff`，`python -m ruff check .` 无法运行。

## Out of scope

- 下载或整理 ABC / Fusion 360 / DeepCAD / Thingi10K 全量数据。
- LLM API 调用。
- CAD 脚本生成质量优化。
- geometry gate / mesh distance。
- 固定 IR、建模序列 DSL 或专用 B-Rep 编码器。

## Notes

- CAD/B-Rep 后端应按 M1 最小 probe 能力选择，不以训练或全量数据处理为目标。
- 若后端依赖较重，优先把依赖选择和安装步骤记录清楚，再进入实现。