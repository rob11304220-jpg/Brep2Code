# Development

A change starts with a problem and observable acceptance condition. Implement
the smallest slice, add focused tests, run Ruff and relevant tests, then commit
when requested. Ordinary changes need no governance artifact. Changes to
sandboxing, secrets, or provider egress require explicit tests and review of
their boundary. Run artifacts belong under `runs/` and are not documentation.

Use `D:\coderemote\Brep2Code_new` on `codex/v2-lean-rebuild` as the default
checkout. At task start, inspect the current directory, branch, dirty status,
worktree ownership, and HEAD relationship once. Continue in place when they
match; do not create or switch worktrees without a concrete need. An unrelated
detached worktree can remain in place. Stop before editing if the expected
branch is owned elsewhere or the current checkout has an unexpected HEAD.
Preserve all pre-existing changes as user work and keep them out of task commits.

The commit boundary is one smallest tested vertical slice: one observable
behavior change, its focused tests, and only the schema, case metadata, or docs
required by that behavior. Once Ruff and the relevant tests pass, treat that
slice as independently committable instead of accumulating it with the next
stage. Do not mix case expansion with unrelated CLI refactoring, hosted config
with runner development, or behavior changes with broad formatting. Commit
only when requested; when a task explicitly requests staged commits, commit
each verified slice before starting the next one. Commit messages should name
the behavior delivered rather than the work period or checkpoint.

The contract-first L2 entry slice is implemented: one unified action envelope,
one `edge_candidates` probe, one allowlisted `ocp_symbol` reference tool, and a
controller for `probe`, `retrieve`, `submit`, and advisory `finish`. Model
request, probe, retrieval, script submission, execution, repair, token, and cost
budgets remain independent. The active loop has deterministic fake coverage, a
validated five-cohort decision gate, unified hosted readiness, and a narrowly
bounded fresh-root live path for one runtime case.

The current phase is post-pilot diagnostic refinement. Classify stable hosted
failures and reproduce them offline before changing behavior. Prefer bounded
compatibility diagnostics for unambiguous Python/OCP binding mistakes, preserve
execution budget when rejecting them before the sandbox, and attach a
`reference_topic` only when the exact topic is already allowlisted. Do not make
prompt tuning, larger request/repair budgets, or broader hosted cohorts the
default response to a failed pilot.

L2 edge observations use unique indexed subshapes and bounded, path-free
geometry keys. Each edge can expose analytic curve parameters, parameter range,
local tangent, adjacent face IDs, and a sampled dihedral classification. The
probe also returns bounded face-edge incidence plus parallel and collinear line
groups. Additional OCP binding guidance belongs in the `ocp_symbol` allowlist,
not in the active system prompt.

The fake active pilot decision gate consumes validated saved results for the
nominal, parameter-variation, failure-sensitive, control, and held-out cohorts.
Its artifact preserves action order, independent budget usage, terminal
classification, and the comparison with the fixed fake pilot. Passing every
check permits only a later request for one fresh hosted authorization; it does
not carry authorization state and does not run a provider.

The controller proof required before hosted expansion is a deterministic fake
provider sequence: probe edge candidates, retrieve `TopoDS.Edge_s`, submit a
candidate, receive typed geometry feedback, submit one repair, and pass. Keep
that proof passing as an entry gate for any future hosted expansion; do not
replace it with a general-purpose agent or an additional hosted pilot.

Keep active hosted readiness separate from execution. Preflight must remain
credential-free; config-check may read provider configuration but must remain
network-free and redact credentials. An execution entry point requires its own
secure-backend readiness test, exact outbound projection, fresh itemized
authorization, and controller/provider budget binding. Continuation requires a
new authorization rather than inheriting permission from the interrupted run.

Classify a failure before changing behavior: provider protocol and accounting,
OCP compatibility/runtime diagnostics, observation or probe coverage,
controller/session policy, or modeling-asset projection. Provider adapters
normalize transport and usage; compatibility checks diagnose binding mistakes;
probes reduce geometric uncertainty; the controller allocates actions; approved
references supply modeling knowledge. Add prompt rules only for stable general
constraints, not as the default response to a hosted or case-specific failure.

