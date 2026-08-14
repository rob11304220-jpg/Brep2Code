# 自建案例总览

本页用于人工审阅和跨案例比较。机器可读的数值基线、文件 hash 和路径以 [自建案例注册表](registry/self-authored.json) 为准；本页不作为 Harness manifest。

| Case | Tier | 特征 | 尺寸级别（mm） | Reference script | 审阅状态 |
|------|------|------|----------------|------------------|----------|
| [box](cases/box.md) | P0 | box, primitive | 10 × 20 × 30 | 不适用：默认 scaffold 基线 | 已登记 |
| [cylinder](cases/cylinder.md) | P0 | cylinder, primitive | Ø10 × H12 | 可用 | 已登记 |
| [block_with_hole](cases/block_with_hole.md) | P0 | block, hole, boolean | 20 × 20 × 8；Ø8 通孔 | 可用 | 已登记 |
| [filleted_block](cases/filleted_block.md) | P1 | block, fillet | 16 × 12 × 8；R1 | 可用 | 已登记 |
| [chamfered_block](cases/chamfered_block.md) | P1 | block, chamfer | 16 × 12 × 8；1 × 1 倒角 | 可用 | 已登记 |
| [three_hole_plate](cases/three_hole_plate.md) | P1 | plate, hole, array, boolean-cut | 30 × 10 × 4；3 × Ø3 通孔 | 可用 | 已登记 |
| [box_cylinder_union](cases/box_cylinder_union.md) | P1 | box, cylinder, boolean-fuse | 14 × 10 × 5 + Ø6 × H6 | 可用 | 已登记 |
| [offset_through_hole_block](cases/offset_through_hole_block.md) | P2 | block, offset-hole, boolean-cut | 24 × 18 × 10；偏置 Ø6 通孔 | 可用 | 已登记 |
| [blind_hole_block](cases/blind_hole_block.md) | P2 | block, blind-hole, boolean-cut | 24 × 18 × 10；Ø6 × 深6 | 可用 | 已登记 |
| [counterbored_plate](cases/counterbored_plate.md) | P2 | plate, through-hole, counterbore | 30 × 20 × 6；Ø4/Ø8 沉孔 | 可用 | 已登记 |
| [stepped_block](cases/stepped_block.md) | P2 | block, step, boolean-fuse | 30 × 20 × 12 | 可用 | 已登记 |
| [dual_boss_plate](cases/dual_boss_plate.md) | P2 | plate, boss-array, boolean-fuse | 30 × 20 × 4 + 2 × Ø6 × H6 | 可用 | 已登记 |
| [boss_with_blind_hole](cases/boss_with_blind_hole.md) | P2 | plate, boss, blind-hole, fuse-cut | 30 × 20 × 12 | 可用 | 已登记 |
| [cross_fuse_block](cases/cross_fuse_block.md) | P2 | block, cross-profile, boolean-fuse | 30 × 30 × 6 | 可用 | 已登记 |
| [hollow_open_box](cases/hollow_open_box.md) | P2 | box, cavity, boolean-cut | 30 × 20 × 12 | 可用 | 已登记 |
| [slot_plate](cases/slot_plate.md) | P2 | plate, slot, boolean-fuse-cut | 30 × 20 × 5 | 可用 | 已登记 |
| [small_cylinder](cases/small_cylinder.md) | P3 | cylinder, primitive, small-scale | Ø1 × H1.25 | 可用 | 已登记 |
| [large_box](cases/large_box.md) | P3 | box, primitive, large-scale | 1000 × 500 × 250 | 可用 | 已登记 |
| [side_hole_block](cases/side_hole_block.md) | P3 | block, side-hole, orientation | 24 × 18 × 10；侧向 Ø6 通孔 | 可用 | 已登记 |
| [concentric_hole_plate](cases/concentric_hole_plate.md) | P3 | plate, through-hole, topology-pair | 30 × 20 × 6；中心 Ø8 通孔 | 可用 | 已登记 |
| [thin_plate](cases/thin_plate.md) | P3 | plate, thin-wall, aspect-ratio | 80 × 40 × 1 | 可用 | 已登记 |

所有案例均为已提交的自建 fixture、单位为 mm、状态为 `active`。未来案例的选择应由 M7-003 的专项证据与覆盖需求决定，而非仅以数量扩展。
