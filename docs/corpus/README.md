# 开发侧案例治理

M83 的 [候选参考包合同](reference-packs/reference-pack-contract-v1.json) 只含声明性的 OCP 模块、参数占位、短构造轮廓、输出要求、反例与 source hash。它不含原始输入 STEP、完整参考脚本、held-out authoring evidence 或 `runtime_resources/` 路径；用 `uv run python tools/audit_reference_packs.py` 审计固定 P0/P1 split、内容 hash、source record 与这条拒绝边界。它是 experimental development metadata，不是经验卡、检索或 runtime 输入，也不解锁 M19-002。

本目录是 Brep2Code 的**开发治理案例与证据入口**。它面向 Codex、Cursor 与人工开发者，用于登记、审阅和维护可复现 CAD 案例；不属于 Harness 运行时材料。案例是知识系统的 oracle、对照、回归或 OOD 证据，而不是能力覆盖数量的替代指标；完整定位见 [Harness 闭环知识库架构](../architecture/v1/knowledge-base-architecture.md)。

运行时 LLM 不读取本目录，Harness 也不从这里注入 prompt、tool schema、geometry gate 或执行输入。现有 `case-library/manifests/self-authored/p0.json` 与 `p1.json` 仍是 corpus runner 的执行 manifest；本目录不替代、也不改变它们。

边界与决策见 [ADR-0007](../architecture/adr/0007-development-case-governance.md) 和 [runtime boundaries](../architecture/v1/runtime-boundaries.md)。

## 入口

| 材料 | 用途 | 权威性 |
|------|------|--------|
| [自建案例注册表](registry/self-authored.json) | 开发 Agent 可读取的结构化案例元数据和数值基线 | 自建案例的数值与文件身份权威来源 |
| [案例总览](catalog.md) | 人工跨案例比较、筛选和审阅 | 导览；数值冲突时以注册表为准 |
| `cases/<case_id>.md` | 每个案例的意图、尺寸和维护记录 | 人工审阅材料 |
| [外部数据登记](external/registry.json) | 数据集级来源、许可和启用边界 | 外部数据集登记来源 |
| [外部选样模板](external/selection-template.json) | 后续专项 workpack 的样本级审计模板 | 模板；不是已选数据 |
| [统一案例库](library/README.md) | 跨来源定位 input B-Rep、参考序列、manifest 与运行证据；维护候选接入顺序 | 开发治理索引；不是 Harness 输入 |
| [案例组合进度](case-portfolio.md) | 跨案例查看人工 case card、reference script、pack、runtime card 与 hosted 证据准备度 | 只读导航；不替代任一权威记录 |
| [建模知识库](knowledge/README.md) | 从 B-Rep 观察、受限建模假设、执行/修复到证据链的开发侧决策底座 | 可追溯知识索引；不改变资产或 runtime |

## 自建案例维护

新增、修改或弃用自建案例时，按以下顺序进行：

1. 在 `registry/self-authored.json` 登记或更新案例；新增案例先获得稳定、从不复用的 `case_id`。
2. 创建或更新 `cases/<case_id>.md`，说明几何意图、关键尺寸、单位、验证用途和非目标。
3. 添加或修改提交到 Git 的 STEP fixture 与本地 reference script（适用时）。
4. STEP 或 reference script 变更时，递增 `fixture_version`，更新 SHA-256、数值基线和案例卡的变更记录。
5. 仅在专项 workpack 明确需要时，才将案例加入运行用 manifest 或改动 Harness/corpus 行为。

每个 `case-library/self-authored/<case_id>/case.json` 是自建案例的数值基线和文件身份权威来源；`self-authored.json` 只保留指向这些记录的稳定索引。参数化案例还记录 `family_id` 与 `data_split`，且同一家族不得跨 split。使用 `uv run python tools/audit_case_library.py --replay` 离线核验 hash、目录、manifest 对齐、split 隔离与参考脚本重放；它不扩大 Harness 运行时职责。

新增 sequence-paired family 先复制
`sequence-paired/family-intake-template.json`，在候选资产生产前冻结 grammar、
rows/split、oracle、mutation、semantic 与 rejection evidence，再运行
`uv run python tools/audit_sequence_paired_intake.py <record>`。该通用审计只
验证预注册治理契约；生产后仍须由 family-specific audit 验证 geometry、exact
sequence、editability 与语义。完整步骤见
[case-library-maintenance runbook](../runbooks/case-library-maintenance.md) 和
[ADR-0026](../architecture/adr/0026-case-family-intake-contract.md)。

