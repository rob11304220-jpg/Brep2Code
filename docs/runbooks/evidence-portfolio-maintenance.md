# Case and Hosted Evidence Portfolio Maintenance

## Purpose

Maintain the read-only [case portfolio](../corpus/case-portfolio.md) and
[hosted experiment registry](../workflow/hosted-experiment-registry.md) as
low-context navigation. This procedure implements [ADR-0059](../architecture/adr/0059-case-and-hosted-evidence-portfolio.md); it does not alter any source authority.

## Authority boundary

| Fact | Authoritative source | Portfolio role |
|---|---|---|
| Case identity, hash, baseline, lifecycle | per-case `case.json` and `registry/self-authored.json` | link/group only |
| Executable selection | explicit manifest | list only when already selected |
| Reference-pack fields and hashes | `reference-pack-contract-v1.json` | link/status only |
| Runtime card status and applicability | `runtime_resources/experience-cards/` | link/status only |
| Hosted accounting and terminal result | frozen report plus terminal workpack/review | compact, bounded summary |
| Authorization | user authorization recorded by the G3 workpack | never reproduced or granted here |

## When to update

Update the case portfolio after an accepted case lifecycle/card/pack change or
when a later G1 package adds missing human case cards. Update the hosted
registry only after a terminal report has its required independent review.
Preflight, `running`, and unaudited report files may be linked in an active
workpack but are not terminal registry results.

## Use the efficient operating model

For a new bounded question, first identify its four-track owner and assemble
the smallest applicable evidence product from [ADR-0060](../architecture/adr/0060-efficient-four-track-operating-model.md): mechanism dossier, family design/release, card qualification dossier, or hosted campaign charter/readiness check.
Use links to existing case records, decision packages, packs/cards, policies
and reports; do not create a parallel registry. A case addition normally
extends an existing family/dossier, not a new hosted project.

If the question concerns current hosted evaluation scope, finite cases,
limited reference material, five-family portfolio meaning, or batch-campaign
interpretation, align the workpack wording with
[current hosted evaluation framing](../architecture/v1/current-hosted-evaluation-framing.md)
before editing the portfolio or selecting a campaign.
When the next selected package is a hosted campaign, draft its frozen scope
using the [hosted campaign charter template](hosted-campaign-charter-template.md)
before preflight or authorization text is prepared.

Before requesting any G3 authorization, the workpack must state the frozen
campaign question, split/conditions, accounting and terminal interpretation,
then complete the existing preflight requirements. One hosted campaign owns
its report/monitor paths until independent terminal review. A pass/failure in
another track neither releases capacity nor satisfies this campaign's entry
criteria.
When a hosted run has already terminalized, classify its next-step routing with
[Hosted terminal triage](hosted-terminal-triage.md) before editing the
registry wording or selecting a follow-on package.

## Procedure

1. Read `docs/workflow/status.md` and the active workpack. Do not use a
   portfolio entry to select a task or authorize a provider request.
2. Read the primary record first. Check case cards against the active registry;
   check packs/cards against their own contracts; check hosted outcome against
   the frozen policy, terminal report and review.
3. Update only the compact row/group and link. Preserve exact case IDs,
   split, terminal status and interpretation boundary. Do not copy raw STEP,
   provider payload, response, trace, credentials, local absolute path or
   reference script.
4. For a hosted row, record lifecycle, script/API/sandbox, provenance and
   geometry/semantic/editability gate states separately. Use `not evaluated`
   if the terminal path did not reach a gate.
5. State one allowed conclusion and one explicit non-inference. Never compute
   a global pass rate across different frozen policies.
6. If this changes project convention rather than only an entry, write an ADR;
   otherwise update the associated workpack, `status.md` and handoff under the
   normal lifecycle rules.
7. Run `uv run python tools/check_governance.py` and `git diff --check`.

## Five-family delivery projection

For a family in the ADR-0062 portfolio, update the projection only after its
primary offline release/review changes. Link the family evidence and state the
remaining hosted eligibility gap; do not mark it hosted-capable from local
replay. After a hosted campaign, wait for independent terminal review, then
add the corresponding registry row and point the portfolio to that row. The
registry continues to record no aggregate success rate across families or
policies.

## Prohibited shortcuts

- Do not promote a case, card or pack merely because it appears in a portfolio.
- Do not turn a reference script or case card into runtime context.
- Do not relabel an interrupted report as a failure/pass aggregate or reuse its
  remaining request count.
- Do not inspect held-out input to make a documentation row more detailed.
