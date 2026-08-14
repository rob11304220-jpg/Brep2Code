# 案例证据、建模机制与多轴难度报告 v1

- **状态**：reviewed development-side report（M145）
- **范围**：87 个 active self-authored cases，以及其已审查的 knowledge、decision
  与 admission evidence；不读取 STEP、reference script 或 held-out fixture。
- **用途**：帮助选择下一个有信息增益的决策缺口；不是案例注册表、manifest、
  runtime resource、训练集或 hosted 授权。

## 结论

案例的“难度”不能由 P0--P3 tier、几何复杂度或案例数量单独表达。项目当前最有
用的描述是一个六轴画像：**建模机制、实体引用稳定性、序列依赖、参数/split、证据
成熟度、准入风险**。同一几何可以在一个轴上简单、另一个轴上高风险：双 boss 的
形状简单，却因候选实体不唯一而必须 fail-closed；有多个操作的 family 若冻结了
grammar、replay、gate 和 split，则可拥有可审查但仍不自动准入的证据。

M143 的 admission profile 只回答“现有证据可以支持什么准入处置”，不构成一般
难度排名。coverage matrix 则回答“哪一个 Q01--Q04 决策缺口最值得做”，不以案例
数、feature 名或难度 tier 为进度指标。

## 六轴词汇

| 轴 | 低风险端 | 高风险端 | 需要避免的误读 |
|---|---|---|---|
| 建模机制 | primitive、固定单切除 | 多轮廓、join 后依赖切除、pattern、revolve、未来 shell/rib | 几何复杂不自动等于可重建历史 |
| 实体引用稳定性 | 不依赖选择器，或 declared predicate 唯一候选 | 对称/多候选、edge reference、拓扑命名、任意 frame | 不可用坐标/枚举偷偷打破歧义 |
| 序列依赖 | base 后独立操作 | profile/feature 消费上游实体、verified prefix、选择器依赖 | replay 不证明唯一逆序列 |
| 参数与 split | 单例或未声明 split | 冻结 development/held-out family、方向/尺寸 mutation | 参数变体不等于 arbitrary robustness |
| 证据成熟度 | fixture + baseline | family replay/gates/mutations、negative controls、hash-bound admission record | evidence level 不等于 runtime eligibility |
| 准入风险 | 仅在精确 scope 内 predicate 可审计 | unknown、缺证据、歧义、需要独立 oracle | profile 不改变 lifecycle 或 runtime 权限 |

## 当前组合：按设计意图和机制

