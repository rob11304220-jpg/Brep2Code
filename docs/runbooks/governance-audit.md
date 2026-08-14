# Governance Audit

Run the repository governance audit whenever changing task lifecycle documents,
and rely on CI to run it for every push and pull request.

## Command

```powershell
uv run python tools/check_governance.py
```

The audit is dependency-free apart from the project Python runtime. It reads
governance files and does not call providers, execute Harness workspaces, or
inspect credentials.

## Enforced invariants

- `docs/workpacks/active/` contains at most one Markdown workpack, and it has
  `Status: active`.
- `docs/handoff/active/` contains at most three Markdown handoffs, and each
  has `Status: active`.
- Every `docs/workpacks/done/` file has `Status: done`; every backlog file has
  `Status: backlog` or `Status: blocked`.
- `docs/workflow/status.md` names the active workpack, or explicitly says that
  none exists when the active directory is empty, and has a valid ISO update
  date.
- ADR files use contiguous four-digit, kebab-case names beginning at `0001`.

## When it fails

1. Treat the diagnostic as a lifecycle inconsistency, not as a reason to alter
   Harness behavior or evidence-gated research decisions.
2. Reconcile `status.md` first, then the workpack and active handoff, following
   the status update rule in `docs/workflow/status.md`.
3. Archive completed handoffs rather than leaving them in `active/`.
4. Re-run the audit, focused tests, Ruff, and the relevant full test suite.

## CI baseline

`.github/workflows/ci.yml` runs the governance audit, Ruff, pytest, and
`git diff --check` on pushes and pull requests. It intentionally contains no
hosted-provider command, credential, external corpus download, or runtime
workspace execution.

## Low-context inventory

Use the compact inventory instead of scanning historical workpacks or handoffs
when deciding what to read next:

```powershell
uv run python tools/check_governance.py --inventory
```

It reports only the current entry paths and directory counts. It is not an
implementation authorization and does not interpret archived snapshots.
