# Case-Evidence Relationships v1

This is the M150 companion mapping to the
[development-evidence crosswalk](development-evidence-crosswalk-v1.md). It
answers which *already reviewed* case or documentary evidence set supports a
bounded hypothesis and in what role. It is not a case registry, case-card
replacement, manifest, runtime resource, or hosted authorization.

## Relationship coverage

| M146 hypothesis | Development-side relationship | Documentary relationship | Boundary |
|---|---|---|---|
| `hm-q01-selector-cardinality-v1` | One unique-selector oracle and one twin-boss discriminating control | Held-out ambiguity is retained only as reviewed documentary evidence | No generic face identity, tie-breaker, or runtime selector claim. |
| `hm-q01-blind-through-observability-v1` | Through-cut oracle set and counterbore negative controls | Held-out blind evidence is documentary-only | Only the reviewed +Z single-cylinder observable. |
| `hm-q02-family-scoped-sequence-grammars-v1` | Reviewed development oracle sets for rounded slot, multi-contour pocket, boss-dependent cut, multi-inner-loop pocket, oriented rounded slot, and repeated pattern | Held-out family evidence is documentary-only | Every link remains inside its individual frozen grammar. |
| `hm-external-history-boundary-v1` | None promoted by this mapping | Three reviewed external source-specific records | A boundary on reconstruction claims, not compatibility evidence. |

The mapping intentionally has no relationship for
`hm-q04-verified-prefix-rollback-v1`: its existing evidence is a fixed-script
execution boundary rather than a case-evidence relationship that this mapping
could safely elevate.

## Use and authority

1. Start with a M146 `hypothesis_id` and its evidence/adoption boundary.
2. Use this mapping only to identify the declared evidence role and documentary
   source for a selected relationship.
3. Return to the source authority for case identity, lifecycle, split, hash,
   admission, manifest, or runtime questions.

Held-out relationships contain no case ID, fixture path, metadata, parameter,
input hash, or sequence. They only record that an already reviewed documentary
source exists. A missing mapping is `unknown`, not evidence that an asset may
be inspected or promoted.

## Maintenance and audit

Update the authority first, then this companion mapping and its hashes. Do not
inspect a fixture, script, held-out asset, or runtime resource to repair drift.

```powershell
python tools\audit_case_evidence_relationships.py
python tools\audit_development_evidence_crosswalk.py
```

The companion audit checks source hashes, crosswalk hypothesis IDs, controlled
roles/modes, source-declared case references, prohibited paths, and the absence
of held-out case IDs in documentary-only relationships.
