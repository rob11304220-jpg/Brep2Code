# Handoff: M47 Q01 observation / build capability-separation design

- **Date**: 2026-08-08
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M47-001-q01-observation-build-capability-separation-design`

## Goal

Design the minimal offline Q01 observation and Q02 build-capability contract:
recorded bounded B-Rep tools may inform script generation, but the executed
build script must have no original-STEP read capability.

## Done

- M46 is closed with provenance evidence and independent review.
- User selected the bounded G1 M47 design workpack.
- ADR-0049, the planned decision package, and the detailed capability contract
  are complete; JSON parsing, governance audit, and `git diff --check` pass.

## In progress

- No work remains in M47.

## Next

- Start no further work without explicit user selection; M48 is the candidate
  G2 implementation workpack.

## Decisions

- Design only: no runtime implementation, provider request, prompt change,
  case/manifest update, raw STEP access, or external egress is authorized.
- M46 provenance remains a prerequisite for any future reconstruction claim.
- ADR-0049 freezes the two-plane boundary and links the planned capability
  contract at `docs/architecture/v1/contracts/q01-observation-build-separation.md`.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Branch | `main` |
| Workpack | `docs/workpacks/active/WP-M47-001-q01-observation-build-capability-separation-design.md` |
| Runtime boundary | `docs/architecture/v1/runtime-boundaries.md` |
| Provenance ADR | `docs/architecture/adr/0048-reconstruction-provenance-gate-design.md` |

## Resume prompt

```
M47 is complete. Do not start M48 or any other workpack without explicit user
selection.
```
