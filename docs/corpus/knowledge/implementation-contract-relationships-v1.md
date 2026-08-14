# Implementation-Contract Relationships v1

This is the M152/M156 companion mapping from reviewed development-side hypotheses
to its current implementation-contract representation. It is not a runtime
resource, manifest, provider input, training dataset, or hosted authorization.

## Current coverage

| Hypothesis | Status | Q01 | Q02 | Q03 | Q04 | Boundary |
|---|---|---|---|---|---|---|
| `hm-q01-selector-cardinality-v1` | `contract_only` | `planar-face-selector-cardinality-v1` | `face-selected-dependent-cut-v1` | family-scoped selector-cardinality and geometry/topology audit evidence | `selector_ambiguous -> stop_unsupported`, zero requests | Exact fail-closed chain is represented, but no reusable Harness/runtime selector contract is implemented. |
| `hm-q01-blind-through-observability-v1` | `contract_only` | `blind-through-cylindrical-extent-v1` | `prismatic-hole-v1` | offline measured-fact audit and frozen deterministic replay evidence | not a declared stage; no repair route is claimed | Declared Q01/Q02 contract is represented, but no reusable Harness/runtime observation contract is implemented. |

## Interpretation

`contract_only` is intentional. A mapping may cover the full Q01--Q04 chain
when those are the hypothesis's declared stages, as with selector cardinality,
or cover only the declared Q01/Q02 contract, as with blind/through
observability. In both cases, the reviewed development-side evidence does not
provide a reusable Harness/runtime contract and therefore cannot justify
recording the hypothesis as `implemented`.

This mapping therefore answers a narrow question only: where are the exact
declared-stage contracts represented today, and what prevents them from being
promoted to an implementation claim?

## Use and authority

1. Start with the M146 `hypothesis_id` and M150 relationship IDs.
2. Use this mapping to locate the current Q01--Q04 representation and its
   validation evidence.
3. Return to the source authority for runtime behavior, case lifecycle,
   manifest, provider, or hosted questions.

The mapping may support later route selection, but it cannot upgrade a
development-side hypothesis to runtime or hosted eligibility.
