# Hosted Campaign Charter Template

Use this template when a new hosted campaign is the selected next bounded
package. It implements the current hosted-evaluation framing, but does not
replace workpack, preflight, terminal review, or user authorization.

This template is for:

- one single-case smoke;
- one single-family development campaign; or
- one single-family held-out campaign after reviewed development evidence.

It is not for:

- selecting a family;
- loosening a frozen policy;
- combining multiple unrelated mechanisms under one denominator; or
- retrofitting old terminal reports into a new campaign.

## How to use this template

1. Select exactly one four-track owner.
2. Name exactly one campaign question.
3. Freeze the finite case scope and limited reference scope before preflight.
4. Fill every field below before requesting hosted authorization.
5. If a field cannot be frozen, stop and create the missing offline package
   instead of forcing a hosted run.

## Campaign identity

```markdown
# <Campaign title>

- Workpack: `<active or proposed workpack id>`
- Track owner: `hosted stability | reference-assisted construction | reference-guided parameter variation | modeling-sequence coverage`
- Campaign type: `single-case smoke | single-family development | single-family held-out`
- Date frozen: `YYYY-MM-DD`
- Status: `planning | preflight-ready | authorized | completed | terminal-failed | blocked`
```

## 1. Bounded question

```markdown
## Bounded question

<State one finite question that this campaign answers.>

Allowed conclusion:
- <One explicit statement this campaign may support if terminal evidence matches the frozen interpretation.>

Explicit non-inference:
- <One explicit statement this campaign may not support even if it passes.>
```

Guidance:

- The question must fit one mechanism, one family, or one fixed card/no-card
  comparison.
- Do not ask for quality ranking, benchmark performance, or generic CAD
  capability.
- For five-family campaigns, define the mechanism question, not a portfolio
  aggregate.

## 2. Finite case scope

```markdown
## Finite case scope

- Scope shape: `single case | frozen family development split | frozen family held-out split`
- Fixed case ids / rows: `<list>`
- Fixed split and order authority: `<manifest, preregistration, or family release record>`
- Denominator: `<number of cases or paired conditions>`
- Replacement policy: `none`
- Stop rule: `<first terminal failure | complete all rows | other frozen rule>`
```

Required rule:

- A terminal failure cannot be replaced by another case, another row, or a
  parameter variant outside the frozen denominator.

## 3. Limited reference scope

```markdown
## Limited reference scope

- Q01 outbound facts: `<frozen observation transcript or measured-fact contract>`
- Allowed pack/card/material: `<none | exact pack/card id and hash>`
- Allowed role or action boundary: `<declared role / constrained Q02 action>`
- Forbidden outbound material:
  - raw STEP
  - local paths / filenames
  - full reference scripts
  - prior provider responses
  - held-out answers
  - post-result card or prompt edits
```

Required rule:

- If the campaign uses a card, it must be one declared card with a frozen hash
  and a predeclared role or applicability boundary.

## 4. Offline prerequisites

```markdown
## Offline prerequisites

- Hosted-stability gate status: `<met | unmet | not applicable>` with source
- Dossier / family release / card qualification source: `<links>`
- No-input secure-executor preflight source: `<link>`
- Applicable negative-control or counterexample source: `<link>`
- Fresh-policy authority: `<policy file or design record>`
```

Stop here if any prerequisite is missing. A route document alone is not enough.

## 5. Hosted execution boundary

```markdown
## Hosted execution boundary

- Destination: `<endpoint>`
- Provider / model: `<provider and model>`
- Executor: `wsl-bwrap`
- Policy id: `<frozen policy>`
- Request shape: `<single-case smoke | paired comparison | family campaign>`
- Maximum requests: `<number>`
- Retry / repair policy: `<zero | exact frozen bound>`
- Provider deadline: `<seconds>`
- Output cap / other transport bound: `<if applicable>`
- Planned report path: `<fresh path>`
- Planned monitor path: `<fresh path>`
```

Required rule:

- One campaign owns one fresh report path and one fresh monitor path.
- A previous `running`, `interrupted`, or `completed` path cannot be reused as
  new capacity.

