---
type: roadmap
related-project: Brep2Code
status: active
---

# Post-M138 Runtime and Knowledge Route

## Purpose

This route turns the five design questions recorded after M135/M138 into
separate, bounded offline workpack choices.  It is a planning authority only:
it neither activates a workpack nor authorizes a provider request, runtime
change, manifest change, external data, or card promotion.  `status.md`
remains the current-state authority.

This page is now primarily a historical dependency record for the M139--M143
route cluster and the original pre-projection sequence. The current
project-level next-step ordering after M155 lives in
[`post-m152-authority-and-contract-hardening-route.md`](post-m152-authority-and-contract-hardening-route.md).

## Ordered route

| Order | Trigger workpack | Decision and implementation boundary | Depends on |
|---:|---|---|---|
| 1 | M139 complete | Implemented a reusable frozen-campaign launcher: registered B-Rep input, bounded Q01 egress, optional declared card, request/repair limits, durable prepare/execute checkpoint. | M138 terminal boundary |
| 2 | M140 complete | Implemented the Harness-owned tool-turn loop so an LLM may request bounded probes or an explicitly selected card, then receive execution/gate feedback. | M139 contract |
| 3 | M141 complete (consumed `WP-TRG-026`) | Defined and implemented classified, bounded repair routes; separated source repair from sequence/IR rollback and plateau handling. | TRG-025 signal/tool contract |
| 4 | M142 complete (consumed `WP-TRG-027`) | Defined and audited one immutable case admission record pilot with replay, gates, editability, split isolation, alternatives and repair signatures. It granted no runtime projection authority. | TRG-026 policy vocabulary |
| 5 | M143 complete (consumed `WP-TRG-029`) | Stratified the existing development-side case library into evidence-bound admission profiles and mapped the reviewed TRG-027 pilot; it granted no case admission or runtime projection authority. | TRG-027 reviewed admission record |
| 6 | `WP-TRG-028` downstream | A later separately selected package may decide, derive and evaluate one safe runtime projection from a reviewed admission record among cards, packs, runtime cards, SDK, IR and case library. | TRG-027 reviewed admission record and M143 reviewed profile crosswalk |

The sequence is deliberate. A card-selection or repair experiment cannot be
interpreted until the launcher fixes the exact outbound and accounting boundary;
a replayed case first becomes an auditable admission record, is then situated
in a reviewed development-side admission profile, and cannot become runtime
knowledge until TRG-028 derives and evaluates a separate, hash-linked
projection.

## Shared non-negotiable constraints

- The input B-Rep is registered, hashed and mounted only to the Harness.  A
  provider receives only the campaign's hash-pinned, allowlisted Q01 facts;
  raw STEP, paths, reference scripts and held-out answers remain prohibited.
- `prepare` is local and credential-free.  It must validate input/split/card
  hashes, no-input `wsl-bwrap`, request accounting, provider configuration
  presence and fresh report/monitor identities before any authorization is
  requested.
- `execute` accepts only a prepared, unchanged campaign identity.  Hosted use
  still requires a selected G3 workpack, independent review, itemized user
  authorization and a new report/monitor pair.
- Runtime tools are Harness-owned, schema-bound, byte/token limited and
  auditable.  The provider never obtains arbitrary filesystem or shell access.
- A frozen evaluation campaign cannot repair, swap cases, revise cards or
  change limits in place.  Such changes form a later campaign with a new
  denominator and authorization.

## Research inputs

The workpacks use the paper-vault synthesis for project-specific evidence
boundaries, and treat the following papers as design inputs rather than
implementation authority: [ReAct](https://arxiv.org/abs/2210.03629) for
interleaved reasoning/action, [Toolformer](https://arxiv.org/abs/2302.04761)
for bounded API invocation, and [RAG](https://arxiv.org/abs/2005.11401) for
retrieval provenance and ablation discipline.  Their results do not prove a
CAD-card effect or authorize broad retrieval in Brep2Code.

## Selection rule

M139 through M143 are complete. `WP-TRG-028` remains a downstream successor,
not an active queue item, and the later hosted/authority ordering is governed
by [`post-m152-authority-and-contract-hardening-route.md`](post-m152-authority-and-contract-hardening-route.md).
A selected package must be assigned a new milestone identifier, one owner and
an independent reviewer; the owner then follows the normal G2/G3 lifecycle.
