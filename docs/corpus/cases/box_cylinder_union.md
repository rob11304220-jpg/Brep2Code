# Case: box_cylinder_union

## 几何意图

14 × 10 × 5 的方块与顶部居中的 Ø6、H6 Z 向圆柱进行 Boolean fuse。

## 关键尺寸

- 单位：mm
- 方块：X=14，Y=10，Z=5；圆柱：直径=6，高度=6。
- 圆柱中心：`(7,5)`；从 `z=5` 起沿 +Z 延伸至 `z=11`。

## 资产与基线

- STEP：[box_cylinder_union.step](../../../case-library/self-authored/box_cylinder_union/input.step)
- Reference script：[box_cylinder_union_build_sequence.py](../../../case-library/self-authored/box_cylinder_union/reference_build_sequence.py)
- 预期：1 solid、1 shell、8 faces、30 edges；bbox `[0,0,0]`–`[14,10,11]`；体积 `869.6460032938548` mm³。
- 权威元数据：[self-authored.json](../registry/self-authored.json) 的 `box_cylinder_union` 条目。

## 适合验证的问题

Boolean fuse、不同 primitive 的组合与连续实体拓扑。

## 非目标

不覆盖相交圆柱、多实体保留或复杂 blend。

## 变更记录

- v1：现有 P1 fixture 纳入开发侧案例治理。
