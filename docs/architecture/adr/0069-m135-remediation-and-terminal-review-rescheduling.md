# ADR-0069: Insert Offline M136 Remediation Before Re-entering M135

- **Status**: Accepted
- **Date**: 2026-08-12
- **Context**: M135's complete no-input `wsl-bwrap` preflight stopped at the
  frozen `axisymmetric_revolve:param_revolve_centered_low:no_card` fixed-script
  control. Its frozen epoch cannot repair, skip, or replace a condition.

## Decision

Create M136 as a separately selected G2, offline-only remediation package. It
may diagnose and correct only the local fixed-script/no-input failure and must
retain M134/M135's frozen cohort and policy. The previously planned M136 G2
terminal epoch-evidence review is renumbered M137. M137 remains user-selected
and cannot begin until a fresh M135 preflight passes, itemized hosted
authorization is granted, and that later epoch reaches a terminal state.

## Consequences

- M135 stays blocked and no existing budget, report/monitor path, or authority
  can be reused.
- A successful M136 requires a full fresh M135 G3 preflight; it does not make
  a hosted request permissible.
- All unrelated family and coverage routes remain deferred through M137's
  independent terminal review.
