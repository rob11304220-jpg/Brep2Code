# 论文库查阅

实现仓通过索引文档链接 Obsidian 论文库，**不复制文献正文**。

## 索引入口

[`docs/links/paper-vault.md`](../links/paper-vault.md) — 所有外部路径的权威列表。

## 查阅步骤

1. 读 `docs/links/paper-vault.md` 定位目标资源
2. 用 `Read` 工具读取 `D:\paper\...` 对应文件（Agent 有文件系统访问时）
3. 或使用 Obsidian MCP（`user-obsidian`）搜索/读取 vault 内容
4. 将结论摘要写入本仓时：
   - 架构决策 → ADR（skill `adr-write`）
   - 会话进度 → Handoff
   - **禁止**把 Q&A 回答全文复制到 `docs/`

## 常见场景

| 需求 | 首选路径 |
|------|----------|
| 项目背景与阅读列表 | `D:\paper\Projects\Brep2Code.md` |
| 当前文献综合与验证交接 | `D:\paper\Projects\Brep2Code-research\outputs\literature-synthesis-and-validation-handoff.md` |
| Q01–Q04 历史路线比较（背景） | `D:\paper\Projects\Brep2Code-research\routes\q01-q04-synthesis.md` |
| Articraft 主文献 | `D:\paper\Literature\zhouArticraftAgenticSystem2026*` |
| 流水线索引（本仓） | `docs/architecture/pipeline.md` |

## Obsidian MCP（可选）

若启用 `user-obsidian` MCP：

- `vault_list` / `search_query` 定位笔记
- `vault_read` 读取内容
- 仍以 `paper-vault.md` 登记的路径为准，避免 ad-hoc 路径漂移

## Skill

显式引用 **`paper-vault-lookup`** 执行上述流程。


