# Case: filleted_block

## 几何意图

16 × 12 × 8 的方块在一条边上施加半径 1 的圆角。

## 关键尺寸

- 单位：mm
- 块体：X=16，Y=12，Z=8；圆角半径：1。
- 坐标：右手 XYZ，块体最小点为原点。

## 资产与基线

- STEP：[filleted_block.step](../../../case-library/self-authored/filleted_block/input.step)
- Reference script：[filleted_block_build_sequence.py](../../../case-library/self-authored/filleted_block/reference_build_sequence.py)
- 预期：1 solid、1 shell、7 faces、30 edges；bbox `[0,0,0]`–`[16,12,8]`；体积 `1534.2831853071807` mm³。
- 权威元数据：[self-authored.json](../registry/self-authored.json) 的 `filleted_block` 条目。

## 适合验证的问题

单边圆角、曲面特征与保留总体包围盒的建模。

## 非目标

不定义依赖于 OpenCascade 遍历顺序的特定 edge 编号；不覆盖多边圆角。

## 变更记录

- v1：现有 P1 fixture 纳入开发侧案例治理。
