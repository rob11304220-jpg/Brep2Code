# B-Rep 输入来源索引

本文件记录 Brep2Code 可按需启用的 B-Rep / CAD 输入来源。这里负责外部资源与本仓使用边界，不保存数据集正文、下载产物或论文笔记。

## 本仓使用约束

- M1 优先使用小型、可控、可提交的 STEP fixtures 跑通 probe tools。
- 大型公开数据集只放在本地 `data/datasets/`，默认不提交。
- 每个实验 record 的输入落在 `data/records/<record_id>/input/`。
- 公开数据集启用前先确认格式、许可、下载体量和采样策略。
- 不把完整 B-Rep、数据集说明或论文 Q&A 复制进 runtime prompt；Harness 通过工具按需读取。
- 开发侧的案例登记、人工审阅卡与外部选样模板位于 [`docs/corpus/`](../corpus/README.md)；它们不属于 Harness runtime material。

## 启用优先级

| 优先级 | 来源 | 当前用途 | 启用方式 | 备注 |
|--------|------|----------|----------|------|
| P0 | 自制 STEP fixtures | M1 probe tools 单元测试、CLI smoke、M4 P0/P1 corpus | `case-library/self-authored/<case_id>/input.step` | box、cylinder、block_with_hole、filleted_block、chamfered_block、three_hole_plate、box_cylinder_union |
| P1 | ABC Dataset | M8-001 本地 STEP 准入试点 | `data/datasets/abc/v00/` + 显式 external manifest | 仅本地研究复现；原始资产不提交、不作为默认输入 |
| P2 | Fusion 360 Gallery Dataset | 带设计语义的 STEP / sequence / segmentation 案例 | `data/datasets/fusion360/` | 适合后续 Q02/Q04 分析建模过程和 face operation 标签 |
| P3 | DeepCAD | 建模序列与生成任务参考 | `data/datasets/deepcad/` | 更偏 Q02 sequence prior，不作为 M1 首选输入 |
| P4 | Thingi10K | Mesh gate / 鲁棒性参考 | `data/datasets/thingi10k/` | 主要是 STL mesh，不作为 B-Rep probe 主输入 |

## 外部入口

| 来源 | 链接 | 关键信息 |
|------|------|----------|
| ABC Dataset | <https://deep-geometry.github.io/abc-dataset/> | 约 100 万 CAD models；STEP / Parasolid / STL / meta 等格式；CAD 模型版权归原创建者 |
| Fusion 360 Gallery Dataset | <https://github.com/AutodeskAILab/Fusion360GalleryDataset> | Reconstruction、Segmentation、Assembly 等子集；含 STEP 扩展下载 |
| DeepCAD | <https://github.com/rundiwu/DeepCAD> | CAD construction sequence JSON / vectorized representation；数据来自 Onshape public documents / ABC links |
| Thingi10K | <https://github.com/Thingi10K/Thingi10K> | 10,000 个 3D printing models，主要为 STL mesh |

## 默认策略

默认路径仍仅启用自制 fixtures。M8-001 允许通过显式 manifest 使用受控的 ABC v00 本地样本；P2/P3/P4 仍只作为 documented sources，不进入默认验收路径。

外部数据集的登记并不授权下载、再分发、选样、归一化或执行。相关动作必须由单独 workpack 完成，并记录许可、release、样本身份和复现边界。
