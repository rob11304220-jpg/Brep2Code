# Handoff: M146 Development-Evidence Information Architecture

- **Date**: 2026-08-13
- **Subproject**: `brep2code`
- **Status**: `done` (archived after independent approval)
- **Related workpack**: `WP-M146-001-development-evidence-information-architecture`

## Goal

Implement a source-linked development-side evidence crosswalk and derived
navigation for mechanism, multi-axis difficulty, evidence maturity, admission
risk, and decision gaps, without transferring existing authority or creating
runtime knowledge.

## Done

- M145 delivered the reviewed cross-sectional report.
- User selected TRG-030; M146 is now active with Liaol as independent reviewer.
- Confirmed that the development knowledge system is the project theory entry,
  centered on bounded modeling hypotheses; pipeline and case/governance records
  retain their distinct system and evidence-asset roles.
- Recorded M146's five derived views and registered the user-confirmed deferred
  follow-on route `WP-TRG-031` through `WP-TRG-035` without activating any of
  those packages.
- Completed the M146 owner-side implementation: the versioned source-linked
  crosswalk, its five derived navigation views, deterministic audit, and
  maintenance guidance. The crosswalk has five bounded modeling hypotheses;
  its audit validates declared hashes, stable IDs, relationship integrity,
  non-projection boundaries, and forbidden asset paths without reading
  fixtures, scripts, held-out inputs, or runtime resources.
- Corrected two discovered governance drifts: M145/M146 current-route state in
  `docs/workpacks/README.md`, and a completed workpack incorrectly retained as
  `next_eligible_workpack` in the coverage matrix.

## In progress

- None. M146 is closed and archived after Liaol's independent G2 approval.

## Next

- Wait for explicit user selection of one deferred successor. Do not activate
  `WP-TRG-031` through `WP-TRG-035` or `WP-TRG-028` automatically.
- After M146 review, do not auto-start a successor.  The confirmed planning
  route is registered as deferred `WP-TRG-031` through `WP-TRG-035`:
  theory-map/document navigation, Agent routing, case-evidence role alignment,
  capability-contract code alignment, then a separately selected hosted
  evaluation; `WP-TRG-028` remains deferred.

## Decisions

- The crosswalk is derived navigation, not a registry, manifest, runtime
  resource, or authority transfer.
- Held-out facts may only be represented through declared metadata and reviewed
  documentary links.
- The theory-navigation entry is a bounded modeling hypothesis.  The Q01--Q04
  pipeline remains the runtime/system entry; case and governance records remain
  evidence-asset management.  The five views are derived projections over one
  relationship layer, not new authorities or directory trees.
- The confirmed follow-on route is planning only.  Each stage needs a fresh
  user-selected bounded package and cannot confer case, code, runtime, or
  hosted authority on a later stage.
- Liaol approved M146's independent G2 review. The pytest outer-deadline
  timeout remains a recorded non-terminal limitation; it is not reclassified
  as a passing or failing test result.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M146-001-development-evidence-information-architecture.md` |
| Crosswalk | `docs/corpus/knowledge/development-evidence-crosswalk-v1.json` |
| Navigation | `docs/corpus/knowledge/development-evidence-crosswalk-v1.md` |
| Audit | `tools/audit_development_evidence_crosswalk.py` |
| Deferred route | `docs/workpacks/deferred/WP-TRG-031-project-theory-map-and-document-navigation.md` through `WP-TRG-035-hypothesis-to-hosted-evaluation.md` |
| M145 report | `docs/corpus/case-evidence-mechanism-difficulty-report-v1.md` |
| M143 profile | `docs/corpus/knowledge/admissions/case-library-admission-profile-v1.json` |
| Deferred successor | `docs/workpacks/deferred/WP-TRG-028-reference-knowledge-projection-and-evaluation.md` |
| Validation | `uv run python tools\\check_governance.py`; `git diff --check` |

## Resume prompt

```
M146 is complete. Read `docs/workflow/status.md` and wait for an explicitly
selected bounded successor. Do not reactivate M146 or infer any case, runtime,
provider, or hosted authority from its crosswalk. The recorded full pytest
timeout remains non-terminal historical validation evidence.
```
