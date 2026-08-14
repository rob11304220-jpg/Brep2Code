---
type: design
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - modules
  - brep
---

# 模块：brep/

`D:\codeai\Brep2Code\brep2code\brep\`

## 职责

Q01 管线：CAD 文件 -> 可查询 shape handle -> probe tool backend。v1 不做统一 B-Rep 编码器。

## 规划文件

| 文件 | 职责 |
|------|------|
| `readin.py` | 读入 STP / IGES / `.brep`，建立 shape handle |
| `probes.py` | 拓扑、bbox、采样、测量等查询 |
| `serialize.py` | 将 probe 结果转为 LLM 可读 JSON |

## 依赖

CAD/B-Rep 后端待实现时选择；优先满足 probe 和导出闭环。
