---
type: navigation
related-project: Brep2Code
status: active
---

# 提问路由与权威落点

本页把常见项目提问映射到对应的**权威层**、入口文档、维护落点和禁止推断。
它是提问与文档维护的导航页，不替代 `status.md`、workpack、case authority、
runtime contract、manifest、provider 配置或 hosted 授权。

## 三层权威

| 层 | 回答的问题 | 主要权威 | 允许沉淀 | 不自动获得 |
|---|---|---|---|---|
| 1. 开发侧知识/治理 | 我们已有哪些受限 hypothesis、证据、边界、反例与 adoption boundary？ | M146 crosswalk、knowledge units、case-evidence mapping、ADR、review、audit | 开发侧知识条目、导航、review 结论、长期维护规则 | runtime 行为、manifest 选择、provider/hosted 授权 |
| 2. Runtime/Harness contract | Harness 实际允许观察什么、执行什么、如何 gate/repair、向 LLM 提供什么受限参考？ | `pipeline.md`、Q01--Q04 contracts、tool/schema contract、runtime projection workpack | runtime contract、受限 projection、gate/repair contract | theory 正确性、case lifecycle、hosted 结果解释 |
| 3. Hosted/campaign evaluation | 在固定 campaign、固定出境边界和固定比较臂下，效果如何？ | hosted preflight、campaign charter、terminal report、authorization record | 受限结果解释、对照结论、后续 G3 提议输入 | runtime promotion、广义能力结论、长期数据出境权限 |

## 四类常见提问

| 提问类型 | 先回答什么 | 所属层 | 首先读取 | 最终维护落点 | 不能误推断 |
|---|---|---|---|---|---|
| 1. 项目针对某类建模或内核机制，当前能支持什么“模型到建模序列”能力？ | 哪个 bounded hypothesis 被证据支持、适用于哪些案例/类别、反例与 stop rule 是什么 | 1 | [`../architecture/v1/project-theory-map.md`](../architecture/v1/project-theory-map.md) | M146 crosswalk、knowledge unit、decision package、evidence review | 不能把 development-side support 当成 runtime 支持或 hosted 效果 |
| 2. Harness 的观察、执行、门控、修复闭环本身能把 LLM 推进到什么程度？ | Q01--Q04 contract 实际如何工作、哪些信号会 fail closed、哪些仍是 unknown | 2 | [`../architecture/pipeline.md`](../architecture/pipeline.md) | pipeline/Q01--Q04 contract、module docs、gate/repair knowledge | 不能从闭环设计直接推断该能力已有案例证据或 hosted 成效 |
| 3. 已有案例和知识应该以什么形式提供给 LLM/Harness 才有效？ | 哪些 development-side 知识可被压缩成受限 runtime projection，形式是 card、pack、tool schema 还是别的最小接口 | 1 → 2 | [`../architecture/v1/modeling-knowledge-adoption.md`](../architecture/v1/modeling-knowledge-adoption.md) | adoption design、`WP-TRG-028` 及其 runtime projection artifact | 不能把 case、crosswalk、reference script 或 review 直接当成 LLM 上下文 |
| 4. 当前覆盖案例在既定前提下的 hosted 结果如何？ | 哪个 hypothesis/projection 被评估、campaign 前提是什么、对照臂与解释边界是什么 | 3 | [`hosted-experiment-registry.md`](hosted-experiment-registry.md) 与 selected G3 workpack | campaign charter、preflight record、terminal report、authorization record | 不能把 hosted 结果当成一般 runtime 结论，也不能绕过固定 case/split/budget 边界 |

## 维护规则

1. 先判定问题所属层，再选择权威文档；不要从导航页反推执行权限。
2. 开发侧知识、runtime contract、hosted 结果分别维护在各自 authority；跨层只允许链接，不允许复制后升级。
3. 新增结论时，正文必须写明“回答什么”和“does not authorize what”。
4. 从第 1 层进入第 2 层，或从第 2 层进入第 3 层，必须通过独立 workpack、review 和验收，而不是沿用上层结论。
5. `status.md` 只裁决“现在可做什么”；它不证明 hypothesis、runtime 或 hosted 结论本身。

## 快速判别

如果问题包含“支持什么 hypothesis / 哪些案例 / 哪些反例”，先看第 1 层。
如果问题包含“Harness 怎么做 / Q01--Q04 怎么限制 / 给 LLM 什么参考”，先看第 2 层。
如果问题包含“hosted 结果 / 对照臂 / 预算 / deadline / terminal report”，先看第 3 层。

## Links

- [`README.md`](README.md)
- [`../architecture/v1/project-theory-map.md`](../architecture/v1/project-theory-map.md)
- [`../architecture/pipeline.md`](../architecture/pipeline.md)
- [`../architecture/v1/knowledge-base-architecture.md`](../architecture/v1/knowledge-base-architecture.md)
- [`../architecture/v1/modeling-knowledge-adoption.md`](../architecture/v1/modeling-knowledge-adoption.md)
- [`status.md`](status.md)
