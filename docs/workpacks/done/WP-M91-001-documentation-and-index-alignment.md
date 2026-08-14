# WP-M91-001: Documentation and Index Alignment

- Status: done
- Milestone: M91
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Align current documentation and knowledge-index links with the completed M90
promotion and the current M80-gated hosted route, without changing any case
asset, executable manifest, Harness behavior, provider boundary, or runtime.

## Scope

- Correct the active self-authored case count and completed-family summary.
- Bring the active sequence-paired route through M90 and repair its stale M23
  workpack link.
- Correct current decision-index workpack paths and the M76 prerequisite.

## Compatibility constraints

Documentation and index metadata only. No case lifecycle field, manifest,
provider, hosted request, credential, runtime, training, external-data, or
Harness change is permitted.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Status transition

After acceptance, update `docs/workflow/status.md` first, move this workpack
to `done/` with `Status: done`, archive its handoff, and then select the
separate G2 case-metadata alignment workpack.

## Out of scope

Editing M90 `case.json` lifecycle metadata, creating an ADR, changing case
membership, or launching a hosted operation.

## Result and closure

- Corrected the active self-authored case count from 75 to 81 in current
  summaries and catalog metadata, and added the completed M90 family to those
  summaries.
- Repaired the active sequence-paired route through M90, its stale M23 link,
  three stale decision-index workpack paths, and the M76 prerequisite wording
  to match ADR-0051.
- Acceptance on 2026-08-10: governance audit, `git diff --check`, JSON parse,
  and repaired-link target checks passed.
- Closure rationale: these are documentation and index corrections only. The
  conflicting M90 `case.json` lifecycle fields remain intentionally deferred
  to the separately scoped G2 workpack.
