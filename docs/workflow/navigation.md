# Low-Context Documentation Navigation

Use this page to avoid treating historical search hits as current work.

## Read order

1. [`status.md`](status.md) is the sole current-state authority.
2. Read `docs/workpacks/active/` and `docs/handoff/active/` only when named by
   the status page.
3. Use [`milestone-history.md`](milestone-history.md), the evidence ledger and
   ADR/contract links only for the specific decision under review.
4. Treat `docs/workpacks/done/` as immutable acceptance evidence and
   `docs/handoff/archive/` as historical session snapshots. Neither directory
   authorizes work or overrides the status page.

## Search discipline

Default searches should exclude `docs/handoff/archive/**` and
`docs/workpacks/done/**`. Add one of those paths only when an active task names
the required historical artifact. This prevents historical `active`, `next` or
`blocked` language from being mistaken for live instructions.

For a machine-readable entry summary, run:

```powershell
uv run python tools/check_governance.py --inventory
```

## Durable-information routing

| Information | Canonical home |
|---|---|
| Current milestone, active task, one next action | `status.md` |
| Current hosted-evaluation framing for finite cases/cards/families | `docs/architecture/v1/current-hosted-evaluation-framing.md` |
| Task scope and acceptance | active workpack; then immutable done workpack |
| Cross-session continuation | active handoff only |
| Architecture decision | ADR |
| Reusable operating procedure | runbook |
| Case-card/pack/runtime-card readiness | `docs/corpus/case-portfolio.md` (navigation only) |
| Hosted terminal-result navigation | `docs/workflow/hosted-experiment-registry.md` (navigation only) |
| Re-entry condition / decision evidence | evidence ledger or decision record |

Completed workpacks and archived handoffs retain audit evidence and links; they
should link to these canonical records instead of becoming a second current
status system.

## Completed-workpack citation boundary

Stable documents may link directly to a completed or archived workpack only
for acceptance detail, an irreplaceable original report, audit/hash evidence,
or historical provenance.  They must first link the ADR, route, contract,
evidence record or milestone-history entry that owns the durable conclusion.

In particular, `status.md` and current-route documents do not use completed
workpacks as route navigation; milestone history may retain closure links; and
evidence/experiment indexes may retain a package when it is the original
terminal record.  See the normative
[durable citation contract](workpack-governance.md#durable-citation-contract)
for the complete rule.

When historical route docs, completed workpacks, and portfolio pages all match
your search, use the hosted-evaluation framing page first to decide whether the
question is about current finite-case evaluation scope or only historical
background.
