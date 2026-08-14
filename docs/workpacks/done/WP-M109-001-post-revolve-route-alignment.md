# WP-M109-001: Post-Revolve Route Alignment

- Status: done
- Milestone: M109
- Owner: Codex
- Reviewer: not required
- Risk tier: G1

## Goal

Align current route and knowledge-index navigation with M108's completed
`revolve-v1` governance promotion.

## Scope

Update current route, five-family portfolio, expansion-priority and coverage
index wording only. Preserve historical records and all technical boundaries.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Out of scope

Case, manifest, runtime, provider, hosted, policy, card or knowledge-content changes.

## Closure rationale

Updated only current navigation to show M108 complete and shell/rib as the next
exclusive modeling-sequence choice. Governance and diff checks passed.
