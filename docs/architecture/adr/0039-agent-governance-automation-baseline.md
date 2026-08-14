# ADR-0039: Agent Governance Automation Baseline

- **Status**: Accepted
- **Date**: 2026-08-07
- **Context**: The repository already defines handoff, workpack, status, and
  ADR lifecycle rules, but their consistency depended on manual review. A
  completed handoff could therefore remain in `active/` even when no active
  workpack existed.

## Decision

Add a dependency-free governance audit under `tools/`, focused regression tests,
and a minimal GitHub Actions CI workflow. The audit is the shared enforcement
point for active-directory status, status-page alignment, and ADR naming.

## Rationale

The checks cover high-value, deterministic invariants without coupling the
development-governance layer to Harness internals or external services. They
remain runnable locally and do not expand hosted-provider authority.

## Consequences

- **Positive**: lifecycle drift is detected before review or merge; local and
  CI behavior use the same audit.
- **Negative**: future governance-format changes must update the audit and its
  focused tests.
- **Mitigation**: the audit emits specific diagnostics and is documented in a
  small runbook.

## Alternatives Considered

| Alternative | Rejected because |
|---|---|
| Manual checklist only | It cannot reliably prevent stale active records. |
| CI without a local audit | Developers would lack a fast, reproducible pre-push check. |
| Parse all Markdown semantics | It would be brittle and disproportionate to the current invariants. |
