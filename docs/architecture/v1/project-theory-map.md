---
type: navigation
related-project: Brep2Code
status: active
---

# Project Theory Map

This is the project-level entry for a development-side question such as:
“which bounded B-Rep-to-modeling-sequence hypothesis is evidenced, what does it
exclude, and what evidence would change that boundary?” It is a navigation map,
not a case registry, executable specification, runtime resource, or task queue.

## Use the four entries in this order

| Entry | Answers | Authoritative material | Does not authorize |
|---|---|---|---|
| 1. Theory navigation | Which bounded hypothesis, evidence role, difficulty/risk, counterexample, and adoption boundary apply? | [M146 development-evidence crosswalk](../../corpus/knowledge/development-evidence-crosswalk-v1.md) and its JSON/audit | Case promotion, code, runtime, provider, or hosted work. |
| 2. System/runtime architecture | How do Q01 observation, Q02 authoring, Q03 gate, and Q04 feedback work? | [Pipeline](../pipeline.md), [knowledge-base architecture](knowledge-base-architecture.md), and Q01--Q04 contracts | A theory claim beyond the source-linked evidence. |
| 3. Evidence-asset management | Which controlled asset supports a claim and under what identity, split, lifecycle, hash, and review boundary? | `case.json`, registry, admissions, [case portfolio](../../corpus/case-portfolio.md), and decision packages | A new hypothesis, manifest selection, or runtime use. |
| 4. Current task selection | What may be worked on now, under what scope and review gate? | [status.md](../../workflow/status.md), active workpack, and active handoff | Any work merely because a theory gap or deferred record exists. |

## How the crosswalk is used

Start at a M146 `hypothesis_id`, then follow its existing five views:

1. capability question;
2. bounded-modeling-hypothesis conditions and stop rule;
3. evidence maturity, roles, and admission risk;
4. evaluation-design boundary; and
5. adoption boundary.

The crosswalk owns none of the linked fields. A source change is made at its
authority, then its relationship/hash is refreshed and checked with:

```powershell
python tools\audit_development_evidence_crosswalk.py
```

## Fast routing examples

| If the question is… | Start here | Then consult |
|---|---|---|
| “What does this hypothesis actually support?” | M146 crosswalk | Linked knowledge unit and decision package. |
| “How does the Harness execute or reject it?” | Pipeline / Q01--Q04 contract | The hypothesis's linked Q03/Q04 boundary. |
| “Can this asset be used, promoted, or sent externally?” | Case/admission authority | Status, workpack, and the applicable G2/G3 gate. |
| “What should be implemented next?” | `status.md` | Only the named active workpack; deferred records remain navigation. |

## Boundary

The development knowledge system is the theory-navigation architecture. The
Q01--Q04 pipeline remains the system/runtime architecture. Case and governance
records remain the evidence-asset architecture. These roles are complementary:
linking across them does not transfer authority or make a reviewed development
hypothesis runtime- or hosted-eligible.

For Agent task-type routing, see the separately selected TRG-032 route; this
page intentionally does not change `AGENTS.md` or agent instructions.
