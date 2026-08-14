# M114 Prismatic End-to-End Card-Effect Policy Design

## Design boundary

This is an offline design record, not a policy, preflight, authorization or
campaign. It does not name a provider, model, case, held-out row, hash, prompt,
budget, report or monitor path. M97 remains terminal and unmodified.

## Estimand

The future policy may observe only the finite **end-to-end treatment**
difference between a fixed card condition and a no-card control under the same
frozen path-free measured-fact transcript. “End-to-end” includes whether the
generated script is API-admissible. It is not a causal estimate beyond the
declared rows, policy and execution environment, and is not a conditional
geometry-quality estimate.

## Required frozen predicates

Before a future development-only policy may be selected, it must pre-register:

1. a split/hash/context integrity predicate proving the two conditions use the
   same allowed measured facts, with the card as the only declared treatment;
2. one versioned static API-admissibility classifier covering imports, symbols,
   constructor arity and the declared through-cut recipe before sandbox launch;
3. mutually exclusive lifecycle, API-admissibility, sandbox/execution,
   downstream-gate and full-success terminal categories; and
4. no-retry/no-repair stop rules, fresh request accounting and a prohibition on
   M97 policy, report, monitor, budget or authorization reuse.

An integrity failure is not a comparison result and terminates the policy. A
provider/lifecycle outcome without a generated script is unavailable for the
estimand and does not advance the route.

## Paired interpretation

| Fixed paired outcome after integrity passes | Bounded interpretation |
|---|---|
| Both conditions reach full success | Feasibility under both conditions for that row; no treatment advantage. |
| Card reaches full success; control is static API-inadmissible | An observed finite end-to-end treatment advantage specifically at the preregistered API-admissibility stage. |
| Card reaches full success; control fails later sandbox or downstream gates | An observed finite end-to-end treatment advantage at the declared terminal stage; no general mechanism claim. |
| Card fails; control succeeds | No observed treatment advantage for that row. |
| Either integrity fails, lifecycle ends before script, or both conditions do not reach a classifiable terminal comparison | Unavailable or inconclusive; no retry, repair or reinterpretation. |

No outcome supports parameter generalization, generic CAD ability, runtime-card
promotion or a result conditional on API-valid scripts.

## Later gates

The required order is: separately selected G2 development-policy freeze and
independent review; separately selected G3 development calibration after the
hosted-stability route, fresh preflight and itemized authorization; independent
terminal review; then, only if that review supports it, a separately frozen
held-out policy with new G3 preflight and authorization. Each stage may stop
the route; none is selected by this design record.

## Disposition

The design is ready only as an offline prerequisite for a future selected
development-policy package. It creates no reusable runtime knowledge and no
hosted authority.
