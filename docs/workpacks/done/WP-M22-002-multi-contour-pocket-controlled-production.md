# WP-M22-002: Multi-Contour Pocket Controlled Production and Validation

- Status: done
- Milestone: M22
- Owner: Codex

## Status transition

Selected by the user on 2026-08-05 after M22-001. This selection authorizes
only the frozen candidate production and validation; it does not select M22-003
or authorize candidate promotion.

## Goal

Produce and validate only the frozen M22-001 multi-contour pocket candidates.

## Entry criteria

- The user explicitly selects this workpack.
- The only selection authority is
  `docs/corpus/sequence-paired/multi-contour-pocket-v1-preregistration.json`.
- The design and contract draft remain linked from
  `docs/architecture/v1/multi-contour-pocket-sequence-pair-design.md`.

## Scope

- Generate only preregistered rows and retain candidate/rejection evidence.
- Audit deterministic replay, STEP hash stability, existing geometry gates,
  exact canonical sequence/dependency agreement, editability mutations,
  semantic anti-degeneration, operation-contract topology invariants, and
  split isolation.
- Create an independent M22-003 review workpack; passing candidates remain
  unadmitted until that review and any later ADR.

## Out of scope

Selection changes, automatic library promotion, manifests, external data,
provider/hosted use, training, runtime integration, parser expansion, helper,
SDK, or IR.

## Result

Completed offline on 2026-08-05. The producer generated exactly the frozen six
experimental candidates, checking each twice in clean directories for
byte-identical normalized STEP output. All six passed the three-layer family
audit, four editability mutations, operation-contract topology checks, and
split isolation. Focused tests passed 4; the 45-record case-library replay
audit, Ruff, and `git diff --check` passed. The candidates remain unregistered
and absent from every manifest, provider, training, and runtime route. See the
M22-002 review for the bounded interpretation.
