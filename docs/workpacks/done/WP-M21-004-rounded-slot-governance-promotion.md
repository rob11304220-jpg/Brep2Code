# WP-M21-004: Rounded-Slot Governance Promotion

- Status: done
- Milestone: M21
- Owner: Codex

## Goal

Determine whether the completed `rounded-slot-v1` evidence justifies a
restricted, family-specific case-library governance promotion. This is not an
automatic admission workpack.

## Status transition

Selected by the user on 2026-08-04. Its
outcome does not select or start M22; the next sequence-paired family remains
a separately selected, two-phase backlog route under ADR-0020 and ADR-0021.

## Entry criteria

- M21-003 is completed and its cross-family review remains linked from the
  workflow status.
- The user explicitly selects this workpack.
- The workpack creates and accepts a dedicated ADR before changing the
  long-term case-library contract, registry, or case lifecycle.

## Scope

- Audit the six frozen rounded-slot records against their preregistration,
  hashes, deterministic replay, sequence/dependency contract, editability,
  semantic anti-degeneration, and split isolation.
- Decide whether the three experimental `offset_rounded_slot` assets can
  become active self-authored library cases and whether all six records can
  carry a backward-compatible, family-specific `sequence_pair` metadata role.
- Extend the offline library audit only as required by the accepted ADR.

## Compatibility constraints

Default execution stays offline and credential-free. A successful promotion
does not add an executable manifest, corpus/provider input, training input,
runtime resource, prompt, Harness behavior, parser feature, helper, SDK, or
general IR.

## Acceptance

- A dedicated ADR defines the family-specific maintenance boundary.
- All six records pass the scoped audit and retain split isolation.
- Any promoted asset has authoritative metadata, baseline, case card, and
  registry pointer, while every executable manifest remains unchanged.
- The audit rejects sequence drift, semantic degeneration, hash/path drift,
  and split leakage.
- Full relevant tests, `uv run python tools/audit_case_library.py --replay`,
  Ruff, and `git diff --check` pass.

## Out of scope

Automatic admission, hosted evaluation, training, B-Rep-to-sequence claims,
native-history claims, external datasets, runtime retrieval, parser expansion,
helpers, and a general IR.

## Result

Completed offline on 2026-08-05. ADR-0023 limits `rounded-slot-v1`
sequence-pair maintenance to the frozen six records. All six passed scoped
sequence, hash, path, split, geometry replay, editability, and
anti-degeneration evidence. The three `param_offset_rounded_slot_*` cases are
now active self-authored library cases with reference scripts, case cards, and
registry pointers, but remain absent from every executable manifest. Focused
tests passed 7, the 45-case replay audit and six-record sequence audit passed,
and Ruff plus `git diff --check` passed. No Harness, provider, runtime, or
manifest path changed.