Do not add workpacks, handoffs, status ledgers, route maps, or evidence ledgers.
Preserve durable direction in README.md, the three files under docs/,
machine-readable schemas, registry/case metadata, tests, and Git history.
Keep generated campaign trees under runs/; do not add root-level experiment
snapshots as permanent project documentation.

## L0-L6 能力梯子与遗留案例路线

本节是开发者路线说明，不是用户能力承诺，也不是 hosted campaign 授权。
`capability_level` 是新仓库用于机制、案例和报告聚合的语义等级；旧仓库的
`P0`--`P3` 是案例/证据层级，不能直接当作能力等级。案例数量、参数数量或
单次 hosted 通过都不能单独证明某个 L 等级已经实现。

### 能力等级定义

| 等级 | 开发目标 | 当前/候选机制 | 代表性案例或机制族 | 状态 |
|---|---|---|---|---|
| L0 | 独立 primitive 和 analytic-surface 构造 | `primitive`, `analytic_surface` | `box`, `cylinder` | 已实现 |
| L1 | 单个有序 boolean feature sequence | `boolean_cut` | through cut、blind cut | 已实现 |
| L2 | 基于边/面的单特征构造 | `fillet`, 后续 `chamfer` | `filleted_box`, `chamfered_block` | fillet 已实现，chamfer 未迁移 |
| L3 | 多特征有序构造与依赖关系保持 | additive fuse、repeated cut、dependent cut、counterbore | `box_cylinder_union`, `three_hole_plate`, `counterbored_plate`, `stepped_block`, `boss_with_blind_hole`, `additive_boss_dependent_cut` | 规划中 |
| L4 | 拓扑语义选择与结构化轮廓建模 | face selection、multi-contour、multi-inner-loop、rounded slot | `face_selected_cut_*`, `multi_contour_pocket_*`, `multi_inner_loop_pocket_*`, `oriented_rounded_slot_*` | 规划中 |
| L5 | 重复特征、参数变化和受控几何泛化 | repeated feature pattern、参数族、held-out split | `repeated_feature_pattern_centered/offset` 及 `low/nominal/high` 变体 | 规划中 |
| L6 | 非棱柱体和复杂拓扑建模 | revolve、shell、rib；后续可独立评估 sweep、loft | `revolve_centered/offset`, `shell_symmetric/asymmetric` | 规划中 |

这个映射是根据遗留案例库和机制路线归纳出的开发目标，不是旧仓库曾经正式
使用的 L3--L6 编号。旧路线的 hosted 准备顺序是按证据成熟度排列的，不能
解释成能力等级顺序。

### L3-L6 的验收边界

- **L3** 必须验证操作顺序和依赖关系，而不只验证最终 bbox、volume 或 topology。
  例如 `base -> boss/fuse -> dependent cut` 中，切削必须作用于正确的前置
  结果，且不能退化成独立 cut。
- **L4** 必须验证选择对象的拓扑语义。唯一面、外轮廓、内轮廓、岛屿和方向
  必须有可观察的角色；wrong-face、ambiguous-selector、wrong-frame 等控制
  必须 fail closed。
- **L5** 必须验证实例数量、位置、间距和尺寸变化，并保持 development/held-out
  参数族隔离。它只能支持冻结参数族内的受控泛化结论，不能直接宣称通用参数
  泛化。
- **L6** 必须验证 profile、axis、angle、direction、opening、thickness 或
  attachment 等非棱柱/复杂拓扑语义。`revolve`、`sweep`、`loft` 是独立机制
  族；`shell` 和 `rib` 也应分开设计，不能合并成一个泛化的 complex-CAD 级别。

每个新等级必须依次具备：机制 registry 定义、冻结的 sequence grammar、
development/held-out 案例、正负控制、适用的 geometry/semantic/editability
gates、停止规则，以及对应的 focused tests。没有这些契约时，只能标记为
候选机制，不能加入 capability 聚合或 runtime manifest。

