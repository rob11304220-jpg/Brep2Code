# Git 设置与工作流

## 初始化

本仓库已 `git init`，默认分支 `main`。

## 分支命名

| 类型 | 格式 | 示例 |
|------|------|------|
| 主分支 | `main` | — |
| 功能分支 | `feat/<topic>` | `feat/q01-brep-input` |
| 修复分支 | `fix/<topic>` | `fix/harness-validation` |
| 文档/框架 | `chore/<topic>` | `chore/handoff-template-update` |

## 提交信息（Conventional Commits 简版）

```
<type>(<scope>): <subject>

[optional body]
```

| type | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复 |
| `docs` | 仅文档 |
| `chore` | 框架/工具/脚手架 |
| `refactor` | 重构 |

`scope` 可选，建议用流水线阶段（如 `q02-codegen`）或 `agent`。

## 何时提交

- 用户明确要求 commit 时
- 完成一个可 review 的逻辑单元（功能 + Handoff 更新）
- Handoff 与代码变更应同一次提交或紧邻提交，便于恢复上下文

## 禁止操作

- 不 force push 到 `main`
- 不 skip hooks（除非用户明确要求）
- 不提交 `.env`、密钥、`secrets/`
- 不擅自 amend 已推送的 commit

## Handoff 与 Git

结束有意义的工作段落后：

1. 更新 `docs/handoff/active/`（skill `handoff-create`）
2. 用户要求 commit 时，Handoff 文件一并纳入

## 远程仓库（待配置）

添加 remote 后在此记录 URL 与保护分支策略。
