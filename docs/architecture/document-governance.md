# 开发 Agent 文档治理原则

本页评估当前文档体系，并定义 **Codex、Cursor 等开发 Agent** 借助文档治理 Brep2Code 的最小原则。它关注仓库外部的实现协作；论文结论仍以论文库为准。

> 本页不定义项目内部运行时 LLM 的 prompt、tool call、案例读取或受限 workspace 行为。那些行为由 Harness 和运行时契约治理，见 [`v1 Runtime Boundaries`](v1/runtime-boundaries.md)。

## 两个不可混用的治理平面

| 平面 | 主体 | 工作对象 | 权威材料 | 成功标准 |
|------|------|----------|----------|----------|
| **开发治理平面** | Codex、Cursor、人工开发者 | 仓库代码、测试、开发文档、Git 工作树 | `AGENTS.md`、workpack、handoff、ADR、runbook、状态页 | 任务可验收、变更可追溯、项目可持续演进 |
| **运行时执行平面** | Harness 调用的 LLM | record/revision 内受限 workspace、`build_sequence.py`、B-Rep probes、artifacts、traces | Harness 代码、tool schema、`signal_bundle.json`、runtime helper 与案例资源 | 在受限权限内产生可执行脚本，并通过 Harness gates 或获得结构化修复反馈 |

开发 Agent 可以修改第二平面的实现和契约，但不能把开发治理文档自动注入给运行时 LLM；运行时 LLM 也不能领取 workpack、修改 ADR/handoff 或裁决项目状态。

## 评估结论

现有体系已经具备有效骨架：`AGENTS.md` 提供入口，workpack 提供可验收任务，handoff 传递上下文，ADR 保存决策，runbook 记录可复现操作，模块文档连接代码边界。M0–M4 的拆分历史也说明该体系能支持逐步交付。

仍有三项改进需求：

1. **状态去重**：动态状态曾重复出现在多个入口并漂移；现由 [`docs/workflow/status.md`](../workflow/status.md) 集中维护。
2. **证据可追溯**：完成状态应关联验收命令、结果日期和产物/报告路径，避免把历史验证误读为当前工作树验证。
3. **任务关闭闭环**：每个 workpack 完成时应同步状态页、handoff、受影响模块/契约与必要 runbook；若改变长期规则或边界，再写 ADR。

Git 基线已于 2026-08-01 建立，当前实现、验收声明与状态更新已有可比较、可回退的版本化记录。后续变更仍应在用户明确要求提交时，将实现、验证证据和相应状态更新作为同一可审计单元提交。

## 文档职责与权威边界

| 文档 | 回答的问题 | 不是 |
|------|------------|------|
| `AGENTS.md` | Agent 从哪里开始、必须遵守什么规则 | 当前任务状态的副本 |
| `docs/workflow/status.md` | 现在做什么、下一步是什么、是否阻塞 | 任务实现细节或历史日志 |
| workpack | 本次任务交付什么、如何验收、边界是什么 | 跨会话长篇叙事 |
| handoff | 下一会话恢复什么上下文、先做什么 | 动态状态的唯一裁决器 |
| ADR | 为什么采用某个长期决策 | 操作步骤或进度报告 |
| runbook | 如何重复执行一项操作 | 架构取舍 |
| 模块/契约文档 | 模块责任、接口和不变量 | 任务排期 |
| 论文库链接 | 外部研究依据 | 本仓实现状态 |

## 文档层次与归档规则

为避免把“当前任务”误当作“长期规则”，开发文档按下列层次维护。一个
事实只在其权威层更新，其余层只链接。

