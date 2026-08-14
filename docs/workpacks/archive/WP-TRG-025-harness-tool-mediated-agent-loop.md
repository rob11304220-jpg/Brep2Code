# WP-TRG-025: Harness Tool-Mediated Agent Loop

- Status: deferred
- Owner: unassigned
- Reviewer: independent reviewer required
- Risk tier: G2

## Entry condition

`WP-TRG-024` is complete and its campaign identity/egress contract has passed
independent review.  The user then selects this workpack.

## Goal

Implement a bounded Harness-owned agent turn loop: the LLM may request declared
Q01 probes or one selected guidance card, receive sanitized tool results, emit
a replacement script, and receive structured execution/gate feedback.

## Scope

- Define provider-neutral tool-call and tool-result continuation semantics.
- Expose only schema-bound, revision-scoped Q01 probes and explicit guidance
  cards; enforce per-turn/total tool budget, response byte cap and trace
  redaction.
- Execute generated scripts only through the restricted Harness and return
  structured signal summaries rather than shell access or raw workspace data.
- Test no-card, unavailable/wrong-card, tool-limit, malformed-call, script,
  execution and gate-feedback paths using fake providers and local sandbox.
- Record the applicability and limits of ReAct/Toolformer as literature inputs;
  do not claim their results validate CAD tool use.

## Compatibility constraints

The LLM may not read arbitrary files, select arbitrary cards, access a shell,
mutate prior revisions or bypass static API, provenance or geometry gates.
This G2 workpack remains offline and does not promote a card or authorize a
provider request.

## Acceptance

```powershell
uv run python -m pytest tests -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Out of scope

Adaptive hosted campaigns, broad retrieval, repair policy, case expansion,
provider/model changes and direct raw B-Rep prompt injection.