### 遗留案例库的开发价值

遗留仓库的 `case-library/self-authored` 包含 101 个案例：P0 为 3 个、P1
为 10 个、P2 为 83 个、P3 为 5 个。它们不是新仓库的 runtime 输入，也不应
整体迁移。应按机制族逐个审计并重新建立新仓库的 `case.json`、`dossier.json`
和 manifest。

当前最有价值的候选机制族包括：

- 多特征依赖：`box_cylinder_union`、`three_hole_plate`、`counterbored_plate`、
  `stepped_block`、`dual_boss_plate`、`boss_with_blind_hole`、
  `additive_boss_dependent_cut_*`；
- 拓扑选择与结构化轮廓：`face_selected_cut_*`、
  `multi_contour_pocket_*`、`multi_inner_loop_pocket_*`、
  `rounded_slot_*`、`oriented_rounded_slot_*`；
- 重复特征和受控变体：`repeated_feature_pattern_*`、
  `reference_guided_through_hole_*` 以及各机制的 centered/offset、
  low/nominal/high 族；
- 非棱柱和复杂拓扑：`revolve_*`、`shell_*`，以及后续独立设计的 `rib`、
  `sweep`、`loft` 候选；
- 横向鲁棒性：`small_cylinder`、`large_box`、`thin_plate`、side-hole、
  orientation 和 topology-pair 案例。

横向鲁棒性不是单独的 L 等级。尺度、单位、方向、薄壁、近切和退化条件应
作为跨等级的 stress family，配合非退化正例、失败分类和停止规则使用。

### 推荐的实现顺序

```text
L0-L2 当前闭环诊断
  -> L0-L2 小规模 development/held-out pilot
  -> L3 多特征依赖
  -> L4 拓扑选择与结构化轮廓
  -> L5 重复特征与受控泛化
  -> L6 revolve / shell / rib 等复杂机制
```

实际机制族的 hosted 顺序可以不同。例如遗留路线曾把 repeated feature
pattern、axisymmetric revolve、dependent face selection 和 multi-inner-loop
pocket 排成一个证据批次；这是因为它们的 dossier 和离线 evidence 已经
准备好，不表示它们的能力等级顺序高于或低于 L3/L4/L5。

新机制的落地边界仍然是：先完成离线 dossier 和 family freeze，再完成受控
production/review，最后才考虑单独选择的 hosted campaign。成功的 replay、
reference script 或 case card 本身不会自动产生 runtime card、manifest admission、
provider scope 或新的 capability claim。

## Hosted pilot phase gates

| Gate | Prerequisite | Recommended command | Successful output | Reads config | Executes generated code | May cost | Creates artifact |
|---|---|---|---|---|---|---|---|
| Case freeze | Case assets, metadata, dossiers, and manifests are final. | `uv run brep2code cases validate` | `status: valid` with the frozen case count | No | No | No | No |
| Control / held-out freeze | Campaign control and held-out matrices match the frozen cases. | `uv run brep2code campaign validate --contract <contract>` | `status: valid` with the expected control count | No | No | No | No |
| Fake pilot validated | A completed fake pilot tree exists. | `uv run brep2code campaign pilot-validate --contract <contract> --result <fake-result>` | `status: valid` | No | No | No | No |
| Hosted contract readiness | Provider, model, limits, cohorts, and a fresh target root are selected. | `uv run brep2code campaign pilot-preflight <hosted arguments>` | `status: ready` with cohort routes and budget | No; it does not read keys | No | No | No |
| Provider configuration readiness | Hosted contract readiness passes and fresh hosted authorization is present. | `uv run brep2code campaign hosted-pilot-config-check <hosted arguments>` | `status: ready` with only the endpoint host and bounded configuration | Yes, including the key | No; it makes no network requests | No | No |
| Hosted execution authorization | A person confirms endpoint host, provider, model, limits, cost ceiling, and a new run root for this execution. | Review the exact `hosted-pilot` command; do not run it until confirmed. | Fresh explicit authorization | No | No | No | No |
| Saved-result validation | The authorized hosted pilot finished and saved all four results. | `uv run brep2code campaign hosted-pilot-validate --contract <contract> --result <hosted-result>` | `status: valid` with mixed-provider routing | No | No | No | No |

