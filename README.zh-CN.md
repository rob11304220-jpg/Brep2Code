# Brep2Code v2

Brep2Code 将 STEP/B-Rep 几何案例转换为可执行的 CAD 构造脚本，并通过受限执行和几何验证确认输出模型是否正确。

项目的目标不是只生成一段 CAD 代码，而是建立一个可复现、可验证、可修复并具有安全执行边界的 B-Rep 重建 Harness。

## 它如何工作

```text
STEP/B-Rep 案例
    ↓
案例契约校验
    ↓
几何观察
    ↓
Fixed Harness 或 Active Harness
    ↓
生成 build.py
    ↓
兼容性检查与安全执行
    ↓
几何/拓扑/语义验证
    ↓
成功，或生成有限修复反馈
```

Fixed Harness 每轮生成一份完整脚本。Active Harness 还可以在提交脚本前执行有限的几何探针或检索批准的 OCP 参考。

## Harness 状态机

Active Harness 使用四类动作：

```text
OBSERVING
   ├─ probe       → PROBING → OBSERVING
   ├─ retrieve    → RETRIEVING → OBSERVING
   └─ submit      → SYNTHESIZING
                         ↓
                     EXECUTING
                         ↓
                     VERIFYING
                      ├─ SUCCEEDED
                      └─ REPAIRING → OBSERVING
```

`finish` 只是模型的建议，不能绕过执行和验证。只有 Harness verifier 可以进入 `SUCCEEDED`；预算耗尽或无法继续时进入 `EXHAUSTED`。

## 当前能力与规划

| 等级 | 能力 | 状态 |
|---|---|---|
| L0 | 独立 primitive 和 analytic-surface 构造，例如 box、cylinder | 已实现 |
| L1 | 有序 boolean feature sequence，例如 through cut、blind cut | 已实现 |
| L2 | 基于边/面的单特征构造，例如 fillet | 已实现，chamfer 尚未迁移 |
| L3 | 多特征有序构造与依赖关系保持，例如 union、重复 cut、boss 后 dependent cut、counterbore | 规划中 |
| L4 | 拓扑语义选择与结构化轮廓，例如 face selection、multi-loop pocket、rounded slot | 规划中 |
| L5 | 重复特征、参数变化和冻结参数族内的受控泛化 | 规划中 |
| L6 | 非棱柱体和复杂拓扑，例如 revolve、shell、rib；sweep/loft 需独立评估 | 规划中 |

L3-L6 是基于既有机制路线归纳出的目标能力，不表示当前已经实现。具体能力必须通过独立案例、正负控制、几何/语义 gates、held-out split 和 focused tests 逐级确认。

## 现有案例

案例位于 `cases/<split>/<case_id>`，每个案例包含 STEP 输入、案例元数据、Harness dossier 和控制脚本。

| Split | 案例 |
|---|---|
| smoke | `box`、`block_with_hole` |
| train | `blind_hole_block`、`filleted_box` |
| eval | `cylinder`、`box_held_out`、`cylinder_held_out`、`through_cut_held_out`、`blind_cut_held_out`、`filleted_box_held_out` |

案例覆盖四类当前机制：primitive、analytic surface、boolean cut 和 fillet。`eval` 案例只由 Harness 评估路径加载，不会暴露给运行时模型。

每个案例通常包含：

```text
case.json
dossier.json
input.step
controls/
├─ nominal.py
├─ parameter_variation.py
└─ failure_sensitive.py
```

## 快速开始

```powershell
uv sync --dev
uv run brep2code --help
uv run brep2code cases validate
uv run pytest -q
uv run ruff check src tests
```

运行离线修复示例：

```powershell
uv run brep2code run --case-id box --run-root runs/box-smoke `
  --fake-script tests/fixtures/broken_box.py `
  --fake-script tests/fixtures/fixed_box.py --max-rounds 2
```

默认 provider 是离线 fake provider，不会自动发起网络请求。

## 输出与验证

运行结果保存在指定的 `runs/<run-id>` 下，主要包括：

- `result.json`：最终状态、预算、执行和验证结果；
- 不可变 revision 目录；
- 生成脚本、请求/响应摘要和执行输出；
- bbox、volume、topology、semantic 或 adjacency gate 结果。

失败会转换为结构化反馈，供下一轮有限修复使用。之前的 revision 不会被覆盖。

## 安全边界

- fake provider 是默认 provider；真实 provider 必须显式选择。
- API key 只来自环境变量，不写入运行产物。
- 生成代码通过 Ubuntu-24.04 WSL2/bubblewrap 执行。
- 执行环境禁止网络，并限制文件、时间、内存、进程和输出大小。
- 运行时模型只接收路径无关的观察、声明过的工具和有界反馈。
- eval 参考答案、私有 oracle、仓库内容、主机路径和 secrets 不进入运行时上下文。

## 当前限制

- 当前实际闭环覆盖 L0-L2，L3-L6 仍是规划能力。
- hosted active continuation 仍是 HTTP-stub-only。
- 更大规模 hosted cohort 尚未开放。
- 单次案例或 hosted 通过不能证明通用 CAD 重建能力。
- 旧仓库的 P0-P3 是案例/证据层级，不等同于 L0-L6 能力等级。

## 进一步阅读

- [Architecture](docs/architecture.md)：系统架构、Harness 合约和信息边界；
- [Development](docs/development.md)：开发路线、L0-L6 机制规划和验证要求；
- [Providers](docs/providers.md)：provider、授权、预算和 hosted 运行策略。
