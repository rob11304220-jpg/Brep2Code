# M7-003 分层覆盖设计

M7-003 将自制、可提交的 corpus 从 7 例扩展到 21 例。所有输入均为本地 OCP reference script 生成的 STEP fixture，单位为 mm；默认执行、manifest replay 和验证均不需要网络或凭证。

| Tier | Cases | Coverage purpose |
|------|------:|------------------|
| P0 | 3 | 基础 box/cylinder 与单一 Boolean cut smoke。 |
| P1 | 4 | 单边倒圆/倒角、孔阵列与 box-cylinder fuse。 |
| P2 | 9 | 多步布尔、孔深度、counterbore、重复 boss、slot、cross profile 与 cavity。 |
| P3 | 5 | 小/大尺度、薄板高长宽比、侧向特征，以及相同 envelope 的拓扑对照。 |

## 选择规则

1. 每个新增 case 必须有稳定 `case_id`、提交的 STEP fixture、local reference script 和 registry 数值基线。
2. P2 必须包含至少一个 feature interaction 或两步建模序列；P3 必须引入尺度、方向、比例或拓扑歧义条件。
3. 几何 gates 使用 fixture probe 的 bbox、volume 与 topology counts；不新增 probe 或 gate。
4. `counterbored_plate`/`concentric_hole_plate` 共享 30 × 20 × 6 的外部 envelope，但拓扑 counts 分别为 9/36 与 7/30；`offset_through_hole_block`、`blind_hole_block` 与 `side_hole_block` 共享 24 × 18 × 10 的 envelope，分别覆盖位置、深度和方向差异。
5. 默认 scaffold 的 primary failure 是可预期对照；每个新增 case 的 local fake-provider reference replay 必须通过，不能据此推断 hosted-model 质量。

## 已完成的离线证据

- `p2.json`：9 个 primary gate failures 后，9/9 local reference replays pass。
- `p3.json`：5 个 primary gate failures 后，5/5 local reference replays pass。
- 两份 report 均为 `completed`，位于忽略的 `data/corpus-runs/`；它们是 Harness 兼容性证据，不是 benchmark。
