# 架构概览

Brep2Code v1 将 **B-Rep 输入** 转为 **可执行 CAD 建模脚本与结果**。当前实现方向是 **Harness 优先**：先搭建通用大模型可用的 probe、执行、门控和修复闭环，再从案例中决定是否沉淀 IR、SDK 或 CAD workplace。

## 双仓角色

| 仓库 | 路径 | 职责 |
|------|------|------|
| **实现仓**（本仓库） | `D:\codeai\Brep2Code` | 代码实现、验证、Agent 规则/Skills、Handoff、架构 ADR、Runbook |
| **论文库** | `D:\paper` | 文献笔记、阅读清单、研究综述、阅读进度、Zotero 元数据 |

本仓不复制文献正文；通过 [`docs/links/paper-vault.md`](../links/paper-vault.md) 单向引用论文库。

## 当前数据流

```
B-Rep 文件
    ↓
Harness 建立 record/workspace
    ↓
LLM 按需调用 B-Rep probe tools
    ↓
LLM 编写/修改 CAD 脚本
    ↓
Harness 执行、导出、门控、对比
    ↓
结构化反馈返回 LLM 修复
```

## 设计原则

1. **Harness 先行**：优先实现可执行、可观测、可迭代的闭环。
2. **按需探查**：Q01 不做大而全的 B-Rep 编码器，先提供 LLM 可调用的 probe 工具。
3. **通用模型优先**：v1 调用 hosted/general LLM；不做本地部署、训练或微调。
4. **延迟收敛**：IR、SDK 分层、CAD workplace 等从案例和失败数据中沉淀。
5. **论文库只链不抄**：研究综述与路线依据保留在论文库，本仓只记录实现决策。
6. **证据先于指导**：案例资产、回放与审计先形成受限建模知识；只有经过独立评审的压缩经验才能成为未来运行时 LLM 的候选材料。

当前项目的统一口径见
[`v1/current-project-route.md`](v1/current-project-route.md)：主线是冻结
Harness 闭环并取得真实 LLM 的可归因 hosted 终端证据；repair/交互预算、案例
治理和参考经验投影分别以证据支持该主线。现阶段 hosted 范围细节仍见
[`v1/current-hosted-evaluation-framing.md`](v1/current-hosted-evaluation-framing.md)。

## 相关文档

- [Agent 规则分层](agent-layers.md)
- [流水线索引](pipeline.md)
- [当前交付状态](../workflow/status.md)
- [提问路由与权威落点](../workflow/question-routing-and-authority.md)
- [Agent 文档治理原则](document-governance.md)
- [项目理论地图](v1/project-theory-map.md)
- [B-Rep 建模知识体系](v1/modeling-knowledge-system.md)
- [M48 后的 LLM 闭环推进路线](v1/post-m48-closed-loop-roadmap.md)
- [Post-M152 authority-and-contract hardening route](v1/post-m152-authority-and-contract-hardening-route.md)
- [四轨项目路线](v1/four-track-program-roadmap.md)
- [当前项目路线：可审计 hosted 闭环](v1/current-project-route.md)
- [现阶段 hosted 评测统一口径](v1/current-hosted-evaluation-framing.md)
- [Q01--Q04 决策包索引](../corpus/knowledge/decisions/README.md)
- [建模知识覆盖矩阵](../corpus/knowledge/coverage-matrix.json)
- [ADR-0001: Agent 框架与 Handoff](adr/0001-agent-framework-and-handoff.md)
- [ADR-0002: 实现仓与论文库分工](adr/0002-paper-repo-split.md)
- [ADR-0003: v1 Harness-first 方向](adr/0003-harness-first-v1.md)
- [ADR-0035: Harness-oriented knowledge-base architecture](adr/0035-harness-oriented-knowledge-base-architecture.md)
- [ADR-0036: Legacy evidence disposition and decision index](adr/0036-legacy-evidence-disposition-and-decision-index.md)
- [ADR-0056: Four evidence-gated program tracks](adr/0056-four-track-program-routing.md)


