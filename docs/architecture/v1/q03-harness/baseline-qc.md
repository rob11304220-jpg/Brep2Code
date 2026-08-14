---
type: design
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - harness
---

# Q03 — Baseline QC

v1 初始 QC 只覆盖闭环必需项：

- 脚本是否成功执行。
- 是否生成预期 CAD 输出。
- 输出是否可被 CAD/B-Rep 后端重新读入。
- bbox、体积、面积是否明显偏离输入。
- mesh sampling distance 是否在可配置阈值内。

更细的语义测试从案例中补充。
