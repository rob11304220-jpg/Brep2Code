# WP-TRG-030: Development-Evidence Information Architecture

- Status: deferred
- Trigger: M145's case-evidence mechanism/difficulty report is complete and
  independently reviewed or explicitly accepted; the user selects a fresh
  bounded package.
- Risk tier on activation: G2
- Reviewer on activation: independent reviewer required

## Goal

Design and implement a source-linked development-side information architecture
that makes mechanism, multi-axis difficulty, evidence maturity, admission risk,
and decision gaps navigable without replacing existing authorities or creating
runtime knowledge.

## Scope on activation

- Define a stable crosswalk schema/ID strategy across case metadata, knowledge
  units, decision packages, coverage cells, and admission records.
- Specify ownership, update flow, drift audit, migration plan, and a compact
  human-facing view derived from canonical sources.
- Preserve case-level lifecycle, manifest, runtime, and split authorities;
  prove derived views do not create a second case registry.

## Compatibility constraints

No fixture or held-out inspection/execution, case production, manifest change,
Harness/runtime/provider change, training use, retrieval, SDK/IR work, or
hosted execution. A crosswalk is development-side navigation only.

## Entry evidence

- `docs/corpus/case-evidence-mechanism-difficulty-report-v1.md`
- `docs/corpus/knowledge/admissions/case-library-admission-profile-v1.json`
- ADR-0073 and the existing knowledge-base architecture.

## Out of scope

Automatic case admission, generic CAD difficulty scoring, runtime projection,
and any authority transfer from existing source records.
