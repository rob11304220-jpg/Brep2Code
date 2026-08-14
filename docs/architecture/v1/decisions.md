---
type: design
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - decisions
---

# Brep2Code v1 — 当前决策

v1 的目标是尽快得到可运行、可观测、可迭代的 CAD agent harness。路线讨论保留在论文库；本文件只记录会影响实现的当前决策。

## 已接受

| ID | Decision | Consequence |
|----|----------|-------------|
| D01 | Harness-first | 优先实现 workspace、工具调用、脚本执行、门控、trace、repair loop。 |
| D02 | 通用 hosted LLM | v1 不做本地模型部署、训练或微调。 |
| D03 | Probe-first Q01 | LLM 通过 B-Rep probe tools 按需获取信息，不先做统一 B-Rep 编码器。 |
| D04 | Script-first Q02 | LLM 先写可执行 CAD 脚本；固定 IR、SDK 分层、CAD workplace 暂缓。 |
| D05 | 轻量 gates | 先做有效性、bbox、体积、mesh distance 等基础门控；精细指标从案例中补。 |
| D06 | Runtime helper only | 早期只沉淀路径、artifact、trace、log 等 helper，不提供项目级 CAD 建模 API。 |
| D07 | Evidence-bounded knowledge adoption | 已治理案例的长期建模知识仅作为开发侧参考；runtime card、helper、IR/SDK 均须跨过独立证据与评审门槛。 |

## 延后决策

| Topic | Deferred until |
|-------|----------------|
| 固定 modeling IR | 有足够成功/失败脚本可分析重复结构。 |
| CAD workplace | 观察通用脚本编辑是否成为瓶颈。 |
| 专用 SDK | 从高频 CAD 操作和错误类型中提炼。 |
| 建模序列 DSL / schema | case corpus 显示稳定步骤类型，且 gate/repair 需要结构化步骤信号。 |
| B-Rep 表示学习/编码器 | probe-first 明确不足，且有数据资产支持评估。 |
| 本地部署/微调 | hosted LLM 成本、能力或数据闭环证明需要替换。 |

## Links

- [README.md](README.md)
- [architecture.md](architecture.md)
- `D:\paper\Projects\Brep2Code-research\routes\q01-q04-synthesis.md`
