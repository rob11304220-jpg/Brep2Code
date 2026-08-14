# ADR-0035: 将知识库定位为 Harness 闭环的可追溯决策底座

- **Status**: Accepted
- **Date**: 2026-08-05

## Context

现有建模知识系统已将治理案例投影为受限 operation units，但其叙事重点仍偏向
“案例覆盖矩阵 → runtime guidance card”。这容易将案例数量或 feature 覆盖误作
进展，也不足以组织 Q01--Q04 中的观察、序列假设、执行门控与失败修复知识。

## Decision

知识库重定位为 Harness 开发侧的可追溯决策底座。它按观察、建模假设/操作契约、
Harness 执行知识和证据/评测四层组织；案例作为这些决策的 oracle、对照、回归或
OOD 证据资产。coverage matrix 以“最小可验证的决策缺口”而非案例数量驱动下一项
工作。现有物理路径、case authority、manifest 和 runtime 边界不变，采用逐步迁移的
逻辑目录，避免仅为文档结构移动资产。

## Consequences

- 新案例必须说明将降低 Q01--Q04 哪一个具体决策的不确定性；没有该价值不应选取。
- 现有 `operations/` units 继续有效，但后续可分别补充 `observables/` 与 `execution/`
  层，而不将它们混为 generic feature recognition 或工具 API。
- IR/SDK 仍是独立、证据驱动的实现提案，不是知识库扩张的自动结果。
- 此决策不改变 Harness、可执行 manifest、provider、训练、runtime 或任何资产状态。
