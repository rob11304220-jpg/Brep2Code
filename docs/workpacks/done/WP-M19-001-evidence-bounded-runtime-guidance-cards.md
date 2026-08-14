# WP-M19-001: Evidence-Bounded Runtime Guidance Cards

- Status: done
- Milestone: M19
- Owner: unassigned

## Goal

Create an offline, auditable foundation for preserving reusable development
evidence without exposing broad development governance material to a runtime
LLM.

## Scope

- Add the experience-card contract, index, three source-linked starter cards,
  and an offline audit.
- Record the lasting governance decision and repeatable authoring procedure.

## Compatibility constraints

No Harness, CLI, provider, prompt, tool, parser, helper, manifest, gate,
corpus-report schema, or default runtime-resource mount changes are permitted.
No provider request occurs.

## Acceptance

```powershell
uv run python tools/audit_runtime_guidance.py
uv run python -m pytest tests/test_runtime_guidance.py
uv run python -m ruff check tools/audit_runtime_guidance.py tests/test_runtime_guidance.py
```

## Result

Completed with three static cards: a two-case direct sandbox-path diagnosis,
an input-probe fail-closed operation, and a geometry-gate counterexample.  The
M17 Fusion mapping remains deliberately excluded while its bounded evidence
audit is active.

## Out of scope

Runtime retrieval, prompt injection, hosted comparison, card promotion,
automatic extraction from traces, model training, and all M17 parser work.