| 设计意图 / 机制 | 主要回答的建模问题 | 代表资产或知识单元 | 引用与依赖难点 | 当前证据与准入处置 | 主要缺口 |
|---|---|---|---|---|---|
| 基础 primitive 与布尔构造 | Harness 是否能安全处理基础 B-Rep 与固定构造 | P0/P1 reference-pack ladder（7）；早期 P2/P3 ladder（14） | 多数无明确 sequence dependency claim | 30 项 `baseline_or_unpaired`，`needs_evidence` | Q01/Q02/Q03 受限假设、反例与停止规则 |
| 早期参数特征 | 单特征尺寸变化是否维持 fixture/replay 基线 | additive boss、through/blind hole、counterbore、fillet、chamfer 等 21 | 通常无 admission-record 级实体引用声明 | 多数 baseline/参数证据；不自动变为 runtime 卡 | 不能将尺寸变化当作通用鲁棒性或 editability oracle |
| Prismatic cylindrical cut 观察 | 能否仅从受限 B-Rep 事实区分 blind/through | `blind-through-cylindrical-extent-v1` | +Z 单圆柱、两个 terminal planar faces、footprint 条件 | `supported` observable；其他数量/方向 fail-closed | 任意方向、多圆柱/counterbore、通用 feature label |
| Nested-cylinder/shoulder 观察 | 能否报告同轴双圆柱与共享平面肩关系 | `nested-cylindrical-shoulder-v1`、`axis-relative-nested-cylinder-v1` | cylinder count、同轴性、半径顺序、轴相对 frame | `supported`，+Y 仅一个 temporary control | arbitrary orientation、history/feature label |
| Rounded-slot / orientation | 固定圆角槽轮廓、+X/+Y 局部轴的 sequence 关系 | `rounded-slot-v1`、`oriented-rounded-slot-v1`；各 6 family rows | declared base support、固定 orientation/轮廓 | family-scoped sequence，`needs_evidence` | 任意 frame、arcs/splines beyond grammar、runtime selection |
| Multi-contour / multi-inner-loop pocket | 内外轮廓、一个/两个岛的切除语义 | `multi-contour-pocket-v1`、`multi-inner-loop-pocket-v1`；各 6 | loop role、profile-to-cut dependency | family-scoped sequence，`needs_evidence` | generic inner-profile pocket、任意轮廓/拓扑 |
| Additive boss dependent cut | 上游 join boss 如何成为下游 blind cut 目标 | `additive-boss-dependent-cut-v1`；6 | boss-to-cut dependency；M31 的 verified prefix/suffix | family-scoped sequence；rollback 仅受限 execution evidence | generic repair、自动 rollback、任意 prefix/suffix |
| Unique planar selector | 何时可将 face selector 绑定到下游 cut | `face-selected-dependent-cut-v1`；6；M142 record | planar +Z maximum-Z predicate 必须恰好一候选 | 精确 M142 scope 的 `admit`，但仍非 runtime authority | rotated/multiple features、edge refs、persistent naming |
| Selector ambiguity counterexample | 多候选时是否可安全继续 | twin-boss experimental controls；M142 record | cardinality=2，禁止依赖操作与 coordinate tie-break | `fail_closed`；不计入 active library profile 数 | 不可“修复”为 choose-first 或坐标选择 |
| Repeated feature pattern | 固定 2×2 四等径通孔如何表达 | `repeated-feature-pattern-v1`；6 | grid cardinality、spacing、共同半径、profile-to-cut | family-scoped sequence，`needs_evidence` | polar/staggered/变数量、通用 pattern recognition |
| Axisymmetric revolve | 固定阶梯径向全旋转构造 | `revolve-v1`；6 | profile/axis/全旋转约束 | reviewed family evidence，`needs_evidence` | sweep/loft、任意 revolve、runtime adoption |
| 执行可读性 | sandbox 内固定脚本是否能读取输入 | `sandbox-input-path-fixed-script-v1` | /input/model.step 映射；与几何成功分离 | `direct` execution boundary | generic generated-script helper 或 geometry repair |
| 独立 editability | 静态 match 后是否保持设计关系 | `q03-editability-oracle-v1` | 需要独立 history/constraint oracle 和 post-edit invariant | `deferred`，不是现有 script mutation 可替代 | 可许可、可重放的独立 constraint oracle |
| Complex topology | single-solid 之外的 shell/rib 等是否可处理 | coverage matrix 的 complex-topology cell | topology、接触/多实体与操作语义耦合 | 尚无 admission disposition | 新 family 先冻结 Q01/Q02 hypothesis、反例与 stop rule |

## M143 准入成熟度快照

| Admission profile | 数量 | 机制/证据含义 | 默认处置 |
|---|---:|---|---|
| `baseline_or_unpaired` | 30 | primitive、ladder 或参数资产；无 scoped `sequence_pair` metadata | `needs_evidence` |
| `family_scoped_sequence` | 51 | 有冻结 grammar、declared split、family replay/gate/mutation evidence | `needs_evidence` |
| `unique_planar_selector` | 6 | face-selected dependent cut；唯一 planar +Z max-Z 候选 | M142 精确范围 `admit` |
| `selector_ambiguity_counterexample` | 不计 active library | twin-boss 多候选的 documentary/discriminating evidence | `fail_closed` |

该 87 行 active inventory 的 split metadata 是 development 36、held_out 30、
undeclared 21。该统计描述资产元数据，不能据此推断一次 held-out execution、训练
划分可用性或 hosted 范围。

## 难度与证据的典型对照