## 6. Preflight checklist

```markdown
## Preflight checklist

- [ ] Input SHA-256 values match the frozen case scope.
- [ ] Manifest / split / row membership matches the frozen scope.
- [ ] Q01 outbound transcript or measured-fact contract matches the frozen text/hash.
- [ ] Pack/card/index hashes match the frozen authority.
- [ ] Secure no-input `wsl-bwrap` control passed locally.
- [ ] Non-secret provider configuration and exact model selection are present.
- [ ] CLI accounting matches the planned request bound.
- [ ] Deadline and any output/token cap are valid and enforced locally.
- [ ] Report and monitor paths are fresh and absent before prepare.
- [ ] The campaign's interpretation table is frozen before authorization.
```

If any item fails, do not ask for authorization.

## 7. Interpretation table

```markdown
## Interpretation table

| Terminal outcome | Interpretation |
|---|---|
| `pass` | <bounded meaning only> |
| `provider timeout` / lifecycle failure | <bounded meaning only> |
| `script/API failure` | <bounded meaning only> |
| `sandbox/provenance failure` | <bounded meaning only> |
| `geometry/semantic/editability gate failure` | <bounded meaning only> |
| `interrupted` | partial evidence only; not a terminal campaign result |
```

Required rule:

- Keep lifecycle, script/API, sandbox/provenance, and downstream gates separate.
- Do not merge them into one capability score.

## 8. Authorization request payload

```markdown
## Authorization payload

Request approval only for:

- destination and model;
- exact outbound content class;
- exact case scope or family split;
- exact request cap;
- retry/repair bound;
- provider deadline;
- output/token cap if used;
- executor;
- fresh report/monitor paths.
```

Required rule:

- Authorization must approve this exact frozen boundary, not a general hosted
  category.

## 9. Terminal review payload

```markdown
## Terminal review payload

After execution, record:

- requests issued / remaining;
- terminal lifecycle status;
- script/API result;
- sandbox/provenance result;
- geometry/semantic/editability gate states, using `not evaluated` where needed;
- one allowed conclusion;
- one explicit non-inference;
- registry/portfolio attachment target after independent review.
```

## 10. Batch sequencing note

```markdown
## Batch sequencing note

This campaign is part of a planned batch: `yes | no`

If yes:
- Batch name: `<batch label>`
- Sequence position: `<n of N>`
- Shared framing source: `docs/architecture/v1/current-hosted-evaluation-framing.md`
- Independence rule: each campaign retains its own preflight, authorization,
  report/monitor paths, and terminal review
```

Required rule:

- `Batch` means a scheduled sequence of independently frozen campaigns. It does
  not create one pooled denominator, one pooled budget, or one cross-policy
  pass rate.

## 11. Old-route noise check

Before execution, explicitly record:

```markdown
## Old-route noise check

- Historical route docs consulted: `<list or none>`
- Why they are background only: `<one sentence>`
- Current controlling records: `<workpack, policy, framing doc, preflight doc>`
```

Use this section whenever old roadmap hits or completed workpacks could be
misread as current execution authority.

## Minimal completion standard

A campaign charter is complete only when:

- the bounded question is singular and frozen;
- finite case scope and limited reference scope are explicit;
- the hosted boundary is exact enough for itemized authorization;
- the interpretation table separates failure classes;
- old route documents are demoted to background when necessary; and
- the next step is unambiguous: either `run preflight`, `request authorization`,
  or `stop and create an offline prerequisite package`.

## Related records

- [Current hosted evaluation framing](../architecture/v1/current-hosted-evaluation-framing.md)
- [LLM provider configuration](llm-provider-config.md)
- [Evidence portfolio maintenance](evidence-portfolio-maintenance.md)
- [One-family development hosted campaign trigger](../workpacks/deferred/WP-TRG-016-one-family-development-hosted-campaign.md)
- [One-family held-out hosted campaign trigger](../workpacks/deferred/WP-TRG-018-one-family-held-out-hosted-campaign.md)
