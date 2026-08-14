# WP-TRG-005: Output Contract and Repair Correctness

- Status: deferred
- Owner: unassigned
- Reviewer: Liaol
- Risk tier: G2

Deferred until a newly documented minimal end-to-end hosted gate passes. Address CAD output schema, OCP
type-safety and structured repair feedback separately from provider latency.

## Goal

Improve Q02/Q04 correctness only after provider lifecycle evidence is stable:
make generated output validation, OCP type boundaries and repair feedback
explicit, testable and independently diagnosable.

## Activation condition

The historical-contract profile must be accepted and a newly documented minimal
end-to-end hosted path must meet every gate criterion with G3 independent
review. If that path stops early or fails, this workpack remains deferred; its
owner must not use CAD changes to compensate for provider wait.

## Scope

- Define/clarify the generated-script output envelope and validation errors.
- Strengthen OCP type-safety at the Harness boundary without loosening existing
  readability, geometry or provenance gates.
- Structure Q03 failure feedback so Q04 repair can distinguish schema/type,
  execution and geometry outcomes using sanitized data.
- Add deterministic fake-provider and sandboxed local regression tests, plus
  the required contract/module/runbook updates.

## Compatibility constraints

Offline by default; no hosted request is authorized by this G2 workpack. Keep
the existing prompt boundary, manifest/split membership, `wsl-bwrap` policy,
provider lifecycle taxonomy, atomic reports and fail-closed gates. Any later
hosted validation is a separate G3 workpack with new preflight and itemized
authorization.

## Acceptance

```powershell
uv run python -m pytest tests -q
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

The validation plan may select bounded relevant tests only when it records why
they cover schema, sandbox and repair feedback separately.

## Status transition

Before activation, assign one owner and retain an independent reviewer. Update
`docs/workflow/status.md` first, then this workpack and an active handoff.
Closure must link the retained historical-contract profile, minimal-path evidence, contract changes,
test output and review decision.

## Out of scope

Provider availability diagnosis, retry or deadline policy, endpoint/model
change, prompt optimization, manifest/corpus growth, external data, held-out
evaluation and claims that a local regression proves hosted model quality.
