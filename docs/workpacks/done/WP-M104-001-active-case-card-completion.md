# WP-M104-001: Active Case-Card Completion

- Status: done
- Milestone: M104
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Add the twelve missing human case cards for active face-selected-cut and
repeated-feature-pattern records, using only authoritative `case.json`
records.

## Scope

- Create the twelve cards enumerated in `docs/corpus/case-portfolio.md`.
- Preserve case IDs, fixture hashes, split and numerical baselines in their
  authoritative records; update only read-only portfolio navigation afterwards.
- Record only links to existing self-authored deterministic-oracle assets.

## Attribution question and sampling intent

No new Q01--Q04 decision, sampling, or evidence claim is introduced. This
work closes a bounded human-navigation gap for twelve already-active records
and stops after those records have one corresponding case card each.

## Inputs

- `case-library/self-authored/param_face_selected_cut_*/case.json`
- `case-library/self-authored/param_repeated_feature_pattern_*/case.json`
- `docs/corpus/case-portfolio.md`

## Docs to update

- `docs/corpus/cases/*.md` for the twelve listed records
- `docs/corpus/case-portfolio.md`
- `docs/workflow/status.md`
- this workpack and its active handoff

## Trace/schema changes

None. This work changes no manifest, trace, schema, storage layout, CLI JSON
output, runtime resource, reference pack or experience card.

## Decision-package impact

- `decision_id`: none; no decision package applies.
- Q01/Q02 effect: none.
- Q03/Q04 effect: none.
- Evidence role: human navigation over existing deterministic-oracle evidence.
- Knowledge disposition: no reusable knowledge.

## Compatibility constraints

Default network-free operation, all fixture paths and hashes, executable
manifests, case lifecycle, runtime behavior, provider boundaries, reference
packs and experience cards must remain unchanged. A human case card is not
LLM guidance or a hosted authorization.

## Acceptance

```powershell
uv run python tools\audit_case_library.py
uv run python tools\check_governance.py
git diff --check
```

## Status transition

Update `docs/workflow/status.md` first. Close only after the twelve cards and
read-only portfolio navigation are complete, all acceptance commands pass, and
the active handoff records the review-ready result.

## Review handoff

- Twelve cards are present under `docs/corpus/cases/` for the IDs that were
  previously listed as missing in `docs/corpus/case-portfolio.md`.
- Acceptance on 2026-08-11: `uv run python tools/audit_case_library.py`
  passed (81 records); `uv run python -m pytest -m fast -q` passed (66 passed);
  `uv run python tools/check_governance.py` and `git diff --check` passed.
- User confirmed review on 2026-08-11; this package may close and archive.

## Closure rationale

The bounded documentation gap is closed: each of the 81 active records has a
human navigation card, while all executable and hosted boundaries remain
unchanged. The owner acceptance evidence passed and the user confirmed review.

## Out of scope

Case production or admission; manifest, reference-pack, runtime-card, Harness,
provider, training or hosted work; lifecycle promotion; card qualification; or
any inference that a human card is LLM guidance.
