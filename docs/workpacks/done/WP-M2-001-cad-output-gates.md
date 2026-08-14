# WP-M2-001: CAD Output Gates

- Status: done
- Milestone: M2
- Owner: unassigned

## Goal

让 Harness 执行的 `build_sequence.py` 生成真实可读入的 STEP 输出，并将输出可读入、bbox、体积、拓扑计数等基础 gate 写入 `signal_bundle.json`。

## Scope

- 默认 `build_sequence.py` 使用当前 CAD backend 生成 `output/model.step`，不再写占位 STEP 文本。
- `run --input` 复制输入到 record input，并在执行后对输入和输出分别运行 probe summary。
- 新增基础 gates：`output_model_step_readable`、`bbox_delta`、`volume_delta`、`topology_count_delta`。
- gate 失败时提供具体 metric 和 repair hint。
- 保持 Harness core 不依赖项目级 CAD modeling SDK 或固定 IR。

## Inputs

- `docs/workpacks/done/WP-M1-001-brep-probe-tools.md`
- `docs/architecture/v1/contracts/build-script.md`
- `docs/architecture/v1/contracts/signal-bundle.md`
- `docs/architecture/v1/q03-harness/geometry-gate.md`
- `docs/modules/brep.md`
- `case-library/self-authored/box/input.step`

## Code paths

| Path | Purpose |
|------|---------|
| `brep2code/scaffold.py` | 默认 build script 模板 |
| `brep2code/agent/harness.py` | 执行后 gate 与 signal bundle |
| `brep2code/brep/` | 复用 probe summary 读入输入/输出 STEP |
| `tests/` | M2 gate 测试 |
| `docs/modules/` | 模块文档同步 |

## Acceptance

- [x] 默认 `build_sequence.py` 生成可由 M1 probe backend 读入的 `output/model.step`。
- [x] `run --record box-smoke --input case-library\self-authored\box\input.step` 生成包含 input/output probe summary 的 `signal_bundle.json`。
- [x] 输出不可读时 gate 失败并保留结构化错误。
- [x] bbox、volume、拓扑计数基础指标进入 gates。
- [x] 当前 smoke box 案例通过基础 gates。
- [x] `uv run python -m pytest` 通过。
- [x] `uv run python -m ruff check .` 通过。

已验证：

```powershell
uv run python -m brep2code.cli run --record box-smoke --input case-library\self-authored\box\input.step
uv run python -m pytest
uv run python -m ruff check .
```

## Out of scope

- LLM repair loop。
- mesh distance / sampling distance。
- 多 CAD backend 抽象。
- 复杂 shape 重建策略。
- 大型公开数据集启用。