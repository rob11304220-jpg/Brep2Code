# WP-M108-001: Revolve Family Governance Promotion

- Status: done
- Milestone: M108
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Promote only the six M107-approved `revolve-v1` records into active self-authored governance cases.

## Scope

Update lifecycle metadata, registry, catalog, case cards, a narrow ADR and the family-specific library audit. No executable manifest changes.

## Acceptance

```powershell
uv run python tools\audit_sequence_paired_revolve.py
uv run python tools\audit_case_library.py
uv run python -m pytest
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Compatibility constraints

Offline only. No manifest, Harness, provider, training, runtime, card, pack or hosted change.

## Status transition

Record owner acceptance, then obtain Liaol's independent review before closure.

## Out of scope

Additional rows, generic revolve claims, runtime or hosted use, shell/rib work.

## Owner acceptance

- Six fixed records are active in the registry and catalog with matching case
  metadata, deterministic reference scripts, sequence files and six case cards.
- Family audit passed six records; library audit passed 87 records; focused
  tests passed (6 passed); Ruff and governance passed.
- ADR-0064 confines this to lifecycle only: no executable manifest, runtime,
  provider, pack, card, training or hosted boundary changed.

## Independent review required

Liaol must verify the exact six registry entries and 3/3 split, ADR-0064,
audit coverage and the no-manifest/no-runtime boundary.

## Independent review and closure

- Reviewer: Liaol
- Outcome: approved on 2026-08-11.
- Review scope: confirmed the six fixed registry entries and 3/3 split,
  ADR-0064, audit coverage and no manifest/runtime/provider/hosted change.
- Closure rationale: active governance evidence only; no runtime or hosted authority.
