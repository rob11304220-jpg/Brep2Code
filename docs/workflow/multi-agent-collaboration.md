# Multi-Agent Collaboration

Use this protocol only for work scoped by one active workpack. It coordinates
development work; it does not grant runtime, provider, external-data, or
hosted authority.

## Roles

- **Owner**: one named agent owns scope, lifecycle records, integration, and
  closure. Only the owner edits `status.md`, the active workpack, the active
  handoff, evidence ledger, or ADR lifecycle fields.
- **Contributor**: may independently inspect, test, or prepare a bounded
  non-overlapping change. A contributor reports evidence to the owner and
  does not transition task state.
- **Reviewer**: required for G2/G3 work and must differ from the owner. The
  reviewer checks scope, acceptance output, evidence boundaries, and lifecycle
  alignment. Review does not confer any external authority.

## Parallel boundary

Record the owner, reviewer, contributors, exclusive paths, and closure
condition in the workpack or a short collaboration-plan section. Never edit
the same file concurrently. Provider policy, executable manifests, runtime
boundaries, and evidence-ledger records are always exclusive-owner paths.

## Review and conflict handling

The reviewer independently verifies the stated acceptance commands and checks
that the change did not widen the workpack. On conflicting findings: stop the
status transition, retain both observations in the workpack, let the owner
reconcile the evidence, then request re-review. Do not resolve a conflict by
silently changing a manifest, scope, or decision boundary.

## Closure

The owner records the reviewer outcome and durable evidence paths, updates
status first, and runs the governance audit. Contributors may continue
read-only analysis after closure only under a new workpack.
