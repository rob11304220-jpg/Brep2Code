# Case: cylinder

## 几何意图

沿 +Z 的圆柱，用于曲面与圆边基线。

## 关键尺寸

- 单位：mm
- 直径：10；高度：12。
- 坐标：右手 XYZ，底面圆心在原点，轴向为 +Z。

## 资产与基线

- STEP：[cylinder.step](../../../case-library/self-authored/cylinder/input.step)
- Reference script：[cylinder_build_sequence.py](../../../case-library/self-authored/cylinder/reference_build_sequence.py)
- 预期：1 solid、1 shell、3 faces、6 edges；bbox `[-5,-5,0]`–`[5,5,12]`；体积 `942.4777960769379` mm³。
- 权威元数据：[self-authored.json](../registry/self-authored.json) 的 `cylinder` 条目。

## 适合验证的问题

圆柱 primitive、曲面与圆形边的读取及可复现 reference script。

## 非目标

不覆盖混合特征、布尔交互或多个圆柱。

## 变更记录

- v1：现有 smoke fixture 纳入开发侧案例治理。
