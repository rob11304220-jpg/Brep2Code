# ADR-0050: Durable Report Monitor Boundary

- **Status**: Accepted
- **Date**: 2026-08-09

## Context

Authorized hosted work can outlast an interactive command window. Existing atomic reports distinguish `running`, `completed` and `interrupted`, but require an operator-visible, durable observation lifecycle.

## Decision

Add an offline monitor that reads one existing report and atomically writes a separate versioned state file. It records heartbeat, last lifecycle phase, report progress, terminal status and an operator handoff. Missing, malformed or stale `running` reports are fail-closed as `operator_action_required`; terminal reports stop monitoring. The monitor must neither construct a provider nor modify the observed report or process.

## Consequences

Future approved runs can be followed durably without granting automation any authority to retry, resume, spend budget, access credentials or make causal claims about a timeout. Starting any new hosted work still requires fresh preflight and explicit authorization.
