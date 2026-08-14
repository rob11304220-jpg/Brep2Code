# Case: three_hole_plate

## 几何意图

30 × 10 × 4 板经连续 Boolean cut 形成沿中心线等间距的三个 Z 向通孔。

## 关键尺寸

- 单位：mm
- 板体：X=30，Y=10，Z=4；孔直径：3。
- 孔中心：`(7.5,5)`、`(15,5)`、`(22.5,5)`；孔轴：+Z。

## 资产与基线

- STEP：[three_hole_plate.step](../../../case-library/self-authored/three_hole_plate/input.step)
- Reference script：[three_hole_plate_build_sequence.py](../../../case-library/self-authored/three_hole_plate/reference_build_sequence.py)
- 预期：1 solid、1 shell、9 faces、42 edges；bbox `[0,0,0]`–`[30,10,4]`；体积 `1115.1769983530735` mm³。
- 权威元数据：[self-authored.json](../registry/self-authored.json) 的 `three_hole_plate` 条目。

## 适合验证的问题

重复特征、位置参数、连续 Boolean cut 与孔阵列。

## 非目标

不覆盖非等距阵列、盲孔、沉孔、螺纹或 pattern API。

## 变更记录

- v1：现有 P1 fixture 纳入开发侧案例治理。
