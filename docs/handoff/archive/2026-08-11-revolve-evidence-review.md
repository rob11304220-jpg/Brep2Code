# Handoff: Revolve Evidence Review

- **Date**: 2026-08-11
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M107-001-revolve-family-evidence-review`

## Goal

Complete the selected G2 read-only evidence review of the frozen six-row
`revolve-v1` experimental release and hand its bounded disposition to Liaol
for independent review.

## Done

- User selected the `WP-TRG-014` route; it is activated as M107-001.
- Owner acceptance supports one narrow, separately selectable lifecycle-
  promotion proposal for the six frozen `revolve-v1` rows.
- The family audit, focused test, fast suite, Ruff, governance audit and diff
  check passed. No candidate, manifest, provider, runtime, pack, card or
  hosted boundary has been changed.

## In progress

- Liaol independently approved the bounded evidence disposition.

## Next

- If selected, create a fresh bounded lifecycle-promotion workpack for the
  six frozen rows; otherwise select another bounded package.

## Decisions

- M107 reviews existing offline evidence only. Any lifecycle promotion must be
  selected later in a fresh workpack.
- The repeated global active-library replay failure is not attributed to this
  review: it occurs while an existing active case cannot write `output/model.step`.

## Blockers

- None.

## Key paths

| Kind | Path |
|------|------|
| Workpack | `docs/workpacks/active/WP-M107-001-revolve-family-evidence-review.md` |
| Evidence | `docs/corpus/sequence-paired/revolve-v1-preregistration.json` |
| Audit | `tools/audit_sequence_paired_revolve.py` |

## Resume prompt

```
Continue Brep2Code work: select a new bounded package after M107-001 closure.
Read docs/handoff/active/2026-08-11-revolve-evidence-review.md.
First action: read docs/workflow/status.md and wait for the user to select a package.
```
