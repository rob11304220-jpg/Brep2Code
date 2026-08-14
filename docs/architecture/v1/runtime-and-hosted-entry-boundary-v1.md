---
type: design
related-project: Brep2Code
version: v1
status: active
---

# Runtime and Hosted Entry Boundary v1

This document is the M155 compact entry-boundary record for any later
runtime-projection or hypothesis-to-hosted-evaluation selection. It is a
planning and governance boundary only. It does not create a runtime card,
reference pack, retrieval index, provider request, campaign charter, or hosted
authorization.

## Purpose

The post-M152 hardening route now has three stable development-side inputs:

1. the maintained authority map from M153;
2. the implementation-contract coverage layer from M154; and
3. the existing crosswalk and case-evidence provenance layers from M146/M150.

Before `WP-TRG-028` or `WP-TRG-035` may be selected, later work must freeze
exactly which of those inputs it is reusing, which authority remains upstream,
and which later-facing artifacts still require a separately reviewed package.

## Required authority inputs

Any later runtime-projection or hosted-evaluation package must cite all of the
following sources explicitly, with ID/path and any declared hash or review
state required by its own workpack:

| Input | Required role | What it does not authorize |
|---|---|---|
| M153 maintained authority map | Fixes route order, reuse boundary, and the prohibition on treating development-side knowledge as runtime/provider material. | Automatic activation, runtime artifact creation, provider input, or hosted authorization. |
| M146 development-evidence crosswalk | Names the bounded `hypothesis_id`, evidence boundary, counterexample, stop rule, and adoption boundary. | Runtime support, card eligibility, provider reference material, or campaign interpretation by itself. |
| M150 case-evidence relationships | Freezes the selected evidence-role/provenance links where case/documentary support is relevant. | Case admission, split changes, runtime projection, or outbound provider content. |
| M152 implementation-contract mapping | Supplies source-linked Q01--Q04 contract representation where a reviewed mapping already exists. | Capability generalization, runtime promotion, or hosted proof. |
| M154 implementation-contract coverage layer | States whether the selected hypothesis is currently `implemented`, `contract_only`, `unsupported`, or still `missing_link`. | Negative evidence beyond the published mapping state, or permission to infer implementation from raw evidence. |
| Existing runtime/hosted boundary docs | Constrain runtime/Harness material, finite case scope, limited reference scope, and hosted campaign discipline. | Reuse of a historical report, policy, or authorization as current approval. |

## Selection gate

No later route may be selected merely because its sources exist. A future
package must show all of the following before activation:

1. one explicitly named downstream workpack (`WP-TRG-028` or `WP-TRG-035`);
2. one bounded question and declared scope;
3. explicit source citations back to the required authority inputs above;
4. a statement of which required later-facing artifacts are still missing and
   will be frozen inside that later package; and
5. a statement that no runtime/provider/hosted authority is inherited by
   default from M155.

If any of those are missing, the downstream route remains deferred.

## Later artifacts that must be frozen separately

M155 does not choose or define any later-facing artifact. The following items
must each be frozen in the later selected package rather than inherited from
M155:

| Later artifact | Must be frozen separately because |
|---|---|
| Runtime-projection form | `WP-TRG-028` must still decide whether the minimal projection is a runtime card, compact pack, tool/schema surface, SDK/IR shape, or another bounded form. |
| Projection applicability and prohibition fields | A later package must pin which case/split/mechanism boundary the projection applies to and what it explicitly excludes. |
| Egress-safe reference projection | `WP-TRG-035` requires a separately reviewed, hash-pinned outbound projection with an explicit schema/allowlist; development-side docs are provenance only. |
| Campaign scope | Any hosted package must freeze case IDs or family rows, split membership, denominator, stop rule, and comparison arms for that campaign. |
| Authorization text | Any hosted package must derive fresh itemized authorization text after preflight; M155 cannot pre-authorize a provider request. |
| Acceptance commands | Each later package must define its own exact validation and acceptance record for its bounded artifact and scope. |

## Route-specific entry requirements

### For `WP-TRG-028`

The activation package must additionally show:

- one reviewed immutable admission record and reviewed admission-profile
  crosswalk already in scope;
- the selected minimal runtime-projection form is still undecided at M155 time
  and will be compared/frozen inside `WP-TRG-028`;
- no script, raw STEP, local path, held-out answer, or unrestricted retrieval
  enters the projection candidate set; and
- the work remains offline and does not imply provider or hosted readiness.

### For `WP-TRG-035`

The activation package must additionally show:

- one selected M146 `hypothesis_id` with frozen crosswalk and case-evidence
  provenance snapshots;
- whether the M154 coverage state for that hypothesis is sufficient for the
  hosted question, or whether missing implementation-contract coverage is a
  stop condition;
- one separately reviewed, hash-pinned egress-safe reference projection with
  explicit outbound schema/allowlist; and
- completion of hosted preflight and fresh itemized authorization before any
  provider request is attempted.

## Stop conditions inherited by later selection

The downstream route remains deferred if any of the following is true:

- the selected hypothesis or evidence boundary is not explicit;
- the later package tries to treat development-side docs as runtime/provider
  material;
- the required runtime-projection or egress-safe projection artifact is still
  undefined;
- a historical report, budget, or approval is treated as reusable authority;
- the later package would need to broaden hypothesis scope, change manifests,
  alter runtime behavior, or make a provider request without a separately
  selected package that explicitly grants that scope.

## Relationship to existing boundaries

- [Modeling knowledge adoption](modeling-knowledge-adoption.md) governs when
  reviewed knowledge may even become a candidate runtime projection.
- [Runtime boundaries](runtime-boundaries.md) keeps `docs/` development
  governance separate from Harness/runtime-injected materials.
- [Current hosted evaluation framing](current-hosted-evaluation-framing.md)
  governs finite case scope, limited reference scope, and hosted campaign
  discipline.

M155 adds one thing only: a compact pre-selection checklist that later
`WP-TRG-028` and `WP-TRG-035` must cite before they may be activated.
