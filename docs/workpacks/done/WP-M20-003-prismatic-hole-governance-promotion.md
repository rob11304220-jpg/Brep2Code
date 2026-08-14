# WP-M20-003: Prismatic-Hole Governance Promotion

- Status: done
- Milestone: M20
- Owner: Codex

## Goal

Promote only the validated `prismatic-hole-v1` paired family to a durable,
audited case-library metadata contract after M20-002's completed nine-case
evidence review.  This workpack does not create a general modeling IR or an
automatic admission path.

## Scope

- Version the per-case sequence-pair metadata for the nine validated cases.
- Promote the three audited counterbore assets from experimental candidates to
  active self-authored library cases, with baseline, case-card, and registry
  records but no executable manifest.
- Extend the offline case-library audit for the promoted family: grammar,
  oracle provenance, sequence agreement, hash, replay, and family split
  isolation.
- Add a concise maintenance runbook and ADR that limit the new rule to this
  grammar/family.

## Compatibility constraints

Default execution remains offline.  Existing manifests, corpus selection,
Harness gates, CLI, provider policy, prompts, runtime resources, SDK, and IR
remain unchanged.  Directory presence and a successful producer never create
manifest, provider, training, or runtime admission.

## Acceptance

- Nine scoped records carry a backward-compatible `sequence_pair` contract.
- Three counterbore cases are active in the development library but absent from
  every executable manifest.
- Audit rejects grammar/provenance/sequence mismatch and a split leak; replay
  validates all promoted references.
- Full pytest, Ruff, and `git diff --check` pass.

## Out of scope

New grammar operations, B-Rep-to-sequence inference, native-history claims,
automatic admission, hosted evaluation, training, Harness changes, runtime
retrieval, a general IR, or a project CAD SDK.

## Result

Completed offline on 2026-08-04.  All nine validated records now carry the
ADR-0019-scoped `sequence_pair` metadata.  The three counterbore cases were
registered as active self-authored assets with case cards and baselines, but
remain absent from every executable manifest.  The extended library audit
checks grammar/provenance/sequence consistency, candidate-sequence agreement,
hashes, replay, and family-split isolation.  Focused tests passed 12 and the
42-case replay audit passed.  No Harness, manifest, provider, or runtime path
changed; no reusable experience card was created.
