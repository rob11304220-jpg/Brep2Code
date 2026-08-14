# ADR-0002: 实现仓与论文库职责边界

- **Status**: Accepted
- **Date**: 2026-07-10
- **Context**: Brep2Code 横跨实现仓（`D:\codeai\Brep2Code`）与 Obsidian 论文库（`D:\paper`），需明确分工避免重复与漂移。

## Decision

| 内容类型 | 归属 | 路径示例 |
|----------|------|----------|
| 文献笔记、阅读列表 | 论文库 | `D:\paper\Projects\Brep2Code.md` |
| Q01–Q04 文献综述与路线依据 | 论文库 | `D:\paper\Projects\Brep2Code-research\routes\q01-q04-synthesis.md` |
| 架构决策（实现侧） | 实现仓 ADR | `docs/architecture/adr/` |
| 可重复操作步骤 | 实现仓 Runbook | `docs/runbooks/` |
| 跨会话进度 | 实现仓 Handoff | `docs/handoff/active/` |
| 代码与验证 | 实现仓（未来） | `src/`、`tests/` 等待建 |

**同步方式**：单向引用（实现仓 → 论文库）。实现侧决策写 ADR 摘要 + 链接论文笔记，不复制全文。

**流水线状态**：Q01–Q04 的实现状态以本仓为准；论文库只保留文献依据与路线综述。

## Rationale

- 论文库适合长期文献积累与 Zotero 联动；实现仓适合 Git 版本化的代码与 Agent 状态。
- 避免双份维护导致内容不一致。

## Consequences

- **Positive**: 职责清晰；Agent 查设计背景走 `paper-vault-lookup`，查实现进度走 Handoff。
- **Negative**: 跨仓跳转需记住两套路径。
- **Mitigation**: [`docs/links/paper-vault.md`](../../links/paper-vault.md) 集中索引。

## Alternatives Considered

| 方案 | 弃用原因 |
|------|----------|
| 论文库也存 Handoff | 无法与代码同 PR review；Git 历史分离 |
| 实现仓镜像全部 Q&A | 用户明确选择仅链接 |


