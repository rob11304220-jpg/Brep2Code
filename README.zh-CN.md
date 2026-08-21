# Brep2Code v2

English: [README.md](README.md)

Brep2Code 将 STEP/B-Rep 任务转换为完整、可执行的 CAD 构造脚本，并且只在独立几何验证通过后接受输出。Active Harness 是主要研究协议；Fixed runner 只作为显式对照，Active 失败不会回退到 Fixed。

## Active Harness

模型是 Harness 内部一个受限的动作策略，不是运行的控制者。每个回合，模型只能从 controller 当前开放的能力中选择一个动作：

- `probe`：请求一个白名单内、路径无关的几何观察；
- `retrieve`：在实验允许检索时，请求批准的 SDK 或通用 recipe 投影；
- `submit`：提交一份完整、确定性的 `build.py`；
- `finish`：表示没有进一步有用的动作。

Harness 管理状态、内部限制、工具调度、不可变 revision、checkpoint 和 continuation。它向模型投影“当前可用能力”，而不是数值预算。Provider 可以看到当前可用的动作和工具，但看不到 controller usage、HTTP 限额、重试、超时、价格、成本、授权、campaign policy 或安全执行器配置。

`finish` 只是建议。只有 verifier 在脚本兼容性检查、安全执行和必要几何 gates 全部通过后，才能将运行标记为成功。

```text
已校验的 B-Rep 任务
        |
        v
路径无关的观察 ------> 模型选择一个当前可用动作
        ^                         |
        |             probe / retrieve / submit / finish
        |                         |
        +---- 类型化反馈 <---- 独立 verifier
                                  |
                           已验证的 output.step
```

模型上下文只包含 case identity、单位、几何观察、当前可用动作和工具、粗粒度 session phase、选定 CAD 后端契约、已有工具结果、当前 revision 和 verifier 反馈。它不能包含 eval references、目标解、私有 oracle、仓库文件、主机路径、环境变量、凭证或未声明的网络访问。

## 安装与验证

```powershell
uv sync --dev
uv run brep2code env doctor
uv run brep2code cases validate
uv run pytest -q
uv run pytest --run-secure -q
uv run ruff check src tests
```

默认 provider 是确定性的离线 fake provider。真实 provider 必须通过显式命令选择并获得新授权。Provider 生成的代码只能通过配置的 WSL2/bubblewrap 安全后端执行；可信本地执行器不是其 fallback。

当前命令和参数以 CLI 为准：

```powershell
uv run brep2code --help
uv run brep2code active-run --help
uv run brep2code active-hosted-live-run --help
uv run brep2code stage1 report --help
```

案例位于 `cases/<split>/<case_id>`。运行时只允许加载 `smoke` 和 `train`；eval 案例及其私有对比材料只属于 Harness。运行产物保存在指定 run root 下，包括原子更新的 `result.json` 和不可变 revision 目录。

## 当前研究状态

Stage 1 冻结的无知识 baseline 已经完成，得到可解释的负向退出结论：

| 条件 | 有效且可解释 | 几何通过 | Provider/Harness 失败 |
|---|---:|---:|---:|
| CadQuery 五案例阶段 | 48/50 | 17/50 | 2/50 |
| CadQuery 三个可比案例 | 29/30 | 5/30 | 1/30 |
| OCP 三个可比案例 | 27/30 | 18/30 | 3/30 |

OCP 在可比案例上显著改善了 primitive 和 boolean 构造，但其基础设施失败率恰好为 10%。冻结契约要求严格低于 10%，因此 Stage 1 没有退出。已有 schema-v6 结果和分类继续作为权威证据，不能选择性重跑或重新分类。

当前 schema-v7 / provider-task-contract-v2 稳定化工作明确分离：

- 模型决策、probe、submission 和 verifier 引导的 repair；
- Provider HTTP 尝试、有限协议重试、token 和 cost；
- 安全执行的时间、资源、进程和输出限制。

这是一项新的协议条件，不是对冻结 Stage 1 的追溯修改。任何 hosted 验证都需要新的 experiment identity 和预先声明的完整 cohort。

该验证现已完成：12 个计划内 schema-v7 run 全部生成有效 artifact 和有效 provider-visible projection；9 个通过几何验证，2 个在执行前被分类为 generation failure，1 个为 geometry failure。整个 cohort 使用 13 次 HTTP attempt、14,903 tokens 和 `$0.007858275`，没有触发 protocol retry。结论为 `protocol_stable`，但不改变 Stage 1 退出判断，也不授权 Stage 2。

强制研究顺序保持为：

1. Active 无知识 baseline 和协议稳定化；
2. 相同知识条件下的 hosted Active 复现；
3. SDK 与通用 recipe 的配对检索消融；
4. 对成熟建模数据集进行治理后再导入和检索。

在前一阶段满足退出标准前，不得进入 Stage 3 或 Stage 4。能力标签和 mechanism metadata 可以用于报告与分组，但不是运行时脚本契约，也不是开发路线。

下一个冻结条件是 `stage1-no-knowledge-v2`：在 schema v7、`active-v4-no-retrieval` 和不变的 Stage 1 阈值下运行 50 个 CadQuery 与 30 个 OCP contrast。其无网络 preflight 已达到授权审查状态，但不授予 provider 执行或 Stage 2 权限。

## 项目权威来源

代码、测试、案例元数据和已验证运行产物是证据权威。永久设计与流程约束只保存在：

- [Architecture](docs/architecture.md)：控制循环、契约、可见性、验证和产物不变量；
- [Development](docs/development.md)：变更纪律、研究阶段、当前证据和验证流程；
- [Providers](docs/providers.md)：Provider 配置、传输、计费、hosted 授权和 continuation 规则。

命令参数以 CLI `--help` 为准；单次运行事实以运行产物为准，不写入永久叙事文档。
