# WP-M22-004: Multi-Contour Pocket Governance Promotion

- Status: done
- Milestone: M22
- Owner: Codex

## Status transition

Selected by the user on 2026-08-05. This workpack may promote only the six
frozen `multi-contour-pocket-v1` records under ADR-0024; it does not select a
successor family or authorize runtime, manifest, provider, or training use.

## Goal

Determine whether the completed `multi-contour-pocket-v1` evidence justifies
a restricted, family-specific case-library governance promotion. This is not
automatic admission.

## Entry criteria

- M22-003 is completed and remains linked from workflow status.
- The user explicitly selects this workpack.
- A dedicated ADR is accepted before changing case lifecycle, registry, or
  long-term metadata.

## Scope

- Audit exactly the six frozen records against preregistration, normalized STEP
  hashes, deterministic replay, sequence/dependency, operation-contract
  invariants, editability, semantic anti-degeneration, and split isolation.
- Decide whether the six experimental assets can become active self-authored
  cases and whether the family can carry backward-compatible `sequence_pair`
  metadata.
- Extend offline case-library audit coverage only as required by the accepted
  ADR.

## Acceptance

- A dedicated ADR defines the family-specific maintenance boundary.
- All six records pass the scoped audit and retain split isolation.
- Every promoted asset has authoritative metadata, baseline, case card, and
  registry pointer; executable manifests remain unchanged.
- Focused tests, relevant replay audits, Ruff, and `git diff --check` pass.

## Out of scope

Automatic admission, hosted evaluation, training, native-history claims,
B-Rep-to-sequence claims, external datasets, runtime retrieval, parser
expansion, helpers, SDK, and general IR.

## Result

Completed offline on 2026-08-05. ADR-0024 limits
`multi-contour-pocket-v1` maintenance to the frozen six records. All six
passed scoped sequence, hash, path, split, geometry replay, editability, and
blind-annular anti-degeneration evidence. They are now active self-authored
library cases with reference scripts, case cards, and registry pointers, but
remain absent from every executable manifest. Focused tests, the six-record
family audit, 51-case library replay audit, Ruff, and `git diff --check` pass.
No Harness, provider, runtime, training, or manifest path changed.