统一案例库不复制 fixture 或外部原始资产。它将现有测试 fixture、忽略的外部数据、显式 manifest 与运行报告按角色关联，避免将没有建模序列的 B-Rep-only 数据集误作 sequence-supervised 数据。具体维护步骤见 [case-library-maintenance runbook](../runbooks/case-library-maintenance.md)。

弃用案例时保留其注册表条目，将状态改为 `retired` 并写明替代关系；不得将其 `case_id` 分配给新几何。

## 引用数据集维护

外部数据集只在 [external/registry.json](external/registry.json) 中登记。原始下载物仅可位于被 Git 忽略的 `data/datasets/<dataset>/<release>/`，不得提交、不得作为默认测试输入，也不得因本目录而被下载或执行。

未来选取外部样本必须先复制 [selection-template.json](external/selection-template.json)，并由单独 workpack 完成许可确认、版本锁定、样本选择、格式/单位归一化与复现审查。

已完成的 M8-001 选择记录为 [ABC v00 selection](external/abc-v00-m8-001-selection.json)；其 [explicit manifest](external/abc-v00-m8-001-manifest.json) 只在本地原始资产已按记录放入忽略的 `data/datasets/abc/v00/` 后才可运行。

M9-001 将同一不可变选择拆为 [development manifest](external/abc-v00-m9-001-development-manifest.json) 与 [held-out manifest](external/abc-v00-m9-001-held-out-manifest.json)。两者仍是显式本地输入：先完成离线 hash/probe/sandbox preflight；任何 hosted `--first-pass` 执行均须按 split 单独取得预算授权，并沿用未改变的 generation policy。

M10-003 在同一 archive 的 M8 截止点之后继续了一个有界的 3 例本地增量：[selection](external/abc-v00-m10-003-selection.json)、[development manifest](external/abc-v00-m10-003-development-manifest.json) 与 [held-out manifest](external/abc-v00-m10-003-held-out-manifest.json)。它仅是离线准入；任何 hosted 使用仍需后续单独 workpack 和明确授权。

M10-007 在 M10-003 cutoff 后继续了第二个有界 3 例本地增量：[selection](external/abc-v00-m10-007-selection.json)、[development manifest](external/abc-v00-m10-007-development-manifest.json) 与 [held-out manifest](external/abc-v00-m10-007-held-out-manifest.json)。它同样只用于离线准入，不授权 hosted 使用。

M10-010 在 verified complete ignored local cache 后继续了第三个有界 3 例增量：[selection](external/abc-v00-m10-010-selection.json)、[development manifest](external/abc-v00-m10-010-development-manifest.json) 与 [held-out manifest](external/abc-v00-m10-010-held-out-manifest.json)。缓存改善本地访问，不改变显式选样、离线准入或 hosted 授权边界。

Fusion 360 Gallery r1.0.1 的 M16 已将 M14 的三例 native-history replay-pass
证据写为分离的 [development manifest](external/fusion360-gallery-r1.0.1-m16-001-development-manifest.json)
与 [held-out manifest](external/fusion360-gallery-r1.0.1-m16-001-held-out-manifest.json)。它们只用于非默认 local-only control；没有 corpus run、provider input 或 hosted authorization。

M17-001 在固定范围内保留一个 held-out Line3D replay mismatch，M17-002 已拒绝仅 endpoint-ordering 的修复；M17-003 的 `ordered_y` 虽通过固定 held-out，却使三个 Line3D controls 退化，故不推广该 mapping。M17-004 提名的 profile-normal / STEP-projection / extent-boundary selector 已在同一固定四例和既有 gates 下完成 M17-005 验证，并由 M17-006 在 2 development/1 held-out 独立 family 上冻结复验；后者有一例 development strict baseline 失败、selector 通过。累计 5 development/2 held-out selector gate pass，但严格 replay 仍为默认；该结果不替换样本、不扩展支持子集，也不授权 corpus、provider 或 hosted 使用。

ABC `v00` 的本地 archive 保留为不可变来源，`data/datasets/abc/v00/step/` 可按 [ADR-0011](../architecture/adr/0011-local-external-archive-cache.md) 完整解压为 Git-ignore 的可重建本地缓存。缓存完成标记只在 archive hash、10,000 STEP members 和 archive-listed byte total 核验后写入；它不构成全量 corpus、默认输入、tracked manifest、provider 输入或再分发授权。任何扩展仍须由 workpack 以小批次、确定性顺序执行：逐例记录来源身份、SHA-256、probe 准入结果、split 与许可边界后，才可加入新的显式 manifest。
