# WP-M92-001: Four-Track Program Routing

- Status: done
- Milestone: M92
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Replace the ambiguous single-roadmap reading with four explicit, evidence-gated
program directions: hosted stability, reference-assisted construction,
reference-guided parameter variation, and modeling-sequence coverage.

## Scope

- Record the four tracks, their entry conditions, outputs and non-goals.
- State cross-track dependencies and the one-primary-track-per-workpack rule.
- Add durable ADR and navigation links without changing an existing task's
  execution, case lifecycle, provider boundary or runtime behavior.

## Compatibility constraints

Documentation/governance only. No provider request, hosted authorization,
case/manifest change, card mounting, prompt, Harness, gate or runtime change.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Status transition

Close after the navigation and ADR are internally consistent, then select the
separate G2 parameter-variation design workpack.

## Out of scope

Implementing retrieval, issuing hosted requests, creating parameter-variation
assets, or selecting a new coverage family.

## Result and closure

- Added ADR-0056 and the four-track roadmap, then linked them from the
  architecture and workflow entrances.
- Acceptance on 2026-08-10: governance audit and `git diff --check` passed.
- Closure rationale: routing now separates the four questions and their
  authorities without altering any execution, case or provider boundary.
