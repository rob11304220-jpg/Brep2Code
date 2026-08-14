# Case: block_with_hole

## 几何意图

20 × 20 × 8 的方块经 Boolean cut 形成一个居中 Z 向通孔。

## 关键尺寸

- 单位：mm
- 块体：X=20，Y=20，Z=8；通孔直径：8。
- 孔中心：`(10, 10)`；孔轴：+Z。

## 资产与基线

- STEP：[block_with_hole.step](../../../case-library/self-authored/block_with_hole/input.step)
- Reference script：[block_with_hole_build_sequence.py](../../../case-library/self-authored/block_with_hole/reference_build_sequence.py)
- 预期：1 solid、1 shell、7 faces、30 edges；bbox `[0,0,0]`–`[20,20,8]`；体积 `2797.876140340492` mm³。
- 权威元数据：[self-authored.json](../registry/self-authored.json) 的 `block_with_hole` 条目。

## 适合验证的问题

Boolean cut、通孔、圆柱工具体与平面/曲面混合拓扑。

## 非目标

不覆盖盲孔、螺纹、多个孔或倒角孔口。

## 变更记录

- v1：现有 smoke fixture 纳入开发侧案例治理。
