# 案例组合进度

本页是案例准备度的低上下文导航，而不是案例注册表、可执行 manifest、runtime
检索索引或 hosted 授权。数值基线与生命周期以每例 `case.json` 和
[`self-authored registry`](registry/self-authored.json) 为准；本页只把已有的
开发侧关系放在同一视图中。

## 先区分四种“卡”

| 材料 | 当前数量/范围 | 含义 | 不能推断 |
|---|---:|---|---|
| 人工 case card | 按 `docs/corpus/cases/` 维护 | 几何意图、尺寸、验证用途的人工审阅材料 | 有可供 LLM 使用的参考 |
| deterministic reference script | 92 / 95 物理 self-authored 目录 | 本地 replay/oracle 资产 | 唯一逆序列或 runtime 输入 |
| development reference pack | 7 个 P0/P1 cases | hash-bound 的紧凑开发元数据 | runtime 可见、自动检索或 hosted 授权 |
| runtime experience card | 5 个 experimental cards | 经独立审计的受限 runtime projection | 泛化建模知识；默认不启用，只有 M19-003/M158 的显式 revision-scoped bridge 可返回一个冻结卡 |

当前唯一含 CAD 动作指引的 runtime card 是
[`vertical-cylinder-construction`](../../runtime_resources/experience-cards/cards/vertical-cylinder-construction.json)。它的直接证据只覆盖 `cylinder` 的
final primitive、`block_with_hole` 的 single boolean-cut tool 和
`three_hole_plate` 的 repeated boolean-cut tool 三个声明角色。其余三张卡是
sandbox/input/gate 边界，不是建模参考。完整 runtime-card 索引见
[`runtime_resources/experience-cards/index.json`](../../runtime_resources/experience-cards/index.json)。

## Active self-authored 案例覆盖

本表按已有治理族分组；case identity、lifecycle 与 active membership 以每例
`case.json` 和 registry 为准，避免将导航页计数误作执行 authority。
“卡片”只指人工 case card，避免同 reference pack 或 experience card 混淆。

| 组 | Active cases | 人工 case card | Reference pack | Runtime CAD card / hosted 证据 | 当前阶段待补齐 |
|---|---:|---:|---|---|---|
| P0/P1 reference-pack ladder | 7 | 7 | 全部 7 个 | card 直接角色：`cylinder`、`block_with_hole`、`three_hole_plate`；三者已有受限 hosted 记录 | 其余四例没有 runtime CAD card；7 pack 均 development-only、不可检索 |
| 早期 P2/P3 ladder | 14 | 14 | 无 | 无 | 若选为新决策输入，先补其 Q01/Q02/Q03 证据，而不是直接制卡 |
| 早期参数族（additive boss、through-hole、counterbore、rounded slot、fillet、blind hole、chamfer） | 21 | 21 | 无 | 无 | 参数化本身不构成 runtime-card 资格 |
| offset rounded-slot | 3 | 3 | 无 | 无 | 未形成 runtime projection |
| multi-contour pocket | 6 | 6 | 无 | reviewed operation unit；无 runtime card | 需独立 direct runtime evidence/retrieval 评测 |
| additive-boss dependent cut | 6 | 6 | 无 | reviewed operation unit；无 runtime card | 同上 |
| multi-inner-loop pocket | 6 | 6 | 无 | reviewed operation unit；无 runtime card | 同上 |
| oriented rounded-slot | 6 | 6 | 无 | reviewed operation unit；无 runtime card | 同上 |
| face-selected dependent cut | 6 | 6 | 无 | reviewed operation unit；无 runtime card | 人工导航已完整；不得由此推断 generic face selection |
| repeated-feature pattern | 6 | 6 | 无 | reviewed operation unit；无 runtime card | 人工导航已完整；不得由此推断 generic pattern retrieval |
| axisymmetric revolve | 6 | 6 | 无 | M107 reviewed family evidence；无 runtime card | 仅限 frozen full-revolution stepped-radial grammar；不得推断 generic revolve |

### 人工 case-card 完整性

人工导航卡位于 `docs/corpus/cases/<case_id>.md`；是否仍为 active record 以
`case.json` 与 registry 为准。
这些卡只链接既有的权威 `case.json` 和确定性 oracle 资产；它们不改变 case
admission、manifest、reference pack、runtime card 或 hosted 范围，也不构成 LLM
指导。

