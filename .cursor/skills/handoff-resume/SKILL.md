---
name: handoff-resume
description: Reads the latest active handoff to produce a resume plan. Use at the start of a new session or when the user asks for /resume.
disable-model-invocation: true
---

# Handoff Resume

Restore context from Git-tracked handoff files and propose the next actions.

## Steps

1. Read root `AGENTS.md`
2. List `docs/handoff/active/` and pick the **latest** file (by `YYYY-MM-DD` prefix in filename)
3. Parse: Goal, Status, Next, Blockers, Key paths, Resume prompt
4. Output to the user:
   - **Summary** (2–3 sentences)
   - **Suggested first action** (one concrete step)
   - **Open blockers**
   - Full **Resume prompt** from the handoff (or reconstruct if missing)
5. Do not assume context not written in handoff or repo files

## If no active handoff

- State that no handoff was found
- Offer to read `README.md` and ask the user for the goal
- Suggest running `handoff-create` after clarifying

## Reference

- `docs/runbooks/handoff-protocol.md`
