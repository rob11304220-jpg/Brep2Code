---
type: navigation
related-project: Brep2Code
version: v1
status: active
---

# Route Decision Map

This is the project-level entry for deciding **which bounded route is worth
selecting next and why**.  It complements, but does not replace, the theory
map: the theory map evaluates one bounded Q01--Q04 hypothesis; this map
compares the route-level decisions that condition the project's hosted
closed-loop claim.

It is neither a task queue nor an authorization source.  `status.md` remains
the authority for work selection, and an active workpack remains the authority
for a bounded change.

## Project decision frame

The current project claim is deliberately narrow: can a real LLM complete one
frozen, bounded and auditable B-Rep-to-CAD closed loop with attributable
terminal evidence?  Three independent supporting decisions determine whether
that claim is interpretable:

| Decision dimension | It decides | Current default | A route is justified only when it can distinguish |
|---|---|---|---|
| Interaction and repair policy | The permitted behavioural space and response budget | One declared Q01 call, one explicit card call, one initial script, and at most one eligible `source_only` edit | A named, trace-supported failure mechanism from random variation, infrastructure failure, or a plateau |
| Case-library evidence denominator | Which controlled assets may represent the claim | M170's three frozen release fixtures, followed by a selected 30-case three-stratum development denominator only after qualification | A missing mechanism, parameter range, counterexample, or denominator risk that the current frozen cohort cannot resolve |
| Experience representation and projection | Which prior knowledge, if any, may enter the loop | One explicitly selected, hash-bound card through the existing tool bridge | The incremental value and risk of a fixed card, selection/retrieval policy, or new representation/interface |

The dimensions support one main route but do not borrow authority from one
another.  A new case does not justify more repair; a successful card-assisted
run does not justify retrieval; an interaction failure does not make SDK/IR
work necessary.

## How to make a route decision

Before proposing a workpack, formulate the decision in this order:

1. State the current default and the precise uncertainty it leaves open.
2. Name the smallest competing disposition: retain, change one bounded
   parameter, add one discriminating asset, or open a prerequisite inquiry.
3. Define the evidence that would discriminate the dispositions, including a
   counterexample, fixed denominator/control, and stopping rule.
4. State what the result may change and what it cannot change.  In particular,
   distinguish a recommendation, an offline implementation, and a hosted
   campaign.
5. Only after a disposition is selected, create or activate one bounded
   workpack with the required risk gate.

This sequence prevents a deferred workpack from being treated as a standing
commitment.  It is a candidate implementation of an earlier decision, not the
decision itself.

## Decision tests by dimension

### Interaction and repair policy

The question is not whether more turns might increase pass rate.  It is
whether a named, reproducible and source-level mechanism has enough evidence
to justify one additional bounded action without confounding the campaign.
Evidence must retain classification, normalized failure signature, attempt and
conversion accounting, a fixed-script reproduction, a non-matching control,
and a plateau rule.  Geometry/semantic, selector ambiguity, editability,
sandbox/provenance, timeout and provider/protocol failures remain fail-closed
unless a separate prerequisite supplies the missing locator or oracle.

The selected downstream route uses M170 (activated from
[TRG-039](../../workpacks/deferred/WP-TRG-039-closed-loop-release-freeze.md))
as the release gate, then separately charters, qualifies, freezes, executes,
and reviews a 30-case campaign. The historical three-case TRG-040/041 route
remains a future option, not this selected milestone's automatic successor.
The selected sequence is described by the Current Project Route; neither it
nor this map authorizes hosted egress.

### Case-library evidence denominator

The question is not whether another case can be made or admitted.  It is
whether the existing denominator lacks a decision-relevant discriminator.  A
new case route must name the mechanism or parameter gap, the evidence role,
the oracle and negative control, split and identity boundary, the conclusion
the case could change, and the stop rule if it does not add discrimination.

Case records govern asset identity and use; they do not by themselves select a
campaign. A historical family dossier may remain useful as design evidence, but
is not a default hosted queue. M170's three-case denominator is a release
fixture; the later 30-case milestone denominator must be selected by its own
charter and qualification gates, not by the size of the library.

### Experience representation and projection

The question is not how to extract a card from a case.  It is whether a
specific knowledge intervention has enough identifiable benefit to outweigh
source leakage, selection bias, egress and maintenance cost.  The intervention
must be explicit: no reference versus one fixed card; a separately proposed
selection/retrieval policy; or a representation/interface such as SDK/IR.

Cards, retrieval, SDK and IR are distinct interventions.  A fixed-card result
cannot establish dynamic selection value; retrieval cannot establish SDK/IR
need; and an implementation inconvenience cannot establish a knowledge effect.
Each requires its own frozen baseline/treatment or representation workpack,
with provenance, hashes, scope, counterexamples and an evaluation plan.

## Route dispositions

When reviewing a candidate or historical route, record one of these
dispositions in the relevant route/index record.  The disposition is planning
metadata, never activation authority.

| Disposition | Meaning | Required re-entry signal |
|---|---|---|
| `current prerequisite` | Needed before the selected main-route decision can be interpreted | Its stated acceptance boundary remains unmet |
| `future option` | May answer a still-relevant question after a named upstream result | The upstream report or decision named by the route |
| `superseded` | Its uncertainty is now answered or better framed elsewhere | A new, distinct uncertainty; do not revive the old package unchanged |
| `rejected` | Existing counterevidence rules out its proposed claim or intervention | New evidence that directly addresses the recorded counterexample |
| `archive-only` | Retained solely for provenance or historical evidence navigation | None; create a new proposal if the question returns |

`deferred` remains a workpack lifecycle state, not a route disposition.  A
deferred package should be read together with its disposition and re-entry
question; absent an explicit current selection, it is not a candidate queue.

## Entry routing

| Question | Start here | Then use |
|---|---|---|
| What does one modeling hypothesis support? | [Project Theory Map](project-theory-map.md) | M146 crosswalk and decision package |
| Which route should be selected, retained, replaced, or retired? | This map | Current Project Route, relevant evidence, then `status.md` |
| How does the selected loop execute? | [Pipeline](../pipeline.md) | Q01--Q04 contracts |
| Can an asset or provider be used now? | `status.md` and its active workpack | Case/provider authorities and risk gates |

## Boundary

This map adds no case, card, retrieval, SDK/IR, repair, manifest, Harness or
provider authority.  It also does not dispose of historical workpacks by
itself.  A later, separately selected governance review may apply these
dispositions to the existing deferred inventory.
