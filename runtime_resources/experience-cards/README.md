# Experience Cards (experimental)

This is a small, versioned collection of runtime-operational guidance derived
from reviewed project evidence. It is not mounted or injected by default. The
completed M19-003 bridge can expose at most one explicitly selected, hash-bound
card through `get_guidance_card` for one revision; it is not automatic prompt
injection or broad directory retrieval.

The current `vertical-cylinder-construction` JSON remains hash-pinned evidence
for completed M85--M97 policies and keeps its pre-bridge wording. Do not edit
that card merely to restate bridge behavior; this README and the guidance
runbook are the current behavior boundary. A changed card requires its own
scoped evidence/policy review.

A caller may only make this directory visible by explicitly selecting the
parent runtime-resource bundle. New card mechanisms or broader retrieval still
need separately scoped, development-split evidence; hosted use also needs the
normal provider preflight and authorization.

Cards must be concise, actionable, and bounded.  They are not copies of
ADRs, handoffs, workpacks, logs, or provider responses.  Each card declares
its evidence level, supporting cases, counterexamples, a safe runtime action,
and a review trigger.  `experimental` cards may inform a future retrieval
experiment but must not alter a model, helper, parser, gate, or policy.

The development-side source layer is the [B-Rep modeling knowledge
system](../../docs/architecture/v1/modeling-knowledge-system.md). A card is a
reviewed projection of a bounded knowledge unit, not an alternative authority
for cases, operation semantics, or runtime policy.

Run the offline audit from the repository root:

```powershell
uv run python tools/audit_runtime_guidance.py
```

The contract is `schema/experience-card.schema.json`; `index.json` is the
authoritative discovery index.
