# Hosted 实验结果注册表

本页将已完成或终态的 hosted 实验放入一个可审阅索引。它不是 report schema、
预算账本、provider 配置、授权记录或 benchmark；每一行只能作链接到的 frozen
policy、workpack 和 terminal report 所允许的解释。`running`/`interrupted` report
不提供可复用额度。

## 读表规则

- `pass` 仅代表该行固定 case/policy/gate 的终态通过；不是模型、卡片或方法的总体成功率。
- `timeout`、`script/API failure` 与 `geometry failure` 分别报告，不能合并为 CAD 能力指标。
- 早期 corpus/ABC 路线与 M48 后 observation-only/reference-assisted 路线使用不同策略，标为历史而非可直接比较样本。
- `data/corpus-runs/` 和 `data/monitor-runs/` 是 Git-ignore 的本地证据路径；克隆中缺失时以对应 workpack/review 为准，不能补跑或复用预算。

## 已归档实验索引

| Experiment / scope | Fixed scope and terminal result | Local evidence | 允许的解释 |
|---|---|---|---|
| M6 P0/P1 early corpus | P0 首轮 1/3 pass，两个 repair pass；P1 retry 3/3 repair pass；`box_cylinder_union` provider timeout | `deepseek-p0-flash-20260801.json` 等；[M6 review](../architecture/v1/m6-hosted-evaluation-report.md) | 历史 Harness/repair evidence，非当前策略基线 |
| M9 ABC first-pass | development 8、held-out 4 的固定 ABC split；脚本失败、provider lifecycle 与少量 gate pass 分离记录 | `abc-v00-m9-001-*.json`; [M9 review](../architecture/v1/m9-abc-hosted-evaluation-review.md) | 外部 B-Rep-only Harness 工程证据，不是 benchmark |
| M51 `box` secure smoke | 一次 observation-only、无输入挂载的 `box` 请求通过 output/geometry gates | `m51-box-deepseek-observation-first-pass.json`; [M51 workpack](../workpacks/done/WP-M51-001-single-case-secure-llm-smoke.md) | 一个安全闭环 smoke |
| M63--M72 stability diagnostics | control/CAD request 分别出现成功与 timeout；M72 按 no-retry 关闭 | `m63-*` 至 `m72-*`; [M69 review](../architecture/v1/m69-project-progress-and-improvement-review.md) | request-specific lifecycle evidence，不能归因网络、模型或几何复杂度 |
| M80-v2 control + `box` | control completed；`box` provider response 返回，但生成脚本导入 `cadquery`，无 output | `m80-v2-*.json`; [M80 workpack](../workpacks/done/WP-M80-001-minimal-p0-end-to-end-revalidation.md) | endpoint 可响应；当前脚本 API/execution contract 未通过 |
| M85 `cylinder` reference-assisted | 固定 final-primitive role、一个 card、2/2 requests，全部安全与 geometry gates pass | `m85-cylinder-reference-assisted.json`; [M85 workpack](../workpacks/done/WP-M85-001-reference-assisted-p0-hosted-smoke.md) | 单一固定 primitive-role smoke |
| M87 `block_with_hole` reference-assisted | 固定 single-boolean-cut role、同一 card、2/2 requests，pass 且 provenance 为 independent reconstruction | `m87-block-with-hole-reference-assisted.json`; [M87 workpack](../workpacks/done/WP-M87-001-reference-assisted-p0-block-with-hole-hosted-smoke.md) | 单一固定 cut-role smoke |
| M89-001 `three_hole_plate` | 第二 provider boundary timeout；2/2 requests consumed，未生成脚本 | `m89-three-hole-plate-reference-assisted.json`; [M89-001 workpack](../workpacks/done/WP-M89-001-reference-assisted-p1-three-hole-plate-hosted-smoke.md) | request-specific timeout，不能判断 card/CAD correctness |
| M89-003 `three_hole_plate` | 4096-token cap、同一 role/card、2/2 requests，no-input executor 和所有既有 gates pass | `m89-003-three-hole-plate-bounded-output.json`; [M89-003 workpack](../workpacks/done/WP-M89-003-bounded-output-reference-assisted-retry.md) | 一次有界 P1 成功；不能归因 token cap 或推广 card |
| M97-001 development calibration | 3/9 issued 后 card script API failure、baseline timeout，terminal interrupted | `m97-reference-guided-through-hole-development-calibration.json`; [M97-001 workpack](../workpacks/done/WP-M97-001-reference-guided-parameter-variation-development-hosted-calibration.md) | 混杂的失败证据；不支持 calibration 或 held-out |
| M97-003 development calibration | 三个 development rows：card 3/3 pass，baseline 2/3 pass；9/9 issued | `m97-003-reference-guided-through-hole-development-calibration.json`; [M97-003 workpack](../workpacks/done/WP-M97-003-reference-guided-parameter-variation-refrozen-development-calibration.md) | development-only terminal evidence，不能作 card effect、泛化或 M98 权限结论 |
| M97-004 retained-evidence audit | nominal baseline 是 `BRepPrimAPI_MakeBox` constructor-arity runtime error；其余五个条件按原报告保留 | [M97-004 audit](m97-004-development-terminal-attribution-review.md) | development-only API-use counterexample；不补样、不重试、不解锁 M98 |
| M118 fresh hosted stability | `three_hole_plate` development row，2/2 requests issued；terminal `provider_error` with `missing_script_update`，无可执行脚本进入后续 gate | `m118-three-hole-plate-stability.json`; [M118 workpack](../workpacks/done/WP-M118-001-fresh-hosted-stability-preflight.md) | 一次新的稳定性失败证据；不能激活 `TRG-005`、不能进入 calibration、不能复用 report/monitor/budget/authorization |
| M127 shared stability re-entry | `three_hole_plate` development row，DeepSeek V4，2/2 requests issued；lifecycle completed within 300 seconds，第二个生成脚本因不可用 `OCP.STEPControl.STEPControl_STEPModelType` 被静态 API contract 拒绝 | `m127-three-hole-plate-stability-reentry.json`; [M127 workpack](../workpacks/done/WP-M127-001-shared-hosted-stability-reentry.md) | 单一固定路径的 script/API failure；不代表 provider lifecycle、模型、card 或几何能力结论，sandbox/provenance 与下游 gates 未评估，预算/路径/授权不可复用 |

## 当前未执行项

[`WP-TRG-009`](../workpacks/deferred/WP-TRG-009-held-out-parameter-variation-evaluation.md)
和 [`WP-TRG-010`](../workpacks/deferred/WP-TRG-010-parameter-variation-evidence-review.md)
仍是 deferred。M97-003/004 的完成不会自动选择 held-out evaluation；任何 held-out hosted
实验仍需新 workpack、通过 preflight、全新 report/monitor path 与逐项明确授权。

## 每个新 hosted 终态应补充的字段

新增条目必须链接并写清：固定 policy/split 与 cases、provider/model、条件和最大
请求数、issued/remaining accounting、terminal lifecycle、script/API/sandbox、
provenance、geometry/semantic/editability gates 的适用状态、report/monitor path，
以及允许与禁止的结论。若某种 gate 未在该实验的运行时路径执行，写 `not evaluated`，
不可借用离线 oracle 的通过结果填为 hosted pass。

维护步骤见 [`evidence portfolio maintenance`](../runbooks/evidence-portfolio-maintenance.md)。
