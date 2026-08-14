# WP-M23-004: Additive-Boss-Dependent-Cut Governance Promotion

- Status: done
- Milestone: M23
- Owner: Codex

## Goal

Determine whether the six completed M23 experimental candidates qualify for
restricted family-specific case-library governance promotion.

## Scope

- Accept ADR-0027 and audit only the six frozen M23 records.
- Add deterministic reference scripts, case cards, registry pointers, and
  active metadata required for long-term maintenance.
- Extend the offline library audit only for this grammar.

## Compatibility constraints

Keep all executable manifests unchanged. Default operation remains offline and
credential-free. No provider, training, runtime, parser/helper/SDK, IR,
external-data, or face-selection change is in scope.

## Acceptance

- All six records pass sequence/hash/path/split/geometry/editability/semantic
  evidence and deterministic reference replay.
- All six acquire active metadata, reference scripts, case cards, and registry
  pointers without manifest admission.
- Focused tests, family audit, case-library replay audit, Ruff, and
  `git diff --check` pass.

## Evidence reuse / guidance-card disposition

No runtime experience card: this is a deterministic family lifecycle decision,
not independent direct runtime mechanism evidence.

## Result

Completed offline on 2026-08-05. ADR-0027 restricted promotion to the six
frozen records. All now have active metadata, reference scripts, case cards,
registry pointers, and exact sequence-pair metadata. The scoped audit passed
6/6 and the 57-record case-library replay audit passed. No executable manifest,
provider, training, runtime, parser/helper/SDK, IR, external-data, or
face-selection path changed.

## Out of scope

New family design, face selector implementation, candidate production,
external-data admission, hosted evaluation, and any runtime path.
