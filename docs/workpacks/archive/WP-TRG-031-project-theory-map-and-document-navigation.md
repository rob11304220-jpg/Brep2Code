# WP-TRG-031: Project Theory Map and Document Navigation

- Status: deferred
- Owner: unassigned
- Reviewer: not required
- Risk tier: G1

## Entry condition

M146 has independently reviewed its source-linked crosswalk and the user
selects this package. The crosswalk must already distinguish bounded modeling
hypotheses from their evidence assets and adoption boundaries.

## Goal

Publish the project-level theory map that makes the development knowledge
system the primary human and Agent entry for understanding verified and unknown
bounded B-Rep-to-modeling-sequence hypotheses.

## Scope

- Add one compact theory-map/document-navigation entry that **reuses** the M146
  crosswalk's five derived views; do not reproduce them as a second registry or
  competing theory summary.
- Route readers from that entry to the existing Q01--Q04 pipeline, authoritative
  knowledge units, source-linked crosswalk, and workflow status, in this order:
  theory navigation, system/runtime architecture, evidence-asset management,
  then current task selection.
- State explicitly that the crosswalk is the theory-navigation view, the
  pipeline is the system/runtime view, and case/governance records are the
  evidence-asset view; `status.md` remains the only execution authority.

## Compatibility constraints

Navigation is derived documentation only. Do not move or rewrite authoritative
source records, reclassify cases, change runtime behavior, or imply that a
reviewed development hypothesis is hosted or runtime eligible.

The entry may link a crosswalk hypothesis ID, but it cannot alter its source
hashes, relationships, evidence maturity, or adoption boundary.

## Acceptance

```powershell
uv run python tools\check_governance.py
python tools\audit_development_evidence_crosswalk.py
git diff --check
```

## Out of scope

`AGENTS.md` routing changes, case metadata changes, code changes, runtime
projection, provider use, and hosted evaluation.
