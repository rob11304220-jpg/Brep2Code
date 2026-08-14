# ADR-0087: Make M180 the Sole Fixed Asymmetric Execute Entrypoint

- **Status**: Accepted
- **Date**: 2026-08-14

## Context

M179 supplied only fake-provider adapter evidence.  The frozen M176 campaign
needs one provider-facing entrypoint that cannot change its cohort, card,
model, token/deadline, executor, serial/no-retry, completion-slot, or
HTTP-request boundaries after itemized authorization.

## Decision

`m180-asymmetric-campaign-execute` accepts only `--authorize-hosted` and the
local env-file location.  It revalidates fresh M179 dual checkpoints, records
authorization before provider construction, accepts only DeepSeek V4 Pro, and
runs the fixed annex then main cohort serially.  Each attempted provider call
atomically consumes its product request budget before provider work.  Reports
retain separate 102 completion-slot and 69 HTTP-request accounting.  Q01 is
local; the annex's card exchange, script generation, and an eligible
`source_only` repair are the only provider requests.

## Consequences

The command remains unusable until fresh local preflight, independent G3
review, and explicit itemized user authorization have occurred.  It offers no
policy overrides and does not permit resume, retry, report reuse, or budget
reuse.  Its offline fake tests establish control-flow and accounting only, not
provider or model evidence.
