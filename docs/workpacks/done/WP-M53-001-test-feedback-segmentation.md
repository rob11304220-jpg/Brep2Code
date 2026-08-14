# WP-M53-001: Test Feedback Segmentation and Performance Baseline

- Status: done
- Milestone: M53
- Owner: Codex
- Reviewer: Liaol
- Risk tier: G2

## Goal

Measure the current offline test suite and establish an auditable
fast/standard/sandbox test-selection interface that shortens development
feedback without weakening CI's complete regression gate.

## Scope

- Collect per-test duration and dependency evidence from the current suite.
- Define explicit, documented fast/standard/sandbox membership rules and
  commands based on that evidence.
- Add markers, runner commands, and focused regressions only as needed.
- Keep CI's full pytest command as the complete acceptance gate.

## Compatibility constraints

Offline and credential-free only. Do not change Harness behavior, provider
selection, M48 transcript content, sandbox policy, cases/manifests, corpus
reports, prompts, external data, or hosted authorization. A fast result must
never substitute for the full-suite acceptance result.

## Trace/schema changes

None. Test metadata and development documentation only; no runtime trace,
signal bundle, provider trace, report, storage, or CLI behavior change.

## Decision-package impact

- `decision_id`: none; quality-engineering work only.
- Q01/Q02/Q03/Q04 effect: none.
- Evidence role: reproducible validation-performance baseline.
- Knowledge disposition: no reusable runtime knowledge.

## Acceptance

```powershell
uv run python -m pytest --durations=0 -q
uv run python -m pytest -m fast -q
uv run python -m pytest -m standard -q
uv run python -m pytest -m sandbox -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Status transition

Record duration evidence, selection rules, all acceptance outputs, and Liaol's
independent review before closure. Update workflow status first, then this
workpack and its handoff.

## Implementation and owner acceptance

- Added registered pytest markers and centralized per-module membership in
  `tests/conftest.py`; no Harness, provider, corpus, or CI behavior changed.
- Recorded measured duration evidence and the command/membership contract in
  `docs/workflow/m53-test-feedback-baseline.md` and
  `docs/runbooks/test-feedback-segmentation.md`.
- Owner acceptance (2026-08-08): baseline `162 passed in 143.15s`;
  `fast` `58 passed, 104 deselected in 1.80s`; `standard` `92 passed,
  70 deselected in 9.72s`; `sandbox` `70 passed, 92 deselected in 137.61s`;
  full regression `162 passed in 144.16s`; Ruff and governance audit passed;
  `git diff --check` passed.
- Pending: Liaol's independent G2 review of scope, evidence boundaries,
  acceptance output, and lifecycle alignment.

## Independent review and closure

- Liaol independently reviewed the marker scope, baseline evidence, complete
  pytest gate, acceptance output, and lifecycle records on 2026-08-08.
- Review outcome: approved. M53 is closed; fast and standard selections remain
  developer feedback only, and full pytest remains the CI acceptance gate.

## Out of scope

Skipping or weakening CI tests, reducing existing coverage, changing test
assertions solely to improve speed, hosted requests, or any runtime behavior.
