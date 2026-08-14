# WP-M135-007: Frozen Epoch Execute Lifecycle

- Status: blocked
- Milestone: M135
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G3

## Goal

Connect M135's frozen transcript contract to a dedicated serial execute
lifecycle with authorization gating, fake-provider regression coverage and
durable per-condition checkpoints.

## Scope

- Add `m135-epoch --phase prepare|execute` with exactly 18 conditions, fixed
  provider/model/deadline/no-cap/zero-repair/retry constraints and fresh
  report/monitor handling.
- Require `--authorize-hosted` before a DeepSeek provider can be constructed;
  keep fake-provider execution local and test-only.
- Invoke one provider request per condition, record the transcript hash only,
  and classify one terminal state before moving serially to the next condition.
- Execute fake scripts through `ObservedBuildLoopRunner` with `wsl-bwrap` for
  the same no-input boundary; update tests and durable contracts.

## Compatibility constraints

No hosted request, credential access, provider construction, case/prompt/card
change, repair/retry, manifest change or reuse of prior M135 artifacts.

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

Publish implementation evidence and obtain independent G3 review. A new full
preflight and explicit itemized user authorization remain required before any
DeepSeek execution.

## Out of scope

Hosted execution, provider construction, credential access, egress, repair,
retry, cohort changes and M137 review.

## Blocked closure rationale

The initially explored provider-completion loop was removed because it bypassed
the required no-input Harness/CAD gates. M135 has no frozen contract yet for
the provider-bound system instruction, prismatic card-content injection and
provider/script/Harness terminal mapping. The detailed record is
[`m135-007-frozen-epoch-execute-lifecycle.md`](../../workflow/m135-007-frozen-epoch-execute-lifecycle.md).
