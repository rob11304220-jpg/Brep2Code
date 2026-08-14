# Development-Evidence Crosswalk v1

This page is a derived, development-side navigation view over
[`development-evidence-crosswalk-v1.json`](development-evidence-crosswalk-v1.json).
It links reviewed metadata and documentary sources; it is not a case registry,
manifest, runtime resource, training dataset, or hosted authorization.

Its primary node is a **bounded modeling hypothesis**. The sources retain their
own authority: `case.json` and the registry own asset facts; knowledge units
own their bounded claims; decision packages own decision framing; the coverage
matrix owns decision gaps; and admissions own immutable evidence records.

## 1. Capability-question view

| Bounded hypothesis | Q01--Q04 question | Current disposition |
|---|---|---|
| `hm-q01-selector-cardinality-v1` | When can a dependent selector bind, and when must it stop? | Reviewed; cardinality one binds, otherwise fail closed. |
| `hm-q01-blind-through-observability-v1` | Which frozen B-Rep facts distinguish the reviewed blind/through observable? | Reviewed only for the +Z single-cylinder scope. |
| `hm-q04-verified-prefix-rollback-v1` | Can a localized suffix be regenerated without rewriting a verified prefix? | Reviewed fixed-script diagnostic boundary. |
| `hm-q02-family-scoped-sequence-grammars-v1` | What do the reviewed family grammars support? | Only their declared, frozen grammars. |
| `hm-external-history-boundary-v1` | What can external B-Rep-only/native-history records establish? | A boundary, not a reconstruction claim. |

## 2. Bounded-modeling-hypothesis view

| Hypothesis | Observation prerequisite | Constrained action or conclusion | Counterexample / stop rule |
|---|---|---|---|
| Selector cardinality | Declared planar +Z maximum-output-Z predicate and candidate cardinality | Bind only exactly one eligible boss top before the dependent cut. | Zero/multiple candidates, coordinate tie-breaks, or generic naming claims stop. |
| Blind/through observable | Reviewed +Z single-cylinder facts | Report the bounded observable; do not name generic history. | Other directions/counts/counterbores fail closed. |
| Verified-prefix rollback | Step-indexed artifacts and a localized failure boundary | Regenerate only the suffix after the verified prefix. | Any prefix mutation or non-localizable failure is unsupported. |
| Family-scoped grammars | Each unit's declared profile, dependency, and split boundary | Use only its frozen sequence grammar. | Unlisted frames, references, profiles, and topology remain unknown. |
| External-history boundary | Restricted source/representation evidence | Preserve the external validation limitation. | Do not infer native-history compatibility or B-Rep-to-sequence recovery. |

## 3. Evidence view

| Hypothesis | Evidence roles | Maturity | Admission risk |
|---|---|---|---|
| Selector cardinality | oracle, discriminating, negative control | Reviewed hash-bound admission record | `bounded_unique_bind`; ambiguity is terminal. |
| Blind/through observable | oracle, regression | Reviewed observable and family-scoped sequence evidence | `needs_evidence` outside the exact scope. |
| Verified-prefix rollback | oracle, negative control, regression | Reviewed fixed-script execution evidence | `diagnose_only`. |
| Family-scoped grammars | oracle, regression | Reviewed family replay/gates | `needs_evidence`. |
| External-history boundary | OOD robustness, native-history validation | Reviewed boundary | Unknown outside reviewed sources. |

## 4. Evaluation-design view

This crosswalk does not design or authorize an experiment. It preserves the
already-declared interpretation boundary for any future, separately selected
package:

- Q01 facts must remain limited to each hypothesis's declared observables.
- Q02 action scope is limited to its frozen grammar or explicitly stated
  non-action conclusion.
- Q03/Q04 interpretation must retain the listed gate/diagnostic and stop rule.
- A comparison may support only the hypothesis's conclusion boundary; it cannot
  establish runtime adoption, provider use, generic reconstruction, or hosted
  performance.

## 5. Adoption-boundary view

All five hypotheses are development-only. None authorizes case promotion,
manifest selection, runtime cards, reference packs, retrieval, SDK/IR work,
provider use, training, or hosted execution. Those require their existing,
separately selected decision and review gates.

## 6. Implementation-contract view

Implementation-contract coverage is now tracked in a dedicated M154 coverage
layer:

| Hypothesis | Coverage status | Coverage note |
|---|---|---|
| `hm-q01-selector-cardinality-v1` | `contract_only` | Exact Q01--Q04 chain is published, but no reusable Harness/runtime selector contract is implemented. |
| `hm-q01-blind-through-observability-v1` | `contract_only` | Declared Q01/Q02 observable/operation contract is published, but no reusable Harness/runtime observation contract or repair route is implemented. |
| `hm-q04-verified-prefix-rollback-v1` | `missing_link` | Reviewed execution evidence exists, but no source-linked implementation-contract mapping is published. |
| `hm-q02-family-scoped-sequence-grammars-v1` | `missing_link` | Reviewed operation-family evidence exists, but no source-linked implementation-contract mapping is published. |
| `hm-external-history-boundary-v1` | `missing_link` | Reviewed boundary evidence exists, but no source-linked implementation-contract mapping is published. |

See
[`implementation-contract-coverage-v1.md`](implementation-contract-coverage-v1.md)
for the compact coverage view, and
[`implementation-contract-relationships-v1.md`](implementation-contract-relationships-v1.md)
for the current source-linked mapping and validation evidence.

## Maintenance and drift

Update the authority first, then refresh the relationship and source hashes in
the JSON crosswalk, run the audit, and finally update this navigation page if a
reader-facing conclusion changes. Do not resolve drift by inspecting fixtures,
reference scripts, held-out inputs, or runtime resources.

```powershell
python tools\audit_development_evidence_crosswalk.py
```

The audit verifies source existence and hashes, stable IDs, relationship
integrity, explicit non-projection scope, and the absence of forbidden source
paths. A failed audit is documentation drift, not permission to infer evidence
or modify an authority.