| 情形 | 几何/操作直觉 | 实际最关键的难度 | 正确项目表述 |
|---|---|---|---|
| 单圆柱 primitive | 简单 | 主要是 fixture/replay 与 runtime 边界，不是 history 反演 | baseline 或 narrowly evidenced primitive role |
| 四孔 2×2 grid | 中等 | cardinality/layout/共同参数与 sequence grammar | fixed rectangular-grid pattern；非 generic pattern recognition |
| boss + blind cut | 中等 | 上游实体到下游操作的依赖 | frozen boss-to-cut sequence；非任意 feature history |
| unique boss-top selector | 几何仍简单 | entity binding 的唯一性 | cardinality=1 才能 bind，精确 M142 scope 可 admit |
| twin boss | 几何简单 | 对称导致实体引用不唯一 | cardinality=2，`FailClosedAmbiguous`，无下游操作 |
| rotated rounded slot | 操作相似 | 局部 frame/方向的可迁移性 | 仅 +X/+Y frozen axes；非 arbitrary orientation |
| shell/rib | 几何/拓扑更复杂 | topology 与建模语义均未有独立受限假设 | uncovered complex-topology decision gap |

## 当前“表述”在哪里维护

| 表述类型 | 权威位置 | 维护原则 |
|---|---|---|
| case identity、lifecycle、hash、split、baseline、script declaration | `case-library/self-authored/<case_id>/case.json`；`docs/corpus/registry/self-authored.json` | `case.json` 为单例权威；registry 是指针/index |
| 人工可读的案例意图与准备度导航 | [case-portfolio.md](case-portfolio.md)、`docs/corpus/cases/` | 导航不能提升 lifecycle/manifest/runtime 权限 |
| Q01 可观测量和歧义 | `docs/corpus/knowledge/observables/` | 记录可测事实与 fail-closed 条件，不命名不可见历史 |
| Q02 操作、内核调用、参数边界与依赖 | `docs/corpus/knowledge/operations/` | 每个 unit 仅覆盖 frozen grammar 与明确 unsupported conditions |
| Q03/Q04 gate、diagnostic、repair | `docs/corpus/knowledge/execution/` 与 decision packages | execution boundary 不等同于 generic repair/helper |
| 证据缺口、下一最小实验与 unlock condition | [coverage-matrix.json](knowledge/coverage-matrix.json) | 以决策 gap，不以数量、feature 名或难度 tier 规划 |
| 决策问题、证据角色、反例、停止规则 | `docs/corpus/knowledge/decisions/` | planned/reviewed/deferred 不授予实现或 runtime 权限 |
| immutable admission evidence 与跨库 profile | `docs/corpus/knowledge/admissions/` | evidence-only；profile 不可自动 admission/promotion |
| 跨层语义和权限边界 | [knowledge-base-architecture.md](../architecture/v1/knowledge-base-architecture.md) | A--D 知识层与 runtime adoption 分离 |

## 当前分散性的具体问题

当前材料的**权威边界是正确的**，但读者若要回答“某机制为什么难、已有何种证据、
还缺什么、是否可准入”，必须跨读至少五类材料。这带来三类可改进性：

1. `case.json` 可表达资产事实，却不表达机制画像或证据角色的总览；
2. operation/observable units 有精确机制边界，却不汇总到 portfolio 的人类导航；
3. coverage matrix 有决策缺口，却不直接展示 profile、admission record 与资产族之间的
   可读 crosswalk。

这些不是修改某一个 registry 的理由；任何收敛都必须保持已有 source-of-truth 与
runtime boundaries。

## 建议的后续路线（未激活）

M145 后可由用户选择 `WP-TRG-030`，设计一个统一的**development-side evidence
architecture**：以稳定 ID 和 source links 生成/维护 crosswalk，统一展示上述六轴，
但不替代 `case.json`、registry、operation unit、decision package、coverage matrix 或
admission record 的权威性。该后续工作需要独立确定 schema、更新责任、drift audit、
迁移策略及其对已有文档的最小改动；它不包含 runtime projection。

## Sources

- [M143 admission profile](knowledge/admissions/case-library-admission-profile-v1.json)
- [Case portfolio](case-portfolio.md)
- [Coverage matrix](knowledge/coverage-matrix.json)
- [Knowledge-base architecture](../architecture/v1/knowledge-base-architecture.md)
- [Modeling knowledge system](../architecture/v1/modeling-knowledge-system.md)
- [M142 admission record](knowledge/admissions/selector-ambiguity-v1.json)
