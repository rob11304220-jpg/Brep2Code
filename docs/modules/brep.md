# 模块：B-Rep

代码路径：`brep2code/brep/`

## 职责

- 从 record input 或显式输入路径读取 CAD/B-Rep 文件。
- 为 Harness / CLI 提供 probe-first 查询接口。
- 建立同一输入文件内稳定的 entity id。
- 控制 tool result 大小；必要时将完整结果落 trace。

## 非职责

- 不提供项目级 CAD modeling SDK。
- 不定义固定 IR、建模序列 DSL 或 B-Rep tensor/schema。
- 不下载、清洗或管理大型公开数据集。

## 当前后端

M1 使用 `cadquery-ocp` 提供的 `OCP` OpenCascade 绑定。当前实现优先支持 STEP (`.step` / `.stp`)；IGES 和 `.brep` 保留为输入发现扩展点。

## 对外入口

| 入口 | 用途 |
|------|------|
| `brep2code.brep.load_model(path)` | 读取 STEP 并建立 probe model |
| `probe_summary(model)` | 文件、bbox、拓扑计数、面积/体积摘要 |
| `probe_topology(model, selector)` | solid/shell/face/edge entity 摘要 |
| `probe_entity(model, entity_id)` | 单个 face/edge 等 entity 的局部信息 |
| `sample_entity(model, entity_id, n)` | face/edge 采样点和法向/切向 |
| `python -m brep2code.cli probe ...` | 本地调试入口 |

## Runtime 路径

| 路径 | 读写 |
|------|------|
| `data/records/<record_id>/input/` | 读取 record CAD 输入 |
| `data/records/<record_id>/traces/` | CLI record probe 大结果 trace |
| `case-library/self-authored/<case_id>/input.step` | M1/M4 自建 STEP 测试样例 |

## 历史与契约

M1 引入 B-Rep probe；M3 将其暴露为受限 LLM tool calls。当前阶段边界、工具
调用位置和 Q01--Q04 契约由 [pipeline](../architecture/pipeline.md) 维护；本页的
接口表是模块行为权威。完成 workpack 仅保留验收 provenance。

验收命令：

```powershell
python -m brep2code.cli probe --input case-library\self-authored\box\input.step
python -m pytest
```
