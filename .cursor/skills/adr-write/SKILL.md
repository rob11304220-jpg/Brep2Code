---
name: adr-write
description: Creates a numbered architecture decision record under docs/architecture/adr/ and links it from the active handoff. Use when making or recording implementation-side architecture or process decisions.
disable-model-invocation: true
---

# ADR Write

Record an implementation-side decision as a numbered ADR.

## Inputs

- Title (short, kebab-case slug)
- Context, Decision, Rationale, Consequences
- Alternatives considered (optional table)

## Steps

1. Read `docs/runbooks/adr-authoring.md` for template
2. List `docs/architecture/adr/` and determine next number (`NNNN`, four digits)
3. Create `docs/architecture/adr/NNNN-<slug>.md` with Status `Accepted` or `Proposed`
4. Update active handoff in `docs/handoff/active/` — add link under **Decisions**
5. Tell the user the ADR path

## Output

- One new ADR file
- Handoff Decisions section updated (if active handoff exists)
- Do not commit unless the user asks

## Rules

- ADR = why; runbook = how
- Design Q&A answers stay in paper vault; ADR may summarize + link

## Reference

- `docs/runbooks/adr-authoring.md`
