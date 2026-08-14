---
type: review
related-project: Brep2Code
status: completed
milestone: M69
updated: 2026-08-09
---

# M69 项目进度、路线与改进评审

## 裁决与范围

本评审整理截至 M69 的已验收工作和后续路线。它是规划与改进
输入，不激活任何 workpack，也不授权 runtime 改动、provider 请求、
外部数据或预算复用。当前工作状态仍以
[`status.md`](../../workflow/status.md) 为准。

## 近期进度摘要

| 区间 | 已完成的可复用成果 | 证据边界 |
|---|---|---|
| M42–M54 | 观测优先的 first-pass/repair 运行契约、单例 secure smoke 与固定 development 预检 | 仅为受限 Harness 工程证据；不构成模型质量或泛化结论。 |
| M57–M60 | 终端 interruption checkpoint、provider worker 期限与 observed-development 生命周期投影 | 超时可被可靠记录和 fail-closed 计费，但不能由此判定根因。 |
| M61–M62 | 独立验证窗口规划和离线测试反馈基线 | 测试选择可审计；不产生 hosted 授权。 |
| M63–M64 | 新鲜预检与一对控制/CAD 超时判别 | 最小控制及时返回、同一 CAD 请求在 300 秒超时；排除简单的全局 endpoint/auth 失败，未证明任务复杂度或网络根因。 |
| M65–M68 | 内容零保留的上下文/时延遥测、超时投影、独立病例报告和传输阶段观测 | 可区分本地阶段与 provider wait；非流式 adapter 不提供独立 TTFT/response-header 时间。 |
| M69 | 顺序 control/CAD 诊断 | control 完成，CAD 在 `http_started` 后 300.029 秒超时；支持 request-specific wait，不能归因于网络、provider 内部或 CAD 几何复杂度。 |

所有 M63–M69 hosted 报告的预算均已结算；`running`、`interrupted`
与名义剩余额度都不可复用。终态解释与报告入口见
[hosted experiment registry](../../workflow/hosted-experiment-registry.md)，
而 milestone/acceptance provenance 见
[milestone history](../../workflow/milestone-history.md)。

## 已确认的当前能力与缺口

| 维度 | 当前强项 | 仍需解决的缺口 |
|---|---|---|
| Q01 上下文 | path-free、受限观测输入与本地时延分段已具备 | 尚无可比较的 token、TTFT 或流式 transport 证据。 |
| Q02/Q04 | first-pass、受限 repair 与失败分类已存在 | 在 provider wait 未稳定前，无法把失败归因于脚本生成或 repair 策略。 |
| Q03 执行与安全 | `wsl-bwrap`、gate 与 fail-closed checkpoint 已建立 | 应保持与 provider 生命周期问题隔离，避免为超时放宽 gate。 |
| 观测性 | worker/HTTP/complete-response 生命周期及内容零保留遥测可用 | 非流式 API 只能看到完整响应；不能从一个超时样本定位 transport/provider 内部阶段。 |
| 实验设计 | 固定输入、单请求预算、独立报告与 no-retry 纪律健全 | 缺少对兼容性模式的离线契约和长期批次的耐久监控。 |
| 治理与交付 | G2/G3 reviewer、preflight、审计和 handoff 路径明确 | 状态页与 workpack 已很严格，但 M70–M73 原先只有摘要，难以直接领取与验收。 |

## 改进优先级与路线

```text
M70 durable monitor (G2, offline)
  -> M71 compatibility diagnostics (G2, offline)
  -> M72 stability-only experiment (G3, fresh preflight + authorization)
  -> [stability gate passed] M73 output-contract / repair correctness (G2)
```

1. **P0：先补齐 M70 耐久监控。** 将报告状态转换为 heartbeat、terminal
   handoff 和 operator-visible outcome；监控只能观察自身自动化状态，绝不
   重试、发请求、变更请求或消耗预算。这解决 hosted 批次可能超过交互窗口的
   交付风险，而不是解释超时。
2. **P0：完成 M71 离线兼容性诊断。** 以 fixture 和 worker boundary 测试锁定
   非流式/流式策略、JSON 输出信封、响应大小和安全控制 metadata 的兼容边界。
   这使未来试验有可复现的候选模式，而不会在远程运行中临时调参。
3. **P1：仅在 M70/M71 验收后提出 M72。** 其 preflight 必须预注册 mode、
   development case、每报告一请求、deadline、总预算、停止条件和新的报告路径；
   获得逐项 G3 授权后才可运行。稳定性门槛应至少要求所有预注册请求都有可解析
   的 terminal report，且无 provider timeout/生命周期错误；任何失败均停止并回到
   离线诊断，不扩大样本寻找成功案例。
4. **P1：M73 只在稳定性门槛满足后激活。** 单独处理 JSON/schema 验证、OCP
   type-safety 与结构化 repair feedback。不得以削弱 gate、隐藏 provider error
   或混合 latency 与正确性指标来获得通过。

## 不建议当前进行的改动

- 不做无界 retry、并发放大、endpoint 切换或 prompt/context 重写；它们会破坏
  M69 的归因边界。
- 不以少量 control/CAD 样本发布 provider、网络或模型性能结论。
- 不修改 manifest、案例 split、sandbox 或 geometry gates 来回避 provider wait。
- 不在 M72 前扩展 held-out、外部数据、runtime retrieval 或 CAD 正确性工程。

## 维护建议

- 将 M42–M69 摘要补入里程碑历史，使 `status.md` 保持简洁而历史可导航。
- 将 M70–M73 都补全 Scope、依赖、验收、停止规则和状态迁移，保持可领取而不自动
  激活。
- 每次完成 G2/G3 工作后，继续以 `status.md → workpack → handoff` 的顺序更新；
  关闭时运行 `uv run python tools/check_governance.py`。

## 相关记录

- [Hosted experiment registry](../../workflow/hosted-experiment-registry.md)
- [Post-M48 closed-loop roadmap](post-m48-closed-loop-roadmap.md)
- [Provider configuration and authorization runbook](../../runbooks/llm-provider-config.md)
- [Task lifecycle](../../workflow/task-lifecycle.md)
