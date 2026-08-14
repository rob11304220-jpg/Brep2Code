# WP-M130-001: Shell Family Design Freeze

- Status: done
- Milestone: M130
- Owner: Codex
- Reviewer: Liaol (independent)
- Risk tier: G2

## Goal

Freeze one bounded `shell-v1` top-opening, uniform-thickness construction grammar before any candidate asset is produced.

## Scope

Define exact rows/split, a three-operation oracle, Q01 facts, one constrained Q02 shell action, single-solid/opening/thickness semantic invariants, directional mutations, and wrong-thickness/missing-opening/bottom-breakthrough/split-leak controls. Use the M24 intake contract and stop if the semantics cannot be stated without broad topology recovery, parser, or IR work.

## Compatibility constraints

Offline design only. No producer, candidate asset, case admission, executable manifest, runtime/card/provider change, hosted request, external data, shell generalization claim, or `rib-v1` scope.

## Acceptance

```powershell
uv run python tools\audit_sequence_paired_intake.py docs\corpus\sequence-paired\shell-v1-preregistration.json
uv run python -m ruff check .
uv run python tools\check_governance.py
git diff --check
```

## Review required

Liaol must independently verify the bounded shell grammar, 3/3 family-isolated split, no-substitution rule, single-solid/opening/thickness invariants, negative controls, absence of assets/provider scope, and acceptance evidence.

## Owner evidence (2026-08-11)

- Added `docs/corpus/sequence-paired/shell-v1-preregistration.json`, freezing
  the three-operation `MakeSolidBox -> SelectTopFaceAsOpening ->
  MakeThickSolidInward` oracle, symmetric development family and asymmetric
  held-out family, six exact rows, no-substitution rule, and candidate-only
  admission boundary.
- Added ADR-0066, selecting shell rather than rib for this one Order-6
  coverage step. The record requires one solid, exactly one complete top
  opening, uniform wall thickness, unchanged outer bbox and no bottom
  breakthrough; it rejects side/bottom openings, variable thickness and
  multi-solid results.
- Acceptance passed: generic intake audit, Ruff, governance audit and
  `git diff --check`. No candidate directory, manifest, provider, runtime or
  hosted artifact was created.

## Independent G2 review and closure (2026-08-11)

Liaol independently approved closure. The review confirmed the bounded
top-opening uniform-thickness grammar, 3/3 family-isolated split,
no-substitution rule, single-solid/opening/thickness invariants, negative
controls, passing acceptance evidence, and absence of assets/provider scope.
M130 closes as an offline design freeze only. Candidate production requires a
separately selected package and cannot alter the frozen record.