| 层次 | 权威位置 | 生命周期与整理方式 |
|---|---|---|
| 入口与强制约束 | `AGENTS.md`、`.cursor/rules/` | 仅记录所有开发 Agent 都必须遵守的入口、安全与协作规则；不记录里程碑或案例结果。 |
| 当前运行状态 | `docs/workflow/status.md` | 唯一动态快照；仅保留当前 workpack、下一步、阻塞和紧凑里程碑结论。完成证据只链接，不累积成长篇日志。 |
| 任务与交接 | `docs/workpacks/active/`、`docs/handoff/active/` | 一项进行中的工作只有一个 active workpack 和一份对应 handoff。完成后 workpack 移到 `done/`，handoff 移到 `archive/`；空闲时两个 active 目录不保留已完成事项。 |
| 长期决定与稳定契约 | `docs/architecture/adr/`、`docs/architecture/v1/contracts/`、`docs/modules/` | ADR 记录“为什么”；契约和模块页记录持续有效的接口、边界和不变量。仅在跨任务仍生效时更新，不复制任务验收叙事。 |
| 操作与维护程序 | `docs/runbooks/` | 记录可重复执行的步骤、检查项和权限边界；每次只能靠口头经验复现的操作应沉淀在此。 |
| 案例与数据治理 | `docs/corpus/`、`case-library/` | 记录资产身份、生命周期、split、准入和审计；目录存在或本地生成不构成 Harness、provider、训练或 runtime 准入。 |
| 路线与研究 | `docs/architecture/v1/*roadmap*.md`、`docs/links/` | 路线图记录依赖与选择条件，论文库链接记录外部依据；它们不裁决当前状态。 |

关闭一个 workpack 时，先把可验证结果写入该 workpack 和 completion
review；再把跨任务的“为什么”写入 ADR、持续不变量写入契约/模块页、可
重复步骤写入 runbook，最后将状态页缩减为链接这些记录的结论。案例、诊断
或归因工作还必须明确记录 experience card、counterexample 或 no reusable
evidence 的处置。没有达到这些条件的内容留在完成 workpack 或 archived
handoff，不提升为长期规则。

## Agent 治理原则

1. **先定位，再行动**：先读 `AGENTS.md`、最新 handoff、状态页和 active workpack；缺失或冲突时先修复信息，不根据猜测开始实现。
2. **一类事实，一个权威位置**：当前状态归状态页；任务范围归 workpack；理由归 ADR；步骤归 runbook；接口归契约；研究归论文库。
3. **计划必须可验收**：每个 workpack 要有范围、非目标、兼容性约束、受影响文档和可运行的验收命令。
4. **结论必须带证据边界**：区分“本次已验证”“历史记录已验证”“尚待验证”；不把 fake-provider 结果扩大为 hosted LLM 或基准质量结论。
5. **状态迁移是原子协作动作**：完成、阻塞或取消一个 workpack 时，同步状态页、workpack、handoff，以及受影响的索引/契约；必要时记录 ADR。
6. **渐进收敛而非预设架构**：仅在 corpus 与 failure evidence 支持时引入 IR、SDK、CAD workplace 或新 gate/tool；将假设写成待验证项。
7. **两个平面严格分离**：`docs/` 治理开发 Agent 的协作；运行时 workspace、LLM 上下文和工具材料由 Harness 显式注入与限制。前者不自动成为后者的 prompt。
8. **版本化让历史可审计**：把实现、文档、验收和状态变化作为一个可审计单元；未提交状态要明确标注其恢复与回退风险。
9. **案例治理不等于运行时材料**：开发侧案例目录、注册表和审阅卡用于 Codex/Cursor 与人工维护，不自动成为 Harness 或运行时 LLM 的输入；边界见 [ADR-0007](adr/0007-development-case-governance.md)。
10. **状态页保留当前，不复制证据日志**：状态页只维护当前快照、紧凑里程碑结果和最近决策；详细验收事实只链接到 workpack、review 或 ledger。
11. **关闭时处置可复用证据**：案例扩展、诊断和归因 workpack 必须记录经验卡、反例或“无可复用证据”之一；这不自动授权 runtime retrieval。

## 最小执行检查表

开始任务：入口规则 → 最新 handoff → 状态页 → active workpack → 模块/契约 → 必要的 runbook/论文链接。

结束任务：运行验收 → 记录经验卡/反例/无证据处置 → 更新 workpack 结果 → 更新状态页 → 更新模块/契约与 runbook → 记录 ADR（如有长期决定）→ 更新 handoff。仅在用户明确要求时提交 Git。
