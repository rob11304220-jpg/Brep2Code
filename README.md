# Brep2Code

将 **B-Rep 输入** 转为 **可执行 CAD 建模脚本与结果** 的研究实现仓库。当前 v1 方向是 Harness 优先：先搭建通用大模型可调用的 probe、执行、门控和修复闭环，再从案例中沉淀 IR、SDK 或 CAD workplace。

## 仓库分工

- **本仓** — 代码实现、验证、Agent 协作框架（规则、Skills、Handoff）
- **论文库** — 文献、阅读清单与研究综述：[`D:\paper\Projects\Brep2Code.md`](D:\paper\Projects\Brep2Code.md)

## 快速入口

| 读者 | 入口 |
|------|------|
| Agent | [`AGENTS.md`](AGENTS.md) |
| 架构与流程 | [`docs/architecture/overview.md`](docs/architecture/overview.md) |
| 理论 / 受限建模假设 | [`项目理论地图`](docs/architecture/v1/project-theory-map.md) |
| Harness Q01--Q04 行为 | [`流水线索引`](docs/architecture/pipeline.md) |
| 案例与证据资产 | [`案例组合导航`](docs/corpus/case-portfolio.md) |
| 当前可执行工作 | [`docs/workflow/status.md`](docs/workflow/status.md) |
| 跨会话恢复 | [`docs/handoff/active/`](docs/handoff/active/) |

理论地图将受限 hypothesis 导向 M146 crosswalk；案例资产、系统契约和当前
workpack 各有自己的权威。一个 hypothesis 链接不构成案例 promotion、代码、
runtime、provider 或 hosted 权限。

## 能力概览

Harness 已具备 probe、CAD 执行与门控、provider/trace、tool bridge、fake-provider repair loop、受限 hosted 评测，以及经验证的 WSL bubblewrap sandbox。当前项目主线是冻结这些组件为一个真实 LLM 闭环并取得可归因 hosted 终端证据；repair/交互预算、案例治理和经验投影分别以证据推进。M20--M27 与 M90 已补充受限的离线 self-authored sequence-pair 证据；案例身份、lifecycle 与当前构成以 `case.json`、registry 和 [`docs/corpus/case-portfolio.md`](docs/corpus/case-portfolio.md) 为准，active workpack 与下一工作以 [`docs/workflow/status.md`](docs/workflow/status.md) 为准。默认路径仍保持离线、无凭证，DeepSeek 仅在显式选择 provider 且取得逐批授权时接入。

当前里程碑、active workpack 与下一工作以 [`docs/workflow/status.md`](docs/workflow/status.md) 为唯一事实源；工作路由见 [`docs/workflow/README.md`](docs/workflow/README.md)。

## 快速运行

环境目标为 Python 3.12 到 3.14；项目依赖入口为 [`pyproject.toml`](pyproject.toml)。M1/M2 B-Rep probe 和 CAD smoke backend 使用 `cadquery-ocp` 提供的 `OCP` OpenCascade 绑定。

推荐安装：

```powershell
uv sync --dev
```

无 `uv` 时：

```powershell
python -m pip install -e .
python -m pip install pytest ruff
```

```powershell
uv run python -m brep2code.cli run --record box-smoke --input case-library\self-authored\box\input.step
```

该命令会创建或打开 `data/records/box-smoke/`，复制输入 STEP，生成一个 revision workspace，写入默认 `build_sequence.py`，执行脚本导出 `output/model.step`，并保存 stdout、stderr、`execution.json` 和包含 probes/gates 的 `signal_bundle.json`。

开发测试：

```powershell
uv run python -m pytest
```

M1 probe smoke：

```powershell
uv run python -m brep2code.cli probe --input case-library\self-authored\box\input.step
```

M4 P0 case corpus：

```powershell
uv run python -m brep2code.cli corpus --manifest case-library\manifests\self-authored\p0.json --data-root data
```

M4 P1 parametric case corpus：

```powershell
uv run python -m brep2code.cli corpus --manifest case-library\manifests\self-authored\p1.json --data-root data
```

更多环境说明见 [`docs/runbooks/dev-environment.md`](docs/runbooks/dev-environment.md)。
