# Handoff: M134 Frozen Hosted Batch Epoch Policy

- **Date**: 2026-08-12
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M134-001-frozen-hosted-batch-epoch-policy`

## Goal

Freeze a comparable 18-condition existing-case hosted batch policy that
continues after per-condition failures but stops for defined integrity faults.

## Done

- User selected M134; lifecycle records were created.
- Added ADR-0067, M134's frozen 18-condition batch policy and aligned all
  current hosted routing to M135 then M136.
- Ruff, governance audit and diff checks passed; no provider was constructed,
  preflight run, or request issued.
- Liaol independently approved the cohort, stop rules and M135/M136 sequence;
  M134 is closed.

## In progress

- None; M134 is closed.

## Next

- Wait for the user to select M135. It begins with offline preflight; no
  provider action is authorized unless the later itemized request is approved.

## Decisions

- Serial scheduling is for accounting and monitoring, not family dependency.
- [ADR-0067](../architecture/adr/0067-frozen-hosted-batch-epochs.md) freezes
  comparable epoch handling and separates integrity faults from observations.

## Blockers

- None for M134. M135 remains unselected and requires G3 preflight plus later
  itemized hosted authorization.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/active/WP-M134-001-frozen-hosted-batch-epoch-policy.md` |
| Policy | `docs/workflow/m134-frozen-hosted-batch-epoch-policy.md` |
| ADR | `docs/architecture/adr/0067-frozen-hosted-batch-epochs.md` |

## Resume prompt

    Continue Brep2Code work: complete M134 frozen hosted batch epoch policy.
    Read docs/handoff/active/2026-08-12-m134-frozen-hosted-batch-epoch.md.
    First action: publish the 18-condition cohort and integrity-versus-observation rules.
