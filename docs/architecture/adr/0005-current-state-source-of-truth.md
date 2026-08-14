# ADR-0005: 当前交付状态单一事实源

- **Status**: Accepted
- **Date**: 2026-08-01
- **Context**: M4-002 完成后，`workflow`、里程碑和模块索引对“当前 workpack”的表述发生漂移。状态同时散落在 README、pipeline、workflow、milestones、workpacks 与 handoff，Agent 需要自行裁决，容易领取过期任务。

## Decision

以 [`docs/workflow/status.md`](../../workflow/status.md) 作为实现仓当前交付状态的唯一事实源。该页维护当前里程碑、active workpack、下一项工作、阻塞、里程碑进度与证据边界。其他入口只链接该页；workpack、handoff 和 ADR 分别继续承载任务细节、跨会话恢复和决策理由。

## Rationale

当前状态是高频、可变且直接影响 Agent 行动的信息，应有一个明确的所有者和最短的读取路径；历史记录和计划文档不适合作为状态裁决器。

## Consequences

- **Positive**：Agent 可在领取任务前快速确定唯一行动入口；状态漂移可被局部修复。
- **Negative**：workpack 状态迁移增加一次同步动作。
- **Mitigation**：在 `AGENTS.md`、workflow 路由和 handoff 中明确更新顺序，并在 workpack 验收清单中加入状态同步。

## Alternatives Considered

| 方案 | 弃用原因 |
|------|----------|
| 继续以 `docs/workflow/README.md` 为唯一真源 | 路由说明与动态状态混在一起，已经产生重复和漂移。 |
| 只以目录位置（`active/`、`done/`）推断状态 | 无法表达“无 active workpack”、下一步和阻塞，也缺少证据边界。 |
| 每份入口文档各自维护状态 | 已被现有历史证明容易失同步。 |
