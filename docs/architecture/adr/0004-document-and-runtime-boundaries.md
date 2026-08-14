# ADR-0004: Document, Workpack, and Runtime Boundaries

- **Status**: Accepted
- **Date**: 2026-07-22

## Context

Brep2Code 需要在实现前建立工作文档：模块文档对照代码、开发路由、workpack 分发，以及项目内外文档边界。同时，v1 参考 Articraft 的 SDK + Harness 模式，运行时 LLM 的上下文和操作材料应由 Harness 注入或通过 tool 读取，而不是作为 `docs/` 下的普通治理文档。

## Decision

- 使用 `docs/workflow/` 作为开发协作路由，不使用 `docs/workspace/`。
- 使用 `docs/workpacks/` 分发可领取、可验收的开发任务包。
- 使用 `docs/modules/` 维护模块文档和代码路径对照。
- 将 runtime workspace、Harness 注入上下文、SDK/案例/操作材料定义为项目内可调用材料，由 Harness 控制读取和注入。
- 保持 `D:\paper` 为项目外研究文档源，本仓只链接，不复制论文正文。

## Consequences

- `workspace` 一词保留给 Articraft 式受限运行时工作区。
- `docs/` 聚焦开发治理，不直接充当运行时 LLM 的上下文库。
- 后续实现 Harness 时，需要提供读取项目内 SDK/案例/操作材料的 tool，并限制可见范围和返回大小。

