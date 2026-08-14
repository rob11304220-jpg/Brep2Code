# Handoff: M180 Asymmetric Hosted Execute Entrypoint

- **Date**: 2026-08-14
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M180-001-asymmetric-hosted-execute-entrypoint`

## Goal

Implement and offline-validate the fixed M179 hosted execute entrypoint; issue no request.

## Done

- Added fail-closed M179 dual-checkpoint authorization gate and provider-injected serial adapter.
- Added M180 CLI authorization rejection and fixed `deepseek-v4-pro` provider boundary.
- Focused asymmetric tests pass (4 passed); no credential or provider action occurred.
- Completed the fixed Q01/card/generation/gate/classified-source-only-repair
  state machine, checkpoint-before-request accounting, and separate 102-slot /
  69-request reporting.  The M180 CLI revalidates M179 before env-file access
  and has no campaign-policy overrides.
- Owner-side validation passed: M179 admission (zero-request 102/69), M180
  authorization refusal, focused fake tests, Ruff, governance/diff checks, and
  full pytest (`293 passed in 524.06s`).
- Liaol approved the independent M180 G3 review.  The approval verifies the
  offline boundary and evidence only; it does not authorize egress.
- Recorded the post-campaign readiness-lifecycle proposal and `TRG-042` future
  option.  It preserves M180 as the current route, requires a terminal
  independently reviewed report before selection, and defers interpretation of
  that report to a later decision.

## Next

- Wait for the user to select a new bounded G3 hosted-execution workpack.  Its
  fresh preflight, independent review, and exact itemized authorization remain
  required before any provider construction or request.
- After the fixed campaign has fresh itemized authorization, executes, and
  receives independent terminal review, the user may separately select
  `TRG-042` to improve future campaign readiness.  Do not evaluate the
  campaign's model result as part of that process workpack.

## Decisions

- The current campaign must complete its existing M180-to-terminal-review path
  without a long-term process change.  Future lifecycle improvement is a
  `future option`, not an active successor or hosted authorization.
- The proposed future lifecycle is `draft -> frozen -> executable_offline ->
  reviewed_ready -> authorized -> running -> terminal_reviewed`; its durable
  proposal is
  [`hosted-campaign-readiness-lifecycle-proposal.md`](../../architecture/v1/hosted-campaign-readiness-lifecycle-proposal.md).

## Blockers

- Hosted egress requires later independent review and itemized user authorization.
- `TRG-042` cannot be selected until the current campaign's terminal report is
  independently reviewed; it cannot be used to interpret that report.
