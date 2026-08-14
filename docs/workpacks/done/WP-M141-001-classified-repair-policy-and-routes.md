# WP-M141-001: Classified Repair Policy and Routes

- Status: done
- Milestone: M141
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2
- Trigger consumed: `WP-TRG-026`

## Entry condition

M140 is complete and independently reviewed. The user selected this workpack
after deciding that a bounded repair policy, rather than card revision, is the
next decision gap.

## Goal

Define and implement a fail-closed repair router that maps sanitized terminal
signals to one allowed edit scope, bounded request count and explicit plateau
or stop rule.

## Scope

- Classify static API/output, execution, selector ambiguity, sandbox/provenance,
  geometry/semantic/editability and lifecycle outcomes separately.
- Define source-level repair for local code errors independently from
  sequence/IR rollback or regeneration; the two must not share an editor or
  silently fall back to full-script regeneration.
- Define per-route maximum rounds, request accounting, changed-artifact scope,
  regression checks, repeated-failure plateau detection and terminal evidence
  schema.
- Implement local/fake-provider regression paths for admitted routes and reject
  unsupported/ambiguous routes before provider work.

## Compatibility constraints

M135 remains a completed zero-repair epoch.  No frozen campaign may be repaired
in place, and no retry/repair becomes hosted authority through this workpack.
Any hosted repair experiment requires a later fresh G3 policy, preflight,
authorization, denominator and report/monitor paths.

## Owner completion boundary

Publish a reviewed fail-closed classification/router contract, local
fake-provider implementation and regression evidence; update relevant traces,
runbooks and handoff; then obtain Liaol's independent G2 review. Do not request
hosted authorization as a completion substitute.

## Implementation status

- Added `classified-repair-v1`: a deterministic vocabulary with one admitted
  `source_only` fake-provider edit route, request cap, normalized plateau
  signature and per-revision trace evidence.
- Selector ambiguity, geometry/semantic/editability, sandbox/provenance,
  timeout, protocol and mixed feedback currently stop fail-closed. Sequence/IR
  repair remains unimplemented because no admitted locator/editor contract
  exists.
- Focused offline evidence: `tests/test_m141_classified_repair_policy.py`.
- Pending: Liaol's independent G2 review.

## Validation evidence (2026-08-12)

| Command | Terminal result |
| --- | --- |
| `uv run python -m pytest tests\test_m141_classified_repair_policy.py -q` | 5 passed in 2.47s |
| adjacent repair/tool-turn selection | 19 passed in 31.90s |
| `uv run python -m pytest -m fast -q` | 66 passed, 199 deselected in 4.57s |
| `uv run python -m pytest -q` (first window) | outer command window timed out after 484.1s; no pytest terminal result, so it is neither a pass nor a failure |
| `uv run python -m pytest -q` (fresh window) | 265 passed in 667.99s |
| `uv run python -m ruff check .` | passed |
| `uv run python tools\check_governance.py` | passed |
| `git diff --check` | passed |

## Closure

Liaol completed the independent G2 review and approved closure on 2026-08-12.
The delivered policy remains offline and fake-provider-only; sequence/IR and
hosted repair were explicitly not admitted.

## Permitted stop conditions

Independent review; a reproducible conflict with M139/M140 contracts; an
out-of-scope dependency on case admission, knowledge projection or hosted
authority; frozen input/resource drift; or a reproducible local validation
blocker.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff. On closure, archive this workpack and leave TRG-027 through TRG-028
deferred.

## Acceptance

```powershell
uv run python -m pytest tests -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Out of scope

Prompt tuning from M135, card revision, model/provider changes, case additions,
held-out evaluation and hosted execution.
