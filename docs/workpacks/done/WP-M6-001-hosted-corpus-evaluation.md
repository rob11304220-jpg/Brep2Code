# WP-M6-001: Hosted Corpus Evaluation and Failure Taxonomy

- Status: done
- Milestone: M6
- Owner: unassigned

## Goal

Extend the manifest-driven P0/P1 corpus workflow into a bounded, auditable DeepSeek V4 repair evaluation that produces evidence for the next modeling, probe, gate, or productization decision. The evaluation is not a benchmark-quality claim and must not run until the user explicitly authorizes the hosted batch, including its budget.

## Scope

- Add an explicit hosted-evaluation mode to the corpus runner and CLI. It must select `DeepSeekProvider` only when the caller explicitly requests it, use the ignored local environment file, and route every provider-generated script through `wsl-bwrap`.
- Keep the existing local primary-run and fake-provider replay modes network-free and behaviorally compatible.
- Add a preflight that validates provider configuration, sandbox availability, manifest path, record/report destination, round limit, and declared run budget before any network request.
- Define a compact hosted-evaluation report schema. Record the manifest hash/path, provider/model identifier, prompt or policy version identifier, executor, max rounds, configured case/run budget, per-case primary and repair results, gate outcomes, retry/error class, sanitized trace paths, and a failure taxonomy.
- Classify failures at least as `provider_configuration`, `provider_request`, `provider_response`, `sandbox`, `script_execution`, `missing_output`, `output_probe`, `geometry_gate`, `repair_exhausted`, or `unknown`. Preserve the existing primary-run failure classification where applicable.
- Add network-free tests for argument validation, preflight refusal, report serialization, taxonomy classification, and enforcement that `--provider deepseek` uses the secure executor. A real hosted run remains manual and opt-in.
- Produce a runbook describing the authorization gate, secret handling, report location under ignored `data/`, budget declaration, interruption behavior, and how to review evidence without exposing credentials or full provider responses.

## Inputs

- `docs/architecture/v1/contracts/case-corpus.md`
- `docs/architecture/v1/contracts/repair-loop.md`
- `docs/architecture/v1/contracts/runtime-sandbox.md`
- `docs/runbooks/llm-provider-config.md`
- `docs/workpacks/done/WP-M3-004-hosted-provider-integration.md`
- `docs/architecture/v1/m4-review-report.md`
- `case-library/manifests/self-authored/p0.json` and `case-library/manifests/self-authored/p1.json`

## Code paths

| Path | Purpose |
|------|---------|
| `brep2code/cli/__init__.py` | Explicit hosted corpus flags and offline-compatible defaults. |
| `brep2code/corpus/runner.py` | Bounded hosted repair orchestration and failure classification. |
| `brep2code/corpus/report.py` | Versioned compact report serialization. |
| `brep2code/agent/provider.py` | Reuse provider contract; do not add a second provider abstraction. |
| `brep2code/agent/harness.py` | Secure-executor selection boundary, if integration requires it. |
| `tests/test_corpus_m4.py` or new focused tests | Network-free acceptance coverage. |

## Docs to update

- `docs/workflow/status.md`
- `docs/architecture/v1/contracts/case-corpus.md`
- `docs/runbooks/llm-provider-config.md` or a focused hosted-evaluation runbook
- `docs/modules/corpus.md`, if the CLI/report interface changes
- active handoff and this workpack on every status transition

## Trace/schema changes

The corpus report gains a versioned hosted-evaluation section and sanitized references to existing revision/provider traces. Do not store API keys, environment snapshots, or full provider responses in reports, metadata, or traces. Update the case-corpus contract before implementing the schema.

## Compatibility constraints

- Default commands remain offline, credential-free, and deterministic.
- Existing `corpus --repair` continues to use local `FakeLLMProvider` reference scripts.
- Hosted provider execution is DeepSeek-only for this workpack and is opt-in; no additional provider integration, fine-tuning, IR, CAD SDK, or CAD workplace is in scope.
- Provider-generated scripts must never use `unsafe-local`.
- Reports and record artifacts remain under ignored `data/`; committed fixtures and source must contain no credentials.

## Authorization gate

Before a real hosted batch, the user must explicitly approve the provider/model, maximum cases, maximum rounds per case, and a cost or request budget. Until then, implement and test only the offline code paths and preflight refusal behavior.

## Acceptance

- [x] Offline tests prove defaults make no provider request and do not require credentials.
- [x] Hosted mode refuses missing authorization/budget and invalid bounds before issuing a request; unavailable WSL is preflighted before provider construction.
- [x] Hosted mode has a schema-v2 sanitized evaluation section and repair failure taxonomy, covered by network-free serialization tests.
- [x] `CorpusRunner` rejects hosted providers unless its executor is `WslBubblewrapExecutor`; CLI selects that executor for `--provider deepseek`.
- [x] P0 and P1 can each be selected as bounded evaluation inputs.
- [x] A manual user-authorized P0 DeepSeek Flash run produced an ignored schema-v2 report at `data/corpus-runs/deepseek-p0-flash-20260801.json`; it used 2 of its 3-request budget and exposed no credentials.
- [x] Corpus reports are atomically checkpointed before the first case and after every completed case; handled interruption produces `run_status: interrupted` while preserving completed-case evidence, covered by network-free tests.
- [x] A stopped P1 retry retained its atomic `running` checkpoint with three completed cases and 3/4 requests used; external force-stop does not claim a false terminal state.
- [x] DeepSeek requests use an independently terminable per-request deadline (`--provider-timeout`, default 120 seconds); deadline expiry records `provider_request_timeout` without blocking later checkpoint/report handling.
- [x] Hosted request accounting increments when a request is issued, including timeout/error paths; network-free repair tests cover successful, exhausted, and provider-error request counts.
- [x] `uv run python -m pytest` completed as three bounded groups: 42 passed. The corpus group reported 13 passed in 61.02 seconds, although the outer 60-second tool wrapper returned 124 after pytest completed.
- [x] `uv run python -m ruff check .` passes.

