# WP-M135-008: Frozen Runner Contract

- Status: done
- Milestone: M135
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Freeze and test the complete offline M135 per-condition contract from the
provider-bound request bytes through one no-input Harness execution and the
resulting epoch terminal category, without constructing a hosted provider.

## Scope

- Define one exact, hash-pinned provider-bound system instruction and request
  message construction for every frozen condition.
- Derive the prismatic treatment's bounded card response from the existing
  hash-pinned card, preserve its exact UTF-8 bytes/hash, and append it only to
  that condition's single request.
- Execute fake replacement scripts through `ObservedBuildLoopRunner` using
  `WslBubblewrapExecutor`, with `build_without_input=True`, and map provider,
  script, Harness and repair outcomes to M134 terminal categories.
- Add focused offline regressions and a concise contract record.

## Code and record paths

- `brep2code/agent/m135_epoch.py`
- `tests/test_m135_epoch.py`
- `docs/workflow/m135-008-frozen-runner-contract.md`

## Compatibility constraints

The M134 cohort, condition order, input/transcript hashes, provider/model,
executor, 120-second deadline, 18-request cap and zero repair/retry policy
remain unchanged. Default operation remains offline and credential-free. Do
not construct a provider, access credentials, issue requests, send data,
change a manifest, modify card content, or reuse epoch report/monitor paths.

## Acceptance

```powershell
uv run python -m pytest tests\test_m135_epoch.py -q
uv run python -m pytest -m fast -q
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the frozen contract, fake-provider no-input Harness evidence and
terminal-mapping tests; pass every acceptance command and obtain Liaol's
independent G3 review. A separate user-selected serial lifecycle workpack and
then a fresh hosted preflight remain required before authorization can be
requested.

## Permitted stop conditions

Independent review; explicit hosted authorization; frozen-input drift; an
out-of-scope dependency; or a reproducible offline validation blocker.

## Status transition

Update `docs/workflow/status.md` first, then this workpack and the active
handoff. On owner completion, set this workpack to `review`; only the
independent reviewer may close it as `done`.

## Out of scope

Hosted execution or authorization; provider construction; credential access;
serial lifecycle implementation; repair/retry; cohort/prompt/card/model or
provider changes; case or manifest changes; held-out evaluation; card
promotion; and M137 terminal review.

## Owner completion evidence (2026-08-12)

The request builder freezes the common system-instruction hash, path-free
condition transcript and exactly one direct card message only for the three
card conditions. The card regression proves that its injected bytes are the
same bytes consumed by `ObservedBuildLoopRunner`; the generated reference
script then completes through the no-input `wsl-bwrap` Harness gate and maps
to `full_success`. The terminal mapping is recorded in
[`m135-008-frozen-runner-contract.md`](../../workflow/m135-008-frozen-runner-contract.md).

Owner-side acceptance passed: focused M135 `10 passed in 90.21s`; fast `66
passed`; full suite `248 passed in 432.52s`; Ruff, governance audit and diff
check passed. This workpack now awaits Liaol's independent G3 review. It does
not construct a provider or authorize hosted execution.

## Independent review and closure (2026-08-12)

Liaol approved the independent G3 review. The review accepted the bounded
offline scope, frozen request/card hashes, fake-provider no-input Harness
evidence, terminal mapping and recorded acceptance results. It grants no
hosted authorization. The next serial lifecycle implementation remains a
separately user-selected workpack.
