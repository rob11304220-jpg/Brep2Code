# Workpack Governance

Workpacks are **bounded execution ledgers**.  They record who may perform one
change, its inputs, acceptance evidence, compatibility constraints and closure
rationale.  They are not the long-lived authority for a project route,
architecture decision, contract, case disposition, runtime capability or
hosted authorization.

## Durable-information rule

Before a workpack closes, its owner must promote every conclusion that remains
useful after execution to its durable authority:

| Durable content | Authoritative destination |
|---|---|
| Lasting architecture or governance decision | ADR |
| Current route, route disposition, or non-goal | architecture route / route-decision index |
| Contract or behaviour | contract or module documentation |
| Evidence interpretation, asset role, or adoption boundary | evidence/case/knowledge authority |
| What may be selected now | `status.md` |

The closed workpack retains acceptance commands, paths, detailed scope and
provenance.  A stable navigation document may link it only when those primary
records are the material being sought; it must not make the workpack the sole
statement of a current conclusion.

## Durable citation contract

Direct links to `done/` or `archive/` workpacks are historical-provenance
links, never a substitute for a stable authority.  The referring document
must first state and link the still-valid ADR, architecture route, contract,
evidence authority or milestone record that owns the conclusion.

| Referring stable document | Direct completed/archived-workpack link | Required treatment |
|---|---|---|
| `status.md`, current-route and route-decision documents | No, except an explicitly labeled provenance note | State the current route/disposition from its stable authority; do not make an old package an entry point or selection instruction. |
| ADR, architecture, contract and module documentation | Only as secondary provenance | The ADR/contract/module record states the decision or behavior in full; the link is limited to acceptance detail or implementation history. |
| Milestone history | Yes, for closure/acceptance provenance | Link the stable conclusion first when one exists; use the workpack to open the bounded execution record. |
| Evidence ledger, decision record, case/experiment registry | Yes, when the package contains irreplaceable original report, hash, audit or terminal evidence | Preserve the evidence path and its interpretation/adoption boundary; do not infer current authority, capacity, budget or authorization from it. |
| Workpack and handoff indexes | Yes | Identify the link as execution or session provenance, not as a route or fact authority. |

`deferred/` records may be directly named by a route-disposition index because
their trigger identity and re-entry condition are the information being
navigated.  Their lifecycle location alone is never a current-route claim.

Before adding or retaining a direct completed-workpack link, verify all three:

1. A durable authority records the conclusion independently of the workpack.
2. The reader is told why the execution record is needed (acceptance, original
   report, audit, hash or historical provenance).
3. The wording does not make the link a current task, route, runtime, provider
   or hosted-authorization entry point.

## Lifecycle and archive policy

| Location/state | Meaning | Navigation treatment |
|---|---|---|
| `active/` | Selected execution authority | Must be named by `status.md` and active handoff |
| `backlog/` | Identified but not selected execution proposal | Not current-route authority |
| `deferred/` | Unconsumed semantic trigger with a stated re-entry condition | Navigation only; pair with a route disposition |
| `done/` | Closed execution ledger | Historical provenance; durable outputs carry its conclusions |
| `archive/` | Consumed, superseded, rejected or evidence-only workpack/trigger | Never an execution candidate; cite only for provenance |

`deferred` is a lifecycle location, not a claim that the route remains worth
selecting.  The Route Decision Map's `current prerequisite`, `future option`,
`superseded`, `rejected` and `archive-only` dispositions answer that separate
question.

## New-workpack rule

Create a new workpack only after the route decision names the uncertainty,
smallest competing disposition, discriminating evidence, counterexample, stop
rule and adoption boundary.  A completed or archived workpack is never
reactivated: a new selection receives a new M-number and freezes fresh scope,
inputs, reports and authorization.

## Closure checklist

1. Promote durable conclusions to their authority and link them from the
   workpack closure rationale.
2. Update `status.md` first, then move the workpack and archive its handoff.
3. For a trigger, record whether it remains a `future option`, is superseded,
   is rejected, or becomes `archive-only`; consumed triggers move to archive.
4. Run the governance audit.  Do not use the closed workpack as a replacement
   for its promoted ADR, route, contract or evidence record.

## Deferred inventory boundary

The maintained disposition index is
[workpack-route-disposition-index.md](workpack-route-disposition-index.md).
It is an incremental governance record, not a bulk retirement claim: each
historical cluster is classified only after its durable authority and re-entry
condition have been checked.
