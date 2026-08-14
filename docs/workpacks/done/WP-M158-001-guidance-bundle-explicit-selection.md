# WP-M158-001: GuidanceBundle Explicit Selection

- Status: done
- Milestone: M158
- Trigger consumed: M157 blocked re-entry condition
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Entry condition

The user selected the bounded remediation required by archived M157. Current
`GuidanceCardBridge` accepts only the hard-coded
`vertical-cylinder-construction` card ID and global role set, preventing a
separately selected hash-bound card from being evaluated.

## Goal

Replace the hard-coded card identity and role set with an explicit
revision-scoped `GuidanceBundle` declaration while preserving hash validation,
one-card selection, opt-in behavior, traceability, and the prohibition on
directory search or retrieval.

## Scope

- Extend `GuidanceBundle` so the caller explicitly declares one selected card
  path and its allowed roles when building the hash-bound bundle.
- Validate only that declared card against the hash-pinned index and its own
  identity; do not accept a runtime card ID query, enumerate cards, rank cards,
  or search a directory.
- Keep legacy vertical-cylinder callers behaviorally compatible through their
  existing three roles.
- Add focused bridge/Harness tests for explicit card identity, role mismatch,
  hash drift, single-card response, no-guidance baseline, and no index search.
- Record the interface decision in an ADR and update runtime-guidance
  documentation only where behavior changes.

## Compatibility constraints

No new experience card, reference pack, case, manifest, provider call, hosted
request, retrieval, training material, SDK, IR, repair-policy, or tool-schema
change. A bundle is still created by trusted Harness-side code from explicit
paths; runtime callers may request only the bundle's declared role and receive
only that one selected card.

## Acceptance

```powershell
uv run python -m pytest -m fast -q
uv run python -m pytest tests\test_guidance_bridge.py -q
uv run python -m pytest -q
uv run python -m ruff check brep2code\agent\guidance.py tests\test_guidance_bridge.py
uv run python tools\audit_runtime_guidance.py
uv run python tools\check_governance.py
git diff --check
```

## Owner completion boundary

Publish the bounded GuidanceBundle selection contract, regression evidence, and
ADR; then obtain Liaol's independent G2 review. M157 remains blocked until that
review approves this workpack.

## Permitted stop conditions

Independent review; an incompatibility requiring a provider/hosted, case,
manifest, retrieval, tool-schema, repair, SDK, or IR change; source-hash
validation failure; or a reproducible local validation blocker.

## Current result

- Implemented bundle-local, explicit card roles and selected-card identity
  validation in `GuidanceCardBridge`; legacy vertical-cylinder callers retain
  their original role set.
- Added focused coverage for a temporary non-legacy card, bundle-local role
  rejection, and invalid empty/duplicate role declarations.
- Added ADR-0075 and updated the runtime-guidance runbook to describe explicit
  selected-card paths and compatible roles.

## Resumed completion state

M159 independently resolved the registry/case lifecycle conflicts and M160
independently aligned the M21 active-versus-experimental audit interpretation.
M160's final full suite ran against this worktree, including M158's
GuidanceBundle change, and passed with `284 passed in 502.06s`. M158's earlier
focused bridge tests, fast tests, Ruff, runtime-guidance audit, and governance
audit also passed.

## Owner validation record

```powershell
uv run python -m pytest tests\test_guidance_bridge.py -q
# 8 passed in 6.59s
uv run python -m pytest -m fast -q
# 66 passed, 217 deselected in 2.42s
uv run python -m pytest -q
# 284 passed in 502.06s (M160 final run, including M158 changes)
uv run python -m ruff check brep2code\agent\guidance.py tests\test_guidance_bridge.py
uv run python tools\audit_runtime_guidance.py
uv run python tools\check_governance.py
git diff --check
```

`git diff --check` reported only LF/CRLF conversion warnings. The owner-side
scope is complete and ready for Liaol's independent G2 review.

## Independent review

Pending Liaol's independent review of the explicit selected-card identity,
bundle-local role boundary, legacy-role compatibility, hash validation,
no-directory-search constraint, ADR-0075, and final validation evidence.

Liaol approved the independent G2 review on 2026-08-13. The explicit
selected-card identity, bundle-local roles, legacy compatibility, hash
validation, no-directory-search constraint, ADR-0075, and final validation
evidence were accepted without introducing retrieval, provider, or hosted
behavior.

## Closure rationale

M158 closes because it replaced the hard-coded card identity with one explicit
hash-bound selected card and bundle-local roles, preserved the opt-in
single-card no-search boundary, passed focused/fast/static/audit checks and the
284-test full suite, and received independent G2 approval.

## Status transition

Update `status.md` first, then this workpack and active handoff. On approved
closure, archive M158 and resume M157 under a fresh active workpack/handoff;
do not activate the case-testing dossier or `WP-TRG-035`.

## Out of scope

Selector-ambiguity card creation, M157 ablation execution, automatic card
selection, multi-card bundles, directory discovery, retrieval, provider or
hosted execution, and case/manifest/Harness tool-schema changes.
