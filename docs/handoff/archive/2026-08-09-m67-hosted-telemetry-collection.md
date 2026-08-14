# Handoff: M67 hosted telemetry collection

- **Date**: 2026-08-09
- **Subproject**: `brep2code`
- **Status**: `done`

## Closure

Liaol approved M67 on 2026-08-09. Two cases timed out before response and one
returned then failed in sandboxed script execution; no retry is authorized.
- **Related workpack**: `WP-M67-001-hosted-telemetry-collection-and-analysis`

## Goal

Prepare a fresh development-only hosted collection using M65/M66 telemetry.

## Done

- M66 is independently approved and closed. It makes timeout checkpoints retain
  strict count/timing telemetry with null unavailable response fields.

## In progress

- Fresh preflight is complete in
  [`m67-hosted-telemetry-preflight.md`](../../workflow/m67-hosted-telemetry-preflight.md).
  It fixes three independent low-variant operation-family cases, one request
  each, no repair and a 300-second deadline.

## Next

- Obtain new itemized authorization; do not launch automatically.

## Decisions

- Each case must use a new independent report and one new request budget; no
  prior report/budget/authorization is reusable.

## Blockers

- No hosted authorization has been granted for M67.

## Resume prompt

```
Continue M67 read-only preflight. Do not issue a provider request before a new
itemized user authorization.
```