## Out of scope

- Benchmark or model-quality claims.
- Public dataset download, new external corpus, or dataset-scale expansion.
- New modeling IR, project CAD SDK, CAD workplace, probes, or geometry gates unless a reviewed hosted-evaluation report demonstrates the need.
- Automated recurring hosted runs or spending authority.

## Notes

The offline-safe evaluator, contract, module boundary, and runbook are implemented. The authorized P0 Flash acceptance run completed with 1/3 primary passes and 2/2 repaired failures passing after one round. A separately authorized P1 Flash run was interrupted before its final report: completed revisions show `chamfered_block` and `three_hole_plate` repaired to pass, `filleted_block` still failed after one round, and `box_cylinder_union` did not finish. This is incomplete evidence, not a corpus result or benchmark claim.

The interruption exposed a follow-up gap within M6-001: the runner wrote the report only after all cases finished, so an interrupted batch had revision artifacts but no corpus-level summary. That gap is now addressed by atomic per-case checkpoints and a terminal `interrupted` state for handled interruption/runner exceptions. Any P1 retry still requires a new explicit request budget authorization.

## Result

M6 is complete. The final evidence boundary, P0/P1 outcome table, failure taxonomy, request-accounting caveat, decisions, and follow-up candidates are recorded in [`m6-hosted-evaluation-report.md`](../../architecture/v1/m6-hosted-evaluation-report.md). The result supports the hosted execution/recovery infrastructure, not a benchmark or a new modeling abstraction.

## 开发记录：踩坑与归档

- **现象**：P1 Flash 批处理在正式 report 写入前卡住并被终止。此前 runner 只在所有 case 结束时写 report，导致已有 revision artifact 却没有 corpus 级汇总；不能把这些零散 artifact 当作完整 P1 结论。
- **根因边界**：当前证据只能确认 final-report 单点写入缺少中断恢复能力；不将该事件归因于模型质量、DeepSeek 服务、WslBubblewrapExecutor 或几何 gate，除非后续有对应 trace/复现实验支持。
- **处理**：报告改为原子 checkpoint，并显式记录 `running`、`completed` 或 `interrupted`。外部强杀无法写最终状态，但最后一个已完成案例的 checkpoint 仍有效。
- **重试纪律**：中断 batch 的未用请求额度不得自动复用；P1 重试须重新获得模型、案例/轮次上限及成本或请求预算授权。
- **第二次验证**：启用 checkpoint 后的 P1 Flash 重试已完成 `filleted_block`、`chamfered_block`、`three_hole_plate` 三例；三者的 primary 均为 geometry-gate failure，均在一轮修复后通过，累计使用 3/4 请求。`box_cylinder_union` 长时间未完成，进程被外部停止；report 正确保留为 `running`、三例 completed checkpoint，而不是伪造 `interrupted` 或 `completed` 结论。
- **后续排障方向**：若需继续 P1，应先离线定位第四例的 provider/WSL 阶段耗时，并决定是否增加每案例 orchestration watchdog 与可处理的取消信号；在没有 trace 证据前，不将长时间运行归因于模型、provider、sandbox 或 geometry gate。
- **定位结果**：第二次 P1 retry 的 `box_cylinder_union` 初始与修复前 `wsl-bwrap` execution 分别约 0.93s 和 1.05s，均正常完成；修复前 revision 写入了 `llm_messages.jsonl` 请求记录，却没有 `provider_response.json`。因此证据将滞留范围缩小到 provider HTTP 调用，排除 CAD 脚本、沙箱执行和输出探测；不据此断言远端服务根因。
- **处理二**：DeepSeek completion 现在运行在独立可终止 worker 中，`--provider-timeout` 到期时产出 `provider_request_timeout`。fake-provider 不走该 worker，继续保持确定性本地测试语义。
- **单案例验证**：在新授权下仅运行 `box_cylinder_union`（Flash、1 轮、1 请求、120s deadline）。初始与修复前的 sandbox execution 正常，provider 在 deadline 后返回 `provider_request_timeout`；report 正确为 `completed`，该 case 分类为 `provider_request`，不再阻塞 corpus。
- **账本修正**：这次早期 validation report 错误显示 `requests_used: 0`，但 request trace 与 timeout 证明请求已经发出。原因是旧代码只在 repair 返回后扣减预算；现已改为在发起请求时计数，覆盖 timeout/error 路径。保留原报告作为历史 artifact，不回写伪造证据；归档摘要必须写明该报告的已知计数缺陷和实际 1 次请求。
- **归档时总结**：附上 P0 完整 schema-v2 report 路径、P1 checkpoint（含其 terminal/running 状态）、`box_cylinder_union` 单案例 timeout report、各 case revision/trace 路径、实际请求数、失败分类、超时配置与结果、测试命令与结果；明确 P0 是单次工程证据，P1 的旧部分 artifact 不是 benchmark 结果；确认报告和 trace 未含凭证。
