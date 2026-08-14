---
type: index
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
---

# Brep2Code v1 — 架构索引

当前 v1 方向：Harness-first。LLM 通过 probe tools 按需理解 B-Rep，编写 CAD 脚本，Harness 执行、门控并返回结构化反馈。

## 必读

- [README.md](README.md)
- [architecture.md](architecture.md)
- [decisions.md](decisions.md)
- [contracts/probe-tools.md](contracts/probe-tools.md)
- [contracts/build-script.md](contracts/build-script.md)
- [contracts/signal-bundle.md](contracts/signal-bundle.md)
- [milestones/README.md](milestones/README.md)

## 暂缓

- B-Rep 编码器路线。
- 固定 modeling IR。
- 完整 Domain SDK。
- 建模序列 DSL / schema。
- CAD workplace。
- 本地部署和微调。

早期允许实现 runtime helper 和 CAD execution adapter；它们只服务脚本执行、路径管理、artifact 和 trace，不承载 CAD 建模语义。
