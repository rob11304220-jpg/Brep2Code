# ADR-0040: Status Dashboard and Evidence Ledger

- **Status**: Accepted
- **Date**: 2026-08-07
- **Context**: `status.md` mixed operational state with lengthy history.

## Decision

Keep `status.md` compact, place milestone history in
`docs/workflow/milestone-history.md`, and record deferred packages in the
machine-checkable `docs/workflow/evidence-ledger.json`.

## Consequences

- **Positive**: session recovery is faster and re-entry conditions are explicit.
- **Negative**: deferred-package changes update a second index.
- **Mitigation**: the governance audit validates the ledger and index links.
