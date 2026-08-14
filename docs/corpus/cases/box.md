# Case: box

## 几何意图

轴对齐长方体；作为默认 scaffold 和 P0 基本体的基线。

## 关键尺寸

- 单位：mm
- 尺寸：X=10，Y=20，Z=30
- 坐标：右手 XYZ，包围盒最小点为原点。

## 资产与基线

- STEP：[box.step](../../../case-library/self-authored/box/input.step)
- Reference script：不适用；这是默认 scaffold 基线。
- 预期：1 solid、1 shell、6 faces、24 edges；bbox `[0,0,0]`–`[10,20,30]`；体积 `6000` mm³。
- 权威元数据：[self-authored.json](../registry/self-authored.json) 的 `box` 条目。

## 适合验证的问题

基本 STEP 读取、长方体尺寸保持和 P0 默认路径。

## 非目标

不覆盖曲面、布尔运算、阵列或特征顺序推断。

## 变更记录

- v1：现有 smoke fixture 纳入开发侧案例治理。
