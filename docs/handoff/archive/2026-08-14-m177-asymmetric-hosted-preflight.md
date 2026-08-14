# Handoff: M177 Asymmetric Hosted Preflight

- **Date**: 2026-08-14
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M177-002-asymmetric-hosted-preflight`

## Goal

Run and independently review a fresh, local-only M176 asymmetric campaign
preflight. It must create only the four fixed local checkpoints/monitor states
and must not construct a provider, read credentials, or send data externally.

## Done

- M178's fixed dual-product local campaign CLI was independently approved.
- The user selected fresh G3 workpack M177-002; M177-001's authorization
  remains archived and cannot be reused.
- M175/M176 frozen-input audits passed: 30 main rows, 3 annex rows, and 102
  completion slots.
- Fixed local preflight returned `prepared_offline` (102 completion slots; 69
  provider-request ceiling); local admission returned
  `fresh_execute_admission_candidate`.
- Governance audit and `git diff --check` passed. No provider was constructed,
  no credential was inspected, and no request was issued.
- Liaol independently approved the G3 review; it confirms only the local
  preflight and does not authorize hosted egress.

## In progress

- None.

## Next

- A new, separately selected hosted-execution workpack may request fresh,
  itemized user authorization. Approval must cover provider/model, outbound
  content, 33-case scope, serial/no-retry policy, 4096-token cap, 120-second
  deadline, and the 102 completion-slot / 69 HTTP-request ceilings.

## Decisions

- The 102 completion slots and 69 provider HTTP-request cap are distinct;
  neither is an issued-request count. See
  [`ADR-0085`](../../architecture/adr/0085-asymmetric-campaign-request-accounting.md).
- A passing local preflight does not authorize hosted activity; a later request
  must separately itemize the provider/model, content, case scope, rounds,
  deadline, and request/cost limit.

## Blockers

- Hosted egress is not authorized and is out of scope pending independent
  review plus fresh, itemized user authorization.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M177-002-asymmetric-hosted-preflight.md` |
| Freeze | `docs/corpus/knowledge/m176-asymmetric-campaign-freeze-v1.json` |
| CLI | `brep2code/cli/__init__.py` |
| Contract | `brep2code/asymmetric_campaign.py` |

## Resume prompt

```
Continue Brep2Code M177-002: run the fixed local asymmetric preflight and
admission checks, then prepare the result for independent G3 review. Do not
construct a provider, inspect credentials, or issue a hosted request.
```
