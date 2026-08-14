# Handoff: M9-001 ABC hosted first-pass evaluation

- **Date**: 2026-08-02
- **Subproject**: `brep2code`
- **Status**: `done`

## Goal

Prepare and execute a bounded, two-stage hosted first-pass evaluation on the M8 ABC v00 8/4 split, then review only completed engineering evidence.

## Done

- Added explicit development and held-out manifests preserving the M8 selection order.
- Added offline static audit coverage that proves the splits are disjoint, exhaustive, local-only, and fixture-free.
- Created M9 workpack and review template.
- Verified all 12 local assets against the M8 SHA-256 record.
- Completed M9-002: shared bounded input probe (45 seconds), output probe remains 15 seconds, input failures now fail closed, and first-pass cannot issue a provider request after input-probe failure; see [`ADR-0008`](../../architecture/adr/0008-bounded-input-probe-timeout.md).
- Revalidated both ignored `wsl-bwrap` control reports: all 12 input summaries and scripts succeeded; all 12 fixed-scaffold geometry failures are expected control evidence.
- Formally recorded the M9-post evidence-gated route: M10-001 reviews two completed split reports before selecting one conditional follow-on; no follow-on workpack may be started before then.
- An authorized development launch was externally stopped by the host command limit. Its atomic report `data/corpus-runs/abc-v00-m9-001-development-pro-authorized-20260802.json` is `running`, has 0 completed cases and `requests_used: 0`; no provider request was issued.
- The separately authorized development retry completed with `deepseek-v4-pro` and `wsl-bwrap`: 8/8 cases, one repair round, 120-second provider deadline, and 12/16 requests used. Its schema-v3 report `data/corpus-runs/abc-v00-m9-001-development-pro-retry-20260802.json` records four final `script_failure` outcomes, four final `provider_request` outcomes, and one successful repair among four repair attempts.
- The separately authorized held-out batch completed under the unchanged policy: 4/4 cases, 5/8 requests, one first-pass pass, one `script_failure`, two `provider_request` outcomes, and one failed repair.
- M10-001 reviewed both completed reports and selected M10-003 deterministic external corpus increment; no helper attribution threshold or geometry-diagnostics trigger was established.

## In progress

- None. M9-001 is complete; the active follow-on is M10-003.

## Next

- Preserve this completed review as bounded engineering evidence only. M10-003 may admit local external inputs offline but does not authorize provider calls.

## Decisions

- The held-out batch must use the unchanged provider/model, policy, executor, deadline, and repair bound after a separate explicit authorization (4 cases, 8 requests maximum).
- `running` or `interrupted` reports are partial evidence and never support aggregate conclusions or budget reuse.
- Input summaries are bounded at 45 seconds while generated output summaries remain bounded at 15 seconds; input probe failure blocks provider issuance with zero request use.
- [ADR-0009](../../architecture/adr/0009-evidence-gated-post-m9-evolution.md) requires completed external evidence before a geometry diagnostic, external increment, narrow helper, IR, or SDK decision; it does not authorize a provider request.
- Completed M9 evidence selected M10-003; see [`m9-abc-hosted-evaluation-review.md`](../../architecture/v1/m9-abc-hosted-evaluation-review.md).

## Blockers

- None for M9-001. M10-003 is active and remains offline.

## Key paths

- `docs/workflow/status.md`
- `docs/workpacks/done/WP-M9-001-abc-hosted-first-pass-evaluation.md`
- `docs/architecture/v1/m9-abc-hosted-evaluation-review.md`
- `docs/architecture/v1/post-m9-evidence-gated-roadmap.md`
- `docs/workpacks/backlog/WP-M10-001-m9-evidence-review-and-routing.md`
- `docs/corpus/external/abc-v00-m9-001-development-manifest.json`
- `docs/corpus/external/abc-v00-m9-001-held-out-manifest.json`
- `data/corpus-runs/abc-v00-m9-001-development-pro-authorized-20260802.json` (ignored partial checkpoint)
- `data/corpus-runs/abc-v00-m9-001-development-pro-retry-20260802.json` (ignored completed development report)

## Resume prompt

```
M9-001 is complete. For active work, read docs/handoff/active/2026-08-02-m10-003-external-increment.md and continue M10-003 without issuing provider requests.

After both split reports are completed, read ADR-0009 and WP-M10-001 before selecting exactly one evidence-gated follow-on route.
```
