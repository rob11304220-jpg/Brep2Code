# ADR-0003: v1 采用 Harness-first 方向

- **Status**: Accepted
- **Date**: 2026-07-16
- **Context**: 早期 v1 文档同时展开 B-Rep 编码器、IR、SDK、CAD 后端和评测路线，容易在代码未落地前过早收敛。当前目标是先得到可运行、可观测、可迭代的闭环。

## Decision

1. v1 优先搭建 Harness：workspace、tool-calling、脚本执行、门控、trace、repair loop。
2. 调用通用 hosted LLM；不做本地部署、训练或微调。
3. Q01 采用 probe-first：LLM 按需调用 B-Rep 查询工具，不先做统一编码器。
4. Q02 采用 script-first：LLM 先写可执行 CAD 脚本；固定 IR、完整 SDK 和 CAD workplace 延后。
5. 从案例、资产和失败信号中反向决定是否引入 IR、SDK、专用表示或 CAD workplace。

## Consequences

- **Positive**: 更快得到实验闭环，降低早期路线噪声。
- **Positive**: 案例数据会直接指导后续抽象，而不是由文献路线先行锁死实现。
- **Negative**: 初期脚本质量和一致性依赖通用 LLM 与反馈设计。
- **Mitigation**: Harness 必须保存 trace、版本和结构化信号，支持后续系统性复盘。
