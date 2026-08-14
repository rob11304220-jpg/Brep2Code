---
type: review
related-project: Brep2Code
status: completed
---

# M22-003 Review: Cross-Family Dependency Evidence

## Scope

This review compares the completed self-authored deterministic-oracle families
without promoting an asset, changing a manifest, or enabling a runtime,
provider, parser, helper, SDK, or IR route.

## Evidence comparison

| Dimension | `prismatic-hole-v1` | `rounded-slot-v1` | `multi-contour-pocket-v1` | Review finding |
|---|---|---|---|---|
| Frozen rows / split | 9, 6 development / 3 held-out | 6, 3 / 3 | 6, 3 / 3 | All use family-isolated, preregistered rows. |
| Profile semantics | circular cut | one composite rounded-slot loop | two nested rectangular loops | M22 adds a second loop role and containment boundary. |
| Dependency | base to cylindrical cut | base plus second profile | base plus outer-and-inner-loop profile | All retain explicit canonical dependencies; none uses face/edge references. |
| Validation | replay, sequence, editability | replay, sequence, editability, anti-degeneration | replay, sequence, editability, containment, blind annular invariants | The same three-layer discipline remains reproducible. |
| Producer and negative controls | hash stability / sequence and split controls | hash stability / semantic and split controls | hash stability / single-loop, containment, and split controls | Each family retains negative evidence rather than silently resampling. |
| Scope | local deterministic oracle | local deterministic oracle | local deterministic oracle | None is native history, B-Rep-to-sequence recovery, provider evidence, or a general IR. |

## Knowledge disposition

The six M22 records justify the bounded `multi-contour-pocket-v1` knowledge
unit at `supported` evidence. It records only the frozen nested-rectangle,
blind-annular-pocket grammar and explicit counterexamples. No experience card
is eligible: no single runtime mechanism has three independent `direct` cases.

The coverage matrix now marks the concrete outer-plus-inner-loop and
inner-profile-pocket gaps as tested only within this grammar. Curves, multiple
inner loops, orientation ambiguity, face/edge dependencies, correct-prefix
repair, equivalent-sequence ambiguity, and generic feature recovery remain
open.

## Successor selection

Select exactly one successor: propose `WP-M22-004` for a separate
family-specific governance promotion of `multi-contour-pocket-v1`.

An additive-boss/dependent-cut design is deferred until this family has a
clear governance disposition. The conditional IR shadow remains blocked:
there is no repeated, trace-supported failure showing that scripts cannot
retain a correct prefix without one structured dependency representation.

## Boundaries

M22-004, if separately selected, must create and accept a dedicated ADR before
changing case lifecycle or long-term metadata. This review does not itself
promote the six candidates, authorize external material, or change runtime
behavior.