## Reference-pack 与 runtime-card 进度

| Case | Development reference pack | Runtime CAD card 状态 | 已有 hosted 证据 |
|---|---|---|---|
| `box` | `reference-pack-box` | 无 | M51 secure smoke pass；M80 因 `cadquery` import fail |
| `cylinder` | `reference-pack-cylinder` | `vertical-cylinder-construction`：final primitive | M85 pass |
| `block_with_hole` | `reference-pack-block-with-hole` | 同卡：single boolean-cut tool | M87 pass |
| `filleted_block` | `reference-pack-filleted-block` | 无 | 无 |
| `chamfered_block` | `reference-pack-chamfered-block` | 无 | 无 |
| `three_hole_plate` | `reference-pack-three-hole-plate` | 同卡：repeated boolean-cut tool | M89-001 timeout；M89-003 pass |
| `box_cylinder_union` | `reference-pack-box-cylinder-union` | 无 | 历史 M6 timeout，非当前 reference-assisted 轨道 |

Pack 的字段、hash 与 counterexample 以
[`reference-pack contract`](reference-packs/reference-pack-contract-v1.json) 为准。当前
pack 的 `runtime_visible: false`；“有 pack”不可解释为 LLM 自主选择该 pack。

## Experimental parameter-variation assets

M94/M95 还产生了 3 development + 3 held-out 的
`reference_guided_through_hole` experimental candidates。它们不在 active registry，
没有人工 case card，也不是 manifest/provider/runtime 输入。M97-003 仅发送了
development 三行；held-out 三行不得为补文档或调参而被读取。冻结边界见
[`M94 preregistration`](sequence-paired/reference-guided-through-hole-variation-v1-preregistration.json) 与
[`M96 policy`](sequence-paired/reference-guided-through-hole-variation-v1-m96-policy.json)。

## Five-family delivery projection

This is a read-only delivery view defined by
[ADR-0062](../architecture/adr/0062-five-family-hosted-capability-portfolio.md).
It neither makes a family an executable/provider input nor records a hosted
pass. Primary case, split, pack/card and report authorities still control.

| Family | Offline basis | Portfolio gap before hosted consideration | Terminal hosted attachment |
|---|---|---|---|
| Prismatic cylindrical cut | prismatic-hole and M94--M97 assets | M112 closed the unchanged paired policy as `inconclusive`; M114/M115 then supplied a discriminating successor design and a reviewed development-only policy freeze | no `TRG-009` campaign; any future hosted work must start from the completed M114/M115 line with a fresh bounded package |
| Dependent face selection | active six-row `face-selected-dependent-cut-v1` | M110 dossier complete; `not-card-eligible` | one-family reviewed no-card campaign row only |
| Multi-inner-loop pocket | active six-row `multi-inner-loop-pocket-v1` | M110 dossier complete; `not-card-eligible` | one-family reviewed no-card campaign row only |
| Repeated feature pattern | active six-row `repeated-feature-pattern-v1` | M110 dossier complete; `not-card-eligible` | one-family reviewed no-card campaign row only |
| Axisymmetric revolve | active six-row `revolve-v1` governance family | M110 dossier complete; `not-card-eligible` | one-family reviewed no-card campaign row only |

`fillet`/`chamfer` is a post-portfolio edge-finishing extension, not an
implicit sixth hosted case. It remains a peer mechanism, while `shell`/`rib`
is a later complex-topology route.

The table is an offline navigation view only. Every row remains blocked by the
separate hosted-stability route; a later campaign still needs one user-selected
family, fresh G3 preflight and itemized authorization. The no-card labels do
not create runtime guidance or a provider input.

## 使用本页选择后续工作

1. 先从 [`coverage matrix`](knowledge/coverage-matrix.json) 选一个 Q01--Q04 决策缺口，而不是从“无卡片案例”反推任务。
2. 若要补 case card，只更新人工导航；若要新增/变更 runtime card、pack、manifest 或 hosted 范围，必须走其独立 workpack 和门槛。
3. 查 hosted 结论时使用 [`hosted experiment registry`](../workflow/hosted-experiment-registry.md)，并以其链接的 terminal report/workpack 为准。

维护步骤见 [`evidence portfolio maintenance`](../runbooks/evidence-portfolio-maintenance.md)。
