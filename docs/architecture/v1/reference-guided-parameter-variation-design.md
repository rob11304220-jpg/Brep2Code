# Reference-Guided Parameter-Variation Design

## Question

Can a bounded derived action card help produce an independent script for an
unseen parameter combination of one frozen mechanism, without leaking a local
reference answer or treating a geometry match as generalization?

## Candidate boundary

The only candidate mechanism is `vertical-cylinder-construction` from the
existing experimental card. The development source records are
`param_through_hole_low`, `param_through_hole_nominal`, and
`param_through_hole_high`: each has a rectangular base and one +Z cylindrical
through cut, with radius and x-position variation. They calibrate the contract
only; their reference scripts, hashes, paths and concrete parameter answers
must not enter a card or provider payload.

`param_blind_hole_*` is excluded because blind depth changes the mechanism.
M90 repeated-feature-pattern is excluded because four-instance placement is a
different grammar and no runtime card has been qualified for it.

## Required successor design

A later workpack must preregister a new, family-isolated held-out through-hole
set before producing it. It must freeze exact rows, parameter intervals,
containment, development/held-out split, canonical sequence, mutations,
negative controls and stopping rule. It may not reuse a blind-hole row as a
held-out proxy or modify the card after observing a held-out result.

## Derived reference boundary

The permitted card content is limited to the existing action contract:
`BRepPrimAPI_MakeCylinder` as a +Z circular primitive/cutter when the required
radius, height and position are observed. It may contain applicability facts,
parameter placeholders, output requirements and counterexamples. It must not
contain raw STEP, a complete reference script, local path, source hash,
development parameter value, held-out answer, prompt transcript or report.

## Offline evidence before any provider use

The successor must establish all of the following locally:

1. A fake-provider script uses only the declared role/card and passes the
   existing OCP API, no-input sandbox, provenance, output and geometry gates.
2. The generated construction is independently parameterized: declared radius
   and x-position mutations change the expected observables while preserving
   one solid and one through cut.
3. Source-leak negative controls reject a card or payload containing a path,
   raw STEP, full script, source hash or case-specific reference answer.
4. Development evidence cannot adapt the card, case set or prompt after a
   held-out row is seen.

## Actual context and API conformance

The actual provider-bound transcript, not merely an offline adapter output,
must contain the M96 measured `base_bbox`, cylinder `radius`, `axis`,
`center_xy` and `extent` facts. Generic bbox/volume/topology summaries are not
an admissible substitute. A pre-issuance assertion must reject missing facts,
held-out rows and forbidden source fields with zero provider requests.

The declared +Z through-cut recipe must use the installed OCP surface (for
example `gp_Dir(0, 0, 1)`, a measured centre/radius and cutter extents crossing
the base). Unsupported import symbols such as `gp_DZ` are a local API-contract
failure, not a provider or card outcome. Changing this recipe, prompt or card
requires a new frozen policy before any hosted paired comparison.

## Hosted boundary

M97-001 is invalid calibration evidence because its provider context omitted
the required measured parameter facts; its report and remaining capacity may
not be reused. M97-003 subsequently completed a new development calibration,
and M97-004 classified its nominal baseline failure as a generated-script OCP
constructor-arity counterexample. Neither result selects or authorizes M98.
Any later held-out route must first receive a user-selected M97/M98 readiness
decision, then retain the frozen three-row paired policy with fresh hashes,
manifest/split and `wsl-bwrap` preflight, report path, explicit
destination/derived-egress description, model, deadline and request-budget
authorization. A terminal result remains bounded evidence, not a
parameter-generalization claim.
