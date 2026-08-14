# Case: chamfered_block

## 几何意图

16 × 12 × 8 的方块在一条边上施加 1 × 1 倒角。

## 关键尺寸

- 单位：mm
- 块体：X=16，Y=12，Z=8；两个倒角距离均为 1。
- 坐标：右手 XYZ，块体最小点为原点。

## 资产与基线

- STEP：[chamfered_block.step](../../../case-library/self-authored/chamfered_block/input.step)
- Reference script：[chamfered_block_build_sequence.py](../../../case-library/self-authored/chamfered_block/reference_build_sequence.py)
- 预期：1 solid、1 shell、7 faces、30 edges；bbox `[0,0,0]`–`[16,12,8]`；体积 `1532` mm³。
- 权威元数据：[self-authored.json](../registry/self-authored.json) 的 `chamfered_block` 条目。

## 适合验证的问题

单边倒角、平面特征以及与圆角案例的相邻对照。

## 非目标

不定义依赖于 OpenCascade 遍历顺序的特定 edge 或 face 编号；不覆盖多边倒角。

## 变更记录

- v1：现有 P1 fixture 纳入开发侧案例治理。