`pilot-preflight` never reads secrets or connects to a provider.
`hosted-pilot-config-check` reads local provider configuration but remains offline.
Only `hosted-pilot` reads configuration and may send hosted requests, incur cost,
execute generated code in the secure backend, and create a run artifact tree.

Case changes must update the case metadata and its split manifest together.
Run `brep2code cases validate` after copying a STEP asset; use the computed
asset hash rather than trusting legacy metadata. Every admitted case must also
have a validated dossier.json. Its modeling and Harness fields are not runtime
inputs. Update the shared mechanism registry when adding a mechanism, and let
the validator reject drift between the case, registry, dossier, and campaign
contract.

Use the fake provider for repair-loop development. Its script queue is finite,
so request accounting and revision budgets remain deterministic. Inspect
`result.json` plus each revision's request, response, script, and output when a
loop fails. Do not run untrusted generated scripts with the local executor.

Use `--initial-script` for a controlled repair experiment. The initial script
occupies revision zero, runs through the same untrusted backend, and consumes
no provider request. Later revisions receive its complete source plus bounded
execution or geometry feedback. `max_rounds` counts the initial revision, so
the number of fake scripts and hosted provider rounds is `max_rounds - 1`.

The local executor is limited to trusted fixtures and developer-authored smoke
scripts. Provider responses run through `run_untrusted_build`, which requires
the verified `Ubuntu-24.04` WSL2/bubblewrap backend and fails closed when that
backend is unavailable. Its focused integration tests cover filesystem and
environment isolation, network denial, timeout, descendant/process bounds,
memory, stdout/output size, and an OCP-to-STEP positive control.

## Local Windows and WSL2 setup

The secure integration and end-to-end tests need the same backend as a real
provider run. The host must have WSL2, an `Ubuntu-24.04` distro, and the
project runtime installed at `/home/liaol/.brep2code-runtime`. That runtime
must contain Python, OCP, `bwrap`, `prlimit`, and `timeout`. Generated scripts
must never run through the trusted local executor.

Use these read-only checks before debugging a failing test:

```powershell
wsl.exe --status
wsl.exe -l -v
wsl.exe -d Ubuntu-24.04 -- sh -lc "command -v bwrap; command -v prlimit; command -v timeout; test -x /home/liaol/.brep2code-runtime/bin/python"
```

The distro must be running as version 2. If `wsl.exe` reports
`Wsl/Service/E_ACCESSDENIED`, repair the host service/distro access first;
the application now records this as `sandbox_unavailable` instead of
misreporting it as a generated-script error. A practical recovery sequence is
to close active WSL terminals, run `wsl.exe --shutdown`, start Windows
Terminal or PowerShell with the account that owns the distro, and repeat the
three checks. If enumeration is still denied, repair or recreate the distro
from Windows Settings/WSL administration rather than weakening the sandbox.

Pytest is configured to keep `tmp_path` under a unique project-local directory
named `.pytest-tmp-<process-id>`, so it does not depend on permissions of the
user-wide Windows temporary directory and stale WSL-created files do not block
the next run. If a previous run left an ACL or locked handle, close
Python/pytest processes and remove only an accessible project-local directory
before retrying:

```powershell
Remove-Item -LiteralPath .pytest_cache -Recurse -Force -ErrorAction SilentlyContinue
uv run pytest -q
uv run ruff check src tests
```

The expected validation order is:

```powershell
uv sync --dev
uv run brep2code cases validate
uv run pytest -q
uv run pytest --run-secure -q
uv run ruff check src tests
```

If WSL is intentionally unavailable, unit tests and case validation can still
run; the default pytest command skips tests marked `secure` and reports the
backend reason. After the WSL checks pass, `--run-secure` is required for the
full security and end-to-end gate. Never switch those runs to the trusted local
executor as a workaround.
