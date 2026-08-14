---
name: paper-vault-lookup
description: Locates and reads Brep2Code design notes and literature in the external paper vault via docs/links/paper-vault.md. Use when the user asks about Q&A, literature, Articraft, or design background. Do not copy paper content into this repo.
disable-model-invocation: true
---

# Paper Vault Lookup

Find design and literature context in `D:\paper` without duplicating content into this repo.

## Steps

1. Read index: `docs/links/paper-vault.md`
2. Identify the target resource (project entry, Q&A, literature note)
3. Read the external file with the `Read` tool, or use Obsidian MCP (`user-obsidian`) if available
4. Summarize findings for the user in the chat
5. If a decision must be recorded in this repo:
   - Write ADR summary + link to paper note (skill `adr-write`)
   - Or update Handoff Decisions — **never** paste full Q&A answers into `docs/`

## Common targets

| Need | Path |
|------|------|
| Project overview | `D:\paper\Projects\Brep2Code.md` |
| Q01–Q04 design | `D:\paper\Literature\zhouArticraftAgenticSystem2026-QA.md` |
| Pipeline index (this repo) | `docs/architecture/pipeline.md` |

## Rules

- Paper vault is source of truth for Q&A status and literature notes
- This repo only links and records implementation-side ADRs

## Reference

- `docs/runbooks/paper-vault-access.md`
