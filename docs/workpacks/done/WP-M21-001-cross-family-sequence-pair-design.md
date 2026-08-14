# WP-M21-001: Cross-Family Sequence-Pair Design and Preregistration

- Status: done
- Milestone: M21
- Owner: Codex

## Goal

Freeze the next sequence-paired family and its evidence design before any new
candidate asset is produced.

## Scope

- Compare the completed `prismatic-hole-v1` evidence with available
  self-authored parameter families using a capability matrix.
- Select a structurally distinct, bounded second grammar.
- Preregister exact development/held-out rows, mutations, semantic
  anti-degeneration predicates, rejection taxonomy, and producer-stability
  requirements.
- Create a separate controlled-production workpack; do not create new cases.

## Attribution question and sampling intent

Determine whether a second-profile dependency can be represented and audited
without confusing a successful parameter variation with cross-family evidence.
The six rows and their splits are fixed before production.  Stop at the design
record: no producer, case asset, manifest, or audit pass is created here.

## Inputs

- ADR-0019 and the completed `prismatic-hole-v1` nine-case review.
- Existing M12 `rounded_slot` development family and its deterministic OCP
  reference scripts.
- The local paper-vault Zero-to-CAD case note, used only for the
  catalog/producer/gate separation rationale.

## Docs to update

- ADR-0020, the sequence-paired route roadmap, this design record, the
  preregistration record, workpack index, workflow status, and active handoff.

## Trace/schema changes

No Harness trace, provider trace, corpus report, CLI JSON, storage layout, or
runtime schema changes.  The preregistration record is development governance
metadata only.

## Compatibility constraints

Default execution remains offline and credential-free.  Existing manifests,
fixtures, Harness gates, provider policy, runtime resources, prompts, SDK, IR,
Fusion, ABC, external-source, and training boundaries remain unchanged.

## Acceptance

- [x] A capability matrix demonstrates a dependency distinction from
  `prismatic-hole-v1`.
- [x] The grammar, six exact rows, split isolation, mutations, semantic
  predicates, rejection taxonomy, and reproducibility requirements are frozen.
- [x] The follow-on production workpack cannot change that selection.
- [x] `git diff --check` passes.

## Evidence reuse / guidance-card disposition

No reusable experience card.  This is a planning contract, not runtime
evidence.

## Status transition

Completed on 2026-08-04.  M21-002 was then promoted as the sole active
workpack and has since completed.  The status page is the dynamic source of
truth.

## Out of scope

Candidate production, case-library registration, manifests, provider use,
training, runtime integration, a generic sequence grammar, native-history
claims, or an IR decision.

## Result

Completed offline on 2026-08-04.  The next family is `rounded-slot-v1`, with
three existing development rows and three preregistered offset-profile
held-out candidates.  No case asset or runtime-facing artifact was created.
