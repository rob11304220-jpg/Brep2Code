# WP-M20-002: Prismatic-Hole Controlled Expansion

- Status: done
- Milestone: M20
- Owner: Codex

## Goal

Test whether the completed `prismatic-hole-v1` pilot remains auditable when
expanded to nine preregistered paired cases, without widening its grammar or
promoting it to global case-library governance.

## Scope

- Retain the exact `SketchRect -> ExtrudeBase -> CutCylinder` grammar and the
  existing three evidence layers.
- Preregister nine cases before audit outcome: three development `through_hole`
  variants, three development `counterbore` variants, and three held-out
  `blind_hole` variants.  Each template family stays in one split.
- Add a deterministic candidate producer for the new counterbore family.  It
  produces local candidate assets and metadata only; an audit remains the sole
  path to selection evidence.
- Extend the offline audit to validate all nine cases, candidate/sequence
  agreement rejection, family isolation, hashes, deterministic replay, and
  declared editability mutations.
- Write a completion review that decides only whether a *future* governance
  promotion workpack may be proposed.

## Attribution question and sampling intent

Determine whether the pilot's grammar and audit are stable across parameter
variation and all three supported hole semantics, including an unseen held-out
family.  The exact 6 development / 3 held-out selection is fixed before case
generation and audit.  Stop after these nine rows: do not replace failures,
widen grammar, move families, or add rows to improve a result.

## Inputs

- M20-001 contract, seed, audit, and completed review.
- Existing M12 through-hole development and blind-hole held-out parameter
  families.
- Direct OCP primitives and booleans already used by committed reference
  scripts.

## Code paths

- `docs/corpus/sequence-paired/` for the preregistered expansion record.
- `case-library/self-authored/` only for explicitly generated counterbore
  candidates and their authoritative metadata.
- `tools/` and `tests/` for deterministic producer/audit coverage.

## Docs to update

- M20 contract and route roadmap, if the expanded audit needs a documented
  pilot-only metadata field.
- `docs/corpus/library/README.md`, `docs/workflow/status.md`, this workpack,
  workpack index, active handoff, and a completion review.
- Do not change ADR-0014 or a maintenance runbook unless a later promotion
  workpack is selected and accepted.

## Trace/schema changes

No Harness trace, provider trace, corpus report, CLI JSON, or runtime schema
change is authorized.  Expansion metadata remains development-side only.

## Compatibility constraints

- Default execution remains offline and credential-free.
- Existing manifests, fixture paths, Harness gates, Fusion scope, ABC boundary,
  hosted policy, runtime resources, prompt, SDK, and IR remain unchanged.
- A produced candidate never becomes a default fixture, corpus selection,
  provider input, or training input merely by passing local generation.

## Acceptance

- Exactly nine preregistered rows retain 6 development / 3 held-out counts and
  three disjoint family/template IDs.
- Every row passes geometry, exact sequence contract, and its preregistered
  editability checks.
- Tests demonstrate rejection of a mismatched candidate sequence and a split
  leak; deterministic producer output matches checked-in hashes.
- Full pytest, Ruff, and `git diff --check` pass.
- The completion review recommends promotion, revision, or retirement without
  changing global case-library governance.

## Evidence reuse / guidance-card disposition

Record exactly one completion disposition: a source-linked experience card, a
counterexample, or no reusable evidence.  It does not authorize runtime use.

## Status transition

On completion update status, this workpack, workpack index, active handoff, and
completion review.  Any global governance change requires a distinct workpack
and ADR after review.

## Out of scope

New grammar operations, native-history claims, generic B-Rep inference,
provider/hosted evaluation, training, automatic admission, Fusion/DeepCAD
expansion, Harness or gate changes, runtime IR, SDK, and benchmark claims.

## Result

Completed offline on 2026-08-04.  The nine preregistered rows retained exactly
six development cases across the `through_hole` and `counterbore` families and
three held-out `blind_hole` cases.  All passed deterministic geometry replay,
canonical sequence validation, and two declared editability mutations.  The
new counterbore producer creates experimental candidate-only assets and
normalizes OCP header variability so regenerated hashes match the checked-in
assets; tests reject a mismatched candidate sequence and split leakage.

Focused M20 tests passed 8; the nine-case audit passed.  The completion review
permits only a future, separately approved governance-promotion proposal.  It
does not promote ADR-0014 rules or change a registry, manifest, corpus,
provider, training, Harness, or runtime path.  Evidence disposition: no
reusable experience card.
