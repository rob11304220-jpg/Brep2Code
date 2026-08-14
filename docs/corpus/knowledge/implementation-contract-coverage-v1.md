# Implementation-Contract Coverage v1

This is the M154 companion coverage layer over reviewed development-side
hypotheses and published implementation-contract mappings. It is not a runtime
resource, manifest, provider input, training dataset, or hosted authorization.

## Current coverage view

| Hypothesis | Coverage status | Declared stages | Represented stages | Missing stages | Boundary |
|---|---|---|---|---|---|
| `hm-q01-selector-cardinality-v1` | `contract_only` | `Q01`, `Q02`, `Q03`, `Q04` | `Q01`, `Q02`, `Q03`, `Q04` | none | Exact fail-closed chain is represented, but no reusable Harness/runtime selector contract is implemented. |
| `hm-q01-blind-through-observability-v1` | `contract_only` | `Q01`, `Q02` | `Q01`, `Q02` | none | Declared Q01/Q02 contract is published, but no reusable Harness/runtime observation contract or repair route is implemented. |
| `hm-q04-verified-prefix-rollback-v1` | `missing_link` | `Q03`, `Q04` | none | `Q03`, `Q04` | Reviewed execution evidence exists, but no source-linked implementation-contract mapping states the bounded rollback chain. |
| `hm-q02-family-scoped-sequence-grammars-v1` | `missing_link` | `Q02`, `Q03` | none | `Q02`, `Q03` | Reviewed family-scoped units exist, but no source-linked implementation-contract mapping records an exact chain for this grouped hypothesis. |
| `hm-external-history-boundary-v1` | `missing_link` | `Q01`, `Q03` | none | `Q01`, `Q03` | The reviewed external-history material is a boundary pattern, and no implementation-contract mapping is published for it. |

## Interpretation

This coverage layer answers one narrow planning question only: which reviewed
hypotheses already have a published implementation-contract mapping, and which
still need a bounded mapping step before later routes may discuss runtime
projection or hosted-entry boundaries.

`missing_link` is not a negative evidence claim. It means the repository does
not currently publish a source-linked implementation-contract mapping for that
hypothesis. The reviewed evidence may still exist in the crosswalk; M154 does
not reinterpret that evidence into an implementation claim.

## Status definitions

- `implemented`: a published source-linked mapping shows the hypothesis's
  exact declared-stage contract and records it as implemented.
- `contract_only`: a published source-linked mapping shows the hypothesis's
  exact declared-stage contract, but the project still lacks the reusable
  Harness/runtime contract needed for an implementation claim.
- `unsupported`: a published source-linked mapping records an exact
  declared-stage boundary as unsupported rather than implemented.
- `missing_link`: no published source-linked implementation-contract mapping
  currently records the hypothesis's exact implementation-contract
  representation.

## Use and authority

1. Start with the M146 `hypothesis_id` in the development-evidence crosswalk.
2. Check this coverage layer to see whether a published implementation-contract
   mapping already exists, and whether it is `implemented`, `contract_only`,
   `unsupported`, or still `missing_link`.
3. Return to the authoritative source-linked mapping for any contract detail,
   and return to the route document for later selection order.

This layer may support later route selection, but it cannot upgrade a
development-side hypothesis to runtime or hosted eligibility.
