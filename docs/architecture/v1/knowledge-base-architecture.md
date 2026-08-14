---
type: architecture
related-project: Brep2Code
status: active
---

# 面向 Harness 闭环的知识库架构

## 结论

本项目的知识库不是论文仓、案例清单、训练集，也不是直接塞入 prompt 的
“CAD 常识”。它是 **Harness 的开发侧、可追溯决策底座**：把可观测的 B-Rep
证据，约束为可执行且可验证的建模假设，并记录何时应停止、诊断或修复。

它首先服务 Q01--Q04 的闭环：

```text
Q01 观察 B-Rep  ->  候选建模假设  ->  Q02 生成脚本
       ^                                      |
       |                                      v
Q04 失败归因/受限修复  <-  Q03 执行、比较与门控
```

案例是这个系统的**证据、回归和评测资产**，不是知识库的组织主轴；“增加案例数”
本身不是进展。只有当一个案例能减少上述某一步的不确定性、区分相互竞争的假设，
或覆盖已知失效边界时，它才值得进入案例库。

## 非目标

- 不主张从最终 B-Rep 恢复唯一、真实或通用的原始 CAD 历史。
- 不以覆盖所有 CAD 特征、所有数据集或所有内核 API 为目标。
- 不把 reference script、外部数据或 provider trace 自动变为 LLM 上下文、训练数据
  或 Harness 行为。
- 不因某个 family 通过 replay 就引入 IR、SDK、helper 或运行时检索。

## 四层知识模型

| 层 | 回答的问题 | 权威材料 | 允许的产物 | 不允许推断 |
|---|---|---|---|---|
| A. 观察与词汇 | 从 B-Rep **实际可见**什么？ | probe schema、B-Rep/STEP facts、单位/坐标约定 | observable profile、测量定义、歧义 | 不可见的历史、feature 名称或拓扑命名 |
| B. 建模假设与操作契约 | 哪个受限序列可产生/解释这些观察？ | reviewed knowledge unit、operation contract | 前置条件、参数域、序列、预期 B-Rep delta、反例 | 唯一逆解或通用 kernel API |
| C. Harness 执行知识 | 如何安全执行、比较并判定该假设？ | tool contracts、sandbox policy、gate/repair taxonomy | 工具调用边界、gate、失败签名、停止规则 | feature-specific helper 自动生产化 |
| D. 证据与评测 | 凭什么相信边界内有效、边界外未知？ | case metadata、manifest、audit、review、报告 | evidence link、split、counterexample、coverage gap | 训练语料、质量基准或 runtime 授权 |

其中 A--C 是可复用的“知识”；D 是它们的证据链。一个知识条目必须能从
`D -> A/B/C` 回溯，也必须从 A/B/C 指回所需的 D；不能只保存结论。

## 物理组织与权威边界

保持现有文件不搬迁、不改变 runtime；以如下逻辑目录作为后续整理准则：

```text
docs/
  architecture/v1/                 # 系统边界、采用门槛和 ADR 链接
  corpus/
    knowledge/
      observables/                 # A：B-Rep 可观测量、术语与歧义边界（待建立）
      operations/                  # B：受限操作/序列假设（现有 units）
      execution/                   # C：可复用的 gate、diagnostic、repair knowledge（待建立）
      patterns/                    # 跨层的失败边界、反例与不支持结论
      coverage-matrix.json         # D：能力假设，而非案例数量仪表盘
      templates/                   # 各层 schema/template
    cases/                          # 人工 case cards；解释单个资产
    library/ registry/ external/    # D：资产生命周期、来源和准入
case-library/                       # 物理 B-Rep、reference sequence、显式 executable manifests
runtime_resources/                  # 仅经独立评审后的受限运行时投影
```

`case.json`、registry 和 manifest 的权威性保持不变。`docs/corpus/knowledge/` 是
开发侧索引，不能提升 case、改变 manifest 或改变 Harness。`runtime_resources/` 只能
保存从知识条目压缩出的、单独验证过的投影。

## 当前迁移状态

