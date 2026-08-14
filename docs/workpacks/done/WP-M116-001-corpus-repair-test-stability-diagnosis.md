# WP-M116-001: Corpus Repair Test Stability Diagnosis

- Status: done
- Milestone: M116
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Diagnose and, only if supported by reproducible local evidence, make the
corpus-repair fake-provider regression test deterministic. The scope is the
qualified full-suite failure recorded while closing M115:
`tests/test_corpus_m4.py::test_corpus_runner_replays_reference_script_with_fake_provider`.

## Scope

- Reproduce the test in isolated local runs and inspect only its test fixture,
  generated local record and relevant corpus/Harness code paths.
- Identify whether the failure is environmental/transient or a deterministic
  product defect; preserve a failing artifact or precise no-reproduction
  record.
- If a product defect is reproducible, make the smallest offline deterministic
  correction and add focused regression coverage.
- Record the causal boundary: M115's offline classifier is not imported by the
  corpus-runner repair path.

## Compatibility constraints

Offline and credential-free. Do not modify M115 policy artifacts, M96/M97
policy/accounting/report/monitor/budget/authorization material, executable
manifests, provider configuration, runtime guidance, cards, prompts, cases,
splits or Harness gates except for a demonstrated minimal fix in the affected
local repair path. Do not construct a provider, run preflight or issue a
request. Do not create the later G3 calibration workpack until this package is
closed and separately selected.

## Acceptance

```powershell
uv run python -m pytest tests\test_corpus_m4.py::test_corpus_runner_replays_reference_script_with_fake_provider -q
uv run python -m pytest -m fast -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

If code changes, also run the smallest relevant corpus/repair selection and a
standalone full suite according to the offline-validation runbook. Record every
terminal result; a window timeout is not a result.

## Status transition

Record owner diagnosis and acceptance evidence, then obtain Liaol's
independent review before closure. Update `status.md` first, then this workpack
and the handoff; archive the handoff after closure.

## Owner diagnosis and acceptance (2026-08-11)

- The selected test passed in five sequential isolated runs (11.40–12.78
  seconds each) and again as the acceptance command (12.65 seconds).
- The complete local module `tests/test_corpus_m4.py` passed 39/39 in 92.21
  seconds, so no same-module ordering interference was reproduced.
- The code path confirms the repair uses an explicitly constructed
  `FakeLLMProvider`; M115's `tools.m115_prismatic_policy` is not imported by
  the corpus runner, repair loop or Harness.
- The earlier full-suite result (232 passed / 1 failed) therefore remains a
  non-reproduced, qualified observation. No generated failing artifact exists,
  no product defect is established, and no repair/Harness code is changed.
- Acceptance passed: focused test, `pytest -m fast -q` (66 passed), Ruff,
  governance audit and `git diff --check`. Liaol's independent G2 review is
  required before closure.

## Independent G2 review and closure (2026-08-11)

Liaol independently approved closure. The review accepted the five isolated
passes, the 39/39 module result, the M115 causal isolation and the conclusion
that no code change is justified without a reproduced defect. This closure
does not establish a root cause for the earlier qualified full-suite failure
and grants no hosted, provider, M97 or development-calibration authority.

## Out of scope

Hosted stability remediation, provider construction, provider request,
development calibration, held-out policy/evaluation, retry or repair of a
hosted campaign, any M97 reuse, or interpretation of card effectiveness.
