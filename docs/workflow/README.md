# 开发工作路由

本目录负责维护 Brep2Code 实现仓的开发工作流入口。这里的 `workflow` 指开发协作路由，不指 Harness 运行时的受限 workspace。

## 路由顺序

1. 从根目录 `AGENTS.md` 进入仓库规则。
2. 读取 `docs/handoff/active/` 最新交接，确认当前上下文。
3. 读取 [`status.md`](status.md)，确认当前状态、active workpack 与下一步。
4. 若状态页列出 active workpack，则从 `docs/workpacks/active/` 领取；若为“无”，按状态页的下一工作创建或等待用户确认新的 workpack。
5. 按 `docs/modules/README.md` 找到模块文档和代码路径。
6. 完成后更新 workpack、handoff；若产生架构决策，补 ADR。

若入口文档之间状态不一致，以 [`status.md`](status.md) 为当前状态裁决器；先核验 workpack 和验收证据，再回补过期索引。

## 文档职责

| 路径 | 职责 | 不负责 |
|------|------|--------|
| `docs/architecture/` | 架构、契约、ADR、v1 设计 | 分发具体开发任务 |
| `docs/modules/` | 模块到代码的对照、模块边界 | 记录长篇研究背景 |
| `docs/workpacks/` | 可领取、可验收的开发任务包 | 替代 handoff |
| `docs/handoff/` | 跨会话恢复上下文 | 拆分任务 backlog |
| `docs/runbooks/` | 可重复操作步骤 | 解释架构取舍 |
| `docs/links/` | 外部论文库索引 | 复制论文正文 |

案例准备度的低上下文导航见
[`docs/corpus/case-portfolio.md`](../corpus/case-portfolio.md)；已终态 hosted
实验及其解释边界见
[`hosted-experiment-registry.md`](hosted-experiment-registry.md)。两者均不替代
`status.md`、workpack、报告、manifest 或授权记录。

常见提问如何路由到对应 authority，以及答案最终应维护到哪里，见
[`question-routing-and-authority.md`](question-routing-and-authority.md)。该页是
提问导航，不替代 theory、runtime、asset、status 或 hosted authority。

## 按任务问题路由

在完成本页的恢复顺序后，按问题进入相应权威，而不是从一个导航页推断另一层的
权限：

| 问题 | 入口 | 继续路径 |
|---|---|---|
| 什么受限 hypothesis 有证据、边界和缺口？ | [`项目理论地图`](../architecture/v1/project-theory-map.md) | M146 crosswalk → knowledge unit / decision package |
| Q01--Q04 如何执行、门控或修复？ | [`pipeline.md`](../architecture/pipeline.md) | 相关 contract / module；crosswalk 只提供边界 |
| 一个资产的 identity、split、lifecycle 或准入是什么？ | `case.json` / registry / admissions | case portfolio；不由 crosswalk 覆盖 |
| 现在能领取或实施什么？ | [`status.md`](status.md) | active workpack / active handoff；deferred 仅是导航 |
| 是否可作 hosted 请求？ | provider runbook 与 hosted preflight | selected G3 workpack、独立 review、逐项授权 |

新的 case、code 或 evaluation proposal 在适用时记录 M146 `hypothesis_id`
（或无关理由）、Q01--Q04 decision、evidence role、counterexample、stop rule
与 adoption boundary。该记录只缩小提案范围；不能转移权威或绕过 lifecycle/G3
授权。

若问题本身是在区分“开发侧 hypothesis / runtime contract / hosted 结果”三层，
或需要判断某类答案应写回 crosswalk、contract、campaign 还是 status，先读
[`question-routing-and-authority.md`](question-routing-and-authority.md)。

## 当前执行状态

当前里程碑、active workpack、下一步、完成项与 backlog 统一维护在 [`status.md`](status.md)。本页不重复动态状态；workpack 的详细范围和验收以其文件为准。

当前项目主线、三条支撑路线与其非主张见
[Current Project Route](../architecture/v1/current-project-route.md)。历史
[四轨项目路线](../architecture/v1/four-track-program-roadmap.md)仍是案例治理、
参考投影与未来 campaign 设计的组合导航；它不定义当前默认队列。每个 workpack
必须声明唯一主路线；跨路线依赖需要显式写入 scope，且不产生 hosted 或 runtime
授权。

若当前任务是在梳理 hosted 评测范围、有限案例/参考边界、五家族 portfolio
或批量 campaign 口径，先读
[`../architecture/v1/current-hosted-evaluation-framing.md`](../architecture/v1/current-hosted-evaluation-framing.md)。
该页不替代四轨路线，只为现阶段评测提供统一解释层；旧路线文档在未被 active
workpack 点名时视为背景证据，而不是当前选择队列。

若当前任务已经进入某个具体 hosted campaign 的冻结与授权准备，再读
[`../runbooks/hosted-campaign-charter-template.md`](../runbooks/hosted-campaign-charter-template.md)。
它用于统一 campaign charter、preflight 与 terminal interpretation 字段，不替代
workpack 或授权本身。

若当前任务是在判断五家族里谁能进入下一批 hosted 候选、谁还缺离线证据，读
[`../architecture/v1/current-hosted-batch-candidate-plan.md`](../architecture/v1/current-hosted-batch-candidate-plan.md)。
该页只做现阶段候选排序和离线缺口梳理，不替代四轨路由或具体 campaign workpack。
