---
name: handoff-create
description: Creates or updates a cross-session handoff document in docs/handoff/active/. Use when ending a session, switching tasks, or when the user asks for /handoff.
disable-model-invocation: true
---

# Handoff Create

Create or update a handoff file so the next agent session can resume without guessing.

## Inputs

Gather from the current session:

- Title (short)
- Subproject: `brep2code`
- Goal, Done, In progress, Next, Decisions, Blockers
- Key paths (files, branch, commands)

## Steps

1. Read template: `docs/handoff/TEMPLATE.md`
2. List existing files in `docs/handoff/active/`
3. If updating the same ongoing task, edit the existing active file; otherwise create:
   - Path: `docs/handoff/active/YYYY-MM-DD-<slug>.md`
   - `<slug>`: lowercase kebab-case, e.g. `agent-framework-init`, `q01-brep-input`
4. Fill all template sections; write a concrete **Resume prompt** at the end
5. Keep `active/` to **1–3 files**: move superseded files to `docs/handoff/archive/`
6. Tell the user the handoff path and the Resume prompt text

## Output

- One primary file under `docs/handoff/active/`
- Do not commit unless the user asks

## Reference

- `docs/runbooks/handoff-protocol.md`
