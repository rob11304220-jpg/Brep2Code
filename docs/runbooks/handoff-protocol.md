# Handoff 协议

跨会话状态通过 Git 追踪的 Markdown 交接单传递。

## 路径

| 用途 | 路径 |
|------|------|
| 模板 | `docs/handoff/TEMPLATE.md` |
| 活跃交接 | `docs/handoff/active/` |
| 归档 | `docs/handoff/archive/` |

## 模板字段

Date, Subproject (`brep2code`), Status, Goal, Done, In progress, Next, Decisions, Blockers, Key paths, Resume prompt

## 创建交接（`handoff-create`）

1. 从当前会话收集：Goal, Done, In progress, Next, Decisions, Blockers, Key paths
2. 读 `docs/handoff/TEMPLATE.md`
3. 若更新同一任务，编辑现有 active 文件；否则新建 `docs/handoff/active/YYYY-MM-DD-<slug>.md`
4. `<slug>` 为小写 kebab-case，如 `q01-brep-input`、`agent-framework-init`
5. 填写 **Resume prompt**（下一会话可直接粘贴）
6. 有进行中 workpack 时，保持 `active/` 仅 **1–3** 个文件；过时或已完成文件移至 `archive/`。没有 active workpack 时，`active/` 不保留已完成交接单。
7. 告知用户 handoff 路径与 Resume prompt

## 恢复会话（`handoff-resume`）

1. 读根 `AGENTS.md`
2. 列出 `docs/handoff/active/`，取文件名日期前缀最新的文件
3. 解析 Goal, Status, Next, Blockers, Key paths, Resume prompt
4. 输出：摘要、建议首步、开放 blockers、完整 Resume prompt
5. 不假设 handoff 或仓库文件未记载的内容

## 无 active handoff 时

- 说明未找到交接单
- 读 `docs/workflow/status.md`；若其也显示没有 active workpack，则等待用户选择 backlog 或给出新的目标
- 澄清后建议运行 `handoff-create`

## 与 ADR 的关系

架构决策写入 Handoff 的 **Decisions** 节，并链接 `docs/architecture/adr/NNNN-....md`。
