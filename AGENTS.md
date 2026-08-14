# Agent 入口地图

本仓库是 **Brep2Code 实现仓**：以 Harness 优先的方式探索 B-Rep → 可执行 CAD 建模脚本/结果的闭环生成与验证。本文档只定义入口、硬边界与任务路由；具体操作放在 Rules、Skills 和 Runbook。文献、阅读清单与研究综述在论文库 `D:\paper`。

> **适用对象**：本文件约束 Codex、Cursor 等在仓库外部执行开发工作的 coding agent，以及人类协作者；它不作为 Harness 内运行时 LLM 的 prompt、tool manual 或 workspace 规则。运行时 LLM 的边界见 `docs/architecture/v1/runtime-boundaries.md`。

## 项目定位

| 仓库 | 职责 |
|------|------|
| **本仓** (`D:\codeai\Brep2Code`) | 代码实现、验证、Agent 规则/Skills、Handoff、ADR、Runbook |
| **论文库** (`D:\paper`) | 文献笔记、阅读清单、研究综述、阅读进度 |

论文库索引：[`docs/links/paper-vault.md`](docs/links/paper-vault.md)

## 流水线锚点（Q01–Q04）

```
Q01 B-Rep按需探查 → Q02 CAD脚本生成 → Q03 Harness执行/门控 → Q04 反馈修复 → (回到 Q02)
```

- 阶段定义与链接：[`docs/architecture/pipeline.md`](docs/architecture/pipeline.md)
- 当前研究结论（论文库，不复制正文）：`D:\paper\Projects\Brep2Code-research\outputs\literature-synthesis-and-validation-handoff.md`
- 历史路线比较（仅背景）：`D:\paper\Projects\Brep2Code-research\routes\q01-q04-synthesis.md`

## 按任务类型进入材料

先完成下文“开始任务前”的恢复顺序；然后按任务问题选择材料，而不要从案例、
历史 workpack 或路线图反推权限。

| 任务问题 | 首先读取 | 然后读取 | 不因此获得 |
|---|---|---|---|
| 理论 / 实验设计：什么受限假设已有证据、缺什么？ | [`项目理论地图`](docs/architecture/v1/project-theory-map.md) | M146 crosswalk、相关 knowledge unit 和 decision package | 实现、case、runtime、provider 或 hosted 权限 |
| Harness / runtime / contract：Q01--Q04 如何工作或须变更？ | [`pipeline.md`](docs/architecture/pipeline.md) 与 Q01--Q04 contracts | 相关 hypothesis 的边界和 active workpack | 理论泛化或自动 adoption |
| 案例 / 治理：资产是否可用、支持什么证据角色？ | `case.json`、registry、admission record 与 case portfolio | status/workpack 和对应审计 | manifest、runtime 或出境权限 |
| 工作选择 / 状态：现在可做什么？ | [`status.md`](docs/workflow/status.md) | active workpack 与 active handoff | 因 deferred/历史记录直接开始工作 |
| 路线 / 组合决策：下一步为何保留、替代或退出某条路线？ | [`Route Decision Map`](docs/architecture/v1/route-decision-map.md) | 当前项目路线、相关证据与 `status.md` | workpack、案例、runtime、provider 或 hosted 权限 |
| Hosted 请求：能否向外部 provider 发送内容？ | 本文的 hosted 预检和 provider runbook | selected G3 workpack、preflight、独立 review | 未经逐项授权的 provider 请求 |

新 case、code 或 evaluation proposal 在适用时必须写明：M146
`hypothesis_id`（或说明为何无关）、Q01--Q04 decision、evidence role、
counterexample、stop rule 和 adoption boundary。它们用于范围与审计，不授予
任何实现、资产、runtime、provider 或 hosted 权限。

## 层级结构

```
Brep2Code/
├── AGENTS.md              ← 本文件（Agent 入口）
├── README.md              ← 人类入口
├── .cursor/
│   ├── rules/             L0/L1/L2 分层规则
│   └── skills/            可复用流程
└── docs/
    ├── architecture/      架构 + ADR
    ├── modules/           模块文档 ↔ 代码路径对照
    ├── workflow/          开发协作路由（非 runtime workspace）
    ├── workpacks/         可分发任务包
    ├── runbooks/          操作手册
    ├── handoff/           跨会话交接
    └── links/             论文库索引
```

## 开始任务前

按以下唯一顺序恢复或领取工作：

1. 读本文档；新会话执行 **`handoff-resume`** 或读 [`docs/handoff/active/`](docs/handoff/active/) 最新文件。
2. 读 [`docs/workflow/status.md`](docs/workflow/status.md)；它是当前执行状态的裁决源。
3. 有 active workpack 时读 [`docs/workpacks/active/`](docs/workpacks/active/)；没有时，只有用户选择新的 bounded package 才能创建任务。
4. 读 [`docs/workflow/task-lifecycle.md`](docs/workflow/task-lifecycle.md)，按风险等级领取并验收。
5. 涉及设计背景时，执行 **`paper-vault-lookup`** 或读 [`docs/links/paper-vault.md`](docs/links/paper-vault.md)。

Workpack 是一次性执行账本，而不是长期路线或证据权威。读取历史结论时，先到
ADR、route、contract 或 evidence authority；仅在需要范围、验收或 provenance 时再读
已完成/归档 workpack。具体归档与引用规则见
[`workpack-governance.md`](docs/workflow/workpack-governance.md)。

不得以 evidence ledger、backlog、历史 handoff 或论文链接推断实施、runtime 或 hosted 授权。

