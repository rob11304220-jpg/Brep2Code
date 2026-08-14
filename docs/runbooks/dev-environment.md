# Development Environment

本 runbook 记录 Brep2Code 本地开发环境的最小配置。依赖入口以 `pyproject.toml` 为准。

## Python

项目目标 Python 范围：

```text
>=3.12,<3.15
```

当前 M1 B-Rep probe backend 使用 `cadquery-ocp` 提供的 `OCP` OpenCascade 绑定。该依赖包含二进制 CAD kernel 绑定，因此升级 Python 或 OpenCascade 相关包前应先跑 probe smoke。

## 推荐安装

优先使用论文库规划中的 `uv`：

```powershell
uv sync --dev
```

若当前机器没有 `uv`，可使用 pip：

```powershell
python -m pip install -e .
python -m pip install pytest ruff
```

## 验证

```powershell
python -m brep2code.cli probe --input case-library\self-authored\box\input.step
python -m pytest
python -m ruff check .
```

也可以用 `just`：

```powershell
just probe
just test
just lint
```

## 依赖边界

- Runtime：只放运行 Harness / probe / CAD backend 必需的依赖。
- Dev：测试、lint、格式检查等开发工具放入 dependency group `dev`。
- 数据集下载工具不进入默认依赖；等对应 workpack 启用 P1/P2/P3/P4 数据源时再加。
- LLM SDK 不提前加入；M3-001 只使用本地 fake provider。Hosted provider 配置边界见 [`docs/runbooks/llm-provider-config.md`](llm-provider-config.md)。