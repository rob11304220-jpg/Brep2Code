# WP-M147-001: Deferred Successor Crosswalk Alignment

- Status: done
- Milestone: M147
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Entry condition

M146 is complete and independently approved. The user selected this bounded
documentation-governance package to align the deferred TRG-031--035 route with
the reviewed development-evidence crosswalk.

## Goal

Make each deferred successor's purpose, handoff artifact, and authority
boundary explicit relative to the M146 bounded-modeling-hypothesis crosswalk,
without activating a successor or changing any authoritative source.

## Scope

- Update `WP-TRG-031` through `WP-TRG-035` so they reuse the M146 crosswalk as
  their common development-side navigation layer rather than duplicate it.
- State each package's exact crosswalk input/output: project entry routing,
  Agent routing, case-evidence relationship links, one bounded implementation
  contract, or a hash-pinned hosted campaign basis.
- Preserve the existing trigger ordering, independent-review requirements, and
  explicit user-selection/hosted-authorization gates.

## Decision-package impact

- `decision_id`: none; M147 changes deferred package wording only.
- Q01/Q02 and Q03/Q04 effects: none.
- Evidence role: navigation and governance alignment only.
- Knowledge disposition: no reusable runtime knowledge and no source-authority
  change.

## Compatibility constraints

Do not modify the M146 crosswalk, case metadata, registry, manifests, Harness,
runtime resources, providers, tests, or hosted configuration. A deferred
workpack remains a navigation record, not an implementation authorization.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the aligned deferred descriptions and record the resulting M147
navigation/authority boundary in the active handoff.

## Closure rationale

Completed on 2026-08-13. TRG-031 now reuses rather than duplicates the M146
views; TRG-032 routes by hypothesis and authority; TRG-033 reserves a separate
case-evidence relationship layer; TRG-034 reserves a one-hypothesis
implementation-contract mapping; and TRG-035 freezes crosswalk ID/SHA-256 as
campaign provenance without treating it as authorization. Crosswalk audit,
governance audit, and `git diff --check` passed. No trigger was activated.

## Permitted stop conditions

User review; a source-authority conflict; or a required change outside
deferred-route documentation.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff. On closure, archive the handoff; do not activate any trigger.

## Out of scope

Activating TRG-031--035 or TRG-028; moving authorities; case alignment;
contract/code changes; runtime projection; provider use; hosted evaluation.