已由用户选择的 active workpack 在其自身边界内具有连续执行授权：owner 必须持续完成 owner-side scope，直至达到明确的 review、外部/hosted 授权、冻结输入漂移或范围外依赖等停止条件。不得仅因创建 workpack、完成局部实现或报告中间进度而交还控制权；新的 bounded workpack 仍须用户显式选择。

## Hosted 请求前的最小预检

任何会向外部 provider 发送数据或派生摘要的请求，在向用户请求授权**之前**必须完成并汇报以下只读预检：

1. 明确目的地、模型、发送内容（原始输入或受限派生摘要）、固定案例/split、最大轮次、请求/成本上限与单请求 deadline。
2. 核验所选输入的 SHA-256、split/manifest 范围，以及对应离线 `wsl-bwrap` preflight 已完成；hash、manifest、input-probe 或 sandbox 失败时不得请求授权。
3. 核验本地 provider 配置项、模型选择与安全执行器可用性，但不得显示密钥或环境快照。
4. 核验 CLI 的实际边界与报告路径；`--first-pass` 的最大请求数为 `max_cases × (1 + max_rounds)`，普通 hosted repair 为 `max_cases × max_rounds`。
5. 检查同一报告路径是否已有 `running` 或 `interrupted` checkpoint。它们仅是部分证据，不能复用剩余预算；必须使用新报告路径并取得新的明确授权。
6. 暴露运行风险：数据出境范围、预算上限、provider deadline，以及宿主/外层执行时间限制。若批次可能超过交互式命令时限，先说明并采用可持续监控的运行方式。

授权文本必须覆盖目的地和出境内容，并逐项确认 provider/model、案例范围、轮次、deadline 与请求或成本预算。详见 [`docs/runbooks/llm-provider-config.md`](docs/runbooks/llm-provider-config.md)。

## 任务与质量门

- 每个 active workpack 只有一名 owner；G2/G3 工作必须有独立 reviewer。并行协作的边界见 [`docs/workflow/multi-agent-collaboration.md`](docs/workflow/multi-agent-collaboration.md)。
- 先更新 `status.md`，再更新 workpack 和 handoff；关闭前运行 `uv run python tools/check_governance.py`。
- G1 及以上工作运行治理审计；G2/G3 的代码共享变更还须运行相关测试、Ruff，并按 [`offline-validation`](.cursor/skills/offline-validation/SKILL.md) 选择完整离线验证。
- G3 先执行 `hosted-preflight`；未取得逐项明确授权前，禁止外发数据或发起 provider 请求。

## 规则分层

| 层级 | 位置 | 何时生效 |
|------|------|----------|
| L0 核心 | `.cursor/rules/00-brep2code-core.mdc` | 始终 |
| L1 流程 | `.cursor/rules/01-*.mdc`, `02-*.mdc` | 始终 |
| L1 文档 | `.cursor/rules/03-docs-capability.mdc` | 编辑 `docs/**` 时 |
| L2 领域 | `.cursor/rules/10-python-domain.mdc` | 匹配 `**/*.py` 时（占位） |

## 可复用 Skills

| Skill | 用途 |
|-------|------|
| `handoff-create` | 会话结束前创建/更新交接单 |
| `handoff-resume` | 新会话恢复上下文与执行计划 |
| `paper-vault-lookup` | 查阅论文库文献与 Q&A（只链不抄） |
| `adr-write` | 记录实现侧架构决策 |

Skills 位于 `.cursor/skills/<name>/SKILL.md`，需显式引用触发。

## Handoff 协议

- **路径**：[`docs/handoff/active/`](docs/handoff/active/)
- **模板**：[`docs/handoff/TEMPLATE.md`](docs/handoff/TEMPLATE.md)
- **详细步骤**：[`docs/runbooks/handoff-protocol.md`](docs/runbooks/handoff-protocol.md)

## 能力沉淀

| 类型 | 路径 |
|------|------|
| 架构概览 | [`docs/architecture/overview.md`](docs/architecture/overview.md) |
| 规则分层 | [`docs/architecture/agent-layers.md`](docs/architecture/agent-layers.md) |
| 流水线索引 | [`docs/architecture/pipeline.md`](docs/architecture/pipeline.md) |
| 开发路由 | [`docs/workflow/README.md`](docs/workflow/README.md) |
| 当前交付状态 | [`docs/workflow/status.md`](docs/workflow/status.md) |
| Workpack | [`docs/workpacks/`](docs/workpacks/) |
| 模块对照 | [`docs/modules/README.md`](docs/modules/README.md) |
| ADR | [`docs/architecture/adr/`](docs/architecture/adr/) |
| Runbook | [`docs/runbooks/`](docs/runbooks/) |
| 论文库链接 | [`docs/links/paper-vault.md`](docs/links/paper-vault.md) |

## Runtime / Docs 边界

- `workspace` 专指 Harness 运行时的受限 workspace，不用于 `docs/` 下的开发路由命名。
- 给运行时 LLM 的上下文、SDK/案例/操作材料属于项目内可调用材料，由 Harness 注入或通过 tool 读取。
- `docs/` 负责开发治理、架构、workpack、模块对照和 runbook，不作为运行时 LLM 的默认上下文库。
- 详细边界：[`docs/architecture/v1/runtime-boundaries.md`](docs/architecture/v1/runtime-boundaries.md)

## 结束会话前

1. 运行适用质量门，至少包含相关的治理审计。
2. 同步 [`docs/workflow/status.md`](docs/workflow/status.md)、workpack 与 handoff；没有 active workpack 时归档完成 handoff。
3. 若有架构决策，写 ADR（skill `adr-write`）；若有可复用步骤，更新 Runbook。
4. 仅在用户明确要求时 git commit。


