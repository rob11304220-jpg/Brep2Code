# ADR 撰写

Architecture Decision Records 记录**实现侧**重要决策；文献依据与路线综述仍以论文库为准。

## 何时写 ADR

- 选定技术栈或工具链（如 uv、内核绑定）
- 确定模块边界或目录结构
- 选定验证/门控策略
- 框架或流程约定变更（影响所有 Agent 会话）

不必为每个小改动写 ADR；重复操作步骤写 Runbook 即可。

## 路径与编号

- 目录：`docs/architecture/adr/`
- 命名：`NNNN-<kebab-slug>.md`（四位序号，从 0001 递增）
- 新建前列出目录，取最大编号 +1

## 模板

```markdown
# ADR-NNNN: 标题

- **Status**: Proposed | Accepted | Superseded
- **Date**: YYYY-MM-DD
- **Context**: 背景与问题

## Decision

决策内容。

## Rationale

为何如此选择。

## Consequences

- **Positive**: ...
- **Negative**: ...
- **Mitigation**: ...

## Alternatives Considered

| 方案 | 弃用原因 |
|------|----------|
| ... | ... |
```

## 与 Runbook / Handoff 的分工

| 文档 | 回答 |
|------|------|
| ADR | **为什么**这样决策 |
| Runbook | **如何**执行步骤 |
| Handoff | **当前**进度与下一步 |

新建 ADR 后，在活跃 Handoff 的 **Decisions** 节添加链接。

## Skill

显式引用 **`adr-write`** 创建 ADR 并更新 Handoff 链接。