| 层 | 已回填内容 | 仍缺内容 |
|---|---|---|
| A 观察 | `planar-face-selector-cardinality-v1` 已验证 unique/ambiguous fail-closed 边界 | blind/through 等其余 Q01 观察仍未形成 reviewed unit |
| B 操作 | 七个 self-authored family-scoped operation units | 仅支持冻结 grammar，不支持通用 history/recovery |
| C 执行 | M10 fixed-script sandbox-path compatibility boundary | 局部几何反馈、rollback 与通用 repair knowledge 尚未验证 |
| D 证据 | sequence-pair、外部边界和 legacy disposition index | 早期 capability-ladder assets 仍待按具体决策审计 |

经验卡通过 disposition index 回链到其来源知识或迁移例外；这种可追溯性不改变
它们的 experimental 状态或运行时采用门槛。

## 条目的最小契约

每个可复用条目以一个**决策问题**为中心，而不是以某个案例或论文为中心：

1. 问题与适用阶段：Q01 观察、Q02 生成、Q03 gate，或 Q04 repair。
2. 输入观察：需要哪些可测的实体、几何、拓扑、单位和坐标事实；哪些歧义会拒绝。
3. 受限动作：候选序列/工具调用/诊断及其前置条件、参数边界和预期结果。
4. 验证：所用 gate、可观测成功标准、失败签名与 stop condition。
5. 证据：正例、负例、split、review/audit 链接和证据等级。
6. 边界：已知不支持内容、替代假设，以及是否允许被提议为 runtime 投影。

`operation_contract` 是 B 层的一个具体形式；它不应兼任 A 层 feature
recognition 定义、C 层工具 API 或 D 层案例目录。

## 案例在体系中的位置

案例按**证据角色**而非难度或覆盖数量来选择和标记：

| 角色 | 应解决的决策 | 典型资产 | 是否默认进入 manifest |
|---|---|---|---|
| oracle | 验证一个冻结的序列假设可重放 | self-authored reference case | 否；需专项选择 |
| discriminating | 区分两个候选建模/诊断假设 | 参数、方向或依赖对照 | 否 |
| negative control | 证明某个观察/修复不能泛化 | wrong-face、wrong-frame、退化控制 | 否 |
| regression | 防止 tool/gate/repair 改动破坏已知行为 | 显式 manifest case | 仅明确选择后 |
| OOD robustness | 检验输入、sandbox 或 gate 的边界 | ABC B-Rep-only 样本 | 仅明确选择后 |
| native-history validation | 比较 source-history/replay 兼容性 | Fusion 等带来源边界的样本 | 否 |

同一物理案例可以拥有多个角色，但每个角色要在 metadata 或相关 review 中可追溯。
案例数量、P0--P3 tier 和参数数量只能是筛选信息，不能作为能力覆盖或知识强度的
替代指标。

## 以决策缺口驱动，而非案例覆盖驱动

coverage matrix 的一个 cell 应描述：

`决策问题 → 所需观察 → 受限假设 → 验证/反例 → 现有证据 → 下一最小实验`。

选择下一项工作时，先从闭环瓶颈开始：

1. Q01 无法稳定观察/消歧：优先做观察或 probe 的离线证据，而不是增加 feature case。
2. Q02 候选序列空间过大：优先做一个能区分序列/依赖假设的 oracle 或 negative control。
3. Q03 无法区分“脚本不对”和“gate 不足”：优先做 gate 或对照资产。
4. Q04 有重复且直接归因的失败：才提议受限 diagnostic/repair；否则保留 unknown。

一个 workpack 只能选一个具体决策缺口，并在生产前冻结假设、最小证据集、反例和
停止条件。没有新决策价值的“补案例”应保持未选中。

## IR / SDK 的定位

IR 或 SDK 不是知识库的预设交付物，而是 C 层重复性不足时的候选实现：只有当多个
operation units 在成功和失败路径中呈现稳定、可比较的中间概念，且现有脚本/工具
边界妨碍 Q02--Q04 的可审计性时，才可单独提出。提案必须写明它替代的决策、最小
表示、丢失信息、迁移与回归计划；不能从 sequence-pair grammar 直接归纳。

## 采用门槛

开发 Agent 可使用 A--D 层来设计离线实验、审阅序列和定位最小决策缺口。向 LLM
runtime、Harness helper、IR/DSL/SDK、manifest、provider 或 training 的采用，仍按
[`modeling-knowledge-adoption.md`](modeling-knowledge-adoption.md) 的独立证据、设计和授权
门槛执行。
