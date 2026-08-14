# 模块文档索引

本目录维护模块文档和代码路径的对照。模块文档负责说明边界、入口、依赖和验收点；具体实现细节以代码为准。

## 模块对照

| 模块 | 计划代码路径 | 职责 | 相关架构文档 |
|------|--------------|------|--------------|
| Harness / Agent | `brep2code/agent/` ([module](harness.md)) | 组织 record、工具调用、脚本执行、provider 边界、trace、反馈修复循环 | `docs/architecture/v1/q03-harness/harness-overview.md` |
| Storage | `brep2code/storage/` ([module](storage.md)) | records、revisions、runtime workspace、trace、artifact 路径管理 | `docs/architecture/v1/modules/README.md` |
| B-Rep | `brep2code/brep/` ([module](brep.md)) | 输入读入、实体索引、probe tools 后端 | `docs/architecture/v1/contracts/probe-tools.md` |
| CAD | `brep2code/cad/` ([module](cad.md)) | 执行 `build_sequence.py`、调用 CAD backend、导出模型 | `docs/architecture/v1/contracts/build-script.md` |
| Eval | 由 `brep2code/agent/harness.py` 内当前 gates 承载；独立 `brep2code/eval/` 暂缓 | validity、bbox、volume、topology count 等 gates | `docs/architecture/v1/q03-harness/geometry-gate.md` |
| Corpus | `brep2code/corpus/` ([module](corpus.md)) | case manifest、批量 Harness 运行、compact report | `docs/architecture/v1/contracts/case-corpus.md` |
| CLI | `brep2code/cli/` ([module](cli.md)) | `run`、`probe`、`repair`、`corpus` | `docs/architecture/v1/modules/README.md` |

## 模块文档约定

每个模块文档应回答：

- 这个模块拥有什么职责。
- 不拥有什么职责。
- 对外入口是什么。
- 读写哪些 runtime 路径。
- 给 Harness 或 LLM tool 暴露哪些稳定契约。
- 对应 workpack 和验收方式是什么。

## 与代码 README 的关系

- `docs/modules/README.md` 是开发 agent 查找“模块文档 ↔ 计划代码路径”的稳定入口。
- `docs/architecture/v1/modules/README.md` 是 v1 架构内的规划视图，负责解释当前版本的数据布局和命令草案。
- `docs/modules/*.md` 记录稳定边界和跨模块关系。
- 代码目录内的 `README.md` 记录本模块当前入口、运行方式和局部约定。
- 若两者冲突，以代码和最近 handoff 为准，并更新文档。
