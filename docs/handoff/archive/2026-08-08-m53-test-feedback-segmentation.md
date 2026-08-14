# Handoff: M53 test feedback segmentation

- **Date**: 2026-08-08
- **Subproject**: `brep2code`
- **Status**: `done`
- **Related workpack**: `WP-M53-001-test-feedback-segmentation`

## Goal

Create measured fast/standard/sandbox test selections while retaining full
offline pytest as CI's complete acceptance gate.

## Done

- M49 roadmap, M50 offline observation loop, M52 secure adapter, and M51
  single-case real-LLM smoke are complete and reviewed.
- User selected M53 as the next bounded G2 workpack; Liaol is reviewer.
- Measured the complete offline suite: 162 passed in 143.15s. Corpus
  runner/replay calls dominated (10.17–13.86s each), followed by Harness and
  repair/observed-build process-boundary checks.
- Added registered `fast`, `standard`, and `sandbox` markers, centralized
  membership rules, a repeatable runbook, and the recorded baseline.
- Owner acceptance passed: fast 58/1.80s, standard 92/9.72s, sandbox
  70/137.61s, full 162/144.16s; Ruff, governance, and diff checks passed.
- Liaol completed the independent G2 review on 2026-08-08 and approved M53.

## In progress

- M53 is complete and its workpack/handoff should be archived.

## Next

- Leave M53 closed. Start no new work unless the user selects a bounded
  workpack; any G3 hosted evaluation requires preflight and explicit approval.

## Decisions

- Fast selection is a developer feedback path only; full pytest remains CI
  and closure evidence.
- `sandbox` marks process-backed Harness, executor, and corpus integration
  tests. It does not imply every marked test invokes WSL bubblewrap.
- This workpack is independent of later G3 development-split evaluation.

## Blockers

- None.

## Key paths

| Kind | Path |
|---|---|
| Workpack | `docs/workpacks/active/WP-M53-001-test-feedback-segmentation.md` |
| Test config | `pyproject.toml` |
| CI | `.github/workflows/ci.yml` |
| Selection rules | `tests/conftest.py` |
| Baseline evidence | `docs/workflow/m53-test-feedback-baseline.md` |
| Runbook | `docs/runbooks/test-feedback-segmentation.md` |
| Route | `docs/architecture/v1/post-m48-closed-loop-roadmap.md` |

## Resume prompt

```
M53 is closed. Read `docs/workflow/status.md` before selecting any next
bounded workpack. Do not start hosted evaluation without preflight and
explicit, itemized user authorization.
```
