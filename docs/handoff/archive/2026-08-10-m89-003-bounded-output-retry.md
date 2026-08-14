# Handoff: M89-003 bounded-output retry

- **Date**: 2026-08-10
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M89-003-bounded-output-reference-assisted-retry`

## Goal

Implement and offline-validate a fixed positive token cap for one fresh,
reference-assisted M89 retry proposal, then perform the required read-only
hosted preflight before asking the user for separate itemized authorization.

## Done

- User selected the bounded G3 retry proposal.
- Status authority, completed M89 workpacks, lifecycle rules, and hosted
  preflight requirements were reviewed.
- The new workpack is registered with a fixed case, role, two-request budget,
  4096-token cap, proposed 300-second deadline, fresh paths, and no-retry
  terminal disposition.
- Added and tested the separate M89-003 command, which requires 4096 tokens,
  records that cap in a fresh checkpoint, and propagates it to both provider
  calls without changing the closed M89-001 command.
- Offline checks passed: observed-build 28, provider-trace 10, fast 66, full
  212, Ruff, governance, and format checks.
- Read-only preflight passed: fixed input/manifest/card hashes; non-secret
  DeepSeek `deepseek-v4-pro` configuration at `https://api.deepseek.com`;
  fresh report/monitor paths; and a passing local no-input `wsl-bwrap`
  reference-script control at `C:\\tmp\\brep2code-m89-003-preflight`.
- Liaol independently approved the M89-003 offline scope on 2026-08-10. This
  review does not grant provider authority.
- Liaol then explicitly authorized the complete fixed M89-003 hosted boundary:
  destination/derived egress, `deepseek-v4-pro`, one hashed case/role/card,
  exactly two requests, zero retry/repair, 4096 tokens, a 300-second deadline,
  no-input `wsl-bwrap`, and the fresh report/monitor paths.
- The one authorized run reached terminal `completed` / `pass`: exactly 2/2
  requests, 4096-token cap, fixed card/role, no input access, independent
  reconstruction provenance, and all script/output/bbox/volume/topology gates
  passed. The durable monitor observed the terminal report.
- Liaol independently approved terminal closure on 2026-08-10 after checking
  the fixed authorization boundary, 2/2 accounting, checkpoint cap,
  sandbox/provenance, gate results, and absence of retry/repair.

## In progress

- M89-003 is closed. The authorized request budget is exhausted and is not
  reusable.

## Next

- Archive this completed handoff and select a new bounded package only on user
  direction.

## Decisions

- The retry is M89-003, not M90+ or M73, because it tests only a bounded
  transport hypothesis using M89-002 diagnostics.
- Use 4096 positive maximum output tokens and a 300-second per-request
  deadline; neither implies a response guarantee or a new provider budget.
- Preserve exactly two requests, the P1 `three_hole_plate` case, the
  `repeated boolean-cut tool` role, `wsl-bwrap` no-input execution, and all
  existing gates.
- ADR-0053 remains the architecture basis for token-cap and first-byte
  diagnostics; no new ADR is needed unless the implementation changes that
  boundary.

## Blockers

- None. The hosted budget is exhausted and cannot be reused.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/active/WP-M89-003-bounded-output-reference-assisted-retry.md` |
| Status | `docs/workflow/status.md` |
| CLI | `brep2code/cli/__init__.py` |
| Runner | `brep2code/agent/observed_build.py` |
| Prior evidence | `docs/workpacks/done/WP-M89-001-reference-assisted-p1-three-hole-plate-hosted-smoke.md` |
| Diagnostic basis | `docs/workpacks/done/WP-M89-002-provider-lifecycle-observability-diagnosis.md` |

## Resume prompt

```
Continue Brep2Code work: select a new bounded package only if requested.
Read docs/handoff/active/2026-08-10-m89-003-bounded-output-retry.md.
First action: read docs/workflow/status.md; no M89-003 provider request may be issued.
```
