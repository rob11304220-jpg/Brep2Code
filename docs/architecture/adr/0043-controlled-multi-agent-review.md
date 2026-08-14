# ADR-0043: Controlled Multi-Agent Review

- **Status**: Accepted
- **Date**: 2026-08-07

## Decision

Use a single-owner model for every active workpack. Contributors may perform
non-overlapping work, while G2/G3 closure requires an independent reviewer.
Lifecycle records and high-risk paths remain exclusive-owner edits.

## Consequences

The protocol supports small, auditable parallel work without adding an agent
scheduler, shared runtime memory, or additional authority. It deliberately
does not attempt large-scale autonomous task dispatch.
