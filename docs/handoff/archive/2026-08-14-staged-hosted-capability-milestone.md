# Handoff: M173 card-qualified-denominator blocker

- **Date**: 2026-08-14
- **Subproject**: `brep2code`
- **Status**: `blocked`
- **Related workpack**: `WP-M173-001-hosted-milestone-case-and-reference-qualification`

## Goal

Resolve M173's card-qualified-denominator blocker before campaign inputs or
hosted preparation.

## Done

- M170 independently closed on focused evidence; its scope and release
  boundaries remain unchanged.
- User explicitly selected M171, an inserted G2 remediation for the recorded
  historical M96/M97 index-hash drift.
- Recorded ADR-0083: restore historical validation using an immutable fixture,
  not a policy/card/current-index rewrite.

## In progress

- M171 independently approved and closed: the historical fixture hashes to
  `dfa731...30517`; the live index remains `bf7175...52181` with the selector
  card, and all 289 tests pass.
- M172 is active as the route's next selected G1 charter.
- M172 closed after publishing the campaign claim and denominator charter.
- M173 is active as the route's selected G2 qualification gate.
- The first metadata-only qualification pass found only three directly
  card-qualified development roles, versus 20 required by M172's S2/S3.

## Next

- Obtain user selection for a bounded denominator redesign or a separately
  evidenced card-role projection workpack; then return to M173.

## Decisions

- M171's independent G2 approval accepted the fixture-only remediation without
  provider or hosted authority.
- M172 froze interpretation only and did not select cases/cards or permit a
  provider request. M173 may qualify development evidence but may not execute.
  See ADR-0082 and ADR-0083.

## Blockers

- M173 cannot qualify the required 20 distinct card rows from the current
  three-role evidence. Do not infer eligibility or auto-claim campaign freeze.

## Key paths

| Kind | Path |
|---|---|
| Files | `docs/workpacks/active/WP-M173-001-hosted-milestone-case-and-reference-qualification.md` |
| Evidence | M172 governance/diff checks passed; M171: 289 passed in 519.78s |
| Route | `docs/architecture/v1/current-project-route.md` |
| Commands | `uv run python tools/check_governance.py` |

## Resume prompt

```
Continue Brep2Code work: resolve M173's blocked card-qualified denominator.
Read this handoff and the active workpack. First obtain explicit user selection
for a bounded denominator redesign or card-role evidence/projection workpack.
```
