# 当前交付状态

- **更新日期**：2026-08-14
- **用途**：实现仓当前执行状态的唯一事实源；任务细节见 workpack，跨会话上下文见 handoff，决策理由见 ADR。

## 当前状态

| 项目 | 状态 |
|---|---|
| 当前里程碑 | M182-001 done：新 continuation contract 已在冻结 33-case batch 中产生完整终态 report；实际使用 36 HTTP requests 和 69 completion slots，未重试或 resume。 |
| active workpack | none。 |
| 下一工作 | 用户可选择一个新的独立 G2 terminal-review workpack，以审查 M182 terminal reports 并决定路线处置；不得从该结果推断重跑、repair 策略或新的 hosted 授权。 |
| 阻塞 | M182 egress authorization 已被该终态 batch 消耗。不得复用 M179/M181/M182 报告、monitor、预算或授权；任何后续 hosted 请求均须新 workpack、fresh preflight、独立 review 和逐项授权。 |
| 默认运行边界 | 离线、无凭证；DeepSeek V4 仅在显式 `--provider deepseek` 时接入。 |

## 运行边界与授权

持续离线案例治理授权只涵盖 coverage-gap 选择、预注册、受控生产、离线审计、evidence review 与受限 library promotion。它不授权修改 executable manifest、Harness、provider、training、runtime、外部数据或任何 hosted 请求。

## 当前项目口径

当前主线是获得真实 LLM 在冻结 Harness 闭环中的可归因 hosted 终端证据；repair/交互预算、案例治理和参考经验投影是相互独立、以证据支持该主线的路线。完整关系、演进规则和非主张见 [Current Project Route](../architecture/v1/current-project-route.md)。历史 family、batch 与 projection 路线只有在被当前 workpack 明确引用时才可作为背景输入。

## 历史与证据索引

- [里程碑历史](milestone-history.md) — 完成与 deferred milestone 的导航索引。
- [Evidence ledger](evidence-ledger.json) — 当前 deferred/backlog decision package、证据路径与重新进入条件。
- [决策包索引](../corpus/knowledge/decisions/README.md) 与 [M34 review](../architecture/v1/m34-next-decision-gate-review.md) — 详细边界。
- [M138 后 runtime 与知识路线](../architecture/v1/post-m138-runtime-and-knowledge-route.md) — 五个 deferred workpack 的依赖与边界。
- [Post-M152 authority-and-contract hardening route](../architecture/v1/post-m152-authority-and-contract-hardening-route.md) — M146--M153 已完成 authority/contract prelude 与 maintained authority map；后续只保留 deferred hardening route。

## Agent 更新规则

1. workpack 状态迁移时，先更新本页，再移动/更新 workpack，并同步 handoff。
2. 更新 deferred/backlog 决策时，同步 `evidence-ledger.json`；不得以 ledger 作为实施或 hosted 授权。
3. 如果本页、active workpack 与 handoff 不一致：停止领取新任务，核验 workpack 与验收证据后以本页为准回补。
4. active workpack 的 owner、risk tier、reviewer 与关联 handoff 按 [`task-lifecycle.md`](task-lifecycle.md) 管理；G3 仍须逐项用户授权。
