# 流水线索引（Q01–Q04）

本文件维护当前 v1 的实现阶段。文献依据与路线综述以论文库为准；本仓只保留当前实现需要的最小路线。

当前研究结论：[`D:\paper\Projects\Brep2Code-research\outputs\literature-synthesis-and-validation-handoff.md`](D:\paper\Projects\Brep2Code-research\outputs\literature-synthesis-and-validation-handoff.md)。四组问题地图由该页链接；[`q01-q04-synthesis.md`](D:\paper\Projects\Brep2Code-research\routes\q01-q04-synthesis.md) 仅保留为历史路线比较。

## 流程

```mermaid
flowchart LR
  Q01["Q01 B-Rep按需探查"] --> Q02["Q02 CAD脚本生成"]
  Q02 --> Q03["Q03 Harness执行/门控"]
  Q03 --> Q04["Q04 反馈修复"]
  Q04 -->|"回到Q02"| Q02
```

## 阶段索引

M4 Case Corpus Review、M5 Runtime Sandbox Foundation 和 M3-004 DeepSeek V4 hosted provider integration 已完成。动态状态以 [`docs/workflow/status.md`](../workflow/status.md) 为准。

| 阶段 | 简述 | 论文 Q&A 锚点 | 本仓实现状态 |
|------|------|---------------|--------------|
| **Q01** | LLM 通过 probe tools 按需查询 B-Rep，不预先训练/编码 | [第 1 组：可观察性与歧义](D:\paper\Projects\Brep2Code-research\routes\q01-feature-recognition-evidence-boundaries.md) | M1 done |
| **Q02** | 通用 LLM 在受限 workspace 编写 CAD 脚本；IR 暂缓收敛 | [第 2 组：操作依赖与可编辑性](D:\paper\Projects\Brep2Code-research\routes\q02-operation-dependency-evidence-boundaries.md) | M2 done；M3 required loop done |
| **Q03** | Harness 执行脚本、导出结果、收集日志、运行基础门控和几何对比 | [第 3 组：模型分类与数据证据](D:\paper\Projects\Brep2Code-research\routes\model-taxonomy-and-dataset-evidence-map.md) | M2 done |
| **Q04** | 将结构化失败信号返回 LLM，迭代修改脚本 | [第 4 组：LLM 参考案例采用门槛](D:\paper\Projects\Brep2Code-research\routes\llm-reference-case-adoption-thresholds.md) | M3 required loop done |

M3 拆分为 provider/trace、tool-calling bridge、repair-loop runner 三个必需 workpack；真实 hosted provider 接入作为可选收尾 workpack。M3-001 到 M3-003 已完成，Harness 本体闭环已具备本地 fake-provider 验证路径。M48 已实现路径无关的 Q01 observation 与无原始 STEP 的 opt-in Q02 build capability；将它接入 provider 的闭环顺序见 [`post-m48-closed-loop-roadmap.md`](v1/post-m48-closed-loop-roadmap.md)。

M4 的 P0/P1 review 已确认当前失败均可由本地 replacement scripts 修复，尚不支持引入 IR、SDK 或 CAD workplace；详见 [`docs/architecture/v1/m4-review-report.md`](v1/m4-review-report.md)。M5 先实现运行时隔离，防止 provider-generated Python 读取开发治理材料或宿主机能力。

M9 之后的实现侧升级遵循[证据驱动路线图](v1/post-m9-evidence-gated-roadmap.md)：只有固定 split 的两个 M9 hosted report 均完成后，才审查并选择 geometry diagnostics、外部案例增量或窄 helper。IR 仅可作为后续 shadow experiment，CAD SDK 必须另行 ADR；这一路线不改变 Q01--Q04 的当前实现状态，也不授权 hosted 请求。

## 参考范式

Articraft 启发：LLM 在受限 workspace 中迭代编辑代码，harness 负责工具调用、执行、导出与结构化验证反馈。Brep2Code v1 借鉴其闭环，而不是先复制完整 SDK/IR。

- 论文项目笔记：[`D:\paper\Projects\Brep2Code.md`](D:\paper\Projects\Brep2Code.md)
- 计划代码栈（论文库记录）：Python 3.12 + uv + just

## 更新约定

- 论文库 Q&A 状态变更时，仅更新上表「本仓实现状态」列（若本仓有对应模块）
- 不在此文件复制 Q&A 回答正文



