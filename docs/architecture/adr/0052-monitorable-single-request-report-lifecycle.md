# ADR-0052: Monitorable Single-Request Report Lifecycle

- **Status**: Accepted
- **Date**: 2026-08-10

## Context

M70 can observe only an existing report with `run_status`. The single-request
control and observation-first-pass producers wrote their first reports after a
provider request ended, leaving no monitorable in-flight state for M80.

## Decision

The producer gains explicit prepare/execute phases. Prepare atomically writes
a content-free `running` report; M70 may then attach without modifying that
report. Execute accepts only the prepared report, records issuance immediately
before the provider call, and writes a terminal report on success or handled
lifecycle failure.

## Consequences

This preserves report/monitor separation and yields a durable terminal record
for an issued request. It adds a local lifecycle step but grants no provider
authority, retry, or budget reuse.
