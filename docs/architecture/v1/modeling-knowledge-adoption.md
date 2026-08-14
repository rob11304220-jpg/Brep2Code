---
type: design
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - modeling-knowledge
  - harness
  - evidence-gated
---

# 从案例知识到 Harness 采用的门槛

## 目的

本页是已治理案例的长期设计入口。它说明开发 Agent 可以怎样使用
`docs/corpus/knowledge/` 中经过评审的建模知识，以及 LLM 参考序列、性质
分析、Harness helper、IR 或 SDK 在何种证据下才可被单独提议。

它不改变 Harness、可执行 manifest、provider、训练数据、runtime prompt 或
runtime resource。案例资产、知识单元与运行时材料的权威边界仍分别由
`case.json`、知识系统和 Harness 控制。

## 证据流

```text
governed case + deterministic replay + family audit
  -> reviewed knowledge unit + coverage matrix
  -> separately reviewed runtime-card experiment
  -> separately selected Harness helper / IR / SDK proposal
```

每一步都是新的决策门；上一步的通过不自动授权下一步。

## 可使用范围与提升门槛

| 目标用途 | 现在可做什么 | 还需要什么 | 明确不能推断 |
|---|---|---|---|
| 开发侧建模参考 | 开发 Agent 可查阅 reviewed unit，设计离线案例、审阅 reference sequence、定位 coverage gap。 | 维持 case/ADR/audit 链接和 `supported` 边界。 | 该序列是 B-Rep 的唯一逆，也不是运行时 prompt。 |
| LLM 建模序列参考 | 将 unit 作为未来 compact card 的候选来源。 | 符合 ADR-0016：同一机制至少三例独立 `direct` runtime evidence，随后通过 M19-002 的离线 retrieval 评测和单独设计评审。 | `supported` deterministic oracle 不能直接注入 LLM。 |
| 性质/拓扑分析 | 用 unit 的 observables、invariants 和 counterexamples 设计新的离线 probe 或 gate 假设。 | 新 workpack 必须说明可观测信号、误报/漏报风险、反例、停止条件与回归验证。 | 现有实例不证明通用 feature recognition。 |
| Harness helper | 将重复出现且有 trace 支持的诊断或安全操作列为候选。 | 跨案例直接归因、最小接口设计、offline regression、独立 workpack/ADR；helper 必须保持 operation-agnostic，除非边界另行获批。 | 案例 reference script 不是 Harness API。 |
| IR、建模 DSL 或 SDK | 用知识单元比较稳定的步骤/依赖结构，形成候选需求。 | 多个家族、成功与失败脚本的重复结构证据；明确替代方案、迁移和 gate/repair 收益；独立 workpack、ADR 与无回归验证。 | 冻结 sequence-pair grammar 不是通用 IR 或 SDK 设计。 |
| manifest、provider、训练或 runtime 行为 | 无自动权限。 | 各自既有的专项 workpack、离线 preflight 与明确授权。 | active case 或 reviewed unit 不构成数据、预算或出境授权。 |

## 当前已知边界

当前知识单元只描述自建、确定性、家族限定的 oracle：孔、圆角槽、单/双
inner-island pocket、boss-dependent cut、唯一 boss-top selector，以及 +X/+Y
axis-aligned rounded slot。它们适合成为后续假设的可审计来源；尚不支持通用
B-Rep-to-sequence recovery、任意方向/轮廓、topological naming、CAD kernel API
目录或运行时检索。

## 维护规则

- 新 family 的 review 必须更新 coverage matrix，并增加/修订知识单元，或明确
  记录无可复用知识。
- 知识单元只链接 case metadata、preregistration、ADR、review 和 audit；不得
  复制完整 workpack、ignored trace 或 provider 内容。
- 对任何 runtime、helper、IR 或 SDK 的提议，必须回链到具体 unit 和反例，并
  新建独立 workpack；该提议不能改写 unit 的证据等级。

## Links

- [Modeling knowledge system](modeling-knowledge-system.md)
- [Runtime boundaries](runtime-boundaries.md)
- [Runtime guidance cards runbook](../../runbooks/runtime-guidance-cards.md)
- [Modeling knowledge maintenance](../../runbooks/modeling-knowledge-maintenance.md)
- [ADR-0034](../adr/0034-modeling-knowledge-adoption-boundaries.md)
