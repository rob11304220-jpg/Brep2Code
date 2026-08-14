# ADR-0001: Agent 框架与仓库内 Handoff

- **Status**: Accepted
- **Date**: 2026-07-10
- **Context**: 初始化 Brep2Code 实现仓，需支持跨 Agent 会话协作，且与外部论文库 `D:\paper` 联动。

## Decision

1. **Agent 入口**：根目录 `AGENTS.md` 为唯一 Agent 地图；人类入口 `README.md` 简短指向 Agent 与论文库。
2. **文档集中**：除根入口外，所有文档写入 `docs/`（architecture、runbooks、handoff、links）。
3. **Handoff 仅仓库内**：使用 `docs/handoff/active/` + `archive/`，Git 追踪，不依赖外部笔记系统存放会话状态。
4. **规则分层**：L0/L1 alwaysApply；L2 按 glob（如 `**/*.py`）限定领域规则。
5. **Skills 显式触发**：`.cursor/skills/` 封装 handoff、论文查阅、ADR 等可复用流程。

## Rationale

- 仓库内 Handoff 可 diff、可 review，与代码变更同版本思维。
- 文档集中降低 Agent 检索成本；根入口保持精简。
- Skills 与 Rules 分工：Rules 约束行为，Skills 封装多步流程。

## Consequences

- **Positive**: 新会话可通过 `handoff-resume` 快速恢复；框架与实现同仓版本对齐。
- **Negative**: 论文库与实现仓需手动保持链接一致（通过 `docs/links/paper-vault.md`）。
- **Mitigation**: `paper-vault-lookup` skill 统一查阅路径；不在本仓复制文献正文。

## Alternatives Considered

| 方案 | 弃用原因 |
|------|----------|
| Handoff 放 `.cursor/handoff/` | 用户要求文档除入口外写入 `docs/` |
| 论文内容镜像到 `docs/knowledge-base/` | 用户选择仅链接与索引 |
