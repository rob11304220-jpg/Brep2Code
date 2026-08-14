# WP-M100-001: Case and Hosted Evidence Portfolio

- Status: done
- Milestone: M100
- Owner: Codex
- Reviewer: not required (G1)
- Risk tier: G1

## Goal

Create one low-context, development-side navigation layer for case-library
readiness and hosted experiment outcomes, without creating a second source of
truth or changing any runtime, corpus, provider, card, manifest, gate, or
authorization boundary.

## Scope

- Add a grouped case portfolio that distinguishes case cards, deterministic
  reference scripts, development-only reference packs, experimental runtime
  cards, knowledge units, and hosted evidence.
- Add a hosted experiment registry that records scope, terminal status,
  result class, report paths and interpretation boundary for the retained
  experiment families.
- Add an ADR and a repeatable maintenance procedure; link the new navigation
  pages from the corpus and workflow entry points.

## Attribution question and sampling intent

Distinguish missing cross-index navigation from missing technical evidence.
The work stops after it has linked existing authoritative records and made
their non-equivalence explicit. It does not sample a case, reinterpret a
report, produce a new card, or infer a capability from portfolio counts.

## Inputs

- `docs/corpus/registry/self-authored.json` and per-case `case.json`
- `docs/corpus/cases/`, `docs/corpus/knowledge/`, and reference-pack records
- `runtime_resources/experience-cards/`
- completed workpacks, frozen hosted policies, and local report/monitor paths

## Code paths

None. Documentation and navigation only.

## Docs to update

- `docs/corpus/case-portfolio.md`
- `docs/workflow/hosted-experiment-registry.md`
- `docs/runbooks/evidence-portfolio-maintenance.md`
- `docs/corpus/README.md`, `docs/workflow/navigation.md`, and
  `docs/workflow/status.md`
- one ADR, this workpack, and the active handoff

## Trace/schema changes

None. The portfolio and registry are Markdown navigation pages, not report,
trace, case, manifest, card, or runtime schemas.

## Decision-package impact

- `decision_id`: none; documentation-governance navigation only.
- Q01/Q02 effect: none; no observation, retrieval, card-selection, prompt, or
  constrained-sequence behavior changes.
- Q03/Q04 effect: none; no executor, gate, diagnostic, repair, or stopping
  rule changes.
- Evidence role: navigation over existing evidence only.
- Knowledge disposition: no reusable knowledge.

## Compatibility constraints

Default operation remains network-free and credential-free. Existing case
registries, manifests, reference packs, runtime cards, reports, workpacks and
their historical conclusions remain authoritative and immutable. This package
does not authorize hosted work, runtime retrieval, card promotion, manifest
selection, case promotion, or report-budget reuse.

## Acceptance

```powershell
uv run python tools\check_governance.py
git diff --check
```

Verify every tracked link targets an existing repository document or explicitly
labelled ignored local evidence path.

## Evidence reuse / guidance-card disposition

No card is created, changed, promoted, mounted, or retrieved. Existing cards
remain experimental unless their own source record says otherwise.

## Status transition

After acceptance, update `docs/workflow/status.md` first, move this workpack
to `done/`, archive the handoff, and retain the portfolio only as navigation.
No ADR or portfolio entry authorizes a new task.

## Closure rationale

- Added [case-portfolio.md](../../corpus/case-portfolio.md), separating human
  case cards, deterministic reference scripts, development packs and runtime
  cards; it identifies the twelve active records without an human case card.
- Added [hosted-experiment-registry.md](../../workflow/hosted-experiment-registry.md),
  which records frozen-scope terminal results without turning heterogeneous
  reports into a benchmark or a reusable budget.
- Added [ADR-0059](../../architecture/adr/0059-case-and-hosted-evidence-portfolio.md)
  and the repeatable maintenance procedure in
  [evidence-portfolio-maintenance.md](../../runbooks/evidence-portfolio-maintenance.md).
- Acceptance on 2026-08-11: `uv run python tools/check_governance.py` and
  `git diff --check` passed. No case, manifest, card, report, Harness,
  provider, credential or hosted request changed.

## Out of scope

Any case/card/pack/report mutation; report parsing automation; runtime or
retrieval implementation; provider request; hosted preflight; manifest or gate
change; new capability or generalization claim.
