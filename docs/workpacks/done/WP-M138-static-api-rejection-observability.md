# WP-M138: Static API Rejection Observability

- Status: done
- Milestone: M138
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Add content-safe diagnostics for future M115 static API rejections so later
evidence review can distinguish declared classifier mechanisms without
persisting generated source or provider responses.

## Scope

- Record classifier version, normalized rejection reason, script SHA-256,
  UTF-8 byte count, parse status, imported module names and direct call names
  when a future card script is statically inadmissible.
- Attach diagnostics only to `static_api_inadmissible` terminal checkpoint
  entries and prove deterministic content-free behavior with local tests.

## Compatibility constraints

Do not alter M115 classifier acceptance semantics, cards, prompts, frozen M135
results, provider behavior, Harness gates, repair/retry or report identities.
Do not store raw generated scripts, provider output, credentials or paths.

## Acceptance

```powershell
uv run python -m pytest tests\test_m135_epoch.py tests\test_m115_prismatic_policy.py -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the content-safe schema and regression evidence, pass acceptance, and
obtain Liaol's independent G2 review.

## Out of scope

Card update, repair policy, hosted execution, re-running M135, held-out
evaluation or any provider request.

## Owner completion evidence (2026-08-12)

Future static rejections now record only normalized classifier reason, version,
SHA-256, byte count, parse status and sorted import/call names. The M135-011
terminal report is not changed or retrofitted. Focused tests passed `15
passed in 205.63s`; full suite passed `251 passed in 573.64s`; Ruff,
governance and diff checks passed. Await independent G2 review.

## Independent review and closure (2026-08-12)

Liaol approved the independent G2 review. The review accepted the narrow
content-safe schema, the no-retrofit M135 boundary and all recorded offline
validation. This closure neither updates a card nor authorizes repair or any
hosted request.
