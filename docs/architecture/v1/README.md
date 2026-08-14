---
type: design
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - design
---

# Brep2Code v1 — Harness-first 入口

本目录记录 Brep2Code 第一版的最小实现思路：优先搭建 Harness，使通用大模型可以按需 probe B-Rep、编写 CAD 脚本、执行、接收结构化反馈并迭代修复。

v1 不追求提前收敛 B-Rep 编码器、固定 IR、专用 CAD workplace 或本地模型路线。相关文献和路线讨论保留在论文库，后续按案例需要再查阅。

## 目标

- **输入：** B-Rep（STP / IGES / `.brep`）
- **输出：** CAD 脚本 + STEP/B-Rep 结果 + trace / feedback
- **闭环：** probe → author script → execute → gate → repair

## 非目标（v1）

- 不做本地模型部署、训练或微调。
- 不提前指定最终 IR 或 CAD workplace。
- 不做大而全的 B-Rep 编码器；优先提供 LLM 可调用的 probe tools。
- 不在本仓复制论文路线细节。

## 笔记地图

| 路径 | 内容 |
|------|------|
| [architecture.md](architecture.md) | 总架构与数据流 |
| [decisions.md](decisions.md) | 当前 v1 决策 |
| [m7-evaluation-roadmap.md](m7-evaluation-roadmap.md) | M7 可靠性、首轮生成与分层 corpus 的证据路线 |
| [post-m9-evidence-gated-roadmap.md](post-m9-evidence-gated-roadmap.md) | M10 外部证据、累计归因与修复路由 |
| [m10-external-attribution-ledger.md](m10-external-attribution-ledger.md) | 已完成外部案例的跨批次归因台账 |
| [modeling-knowledge-system.md](modeling-knowledge-system.md) | 案例证据、建模知识单元与 coverage matrix 的权威边界 |
| [knowledge-base-architecture.md](knowledge-base-architecture.md) | 以 Q01--Q04 决策闭环组织知识与案例证据角色 |
| [project-theory-map.md](project-theory-map.md) | 从受限建模假设进入理论、系统、证据资产与当前任务的导航地图 |
| [modeling-knowledge-adoption.md](modeling-knowledge-adoption.md) | 从案例知识到 LLM 参考、分析、Harness/IR/SDK 提议的证据门槛 |
| [current-project-route.md](current-project-route.md) | 当前项目统一口径：真实 LLM hosted 闭环主线及 repair、案例、经验投影支撑路线 |
| [current-hosted-evaluation-framing.md](current-hosted-evaluation-framing.md) | 现阶段 hosted 评测的统一口径：有限案例、有限参考、五家族与批量 campaign 边界 |
| [current-hosted-batch-candidate-plan.md](current-hosted-batch-candidate-plan.md) | 现阶段 batch hosted 候选序列：哪些 family 还要补离线证据、哪些只差 campaign freeze |
| [five-family-hosted-capability-roadmap.md](five-family-hosted-capability-roadmap.md) | 五类建模机制的离线证据、hosted 准备度与逐族 campaign 路由 |
| [`../runbooks/hosted-campaign-charter-template.md`](../runbooks/hosted-campaign-charter-template.md) | 具体 hosted campaign 的冻结字段模板：bounded question、scope、preflight、authorization 与 interpretation |
| `contracts/` | build script、probe tools、signal bundle |
| `runtime-boundaries.md` | Harness runtime workspace、LLM 可调用材料与 `docs/` 的边界 |
| `q01-brep-probes/` | Probe-first B-Rep 访问 |
| `q02-script-authoring/` | Script-first CAD authoring |
| `q03-harness/` | Harness、执行、门控、工具空间 |
| `q04-repair/` | 反馈修复闭环 |
| `modules/` | 计划源码目录 |
| `milestones/` | Harness-first 交付顺序 |

## 关联笔记

- 论文库项目 hub：`D:\paper\Projects\Brep2Code.md`
- v1 备选思路：`D:\paper\Projects\Brep2Code-research\routes\q01-q04-synthesis.md`
- Articraft 参考：`D:\paper\Literature\zhouArticraftAgenticSystem2026.md`

